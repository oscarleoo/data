"""
List the recurring publications whose next edition should be out by now, so it can be fetched.

    python3 scripts/due.py               # due on or before today
    python3 scripts/due.py 2026-12-31    # due on or before a given date

Reads data/recurring.csv and prints each series whose next_expected is on or before the date, oldest first,
with the newest edition we store and the page where new editions appear. Irregular series (next_expected
"unknown") are named at the end as a reminder to look at them by hand; ended series are skipped.
See docs/UPDATES.md for the routine.
"""
import csv
import datetime
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    day = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    datetime.date.fromisoformat(day)  # fails on a malformed date
    with open(os.path.join(HERE, "data", "recurring.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    due = sorted((r for r in rows if r["next_expected"][:1].isdigit() and r["next_expected"] <= day),
                 key=lambda r: (r["next_expected"], r["series_id"]))
    print(f"{len(due)} of {len(rows)} series due on or before {day}\n")
    for r in due:
        print(f"{r['next_expected']}  {r['series_id']}  ({r['frequency']})")
        print(f"    {r['title']}")
        print(f"    have: {r['latest_stored']} ({r['latest_period']}, published {r['latest_published'] or '?'})")
        print(f"    look: {r['url']}\n")
    irregular = [r["series_id"] for r in rows if r["next_expected"] == "unknown"]
    if irregular:
        print("Irregular, check by hand: " + ", ".join(irregular))


if __name__ == "__main__":
    main()
