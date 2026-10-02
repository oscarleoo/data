"""
Merge research from _inbox/*.json into the tables in data/.

    python3 scripts/merge.py

Everything in the inbox is merged; rows already in the tables are kept.
Ids are derived from content (so re-running the merge doesn't duplicate rows),
raw files get their SHA-256, and indicators proposed by research are added
with "proposed" in their notes until reviewed. Run scripts/check.py afterwards.
"""
import csv
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")

COLUMNS = {
    "sources.csv": ["source_id", "title", "publisher", "author", "source_type", "jurisdiction",
                    "published_date", "accessed_date", "url", "archive_url", "raw_file", "sha256",
                    "covers", "notes"],
    "observations.csv": ["obs_id", "jurisdiction", "program_id", "indicator", "breakdown", "period",
                         "period_basis", "value", "value_high", "unit", "scale", "status", "source_id",
                         "location", "quote", "notes", "superseded_by", "added_date", "added_by"],
    "program_terms.csv": ["term_id", "program_id", "route", "valid_from", "valid_to", "min_amount",
                          "currency", "applies_to", "source_id", "location", "quote", "notes"],
    "events.csv": ["event_id", "date", "date_precision", "jurisdiction", "program_id", "category",
                   "title", "description", "source_id", "location", "quote"],
    "programs.csv": ["program_id", "jurisdiction", "name", "kind", "launched", "ended", "status",
                     "notes", "source_ids"],
    "indicators.csv": ["indicator", "name", "definition", "unit_kind", "notes"],
}


def read(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(name, rows, key):
    rows = sorted(rows, key=lambda r: [str(r.get(k, "")) for k in key])
    with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS[name], extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else str(r.get(c))) for c in COLUMNS[name]})


def content_id(prefix, row, fields):
    """A stable id from what the row says, so the same claim merged twice is one row."""
    text = "|".join(str(row.get(f, "")).strip() for f in fields)
    return f"{prefix}-{hashlib.sha256(text.encode()).hexdigest()[:10]}"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    tables = {name: {} for name in COLUMNS}
    keys = {
        "sources.csv": "source_id", "observations.csv": "obs_id", "program_terms.csv": "term_id",
        "events.csv": "event_id", "programs.csv": "program_id", "indicators.csv": "indicator",
    }
    for name, key in keys.items():
        for r in read(name):
            tables[name][r[key]] = r

    inbox = sorted(glob.glob(os.path.join(HERE, "_inbox", "*.json")))
    for path in inbox:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        slug = doc.get("slug") or os.path.basename(path)[:-5]
        added = doc.get("researched_on", "")
        by = f"research:{slug}"

        for s in doc.get("sources", []):
            s = dict(s)
            raw = s.get("raw_file") or ""
            full = os.path.join(HERE, raw) if raw else ""
            if raw and os.path.exists(full):
                s["sha256"] = sha256_of(full)
            elif raw:
                print(f"  {slug}: raw file missing for {s.get('source_id')}: {raw}", file=sys.stderr)
            tables["sources.csv"][s["source_id"]] = {**tables["sources.csv"].get(s["source_id"], {}), **s}

        for o in doc.get("observations", []):
            o = dict(o)
            fields = ["source_id", "jurisdiction", "program_id", "indicator", "period", "value", "unit", "location"]
            if o.get("breakdown"):  # only part of the id when used, so older rows keep their ids
                fields.append("breakdown")
            o["obs_id"] = content_id("o", o, fields)
            o.setdefault("added_date", added)
            o.setdefault("added_by", by)
            tables["observations.csv"][o["obs_id"]] = o

        for t in doc.get("program_terms", []):
            t = dict(t)
            t["term_id"] = content_id("t", t, ["source_id", "program_id", "route", "valid_from",
                                               "min_amount", "currency", "applies_to"])
            tables["program_terms.csv"][t["term_id"]] = t

        for e in doc.get("events", []):
            e = dict(e)
            e["event_id"] = content_id("e", e, ["source_id", "date", "jurisdiction", "title"])
            tables["events.csv"][e["event_id"]] = e

        for p in doc.get("programs", []):
            old = tables["programs.csv"].get(p["program_id"], {})
            ids = set(filter(None, (old.get("source_ids") or "").split(";")))
            ids |= set(filter(None, (p.get("source_ids") or "").replace(",", ";").split(";")))
            merged = {**old, **{k: v for k, v in p.items() if v not in (None, "")}}
            merged["source_ids"] = ";".join(sorted(ids))
            tables["programs.csv"][p["program_id"]] = merged

        for i in doc.get("new_indicators", []):
            if i["indicator"] not in tables["indicators.csv"]:
                i = dict(i)
                i["notes"] = ("proposed by " + by + ". " + (i.get("notes") or "")).strip()
                tables["indicators.csv"][i["indicator"]] = i

        print(f"{slug}: {len(doc.get('sources', []))} sources, {len(doc.get('observations', []))} observations, "
              f"{len(doc.get('program_terms', []))} terms, {len(doc.get('events', []))} events")

    write("sources.csv", tables["sources.csv"].values(), ["jurisdiction", "source_id"])
    write("observations.csv", tables["observations.csv"].values(),
          ["jurisdiction", "indicator", "period", "source_id"])
    write("program_terms.csv", tables["program_terms.csv"].values(), ["program_id", "route", "valid_from"])
    write("events.csv", tables["events.csv"].values(), ["date", "jurisdiction"])
    write("programs.csv", tables["programs.csv"].values(), ["jurisdiction", "program_id"])
    write("indicators.csv", tables["indicators.csv"].values(), ["indicator"])
    print({name: len(rows) for name, rows in tables.items()})


if __name__ == "__main__":
    main()
