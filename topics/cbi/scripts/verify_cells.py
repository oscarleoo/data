"""
Cell-level check for numbers whose quote is a spreadsheet row put back together from its cells, and a separate
result for derived figures.

    python3 scripts/verify_cells.py      # re-checks the not_found rows in reports/quotes.csv, in place

verify_quotes.py calls the same checks, so a full run gives the same results. Results:

    cell     the quote is a row of the named sheet, cell for cell, and the stored value is in that row under the
             named column (or under the sheet's value column when the location names none)
    derived  status `derived`: the number is calculated from the source's raw records by the recipe in the notes
             (METHODOLOGY.md decision 1), so there is no printed text to find; such figures were recalculated
             independently when admitted
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
_sheets = {}


def norm(s):
    s = "" if s is None else str(s)
    if re.fullmatch(r"-?\d+\.0", s):
        s = s[:-2]
    return re.sub(r"\s+", " ", s).strip().lower()


def sheets(path):
    """{sheet name: [row as list of normalised cells]} for a spreadsheet; cached."""
    if path not in _sheets:
        import pandas as pd
        ext = path.lower().rsplit(".", 1)[-1]
        if ext == "csv":
            with open(path, newline="", encoding="utf-8", errors="ignore") as f:
                data = {"": [list(r) for r in csv.reader(f)]}
        else:
            frames = pd.read_excel(path, sheet_name=None, header=None, engine="odf" if ext == "ods" else None,
                                   dtype=object)
            data = {name: df.where(df.notna(), None).values.tolist() for name, df in frames.items()}
        _sheets[path] = {name: [[norm(c) for c in row] for row in rows] for name, rows in data.items()}
    return _sheets[path]


def _value_forms(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return {norm(value)}
    forms = {norm(value), str(int(v)) if v == int(v) else str(v)}
    return forms


def _pct(c, value):
    """A percentage stored as a fraction (0.678...) against a stored value of 68 (as displayed)."""
    try:
        return 0 <= float(c) <= 1 and round(float(c) * 100) == round(float(value)) and float(value) > 1 or \
            (float(value) == 0 and float(c) == 0)
    except (TypeError, ValueError):
        return False


def cell(quote, location, value, path):
    """True if the quote is a row of the named sheet and the value sits in it under the named column."""
    if not path.lower().endswith((".xls", ".xlsx", ".ods", ".csv")):
        return False
    try:
        book = sheets(path)
    except Exception:  # noqa: BLE001 - unreadable file: leave the row not_found
        return False
    m = re.search(r"sheet ['\"]?([^,'\"]+?)['\"]?,", location or "")
    names = [m.group(1).strip()] if m and m.group(1).strip() in book else list(book)
    q = norm(quote)
    col = re.search(r"column ['\"]([^'\"]+)['\"]", location or "")
    forms = _value_forms(value)
    for name in names:
        rows = book[name]
        for i, row in enumerate(rows):
            cells = [c for c in row if c not in ("", "none", "nan")]
            if " ".join(cells) != q and not _same_row(cells, q):
                continue
            # which column holds the value: the named one, else the last header cell (the sheet's value column)
            want = norm(col.group(1)) if col else ""
            # a column named "% granted" is headed just "%", right after "granted"
            pct_of = want[1:].strip() if want.startswith("%") else ""
            header = next((h for h in rows[:i][::-1] if want in h or (pct_of and pct_of in h and "%" in h)), None) \
                if col else None
            if header is None and not col:
                header = next((h for h in rows[:i][::-1] if sum(1 for c in h if c and not re.fullmatch(r"[\d.,%-]+", c)) >= 3), None)
                idx = max((j for j, c in enumerate(header or []) if c not in ("", "none", "nan")), default=None)
            elif header is not None and want in header:
                idx = header.index(want)
            elif header is not None:
                start = header.index(pct_of)
                idx = next((j for j in range(start + 1, len(header)) if header[j] == "%"), None)
            else:
                idx = None
            if idx is not None and idx < len(row) and (row[idx] in forms or _pct(row[idx], value)):
                return True
    return False


def _same_row(cells, q):
    """The row as displayed: a sheet stores 68% as 0.678..., the quote prints '68%'."""
    toks = q.split(" ")
    out, i = [], 0
    for c in cells:
        n = len(c.split(" "))
        part = toks[i:i + n]
        i += n
        if " ".join(part) == c:
            continue
        if len(part) == 1 and part[0].endswith("%"):
            try:
                if round(float(c) * 100) == round(float(part[0][:-1])):
                    continue
            except ValueError:
                pass
        return False
    return i == len(toks)


def derived(row):
    return row.get("status") == "derived" and "Recipe:" in (row.get("notes") or "")


def main():
    sources = {s["source_id"]: s for s in csv.DictReader(open(os.path.join(DATA, "sources.csv"), encoding="utf-8"))}
    obs = {o["obs_id"]: o for o in csv.DictReader(open(os.path.join(DATA, "observations.csv"), encoding="utf-8"))}
    path = os.path.join(HERE, "reports", "quotes.csv")
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    from collections import Counter
    changed = Counter()
    for r in rows:
        if r["result"] != "not_found" or r["table"] != "observations.csv" or r["id"] not in obs:
            continue
        o = obs[r["id"]]
        raw = sources.get(r["source_id"], {}).get("raw_file", "")
        if derived(o):
            r["result"] = "derived"
        elif raw and cell(r["quote"], r["location"], o["value"], os.path.join(HERE, raw)):
            r["result"] = "cell"
        else:
            continue
        changed[r["result"]] += 1
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("re-checked:", dict(changed), "| now:", dict(Counter(r["result"] for r in rows)))


if __name__ == "__main__":
    main()
