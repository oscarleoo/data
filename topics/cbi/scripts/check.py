"""
Validate the tables in data/ and report where sources disagree.

    python3 scripts/check.py

Writes reports/validation.txt (problems, one per line) and
reports/discrepancies.csv (every jurisdiction, indicator and period for which
sources give different values, with each claim side by side). Each group is
marked as a vintage (forecasts and budgets later replaced by outturns), a
revision (one publisher changing its own figure in later documents), a
conflict (sources disagree about what happened), or same_source (one
document gives two values, usually under two definitions). Exits with 1 if
there are errors, so it can guard a merge or a CI run.
"""
import csv
import hashlib
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
REPORTS = os.path.join(HERE, "reports")

STATUS = {"actual", "provisional", "estimate", "projection", "budget", "reported", "claim"}
SOURCE_TYPES = {"government", "legislation", "imf", "world_bank", "eu", "court", "international_org",
                "academic", "ngo", "media", "industry"}
SCALES = {"1": 1, "thousand": 1e3, "million": 1e6, "billion": 1e9, "trillion": 1e12}
OUTTURN = {"actual", "provisional", "estimate", "reported", "claim"}
KEEP_COPIES = {"government", "legislation", "imf", "world_bank", "eu", "court", "international_org"}


def read(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def number(v):
    try:
        return float(str(v).replace(",", ""))
    except ValueError:
        return None


def precision(o):
    """Half a unit in the last printed digit, in normalised units: '443' million -> 500,000."""
    digits = str(o["value"]).replace(",", "")
    decimals = len(digits.split(".")[1]) if "." in digits else 0
    return 0.5 * 10 ** -decimals * SCALES.get(o.get("scale") or "1", 1)


def distinct(items, exact=False):
    """How many different values, treating two as equal if they differ only by rounding."""
    groups = []
    for i in sorted(items, key=lambda x: x["_normalised"]):
        if groups:
            last = groups[-1]
            tol = 1e-9 if exact else max(precision(i), precision(last)) + 1e-9
            if abs(i["_normalised"] - last["_normalised"]) <= tol:
                continue
        groups.append(i)
    return len(groups)


def main():
    errors, warnings = [], []
    sources = {s["source_id"]: s for s in read("sources.csv")}
    indicators = {i["indicator"] for i in read("indicators.csv")}
    programs = {p["program_id"] for p in read("programs.csv")}
    obs = read("observations.csv")

    released = {}
    manifest = os.path.join(HERE, "raw", "RELEASE_FILES.csv")
    if os.path.exists(manifest):
        with open(manifest, newline="", encoding="utf-8") as f:
            released = {r["raw_file"]: r for r in csv.DictReader(f)}

    for sid, s in sources.items():
        if s.get("source_type") not in SOURCE_TYPES:
            errors.append(f"source {sid}: unknown source_type {s.get('source_type')!r}")
        if not s.get("url"):
            errors.append(f"source {sid}: no url")
        raw = s.get("raw_file")
        if raw:
            path = os.path.join(HERE, raw)
            if not os.path.exists(path) and raw in released:
                if released[raw]["sha256"] != s.get("sha256"):
                    errors.append(f"source {sid}: checksum in raw/RELEASE_FILES.csv differs from sources.csv")
            elif not os.path.exists(path):
                errors.append(f"source {sid}: raw file missing: {raw}")
            elif s.get("sha256"):
                with open(path, "rb") as f:
                    if hashlib.sha256(f.read()).hexdigest() != s["sha256"]:
                        errors.append(f"source {sid}: raw file changed since its checksum was recorded")
        elif s.get("source_type") in KEEP_COPIES:
            warnings.append(f"source {sid}: official document without a stored copy")
        if s.get("source_type") in ("media", "industry") and not s.get("archive_url"):
            warnings.append(f"source {sid}: {s.get('source_type')} source without an archive link")

    for o in obs:
        oid = o["obs_id"]
        for field in ("jurisdiction", "indicator", "period", "value", "unit", "status", "source_id", "quote"):
            if not o.get(field):
                errors.append(f"observation {oid}: missing {field}")
        if o.get("status") and o["status"] not in STATUS:
            errors.append(f"observation {oid}: unknown status {o['status']!r}")
        if o.get("source_id") and o["source_id"] not in sources:
            errors.append(f"observation {oid}: unknown source {o['source_id']}")
        if o.get("indicator") and o["indicator"] not in indicators:
            errors.append(f"observation {oid}: unknown indicator {o['indicator']}")
        if o.get("program_id") and o["program_id"] not in programs:
            warnings.append(f"observation {oid}: program {o['program_id']} not in programs.csv")
        if number(o.get("value")) is None:
            errors.append(f"observation {oid}: value {o.get('value')!r} is not a number")
        if o.get("value_high"):
            hi, lo = number(o["value_high"]), number(o.get("value"))
            if hi is None or lo is None or hi < lo:
                errors.append(f"observation {oid}: value_high {o['value_high']!r} is not a number above value")
        if (o.get("scale") or "1") not in SCALES:
            errors.append(f"observation {oid}: unknown scale {o.get('scale')!r}")
        if not o.get("location"):
            warnings.append(f"observation {oid}: no location in the source")

    for name, idcol in (("program_terms.csv", "term_id"), ("events.csv", "event_id")):
        for r in read(name):
            if r.get("source_id") not in sources:
                errors.append(f"{name} {r[idcol]}: unknown source {r.get('source_id')}")
            if not r.get("quote"):
                warnings.append(f"{name} {r[idcol]}: no quote")

    # Disagreements: same jurisdiction, program, indicator, period and unit, different values.
    groups = defaultdict(list)
    for o in obs:
        if o.get("superseded_by") or o.get("value_high"):
            continue  # ranges are left out of the side-by-side comparison
        v = number(o.get("value"))
        if v is None:
            continue
        o["_normalised"] = v * SCALES.get(o.get("scale") or "1", 1)
        groups[(o["jurisdiction"], o.get("program_id", ""), o["indicator"] + (f' [{o["breakdown"]}]' if o.get("breakdown") else ""), o["period"], o["unit"])].append(o)

    os.makedirs(REPORTS, exist_ok=True)
    rows = []
    for key, items in sorted(groups.items()):
        if distinct(items) < 2:
            continue
        # Kinds, from least to most interesting:
        #   rounding     the values agree once rounded to the least precise one (443 m vs 442,617,122)
        #   vintage      forecasts or budgets that differ from the later outturn
        #   revision     one publisher changing its own figure for what happened, in later documents
        #   same_source  one document gives two values with the same status: usually two definitions
        #   conflict     different publishers disagree about what happened
        outturn = [i for i in items if i["status"] in OUTTURN]
        per_doc = defaultdict(list)
        for i in items:
            per_doc[(i["source_id"], i["status"])].append(i)
        if any(distinct(v) > 1 for v in per_doc.values()):
            kind = "same_source"
        elif distinct(outturn) > 1:
            publishers = {sources.get(i["source_id"], {}).get("publisher", "") for i in outturn}
            kind = "revision" if len(publishers) == 1 else "conflict"
        elif distinct(items, exact=True) > 1 and distinct(items) < 2:
            kind = "rounding"
        else:
            kind = "vintage"
        compared = outturn if kind in ("revision", "conflict") else items
        lo, hi = min(i["_normalised"] for i in compared), max(i["_normalised"] for i in compared)
        spread = (hi - lo) / abs(hi) * 100 if hi else None
        for i in sorted(items, key=lambda x: x["_normalised"]):
            rows.append({
                "jurisdiction": key[0], "program_id": key[1], "indicator": key[2], "period": key[3],
                "unit": key[4], "value": i["value"], "scale": i.get("scale", ""),
                "normalised_value": i["_normalised"], "status": i["status"],
                "source_id": i["source_id"],
                "publisher": sources.get(i["source_id"], {}).get("publisher", ""),
                "published_date": sources.get(i["source_id"], {}).get("published_date", ""),
                "spread_percent": f"{spread:.1f}" if spread is not None else "",
                "kind": kind,
                "obs_id": i["obs_id"],
            })
    with open(os.path.join(REPORTS, "discrepancies.csv"), "w", newline="", encoding="utf-8") as f:
        fields = ["jurisdiction", "program_id", "indicator", "period", "unit", "value", "scale",
                  "normalised_value", "status", "source_id", "publisher", "published_date",
                  "spread_percent", "kind", "obs_id"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(REPORTS, "validation.txt"), "w", encoding="utf-8") as f:
        for e in errors:
            f.write(f"ERROR  {e}\n")
        for wn in warnings:
            f.write(f"WARN   {wn}\n")

    kinds = defaultdict(set)
    for r in rows:
        kinds[r["kind"]].add((r["jurisdiction"], r["program_id"], r["indicator"], r["period"], r["unit"]))
    print(f"{len(sources)} sources, {len(obs)} observations: {len(errors)} errors, {len(warnings)} warnings")
    print("where values differ: " + ", ".join(f"{len(v)} {k}" for k, v in sorted(kinds.items())))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
