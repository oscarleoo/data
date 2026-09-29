"""
Find or create Wayback Machine snapshots for sources we don't store copies of
(news, industry), and record them as archive_url.

    python3 scripts/archive_links.py

Uses an existing snapshot when there is one; otherwise asks Save Page Now to
archive the page. Writes the archive links into the _inbox files (the source of
truth) and data/sources.csv. Run scripts/check.py afterwards.
"""
import csv
import glob
import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "oscarleo-data archiver (https://oscarleo.com)"}


def get(url, timeout=120):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.read()


def existing(url):
    _, body = get("https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe=""))
    snap = json.loads(body).get("archived_snapshots", {}).get("closest")
    return snap["url"].replace("http://", "https://") if snap and snap.get("available") else ""


def save(url):
    final, _ = get("https://web.archive.org/save/" + url, timeout=300)
    return final if "/web/" in final else ""


def main():
    path = os.path.join(HERE, "data", "sources.csv")
    sources = list(csv.DictReader(open(path, encoding="utf-8")))
    found = {}
    for s in sources:
        if s["source_type"] in ("media", "industry") and not s["archive_url"] and s["url"]:
            link = ""
            try:
                link = existing(s["url"])
                how = "existing"
                if not link:
                    link, how = save(s["url"]), "saved"
                    time.sleep(20)  # Save Page Now rate limit
            except Exception as e:  # noqa: BLE001
                how = f"failed: {e}"
            print(f"{s['source_id']}: {how} {link}", flush=True)
            if link:
                found[s["source_id"]] = link
            time.sleep(2)
    for s in sources:
        if s["source_id"] in found:
            s["archive_url"] = found[s["source_id"]]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sources[0].keys()))
        w.writeheader()
        w.writerows(sources)
    for p in glob.glob(os.path.join(HERE, "_inbox", "*.json")):
        doc = json.load(open(p, encoding="utf-8"))
        dirty = False
        for s in doc.get("sources", []):
            if s.get("source_id") in found and not s.get("archive_url"):
                s["archive_url"] = found[s["source_id"]]
                dirty = True
        if dirty:
            json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(found)} archive links recorded")


if __name__ == "__main__":
    main()
