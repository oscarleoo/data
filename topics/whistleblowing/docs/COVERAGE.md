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

## Where we are (as of 2026-10-08)

- Sources: 582, of which 558 have a stored copy.
- Reviewed against their full contents: **0**. Not yet reviewed: **582**.
- Stored documents with no numbers extracted: 388 (many are laws or articles used for rules and events, but none is checked yet).
- Stored documents with only one or two numbers extracted: 54.
- Sources with a written to-do: 25.

So: every number in the dataset is checked against its source (quotes and a
blind second reading, see the README), but the dataset is **not** a complete
extraction of the documents it cites.

## What happens next

An extraction pass works through the stored documents, starting with the
to-dos marked "Priority review" and the known gaps. For each document it lists
what the document contains, extracts what is in scope, and sets the status:
`complete` only when nothing in scope is left, otherwise `partial` with a
to-do. Tables with printed totals must add up; new numbers go through the
quote check and the blind second reading like everything else.
