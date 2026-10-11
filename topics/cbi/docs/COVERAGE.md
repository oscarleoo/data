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

## Where we are (as of 2026-10-11, evening)

- Sources: 1,686, of which 1,681 have a stored copy (news and industry copies are kept locally for checking and not published). Data: 133,546 numbers, 6,563 rules, 1,604 events; 186 programmes in scope (44 citizenship, 142 residence) in 107 countries and territories. Programmes marked out of scope (METHODOLOGY decisions 15 and 18) are kept and not shown.
- Stored documents reviewed: **1,681 of 1,681** (1,615 complete, 36 not applicable, 30 partial). Of the 30 partial documents, 29 are partial only for things that can never be extracted (to_do starts "Not extractable:", METHODOLOGY decision 17: charts without printed values, pages missing from the only copy, paywalls, unreadable scans), and 1 has an optional extra calculation left.
- Sources with no stored copy: 5 (a CAPTCHA or bot check we don't get around, a dead site, a refused connection). They stay `not_reviewed`.
- Quote check (11 October, 141,713 quoted rows): 100,209 match the document word for word, 21,476 as a table row, 3,131 cell for cell in spreadsheets; 12,573 rows whose quote isn't verbatim were confirmed by a blind second reading and 327 by eye on the page; 3,989 are calculated figures (decision 1) whose recipe was recalculated. 7 rows come from sources we don't store and 1 document has no readable text.
- Blind second reading: **40,036 of 133,546 numbers** (30%): all headline totals without a split, the top three in every nationality, route and category table, every newsletter number, every number whose quote couldn't be matched, and samples of the rest. 39,036 agreed at once; the other 1,000 were ruled after a third look at the page (`data/second_read_resolutions.csv`). **4,639 rules** (minimum amounts, fees, periods) were read the same way (`data/second_read_terms.csv`). Where the first reading was wrong it was corrected through `data/corrections.csv`.
- Limit: for scanned documents the stored text is itself OCR, so a matching quote confirms the wording but not every digit; the second reading covers the scans the checks lean on, not all of them.
- Recurring publications: `data/recurring.csv` lists 87 report series and when each is due; `docs/UPDATES.md` describes the routine.

What this does and doesn't mean:

- `complete` means everything in scope was extracted. `partial` documents still hold things we didn't extract; the `to_do` says what.
- The dataset holds every programme we found, not every programme in the world. Leads still open are in `docs/GAPS.md` and the research inbox files.
- Documents we don't store are not reviewed, so the dataset says nothing about what they contain.

## What happens next

An extraction pass works through the stored documents, starting with the
to-dos marked "Priority review" and the known gaps. For each document it lists
what the document contains, extracts what is in scope, and sets the status:
`complete` only when nothing in scope is left, otherwise `partial` with a
to-do. Tables with printed totals must add up; new numbers go through the
quote check and the blind second reading like everything else.
