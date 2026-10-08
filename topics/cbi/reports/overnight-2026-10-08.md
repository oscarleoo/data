# Overnight extraction log, 8–9 October 2026

What ran while Oscar slept, in order. Nothing here is pushed to GitHub or the site; everything is
committed locally in ~/Claude/data. The per-document truth is `data/extraction_status.csv`; this log
says what was done to it.

## Rules followed

- Only documents we already store; no new web research.
- Every document a pass touches gets a status: `complete` (nothing in scope left), `partial`
  (with an exact to-do) or `not_applicable`. Anything not touched stays `not_reviewed`.
- New numbers: merged, validated (`check.py`), quote-checked (`verify_quotes.py`), then a blind
  second reading of a sample (and of every quote the script could not find).
- Figures computed by us (sums of raw data rows) are held back, not merged, pending a decision.

## Done

### Greece (pass `extract-grc`)
- 21 stored Greek documents reviewed: 12 complete, 9 partial.
- 1,733 numbers merged (family-member permits by nationality, applications by year and status,
  permits issued by month, pending files by category and region, 10 fee and rule terms, 1 event).
- Quote check: 1,627 found verbatim, 32 as table rows, 74 not found (all from OCR'd monthly
  bulletins; going to the second reading).
- Held back: 503 figures from the 2016-2019 permit spreadsheets, computed by summing data-sheet
  rows (`_inbox/extract-grc-spreadsheet-sums.pending`). **Decision needed.**
- Partial because: chart labels in the monthly bulletins (5 docs); spreadsheet sums pending (4 docs).

### Antigua and Barbuda (pass `extract-atg`)
- All 19 six-monthly reports reviewed: 1 complete, 18 partial.
- 3,362 numbers merged: applications by country of birth and by investment route, per half-year and
  since inception; fee revenue; fund tables; contribution totals; the 2015 overview.
- Quote check: 2,358 found verbatim, 920 as table rows, 84 not found (OCR; going to the second reading).
- Partial because: cheque-by-cheque payment lists, per-application contribution lists (would give
  contributions by nationality), passport pie charts, and one stored PDF (2023 H2) missing a page.
- Tables that did not add up (recorded as printed, noted): 2022 H1 countries (319 vs printed 229;
  China printed 105 at 6.55%), 2017 H1 and 2018 H2 since-inception totals off by one, 2016 H2 payments.
- Note: Antigua's tables give **country of birth**, recorded as `birthplace=`, not nationality.

