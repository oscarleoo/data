# Coverage: what we have extracted, and what we have not

This file says honestly how complete the whistleblower rewards dataset is. Read it before
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

## Where we are (as of 2026-10-09)

- Sources: 582, of which 558 have a stored copy.
- Stored documents reviewed against their full contents: **558 of 558** (523 complete, 33 partial with a written to-do, 2 not applicable). Not yet reviewed: **0** stored documents.
- Sources with no stored copy: 24. They stay `not_reviewed` until a copy is fetched.
- The review was done document by document between 8 and 9 October 2026; the log is in `../cbi/reports/overnight-2026-10-08.md`.

What this does and doesn't mean:

- Every number has a location and a verbatim quote, checked automatically against the stored copy.
- A blind second reading by a different model covers a sample, not every number: 1,683 of 17,845 numbers. Every difference it found is ruled (`data/second_read_resolutions.csv`).
- `complete` means everything in scope was extracted. `partial` documents still hold things we didn't extract; the `to_do` column says exactly what (charts without printed values, unreadable scans, items waiting for a decision on scope).
- Documents we don't store are not reviewed, so the dataset says nothing about what they contain.

## What happens next

An extraction pass works through the stored documents, starting with the
to-dos marked "Priority review" and the known gaps. For each document it lists
what the document contains, extracts what is in scope, and sets the status:
`complete` only when nothing in scope is left, otherwise `partial` with a
to-do. Tables with printed totals must add up; new numbers go through the
quote check and the blind second reading like everything else.
