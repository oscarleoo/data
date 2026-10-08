"""
Build the extraction ledger: one row per source in data/sources.csv saying what we took from it
and whether anyone has checked that nothing else in it belongs in the dataset.

    python3 scripts/coverage.py

Counts (numbers, rules, events, cases, measures, splits) are recomputed from the tables every run.
The review columns are kept from the existing data/extraction_status.csv and edited by hand or by
an extraction pass:

    status          not_reviewed  nobody has checked the whole document against what we extracted
                    partial       reviewed, and some contents are knowingly not extracted (see to_do)
                    complete      reviewed: everything in scope is extracted
                    not_applicable reviewed: nothing in it belongs in the tables (e.g. used only as context)
    contains        what the document holds, in plain words (from the review)
    to_do           what is still to extract; required for partial
    reviewed_by, reviewed_on   required for partial, complete and not_applicable

New sources start as not_reviewed. Nothing becomes complete without a review; scripts/check.py
enforces this. A summary goes to reports/coverage.txt.
"""
import csv
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
STATUSES = ["not_reviewed", "partial", "complete", "not_applicable"]
COLS = ["source_id", "source_type", "stored", "title", "numbers", "rules", "events", "cases", "measures", "splits",
        "status", "contains", "to_do", "reviewed_by", "reviewed_on"]
KEEP = ["status", "contains", "to_do", "reviewed_by", "reviewed_on"]


def read(name):
    path = os.path.join(DATA, name)
    return list(csv.DictReader(open(path, encoding="utf-8"))) if os.path.exists(path) else []


def main():
    sources = read("sources.csv")
    old = {r["source_id"]: r for r in read("extraction_status.csv")}
    obs = read("observations.csv")
    rules = read("program_terms.csv") or read("program_rules.csv")
    events, cases = read("events.csv"), read("cases.csv")

    n_obs, n_rules, n_events, n_cases = (Counter(r["source_id"] for r in t) for t in (obs, rules, events, cases))
    measures, splits = defaultdict(Counter), defaultdict(set)
    for o in obs:
        measures[o["source_id"]][o["indicator"]] += 1
        for part in filter(None, o.get("breakdown", "").split(";")):
            splits[o["source_id"]].add(part.split("=")[0])

    out = []
    for s in sources:
        sid = s["source_id"]
        row = {
            "source_id": sid,
            "source_type": s["source_type"],
            "stored": "yes" if s.get("raw_file") else "no",
            "title": s["title"][:160],
            "numbers": n_obs[sid],
            "rules": n_rules[sid],
            "events": n_events[sid],
            "cases": n_cases[sid],
            "measures": "; ".join(f"{k} {v}" for k, v in measures[sid].most_common()),
            "splits": "; ".join(sorted(splits[sid])),
            "status": "not_reviewed",
        }
        for k in KEEP:
            if old.get(sid, {}).get(k):
                row[k] = old[sid][k]
        out.append(row)
    out.sort(key=lambda r: (STATUSES.index(r["status"]) if r["status"] in STATUSES else 9, r["source_id"]))
    with open(os.path.join(DATA, "extraction_status.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)

    st = Counter(r["status"] for r in out)
    stored = [r for r in out if r["stored"] == "yes"]
    lines = [
        f"Sources: {len(out)} ({len(stored)} with a stored copy)",
        "Review status: " + ", ".join(f"{k} {st.get(k, 0)}" for k in STATUSES),
        f"Stored documents with no numbers extracted: {sum(1 for r in stored if not int(r['numbers']))}",
        f"Stored documents with 1-2 numbers extracted: {sum(1 for r in stored if 1 <= int(r['numbers']) <= 2)}",
    ]
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    open(os.path.join(HERE, "reports", "coverage.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
