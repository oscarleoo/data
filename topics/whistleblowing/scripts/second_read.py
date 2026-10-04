"""
Compare a blind second reading of the numbers with the first.

    python3 scripts/second_read.py [results_dir]

A second reader (a different AI model) is given each observation's document,
location, indicator and period, but not the value, and reads the number
itself. With a results_dir, its result_*.json files are imported into
data/second_read.csv first. Then every observation with a second reading is
compared, and reports/second_read.csv lists the outcome per row:

    agree          same number (after scale), or the same number at the other's precision
    scale_differs  same digits, different scale: one reader has the scale wrong
    differ         different numbers: needs a human look at the page
    not_found      the second reader couldn't find or pin down the number

Rows that don't agree can be re-read in a later round with the status given
(result_r2.json...), and a person's ruling after looking at the page goes in
data/second_read_resolutions.csv (first_correct, second_correct,
both_in_document). The "final" column combines them: confirmed, a ruling, or
open.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
SCALES = {"1": 1, "": 1, "thousand": 1e3, "million": 1e6, "hundred million": 1e8, "billion": 1e9, "trillion": 1e12}
FIELDS = ["obs_id", "value", "value_high", "scale", "column_label", "page_found", "verbatim",
          "confidence", "comment", "reader", "read_on", "round", "given_status"]


FRACTIONS = {"\u00bd": ".5", "\u00bc": ".25", "\u00be": ".75"}


WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve "
                                     "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def readings(v):
    """Every plausible number a printed value can mean: '4.264' is 4,264 in a Greek table,
    '496,8' is 496.8 in an EU regulation, '4\u00bd' is 4.5, '1.7%' is 1.7."""
    raw = str(v or "").strip().lower()
    if raw in WORDS:
        return [float(WORDS[raw])]
    if raw in ("-", "\u2013", "\u2014", "nil"):
        return [0.0]
    mult = 1e8 if "\uc5b5" in raw else 1  # Korean 억 = hundred million
    raw = raw.replace("\uc5b5", "").replace("\uc6d0", "")  # 억, 원
    raw = re.sub(r"^\((.*)\)$", r"\1", raw.strip())  # (246,000): an outflow in a fund table
    raw = re.sub(r"^(fewer|less|more) than |^over |^about |^around |^approximately |^nearly |^almost |^exceeded |^some ", "", raw)
    raw = re.sub(r"^(us\$|c\$|a\$|\$|\u20ac|\u00a3|\u00a5|\u20a9|krw|usd|cad)\s*", "", raw)
    raw = re.sub(r"\s*(trillion|billion|million|thousand)$", "", raw)
    raw = re.sub(r"^\((.*)\)$", r"\1", raw.strip())
    raw = raw.replace("'", "").replace("\u2019", "").rstrip("+")  # 5'003 (Swiss), 119+
    t = re.sub(r"\s", "", raw).rstrip("%")
    for k, f in FRACTIONS.items():
        t = t.replace(k, f)
    out = []
    for cand in (t.replace(",", ""),                     # 1,234.5
                 t.replace(".", "").replace(",", ".")):  # 1.234,5
        try:
            out.append(float(cand) * mult)
        except ValueError:
            pass
    return out


def number(v):
    r = readings(v)
    return r[0] if r else None


def half_unit(v, scale):
    digits = str(v).replace(",", "").replace(" ", "")
    decimals = len(digits.split(".")[1]) if "." in digits else 0
    return 0.5 * 10 ** -decimals * SCALES.get(scale or "1", 1)


def scale_of(s):
    s = (s or "").strip().lower()
    if "hundred million" in s:
        return 1e8
    words = {"trillion": 1e12, "triliun": 1e12, "billion": 1e9, "bilion": 1e9, "miliar": 1e9, "milliard": 1e9,
             "million": 1e6, "juta": 1e6, "thousand": 1e3, "ribu": 1e3}
    for k, v in words.items():
        if k in s:
            return v
    return {"t": 1e12, "tn": 1e12, "bn": 1e9, "b": 1e9, "m": 1e6, "mn": 1e6, "k": 1e3}.get(s, 1)


def compare(first, second):
    a, bs = number(first["value"]), readings(second.get("value"))
    if not bs:
        return "not_found"
    if a is None:
        return "differ"
    sa, sb = scale_of(first.get("scale")), scale_of(second.get("scale"))
    # a range ("fewer than 20", stored as 0 to 20) agrees when the other reading gives its bound
    candidates = [a] + ([number(first["value_high"])] if first.get("value_high") else [])
    for a_ in candidates:
        for b in bs:
            tol = max(half_unit(first["value"], first.get("scale")), half_unit(b, second.get("scale"))) + 1e-9
            if abs(a_ * sa - b * sb) <= tol:
                return "agree"
    if any(abs(a - b) <= 1e-9 * max(1, abs(a)) for b in bs):
        return "scale_differs"
    return "differ"


def import_results(folder):
    """result_<n>.json are first-round readings (location, indicator, period; no status);
    result_s<n>.json are first-round readings where the reader was also told the status;
    result_r<k>.json are later rounds (round k) of rows that didn't agree, with the status."""
    rows = []
    # rows whose id changed after they were read (e.g. a corrected location): old,new
    id_map = {}
    if os.path.exists(os.path.join(folder, "id_map.csv")):
        id_map = {r["old"]: r["new"] for r in csv.DictReader(open(os.path.join(folder, "id_map.csv")))}
    for f in sorted(glob.glob(os.path.join(folder, "result_*.json"))):
        name = os.path.basename(f)[len("result_"):-len(".json")]
        rnd = int(name[1:]) if name.startswith("r") else 1
        told_status = name.startswith(("r", "s"))
        try:
            results = json.load(open(f, encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"skipping {os.path.basename(f)}: not valid JSON (still being written?)", file=sys.stderr)
            continue
        read_on = __import__("datetime").date.fromtimestamp(os.path.getmtime(f)).isoformat()
        for r in results:
            rows.append({"obs_id": id_map.get(r["row_id"], r["row_id"]), **{k: r.get(k, "") for k in FIELDS[1:9]},
                         "reader": "claude-sonnet-5", "read_on": read_on, "round": rnd,
                         "given_status": "yes" if told_status else "no"})
    with open(os.path.join(DATA, "second_read.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows({k: ("" if v is None else v) for k, v in r.items()} for r in rows)


def main():
    if len(sys.argv) > 1:
        import_results(sys.argv[1])
    obs = {o["obs_id"]: o for o in csv.DictReader(open(os.path.join(DATA, "observations.csv"), encoding="utf-8"))}
    latest = {}
    for s in csv.DictReader(open(os.path.join(DATA, "second_read.csv"), encoding="utf-8")):
        if s["obs_id"] not in latest or int(s["round"]) >= int(latest[s["obs_id"]]["round"]):
            latest[s["obs_id"]] = s
    rpath = os.path.join(DATA, "second_read_resolutions.csv")
    resolutions = {r["obs_id"]: r for r in csv.DictReader(open(rpath, encoding="utf-8"))} if os.path.exists(rpath) else {}

    out = []
    for oid, s in latest.items():
        o = obs.get(oid)
        if not o:
            print(f"second reading for unknown observation {oid}", file=sys.stderr)
            continue
        result = compare(o, s)
        res = resolutions.get(oid, {})
        final = "confirmed" if result == "agree" else res.get("verdict", "open")
        out.append({"obs_id": oid, "source_id": o["source_id"], "indicator": o["indicator"],
                    "period": o["period"], "status": o["status"], "result": result, "final": final,
                    "first_value": o["value"], "first_scale": o["scale"], "first_location": o["location"],
                    "second_value": s["value"], "second_scale": s["scale"], "second_page": s["page_found"],
                    "second_column": s["column_label"], "second_confidence": s["confidence"],
                    "second_round": s["round"], "second_verbatim": s["verbatim"],
                    "second_comment": s["comment"], "resolution_note": res.get("note", "")})
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    with open(os.path.join(HERE, "reports", "second_read.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(sorted(out, key=lambda r: (r["final"] == "confirmed", r["final"], r["source_id"])))
    print("comparison:", dict(Counter(r["result"] for r in out)))
    print("final:", dict(Counter(r["final"] for r in out)))


if __name__ == "__main__":
    main()
