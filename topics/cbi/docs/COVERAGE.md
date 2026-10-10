# Coverage: what we have extracted, and what we have not

This file says honestly how complete the citizenship and residence by investment dataset is. Read it before
saying anything is "all the data".

## The rule

Not extracting everything is fine, as long as it is written down as a to-do and
not presented as done. Every source in `data/sources.csv` has a row in
`data/extraction_status.csv`:

| status | means |
|---|---|
| `not_reviewed` | Nobody has checked the whole document against what we extracted. There may be more in it. |
| `partial` | Reviewed. Some contents are knowingly not extracted; `to_do` says what. |
| `complete` | Reviewed. Everything in scope is extracted. |
| `not_applicable` | Reviewed. Nothing in it belongs in the tables (used only as context). |

`partial`, `complete` and `not_applicable` need `reviewed_by` and
`reviewed_on`; `partial` also needs a `to_do`. `scripts/check.py` fails the
build otherwise, and also fails if any source has no row. `scripts/coverage.py`
recomputes what was taken from each source (numbers, rules, events, cases,
measures, splits) and keeps the review columns.

## Why this exists

The research passes collected each programme's main numbers, rules and events.
They did not record every table in every document they stored. On 8 October
2026 we found nationality tables in stored Greek and Antiguan documents that had
not been extracted, while the page said "every number we could find". That was
wrong. This ledger makes the gaps visible.

## Where we are (as of 2026-10-10, evening)

- Sources: 1,438, of which 1,433 have a stored copy (160 news and industry copies are kept locally for checking and not published, for copyright). Data: 129,029 numbers, 5,104 rules, 1,343 events.
- Stored documents reviewed against their full contents: **1,433 of 1,433** (1,369 complete, 47 partial with a written to-do, 17 not applicable). Not yet reviewed: **0** stored documents.
- Sources with no stored copy: 5. They couldn't be fetched (a CAPTCHA or bot check we don't bypass, a dead domain, a refused connection) and stay `not_reviewed`; their to-do says why.
- The review was done document by document between 8 and 10 October 2026; logs: `../cbi/reports/overnight-2026-10-08.md` and `../cbi/reports/corrections-2026-10-09.md`.

What this does and doesn't mean:

- Every number has a location and a verbatim quote, and each is checked against the stored copy. Of 130,532 quoted rows (numbers, rules, events) in the last full check (10 October): 92,113 match word for word and 19,716 as a table row; 3,131 spreadsheet rows match cell for cell; 10,777 were confirmed by a blind second reading and 245 by eye; 3,989 are calculated figures (decision 1) whose recipe was recalculated independently. None is unconfirmed; 1 document has no readable text and 560 rows come from sources we don't store. Rows added after that check were checked as they were merged.
- Limit of the quote check: for scanned documents the stored text is itself OCR, so a quote that matches it confirms the wording but not every digit. 5,060 numbers are confirmed only that way (mostly Antigua contribution lines, which are almost all 100,000 or 125,000 and add up to the printed totals in most reports, and Thai membership cells, checked against row totals). Reading every payment line of the Antigua reports blind found and corrected 9 misread amounts that a text match had passed.
- A blind second reading by a different model covers 23,459 of 129,029 numbers: every number whose quote could not be matched automatically, every Antigua payment line, every image or chart label, plus samples of the rest. Every difference is ruled (`data/second_read_resolutions.csv`); where the first reading was wrong it was corrected through `data/corrections.csv`.
- `complete` means everything in scope was extracted. `partial` documents still hold things we didn't extract; the `to_do` column says exactly what (charts without printed values, unreadable scans, items waiting for a decision on scope).
- Documents we don't store are not reviewed, so the dataset says nothing about what they contain.

## What happens next

An extraction pass works through the stored documents, starting with the
to-dos marked "Priority review" and the known gaps. For each document it lists
what the document contains, extracts what is in scope, and sets the status:
`complete` only when nothing in scope is left, otherwise `partial` with a
to-do. Tables with printed totals must add up; new numbers go through the
quote check and the blind second reading like everything else.
