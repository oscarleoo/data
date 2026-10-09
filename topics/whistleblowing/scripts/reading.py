"""
How a number was read from its source (METHODOLOGY.md decision 2).

    from reading import classify          # used by merge.py for rows with no `reading` yet
    python3 scripts/reading.py            # report: counts per reading, and rows needing a human look

Values of `reading`:
    digits       printed as a number (the default)
    words        the number itself is written in words ("three applications", "one million")
    bound        printed as a limit; stored as a range ("more than 700", "<5")
    approximate  printed as a rounded figure ("about 20", "nearly 60%")
    implied      no number printed, but the sentence states it unambiguously ("no inflows" = 0)
    inferred     depends on reasoning beyond the sentence: NOT allowed in the data
Derived figures (status `derived`) are calculated, not read, and have an empty `reading`.

classify() is a first pass from the quote and value. It never returns `inferred` (that needs a person), and it
returns "" when it can't tell; such rows are listed by the report for review. A reviewed answer goes in
data/corrections.csv (field `reading`), which merge.py applies last.
"""
import csv
import os
import re
import sys

READINGS = {"digits", "words", "bound", "approximate", "implied", "inferred"}

BOUND = re.compile(r"(more than|over|at least|less than|fewer than|under|up to|in excess of|exceed\w*|above|below|"
                   r"upwards of|not less than|no fewer than|minimum of|maximum of|<|>|≥|≤|"
                   r"mehr als|über|plus de|moins de|más de|menos de|mais de|menos de|oltre|più di|meno di|"
                   r"több mint|kevesebb mint|fazla|az|daugiau nei|vairāk nekā|ponad|πάνω από|πάνω|άνω|"
                   r"이상|미만|초과|以上|以下|超过)\s*$", re.I)
APPROX = re.compile(r"(about|around|approximately|approx\.?|nearly|almost|some|roughly|circa|c\.|~|close to|"
                    r"just under|just over|an estimated|estimated|"
                    r"etwa|rund|ungefähr|environ|près de|presque|aproximadamente|cerca de|casi|quasi|circa|"
                    r"közel|mintegy|körülbelül|yaklaşık|около|почти|περίπου|σχεδόν|apie|aptuveni|"
                    r"약|여|가량|約|近|大约|大約)\s*$", re.I)
APPROX_AFTER = re.compile(r"^\s*(여|가량|odd|-odd|plus|\+|or so)", re.I)
NEGATION = re.compile(r"\b(no|none|nil|not any|zero|neither|nobody|never)\b|keine?\b|aucun|ningun|ningún|nessun|"
                      r"nincs|nem érkezett|nebol|neboli|yok|없|未|无|δεν|nėra|nav", re.I)
WORDS = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
                   r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
                   r"hundred|thousand|million|billion|dozen|half|single|double|twice|"
                   r"zwei|drei|vier|fünf|deux|trois|quatre|cinq|dos|tres|cuatro|cinco|due|tre|quattro|"
                   r"egy|kettő|két|három|négy|öt|bir|iki|üç|dört|beş|vienas|du|trys|viens|divi|trīs|"
                   r"ένα|δύο|τρία|τέσσερα|πέντε|하나|둘|셋|한|두|세|네)\b", re.I)


def _number_forms(value):
    """Ways a stored value can appear in a quote: 1583 -> 1583, 1,583, 1.583, 1 583."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return []
    forms = set()
    for x in (v, abs(v)):
        if x == int(x):
            n = str(int(x))
            forms.add(n)
            g = f"{int(x):,}"
            forms.update({g, g.replace(",", "."), g.replace(",", " "), g.replace(",", " "), g.replace(",", "'")})
        else:
            s = f"{x}".rstrip("0").rstrip(".")
            forms.update({s, s.replace(".", ",")})
            ip, fp = s.split(".") if "." in s else (s, "")
            if fp:
                g = f"{int(ip):,}"
                forms.update({f"{g}.{fp}", f"{g.replace(',', '.')},{fp}", f"{g.replace(',', ' ')},{fp}"})
    return sorted(forms, key=len, reverse=True)


def _find(quote, value):
    """Position of the value as digits in the quote, or None."""
    for f in _number_forms(value):
        for m in re.finditer(re.escape(f), quote):
            a, b = m.start(), m.end()
            if (a == 0 or not quote[a - 1].isdigit()) and (b == len(quote) or not quote[b].isdigit()):
                if a > 0 and quote[a - 1] in ".," and a > 1 and quote[a - 2].isdigit():
                    continue
                return a, b
    return None


def classify(row):
    """First-pass reading for one observation row (dict). Returns a READINGS value or "" (needs review)."""
    if row.get("status") == "derived":
        return ""
    quote = (row.get("quote") or "").replace("\n", " ")
    value = row.get("value", "")
    high = row.get("value_high", "")
    pos = _find(quote, value)
    if pos:
        before, after = quote[:pos[0]], quote[pos[1]:]
        tail = re.sub(r"[\s$€£¥₩₱]|US|EC|HK|R\$|RM|AED|EUR|USD|CAD|AUD|NZD|SGD|KRW|PHP|VT|Rp|Php|P(?=\d)", " ", before)[-40:]
        if BOUND.search(tail.rstrip()) or (high and high != value and BOUND.search(before[-40:])):
            return "bound"
        if APPROX.search(tail.rstrip()) or APPROX_AFTER.search(after):
            return "approximate"
        if high and high != value:
            return "bound"
        return "digits"
    try:
        v = float(value)
    except (TypeError, ValueError):
        v = None
    # masked or suppressed cells printed as "<5", "--" or "x", stored as a range
    if high and high != value and re.search(r"(<\s*\d|--|\bx\b|n\.p\.|\.\.)", quote):
        return "bound"
    # a dash in a table means nil: printed, stored as 0
    if v == 0 and re.search(r"(^|\s)[-\u2013\u2014](\s|$)", quote):
        return "digits"
    # the same value printed with other formatting ("0.90" for 0.9, "1.234,5")
    if v is not None:
        for tok in re.findall(r"\d[\d.,' \u00a0]*\d|\d", quote):
            t = re.sub(r"[ '\u00a0]", "", tok)
            for cand in (t.replace(",", ""), t.replace(".", "").replace(",", ".")):
                try:
                    if abs(float(cand) - abs(v)) < 1e-9:
                        return "digits"
                except ValueError:
                    pass
    if v == 0 and NEGATION.search(quote):
        return "implied"
    if WORDS.search(quote) and not re.search(r"\d", quote):
        return "words"
    if WORDS.search(quote):
        return "words" if not high else "bound"
    if re.search(r"\d", quote):
        # digits present but not this value as printed: a scaled or converted form ("€1.2bn", "4억 5,400",
        # a value read from a table row rebuilt in the quote). Accept as digits when the leading digits match.
        lead = re.sub(r"\D", "", str(value).split(".")[0].lstrip("-0"))[:2]
        if lead and lead in re.sub(r"\D", "", quote):
            return "digits"
    return ""


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rows = list(csv.DictReader(open(os.path.join(here, "data", "observations.csv"), encoding="utf-8")))
    from collections import Counter
    c = Counter(r.get("reading", "") or ("(derived)" if r["status"] == "derived" else "(blank)") for r in rows)
    print("readings:", dict(c))
    review = [r for r in rows if not r.get("reading") and r["status"] != "derived"]
    out = os.path.join(here, "reports", "reading_review.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["obs_id", "source_id", "indicator", "value", "value_high", "quote"])
        for r in review:
            w.writerow([r["obs_id"], r["source_id"], r["indicator"], r["value"], r["value_high"], r["quote"][:300]])
    print(f"{len(review)} rows need a human look: {out}")
    bad = [r for r in rows if r.get("reading") == "inferred"]
    if bad:
        print(f"{len(bad)} rows are 'inferred' and must be removed (data/corrections.csv, field _delete)")


if __name__ == "__main__":
    sys.exit(main())
