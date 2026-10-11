# Updates: keeping the recurring sources current

Many of the numbers in this dataset come from publications that appear again and again: a citizenship unit's
half-year report, a ministry's monthly bulletin, a budget every December, an IMF report every year. This page
says how we notice that a new edition is out and how it gets into the data.

## The list

`data/recurring.csv` has one row per recurring publication (a "series"):

| column | means |
|---|---|
| `series_id`, `title`, `publisher`, `jurisdiction` | which publication |
| `program_ids` | the programmes its stored editions are used for |
| `frequency` | `monthly`, `quarterly`, `half-yearly`, `yearly` or `irregular` |
| `url` | the page where new editions appear (checked with curl; where a site blocks scripts, `notes` says so) |
| `latest_stored`, `latest_period`, `latest_published` | the newest edition we store, what it covers and when it came out |
| `next_expected` | when the next edition should be out, judged from past publication dates; `unknown` for irregular series, `ended` when the series has stopped |
| `source_ids` | every edition we store |
| `notes` | how to fetch it, what blocks it, what format it is in, known gaps |

`next_expected` is an estimate, not a promise. Publishers are often late; an overdue date means "go and look", not
"something is missing".

## The routine, once a month

1. **See what is due.** `python3 scripts/due.py` lists every series whose next edition should be out by today
   (or by a date you give it), oldest first, with the page to look at. Irregular series are named at the end
   to be checked by hand.
2. **Look.** Open each page (curl, never the browser) and see whether a newer edition is really there. If it
   isn't, move `next_expected` forward and say in `notes` what you saw and when.
3. **Fetch and extract.** Each new edition goes through a normal research pass that follows
   `RESEARCH_BRIEF.md` and `EXTRACTION_BRIEF.md`: store the document in `raw/`, record the source, and extract
   everything in scope with a location and a verbatim quote, into an `_inbox/` file (`RESEARCH_FORMAT.md`).
   Sites that block scripts are noted and fetched separately; we never get around a CAPTCHA, a paywall or a
   bot check.
4. **Merge.** Run `scripts/merge.py`, then `scripts/check.py`. Read the last line of the merge output.
5. **Check the quotes.** Run the quote check (`scripts/verify_quotes.py`) on the new rows. Every new number must
   match its document.
6. **Second reading.** A different model reads the new numbers blind against the document
   (`scripts/second_read.py`). Every difference is ruled; wrong readings are fixed through
   `data/corrections.csv`.
7. **Update the list.** In `data/recurring.csv`, add the new source id to `source_ids`, set `latest_stored`,
   `latest_period` and `latest_published`, and set the next `next_expected` from the publication pattern.
   Update the coverage ledger (`scripts/coverage.py`) so the new document has its review status.

A new edition is not "in the data" until steps 3 to 7 are done. Until then it is a to-do, like any other gap
(see `COVERAGE.md`).

## When a series changes

- A publisher stops a series (Portugal's SEF monthly maps ended when SEF was abolished in 2023): set
  `next_expected` to `ended` and say why in `notes`.
- A series moves or is replaced (USCIS's old I-526 tables became the all-forms tables): keep the old row as
  ended and add a new row for the replacement.
- A new recurring publication is found: add a row as soon as its first edition is stored.
- Older editions we don't store are gaps, not updates. `notes` names them where known, so they can be filled.
