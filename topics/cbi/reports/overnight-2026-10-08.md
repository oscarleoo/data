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


### Hong Kong (pass `extract-hkg`)
- 16 stored documents reviewed: all 16 complete.
- 31 numbers added: the two earlier years printed in each Appendix 5 table of the Immigration
  Department annual reports 2013-2023 (22), and 9 from the February 2011 Legislative Council reply
  (monthly averages of investors and money for 2008-2010; two application counts that come from the
  legislator's question, marked unverified; "about 1%" of property sales, under a proposed indicator).
- Every repeated year matched the earlier report. All new quotes found.
- Flagged: the 2023 annual report says the new 2024 scheme's HK$30m is "excluding real estate",
  while the December 2023 brief lets commercial property count up to HK$10m.

### Second reading of the Greek and Antiguan numbers (batches e1-e6)
- 441 of the new numbers read blind by a second model: all 158 quotes the script could not find,
  plus a sample. 435 agreed at once.
- 5 "disagreements" were a parsing fault (a space after "$"); fixed in `second_read.py`, now agree.
- 1 real difference: Turkey's share of pending Greek files, August 2026. The page prints 18,1%
  (checked on the page image); the second reader's OCR gave 18,19. Ruled first reading correct.
- Result: 0 open differences across the whole CBI dataset (5,887 confirmed, 113 ruled).

### St Kitts and Nevis, Vanuatu (pass `extract-kna-vut`)
- 16 documents reviewed: 11 complete, 5 partial (the ledger file; the agent's own summary said 10/6).
- Added 58 numbers, 11 fee rows and 2 events. St Kitts audit reports 2016-2024: programme revenue
  split by component, revenue targets, the programme's share of government cash receipts, running
  costs, the citizen dividend. Vanuatu Treasury monthly reports: December collections, restated
  yearly totals, 2025 target. Vanuatu fee pages: family-size prices, due-diligence and child fees.
- Partial (St Kitts audit reports 2018-2022): spending on the Hurricane Relief
  Programme is printed, but the reports don't say it was paid from programme money. Left out
  pending a decision. **Decision needed.**
- Conflicts noted: Vanuatu fee schedule says a VT5,000 application fee, the web page says USD 250.
  St Kitts 2023 components add to $622.3m against a printed $621m.
- 5 new indicators proposed (revenue component share, account balance, share of cash receipts,
  programme costs, dividend payout); marked "proposed" until reviewed.

### Portugal, batch 2 (pass `extract-cbi-prt2`)
- 20 documents reviewed (17 SEF golden-visa maps 2012-2023, two fee laws, the 2012-2013 map): all complete.
- Added 1 number (the 2012 all-routes investment total, €2,155,873.56), 8 fee rules (card copies and
  replacements, permanent residence for golden-visa holders, 2023 fee table) and 1 event (the 2023 fee table).
- Every existing number in the 17 maps was re-read against the PDF text and two OCR passes; none changed.
  The maps print only the top five nationalities, so no full nationality table exists in these documents.
- April 2023: the two real-estate amounts add to €0.20 more than the printed total (already noted on the row).

### Grenada, St Lucia, Dominica, Antigua (pass `extract-grd-lca-dma-atg`)
- 19 documents reviewed: 16 complete, 3 partial.
- Added 1,058 numbers, 27 rules and fees, 5 events. Grenada Ministry of Finance quarterly sheets
  (2019 Q4, 2022 Q4, 2023 Q1-Q4) and investment-migration sheets (2024 Q4, 2025 Q4) now extracted in
  full: every month and quarter, every row. Also St Lucia annual reports 2015-16 and 2016-17, IMF papers
  on Grenada, St Lucia and Dominica, the 2024 Grenada regulations (18 rules), St Lucia 2017 regulations,
  and Antigua's 2017 "disparities" web page (16 rows, by country of origin).
- Partial:
  - St Lucia 2016-17: charts on pp. 6, 11, 12 have no readable values; the approved-projects table
    (costs, jobs, rooms) has no matching measure yet; agent licence counts not recorded.
  - St Lucia 2015-16: project costs, per-application values, agent counts not recorded.
  - IMF working paper 15/93: one PDF stored under three ids (Dominica, St Kitts, international);
    only Dominica's part extracted here; the rest is to be done once under the international id.
- Tables that did not add up (noted on the rows): Grenada 2023 Q2 first version (year-to-date total
  leaves out fees; the second version adds up), 2022 Q4 (leaves out "Other fees"), several EC$1 and
  one-cent rounding gaps; St Lucia 2015-16 fees 569,748 vs printed 569,747.
- Proposed indicator `cbi_due_to_government` (amounts due to government, calculated by the
  government from approvals, not cash received).

### Portugal, batch 1 (pass `extract-cbi-prt1`)
- 20 documents reviewed: 18 complete, 1 partial, 1 not applicable (Portaria 208/2017, a list of places).
- Added 35 numbers, 16 rules, 2 events. Mostly from the 2014 IGAI audit of the golden-visa
  scheme (applicant files per immigration office, fee revenue per office), the 2026 AIMA fee table,
  reduced minimums for low-density areas, and Decreto Regulamentar 1/2024.
- AIMA annual reports 2023-2025: re-read page by page; everything in scope was already in the data.
- Partial (IGAI audit): three approximate figures have no measure yet (about 90% filed in Lisbon,
  about 300 approved files awaiting fee payment, up to 100 appointments a day).
- Did not add up (recorded as printed): IGAI Madeira "11 + 21 = 33"; AIMA second card copy
  EUR 4,210.30 vs 50% of the issue fee (4,209.45); low-density culture route EUR 220k vs 20% off 250k.
- New split values made up by the pass, to review: `region=sef_*` offices, `applicant=main_and_family`.

### Portugal, batch 3 (pass `extract-cbi-prt3`)
- 14 documents reviewed (SEF annual reports RIFA 2013-2022, July-September 2023 infographics,
  Constitutional Court ruling 1133/2025): all complete.
- Added 9 numbers and 3 events: 2013 shares of applications by nationality (China 80%, Brazil 3%,
  Russia 3%, Angola 2%, South Africa 2%, others 11%; printed shares add to 101%), 2013 refusals,
  2019 family-member permits from the legal-basis table (2,186; the same report's text says 2,390,
  unexplained, both kept), the 2012 and 2013 rule changes, the 2018 portal update.
- Did not add up, no figures printed for the rest (gaps, not to-dos): approvals by route in 2014
  (1,523 vs 1,526), 2015 (764 vs 766), 2017 (1,276 vs 1,351, EUR 26.9m short).
- Fixed: two August 2023 rows quoted "SUBALÍNEA 1", which the page doesn't print. The page prints
  "SUBALÍNEA 3" with "SUBPARAGRAPH 1" (a misprint). Quote corrected via corrections.csv after
  checking the page image.
