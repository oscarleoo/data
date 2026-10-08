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

### Second reading of the St Kitts, Vanuatu, Hong Kong, Portugal 2, Grenada, St Lucia, Dominica numbers (batches f1-f3)
- 251 new numbers read blind (up to 12 per document, all of them where fewer): 244 agreed at once.
- 5 rows are budget targets; the second reader, not told the status, gave the actual printed next to
  the target. Both are in the document; ruled accordingly.
- 2 St Lucia 2015-16 rows are zeros taken from words ("there were no investment inflows", "no outflows").
  No figure is printed. Kept as first reading, but **worth a look**: is a zero from words acceptable?
- 0 open differences in the CBI dataset after this round.

### United States EB-5, batch 1 (pass `extract-cbi-usa1`)
- 20 documents reviewed: all complete.
- Added 3,258 numbers, 6 rules, 5 events.
  - State Department Visa Office tables V and VI, FY2005-FY2008: EB-5 visas for every country listed
    (zeros included), by class (C5, T5, R5, I5) wherever the total is not zero, plus region totals.
  - DHS yearbooks 2013 and 2023: EB-5 green cards by class, by adjustment vs new arrival.
  - DHS Inspector General 2013 and 2015 reports: regional-centre counts and decisions, processing
    times, fees. Court orders in Behring (2021, 2022). trumpcard.gov fees. Jay Peak restitution.
- Every printed total adds up, with three explained exceptions: the 2023 yearbook rounds cells to the
  nearest ten; the 2013 yearbook withholds five small cells ("D"); FY2006 East Timor shows 11 visas
  (looks misplaced in the source, recorded as printed).
- 5 new indicators proposed (regional-centre applications received, approved, denied; intermediary
  fee per investor; processing time in months).

### Hungary, Malta, other Europe (pass `extract-hun-mlt-eur`)
- 16 documents reviewed: 14 complete, 2 partial (both Maltese regulator reports).
- Added 699 numbers, 2 rules, 4 events. All quotes match the PDF text.
  - Malta 2019-20 regulator report (556 numbers): applications, approvals, refusals, naturalisations
    by year 2015-2020; applicant profiles (sex, region, other citizenships, job, education, age);
    properties bought and leased by locality and value; government stock; contributions and how they
    were shared; fees; charity donations; agents.
  - Malta 2014 report: 173 applications to June 2014, shares by country (Russia 54.3%), agents;
    projections marked as such.
  - Hungary debt agency (ÁKK) reports 2013-2022: residency bond series by year in EUR and HUF,
    the 2018 repayment, last issue September 2017. Some series change between reports after sales
    ended, unexplained; recorded as printed and flagged.
  - Turkey: an MP's claims in a parliamentary question (451 main applicants behind 1,198 irregular
    citizenships, USD 181.2m), marked as claims. UK: pre-2008 investor route prices.
- Partial (Malta): ten charts and maps in the 2019-20 report and one in 2014 carry printed values
  that OCR could not tie to months or regions; they need reading by eye. The 135-recipient charity
  list is not copied out (totals are). Smaller figures with no measure yet (agent success rates,
  15 referrals to the financial intelligence unit, 24 review requests) are listed in the to-do.
- 3 new indicators proposed (licensed agents, applicant profile share, applicant donations).

### United States EB-5, batch 2 (pass `extract-cbi-usa2`)
- 20 documents reviewed (Visa Office tables V and VI, FY2009-FY2018): all complete.
- Added 11,049 numbers: EB-5 visas for every country listed, zeros included, by class wherever
  the total is not zero, region totals and grand totals. Every printed total adds up; every quote
  matches. The 9-11 rows per document already in the data were skipped; their values match.
- 14 country codes appear for the first time in the EB-5 rows (small territories, plus Cabo Verde
  and Eswatini under their new names); check.py accepts them.

### Other countries (pass `extract-other`)
- 24 documents reviewed: 23 complete, 1 partial.
- Added 852 numbers, 55 rules, 12 events. Mostly the Philippine Retirement Authority reports
  2016, 2019, 2020 (enrolment by nationality and region, deposits, fees), Australia FOI release 2016,
  Ireland written answer 4 May 2022 (approvals by year and investment type), Malaysia MM2H rules
  (18), Samoa brochure (13), Singapore GIP (7).
- Partial (Philippines 2016): two 2015 targets in a scanned appendix are unreadable; three figures
  with no measure yet (annual-fee payers, receivables, interest on deposits).
- Did not add up or disagree (all recorded as printed): Ireland's investment-type euro values sum
  to €1m more than the printed total; several Philippine figures differ between text, charts and tables.
- **Decision needed:** a 2017 Philippine row files net deposits under `rbi_investment_total`, while
  this pass uses that indicator for gross deposits and proposes `rbi_deposits_net`. One Oman row
  (378 workers given investor residence) has no programme, because the audit doesn't say which.
- 6 new indicators proposed.

## Whistleblowing topic

### Priority documents (pass `extract-wb-priority`, in topics/whistleblowing)
- 25 documents reviewed: 21 complete, 4 partial (the ledger; the agent's summary said 20/5).
- Added 199 numbers, 28 rules, 2 cases, 11 events.
  - Ontario Securities Commission statements 2019-2026: payments to whistleblowers, paid-to-date
    totals, award rules (5-15%, $1m threshold, caps; the 2026 statements drop the caps).
  - HMRC annual reports: reward numbers were already in; added the 2025-26 reward scheme's 15-30%.
  - Slovak Whistleblower Protection Office reports 2021-2025: reports received, cases, protected
    statuses, fines, inspections, law changes. FinCEN bulletins, NHTSA award page, CFTC 2011.
- Partial: Slovak 2023-2025 infographic and chart pages that need reading by eye; the stored CFTC
  2011 report lacks the appendix it refers to.
- Slovak reports disagree with each other on several yearly counts; both versions kept.
- Proposed: a separate programme `svk-uoo` for the Office's protection work, 10 new indicators,
  a rule type for the maximum employer fine.
- Whistleblowing ledger: complete 21, partial 4, not reviewed 557 (of 582 sources).

### Antigua and Barbuda, batch 1 (pass `extract-cbi-atg1`)
- 20 documents reviewed (the 2013 Act, regulations 2013-2024, CIU web pages, IMF 2014 and 2022): all complete.
- Added 34 numbers, 24 rules and fees, 4 events: due-diligence, agent-licence, passport, renewal
  and processing fees; the 35-day stay rule; dependants up to 29 (2017), parents from 58 (2019),
  2024 changes; IMF share-of-GDP figures and projections; 4 Iraqi nationals granted citizenship to
  April 2016 (a CIU page).
- Conflict kept: the CIU's 2017 table shows Iraq with 4 applications and 6 passports to Dec 2015,
  the Iraq page says two approvals and four people.
- **Worth a look:** two IMF numbers have a period the pass had to set (the "about 1.9% of GDP after
  2015" recorded for 2016-2020; St Kitts "more than 10%" recorded as 2014). Notes say so.
- Gaps: the stored 2019 regulations scan stops mid-page 6; the commencement order and the 2016
  regulations are not stored.

### Second reading of US batches 1-2, Hungary/Malta/Europe, other countries, Portugal 3 (batches h1-h5)
- 389 new numbers read blind (up to 8 per document): 374 agreed, after fixing the comparison
  script for amounts written with "billion", "₱" or "Php".
- Ruled: one target vs accomplishment (both printed); three figures printed in words or wrapped over
  two lines (agree); a Denmark visa total where the second reader took the wrong column.
- **Worth a look:** four Philippine chart values have no printed unit. The first reading recorded
  them in thousands, inferred from other printed figures, and says so in the notes. Digits agree.
  Should values with an inferred unit stay, or be dropped?
- 0 open differences in the CBI dataset after this round.

### Second reading, whistleblowing priority pass (batch w1)
- 66 new numbers read blind: 65 agreed; 1 ruled (a Slovak count split by retaliation: 21 of 68).
- **Worth a look:** two Slovak "open reward claims" rows (2023, 2025) the second reader could only
  infer from prose, though they agreed with the first reading.
- 0 open differences in the whistleblowing dataset.

### Whistleblowing: Canada (pass `extract-whistleblowing-can1`)
- 14 documents reviewed: 12 complete, 1 partial, 1 not applicable.
- Added 20 numbers, 15 rules, 3 events: CRA informant programme rules (5-15%, $100,000 minimum, no
  reward for anonymous tips); OSC programme rules; the OSC 2022 programme update (840+ whistleblowers,
  tips by type, by region, insiders who reported internally first, 626 hotline calls, 19 respondents).
- Partial: the OSC update's yearly tip counts exist only in a chart image that isn't stored (the
  image link is listed as a lead).
- **Decisions needed:** these pages print a bare "$"; recorded as CAD to match existing Canadian rows,
  but the dataset's rule says bare "$" outside the US is "unspecified" unless the document names the
  dollar. The OSC update appears to be dated 9 March 2023, while the source record and event say 2022.

### Antigua and Barbuda, batch 2 (pass `extract-cbi-atg2`)
- 6 documents reviewed (IMF Article IV 2023, 2025, 2026; budget speeches 2023, 2024, 2026): 5 complete, 1 partial.
- Added 55 numbers: programme revenue in EC$ and as % of GDP, actual and projected, 2018-2031;
  "nearly 60 per cent of non-tax revenue" (2022, 2023); the 2024 budget's Appendix 2 lines
  ("CIP Collections" 2022 actual EC$67.9m, 2023 preliminary EC$67.0m, 2023 and 2024 budget EC$100m;
  CIU surplus funds EC$30m).
- Partial (IMF 2025): two charts of programme revenue for six Caribbean countries have no printed values.
- Sources disagree on 2022 revenue: 2023 speech EC$88.8m vs 2024 budget EC$67.9m vs IMF 68. All kept.
- Possible correction: the 2026 IMF report says the regional regulator law was approved "in late
  2025"; the existing event says no date is given.

### Malta, batch 1 (pass `extract-cbi-mlt1`)
- 20 documents reviewed (legal notices 2013-2026, the EU Court of Justice case C-181/23, Commission
  documents, IMF 2019): 19 complete, 1 partial.
- Added 24 numbers (IMF budget balances excluding programme money, 2016-2024), 37 rules (deposits,
  due-diligence, administrative, residence-permit, passport, agent-licence and renewal fees; property,
  rent, income and asset thresholds; donations) and 7 events (court case milestones 2020-2023;
  agents' promotional payments; cessation grounds deleted 2017; applications lapsing 29 April 2025).
- Partial: the Commission's 2019 report is stored twice as different PDFs; only Malta's part taken here.
- **Worth a look:** L.N. 159 of 2025 says investment-route applications not approved before
  29 April 2025 "shall cease to have effect". That is a primary source for the closure date the
  Malta programme note currently calls unverified.

### Whistleblowing: United Kingdom (pass `extract-whistleblowing-gbr1`)
- 16 documents reviewed: all complete.
- Added 14 numbers, 21 rules, 1 case. Mostly figures the 2026 Fisher review quotes from other
  sources (marked reported): 774 UK nationals tipping US programmes 2012-2023, SEC, CFTC, CRA and OSC
  totals; its descriptions of other countries' rules; Birkenfeld's $104m award (he went public).
  SFO speeches: "over 700" UK whistleblowers to US programmes.
- **Decisions needed:** a new rule type for the 45% tax HMRC would withhold from rewards (draft law);
  whether rules quoted from a secondary review should stay; three period choices the pass had to make.
- Not recorded (no matching programme yet): FCA and SFO whistleblowing case counts, police payments
  to informants (£1.04m in 2022/23), Korea's tax-informant schemes. Listed as gaps.

### Grenada, batch 1 (pass `extract-cbi-grd1`)
- 20 documents reviewed: 19 complete, 1 partial.
- Added 1,373 numbers, 12 rules, 9 events. Finance Ministry statistics sheets 2014-15, 2016,
  2017 Q3 and Investment Migration Agency sheets 2024 Q4, 2025 Q4, 2026 Q1: every cell, by month or
  quarter and by route, plus yearly shares of applications by country (the sheets don't say whether
  by nationality or residence; recorded as `country=`). IMF reports 2016-2025: programme revenue,
  inflows, bond payments for every year printed. 2024 IMA circular (9 fees).
- Did not add up: the 2014-15 sheet's total column prints 128 applications while the months add to
  131, and EC$70.2m due while the running total reaches EC$71.685m. Both recorded, not resolved.
- Partial: an EU document identical to another stored one; two statements to record once under the other id.
- **Decisions needed:** three new indicators; two percentage figures filed under money indicators
  for lack of a fitting one; bare "$" in the 2025 budget recorded as "unspecified" while the 2024
  row says EC$; one existing rule quotes a fees page that isn't in the stored file.

### Hong Kong, batch 1 (pass `extract-cbi-hkg1`)
- 20 documents reviewed: all complete.
- Added 17 numbers, 6 rules, 2 events: applications filed with an accountant's net-asset report
  (2009-2014, count and share); 2022-2023 visas under the old scheme; the 2012 announcement's totals
  since 2003 (about 8,200 investors, 15,500 dependants, about $58bn); the HK$6.5m and HK$10m
  thresholds; the new scheme's HK$30m net-asset rule and its 2025 change; nearly 7,000 enquiries.
- Every statistics page adds up; approvals in principle plus formal approvals match each year's total.
- **Decision needed (recurring):** Hong Kong annual reports print a bare "$". Existing rows record
  HKD; the dataset's rule says "unspecified". One choice should apply to all of them.

### St Kitts and Nevis, batch 1 (pass `extract-cbi-kna1`)
- 20 documents reviewed: 15 complete, 5 partial.
- Added 338 numbers, 94 rules and fees, 14 events.
  - **Biggest gap found:** the main tables of the 2021 and 2023 IMF Article IV reports are images
    with no text, so earlier passes never took them. Read by OCR: programme revenue in EC$ and as %
    of GDP 2016-2030, due-diligence costs, balances excluding programme money.
  - CIU web pages, December 2022 address, 2023 press release: prices and fees (45 rules).
  - IMF working paper 15/93 (the multi-country one): 75 numbers, 39 rules, 4 events.
- Partial: one fee in the scanned 2022 address reads US$37,500 or US$87,500 depending on scan
  resolution (left out; needs an eye check); balances in EC$ and percentage changes with no measure yet;
  several items in WP 15/93 (listed in the to-do).
- Did not add up: the 2025 IMF report prints -11.0 in a text table and -11.3 in Table 2 for the same
  balance; recorded the Table 2 figure.
- **Decisions needed:** 8 new indicators; past years in IMF tables recorded as "actual" while existing
  rows from the same tables say "estimate"; Comoros programme end (IMF says September 2013, other sources
  May 2016; recorded as a separate event). The low-resolution OCR the quote checker uses reads the
  US$150,000 limited-time price as "190.000"; two sharper passes read 150,000.

### Hong Kong, batch 2 (pass `extract-cbi-hkg2`)
- 20 documents reviewed: 19 complete, 1 partial.
- Added 35 numbers, 8 rules, 2 events. Mostly InvestHK releases on the new investment scheme
  (2024-2026): enquiry counts, 918 applications in the first scheme year, investment by asset class
  (amounts and shares), online applications from 16 September 2024, the March 2026 family-office
  conditions (HK$240m assets, HK$2m yearly spending).
- Every table adds up (statistics pages, the 2008 country table of 1,114, both asset-class tables).
- Partial: the 2005 Legislative Council reply's processing target ("90 per cent within six weeks") and
  staffing have no measure yet.
- **Decisions needed:** a proposed `rbi_investment_share` indicator; one event about the March 2026
  measure now appears twice (from two sources).

### Second reading, batches i1-i3 and x1
- CBI: 267 new numbers read blind (Grenada, St Kitts, Antigua, Malta, Hong Kong, other countries):
  all agree or ruled, after the comparison script learned "nearly", brackets (outflows), "P" and "M".
  Ruled: one target vs accomplishment; six more Philippine chart values with no printed unit (same
  open question as above: inferred "thousand").
- Whistleblowing: 24 new numbers (Canada, UK): all agree.
- 0 open differences in either dataset.

### International documents, batch 1 (pass `extract-cbi-intl1`)
- 20 documents reviewed (European Commission reports on investor schemes 2019-2025, visa-free
  monitoring reports, the EU Court case): 16 complete, 4 not applicable.
- Added 72 numbers, 25 rules, 13 events. Notably: Vanuatu 2015-2021 from COM(2024) 366 (14,504
  applications, 13,489 citizenships, 10,524 passports, 1,015 rejected or revoked; top nationalities);
  Montenegro (109 decisions to 2021 by nationality; 2023: 701 naturalised, 396 Russian, 65 Chinese);
  North Macedonia, Moldova; the US$200,000 Caribbean minimum; 87 Russian applications pending in Grenada
  (September 2024); Bulgarian routes, EU application fees, adoption years of six EU schemes.
- Took the items earlier passes left on the twin copies (Croatia, Cyprus; the Caribbean minimum and
  Serbia's "more than 200" Russians naturalised).
- **Decisions needed:** Dominica rejections printed as both "210 (2023)" and "180 (2023)" (the 180 is
  probably 2024); Serbia has no programme in the dataset (row has none); Vanuatu lists "Republic of
  Korea" among restricted countries (probably North Korea meant; recorded as printed).
