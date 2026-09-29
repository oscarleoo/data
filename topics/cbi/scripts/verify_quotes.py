"""
Check that every quote attached to an observation, term or event can be found
in the stored copy of its source.

    python3 scripts/verify_quotes.py

Extracts text from each stored document once (pdftotext for PDFs, pandas for
spreadsheets, plain read for HTML/text), then looks for each quote with
whitespace, case, hyphenation and common typographic differences ignored.
Writes reports/quotes.csv with one result per row:

    found       the quote appears verbatim (after normalising)
    loose       every word and number in the quote appears close together
                (tables, where a quote is a row put back together from cells)
    not_found   needs a human look: a misquote, or text the extraction mangles
    no_text     no usable text, even after OCR

Scanned PDFs (no text layer) are OCR'd with tesseract; the text_from column
says "ocr" for those, since OCR can misread digits.
    no_copy     no stored copy of the source
    checked     someone compared the quote with the page by eye and it matches
    wrong_copy  the stored file isn't the document the quote comes from
                (data/quote_checks.csv says who, when, and what they saw)
"""
import csv
import os
import re
import subprocess
import unicodedata

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
CACHE = os.path.join(HERE, "_text")  # extracted text, not published


def read(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalise(text, join_hyphens=True):
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub("[\u2018\u2019\u201b\u2032]", "'", text)
    text = re.sub("[\u201c\u201d\u201e\u2033]", '"', text)
    text = re.sub("[\u2010-\u2015\u2212]", "-", text).replace("\u00a0", " ")
    text = re.sub(r"([\u20ac$\u00a3])\s+(?=\d)", r"\1", text)  # "\u20ac 620,001" = "\u20ac620,001"
    # a hyphen at a line end is either a word split ("con-\ntributed") or a real one ("revenue-\nerosive")
    text = re.sub(r"-\s*\n\s*", "" if join_hyphens else "-", text)
    return re.sub(r"[^\w%$€.,:;'\"()/-]+", " ", text).strip()


OCR_MARK = "__ocr__\n"


TESSDATA = os.path.join(HERE, "_tessdata")  # eng, osd and tur models (tessdata_fast), not published
LANGS = {"TUR": "tur+eng"}


def ocr(path, lang="eng"):
    """Text of a scanned PDF: pages rendered at 200 dpi and read by tesseract in
    parallel, with orientation detection for rotated tables."""
    import tempfile
    from concurrent.futures import ThreadPoolExecutor

    def read_page(img):
        env = {**os.environ, "OMP_THREAD_LIMIT": "1"}
        if os.path.isdir(TESSDATA):
            env["TESSDATA_PREFIX"] = TESSDATA
        return subprocess.run(["tesseract", img, "-", "--psm", "1", "-l", lang], capture_output=True,
                              text=True, env=env).stdout

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "200", "-png", path, os.path.join(tmp, "p")], check=True)
        pages = [os.path.join(tmp, p) for p in sorted(os.listdir(tmp))]
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
            return "\n".join(pool.map(read_page, pages))


def extract(path, lang="eng"):
    os.makedirs(CACHE, exist_ok=True)
    cached = os.path.join(CACHE, os.path.basename(path) + ".txt")
    if os.path.exists(cached):
        with open(cached, encoding="utf-8") as f:
            return f.read()
    ext = path.lower().rsplit(".", 1)[-1]
    text = ""
    try:
        if ext == "pdf":
            text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                  text=True, timeout=300).stdout
            # tables often read better without layout; keep both
            text += "\n" + subprocess.run(["pdftotext", path, "-"], capture_output=True,
                                          text=True, timeout=300).stdout
            if len(text.strip()) < 500:
                text = OCR_MARK + ocr(path, lang)
        elif ext in ("xls", "xlsx"):
            import pandas as pd
            sheets = pd.read_excel(path, sheet_name=None, header=None)
            text = "\n".join(df.astype(str).to_csv(sep=" ", index=False, header=False)
                             for df in sheets.values())
        else:
            import html
            with open(path, "rb") as f:
                data = f.read()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:  # older pages declare their own charset (e.g. windows-1254)
                m = re.search(rb'charset=["\']?([\w-]+)', data[:4000])
                text = data.decode(m.group(1).decode() if m else "latin-1", errors="replace")
            text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", text)
            text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    except Exception as e:  # noqa: BLE001 - report and move on
        text = f"__extract_failed__ {e}"
    with open(cached, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def found(quote, haystack):
    q = normalise(quote)
    if not q:
        return False
    if q in haystack:
        return True
    # quotes that span table cells or elisions ("... 20.1"): every piece must appear
    pieces = [p.strip() for p in re.split(r"\.\.\.|…|\[\.\.\.\]", q) if len(p.strip()) >= 4]
    return bool(pieces) and all(p in haystack for p in pieces)


def loose(quote, haystack, window=2500):
    tokens = {t.strip(".,:;'\"()/-") for t in normalise(quote).split()}
    tokens = [t for t in tokens if len(t) >= 2]
    if not tokens:
        return False
    rarest = min(tokens, key=lambda t: haystack.count(t))
    start = 0
    for _ in range(300):
        pos = haystack.find(rarest, start)
        if pos < 0:
            return False
        near = haystack[max(0, pos - window):pos + window]
        if all(t in near for t in tokens):
            return True
        start = pos + 1
    return False


def csv_cells(quote, path):
    """A quote from a CSV written as its row: plain cells, then column=value pairs."""
    parts = [p.strip() for p in quote.split(",")]
    cells = [p for p in parts if "=" not in p]
    pairs = dict(p.split("=", 1) for p in parts if "=" in p)
    if not pairs:
        return False
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            values = set(v.strip() for v in row.values() if v)
            if all(c in values for c in cells) and all((row.get(k) or "").strip() == v for k, v in pairs.items()):
                return True
    return False


_page_cache = {}


def page_of(raw, quote, cited):
    """Check a 'PDF p. N' location: 'ok' if the quote is on page N, else the page it's on
    (for text PDFs; scans are left alone). Quotes that run over a page break count
    for either page."""
    path = os.path.join(HERE, raw)
    if raw not in _page_cache:
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
        _page_cache[raw] = [normalise(t) for t in out.split("\f")]
    pages = _page_cache[raw]
    q = normalise(quote)
    head, tail = q[:50], q[-50:]

    def on(i):
        if not 0 <= i < len(pages):
            return False
        both = pages[i] + " " + (pages[i + 1] if i + 1 < len(pages) else "")
        return found(quote, pages[i]) or loose(quote, pages[i]) or head in pages[i] or \
            (head in both and tail in both and head in pages[i])
    if on(cited - 1):
        return "ok"
    if cited >= 2 and on(cited - 2) and normalise(quote)[:50] in pages[cited - 2] and tail in (pages[cited - 2] + pages[cited - 1]):
        return "ok"  # sentence starts on the page before and runs onto the cited page
    for i in range(len(pages)):
        if on(i):
            return f"p. {i + 1}"
    return "unknown"


_ocr_cache = {}


def ocr_text(raw):
    """OCR of a whole PDF that has a text layer on some pages but not others; cached."""
    if raw not in _ocr_cache:
        cached = os.path.join(CACHE, os.path.basename(raw) + ".ocr.txt")
        if not os.path.exists(cached):
            s = next((x for x in read("sources.csv") if x.get("raw_file") == raw), {})
            with open(cached, "w", encoding="utf-8") as f:
                f.write(ocr(os.path.join(HERE, raw), LANGS.get(s.get("jurisdiction"), "eng")))
        with open(cached, encoding="utf-8") as f:
            t = f.read()
        _ocr_cache[raw] = normalise(t) + "\n" + normalise(t, join_hyphens=False)
    return _ocr_cache[raw]


def main():
    sources = {s["source_id"]: s for s in read("sources.csv")}
    # keyed on what was checked rather than the row id, which changes if a row is edited
    checks = {(c["source_id"], c["location"], c["quote"]): c for c in read("quote_checks.csv")} \
        if os.path.exists(os.path.join(DATA, "quote_checks.csv")) else {}
    texts = {}
    out = []
    for table, idcol in (("observations.csv", "obs_id"), ("program_terms.csv", "term_id"),
                         ("events.csv", "event_id")):
        for r in read(table):
            s = sources.get(r.get("source_id"), {})
            raw = s.get("raw_file")
            text_from = ""
            if not raw or not os.path.exists(os.path.join(HERE, raw)):
                result = "no_copy"
            else:
                if raw not in texts:
                    t = extract(os.path.join(HERE, raw), LANGS.get(s.get("jurisdiction"), "eng"))
                    texts[raw] = normalise(t) + "\n" + normalise(t, join_hyphens=False)
                text, quote = texts[raw], r.get("quote", "")
                text_from = "ocr" if text.startswith("__ocr__") else "text"
                if len(text) < 500:
                    result = "no_text"
                elif found(quote, text):
                    result = "found"
                elif raw.endswith(".csv") and csv_cells(quote, os.path.join(HERE, raw)):
                    result = "found"
                elif loose(quote, text):
                    result = "loose"
                elif (r.get("source_id"), r.get("location", ""), quote) in checks:
                    c = checks[(r.get("source_id"), r.get("location", ""), quote)]
                    result = "checked" if c["result"] == "matches" else c["result"]
                elif raw.lower().endswith(".pdf") and not text.startswith("__ocr__") and \
                        (found(quote, ocr_text(raw)) or loose(quote, ocr_text(raw))):
                    # a scanned page inside a PDF that has text on other pages
                    result = "found" if found(quote, ocr_text(raw)) else "loose"
                    text_from = "ocr"
                else:
                    result = "not_found"
            page_check = ""
            m = re.search(r"PDF pp?\. ?(\d+)(?:\s*[-\u2013]\s*(\d+))?", r.get("location", ""))
            if m and raw and raw.lower().endswith(".pdf") and result in ("found", "loose") and text_from == "text":
                cited = range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1)
                per_page = [page_of(raw, quote, c) for c in cited]
                page_check = "ok" if "ok" in per_page else per_page[0]
            out.append({"table": table, "id": r[idcol], "page_check": page_check, "source_id": r.get("source_id"),
                        "source_type": s.get("source_type", ""), "result": result, "text_from": text_from,
                        "location": r.get("location", ""), "quote": r.get("quote", "")})

    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    with open(os.path.join(HERE, "reports", "quotes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    c = Counter(r["result"] for r in out)
    print(dict(c))
    print("pages:", dict(Counter(("ok" if r["page_check"] == "ok" else "moved" if r["page_check"].startswith("p.")
                                  else r["page_check"] or "not_checked") for r in out)))


if __name__ == "__main__":
    main()
