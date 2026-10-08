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

### Whistleblowing: United States, batch 1 (pass `extract-whistleblowing-usa1`)
- 20 documents reviewed: 18 complete, 2 partial.
- Added 410 numbers, 2 rules, 6 cases, 9 events. Mostly CFTC whistleblower reports to Congress
  FY2012-FY2025: every line of the reward fund table, award liabilities, final orders, denials,
  notices of covered action, tips, and the FY2023 award counts that were missing (174 denied,
  181 decided, 65 withdrawn, 41 orders). Trafigura ($55m, first CFTC case for gagging whistleblowers).
  Two denied claimants from 2024 orders (anonymous). The Zafirov appeal ruling (1 September 2026).
- Partial: the stored FY2012 and FY2013 reports lack their audited financial statements.
- Did not add up: $1 rounding in three fund tables; FY2021 new awards $45,990 in the table vs
  $45,851 in the footnote; FY2025 gives 1,503 tips for FY2023 vs 1,530 in the FY2023-24 reports;
  an unexplained $10m transfer out of the fund in FY2025.
- **Decisions needed:** 5 new indicators; scope calls behind "complete" (website statistics,
  fund accounting detail, "about a third" of leads from tips are not recorded); two ids are the same
  Zafirov file.

### Hong Kong, batch 3 (pass `extract-cbi-hkg3`)
- 13 documents reviewed (Legislative Council replies and annexes 2004-2025): 11 complete, 2 partial.
- Added 21 numbers, 10 rules, 1 event: property investment by the old scheme's investors (HK$14.35bn,
  93% residential; district shares from a sample of 200), 465 applications in 2004, average investment
  per investor (HK$7.17m, 2004), new-scheme counts to May 2024, minimum amounts.
- Partial: a sample count ("10 of 100 renewal cases changed property") and "around three weeks" have
  no fitting measure without converting.
- Hong Kong now: all 69 stored Hong Kong documents reviewed (66 complete, 3 partial; checked in the ledger).
- **Worth a look:** an existing row (o-17157f5c8a) records 0 rejections from the words "no application
  has been rejected so far". Same question as the St Lucia zeros.

### St Kitts and Nevis, batch 2 (pass `extract-cbi-kna2`)
- 20 documents reviewed (budget Estimates 2010-2026, budget addresses 2024-2026): 19 complete, 1 partial.
- Added 324 numbers, 1 rule, 2 events: the programme revenue line in every Estimates volume
  (forward estimates as projections, approved budgets, actuals), its split by item (fees, application
  fees, background checks, hurricane relief and sustainable growth fund contributions, the 2024
  sustainable island state contribution), and the Citizenship by Investment Unit's own budget.
  The 2013 volume was read entirely by OCR. About 17,500 people received the first citizen dividend.
- Did not add up (noted on the rows): 2012 and 2013 actuals (items vs summary line), 2024 budget
  (items EC$5m above the summary).
- **Decision needed:** Estimates 2023 p. 30 appears to swap the labels of the CIU and Human Resources
  rows (the 2024 volume reprints them the other way round). Those 2023 figures are held back.
- Not stored: Estimates Volume I for 2020.

### Grenada, batch 2 (pass `extract-cbi-grd2`)
- 16 documents reviewed: 15 complete, 1 partial.
- Added 2,333 numbers, 15 rules, 1 event: statistics sheets 2018, 2020 Q4, 2021 Q4 (every cell);
  budget books 2017-2026 (the programme fee line and parts, the "CBI Committee" dividend line,
  National Transformation Fund grants, and every capital project funded by that fund, 1,781 rows);
  the 2024-2025 fiscal frameworks; SRO 12 of 2024 fees; the 2025 Citizenship by Invitation launch.
- Did not add up (recorded as printed): fund project lines vs printed totals in the 2021 and 2022
  books (EC$120,000 and EC$100,000 short); 2025 book Table 3 vs line item for 2024 revenue
  (334.3m vs 280,697,922); small rounding gaps.
- **Decisions needed:**
  - The 1,781 fund project lines (cells printed "-" recorded as 0, as earlier passes did): keep all,
    or keep only totals?
  - "International Bonds 2015-2030 ERI" interest is recorded as programme-linked bond payments
    because the amounts match the IMF's "Bondholder CBI-related payments"; the books never spell out ERI.
    That is an inference.
  - Partial: a press release says collections beat target by $7.7m without printing either figure.

### Vanuatu, batch 1 (pass `extract-cbi-vut1`)
- 20 documents reviewed (citizenship laws 2013-2021, regulation orders, the 2020 fee directive,
  Citizenship Office pages, IMF 2015, 2016, 2023): 16 complete, 3 partial, 1 not applicable.
- Added 23 numbers, 82 rules, 4 events: all 16 prices in the 2020 fee directive (VDSP and VCP),
  agent minimum prices and fees in Order 33 of 2019, statutory 3-month decision deadlines, the 2013
  investor-route rules; IMF projections of programme revenue 2024-2028, "down 27 percent" in 2022;
  the IMF 2015 table of 24 programmes worldwide (minimum investments, residence requirements).
- Partial: IMF charts with no printed values; the CIIP agents page (whether to record its "suspension
  lifted as of 21 March 2016").
- **Decisions needed:** statutory deadlines recorded as `processing_time_months` with status budget
  (the European Commission row uses "reported"); three programmes in the IMF 2015 table matched by
  amount (Switzerland, New Zealand, Australia) and one with no programme (France EUR 10m); the IMF says
  the EU delayed full suspension to August 2024, EU documents say it was decided in November 2022.

### St Kitts and Nevis, batch 3 (pass `extract-cbi-kna3`)
- 12 documents reviewed (regulations SRO 26/2023, 20/2024, 43/2024, 1/2026; the Prime Minister's
  October 2024 speech; sugar-industry background sources): 11 complete, 1 partial (a duplicate file).
- Added 24 numbers, 66 rules, 4 events: full price and fee schedules of the 2023, 2024 and 2026
  regulations (couple and dependant prices, due diligence, processing, post-approval fees, agent
  fees, payments to agents out of each donation, transition fees); parents as dependants from 55;
  the PM's claim of "between 60-70 percent of our Federal revenue" (marked as a claim); FAOSTAT
  raw-sugar exports 2008-2017 and 2022.
- **Correction needed:** an existing event attributes the January-June 2023 US$125,000 price to a
  news article that doesn't say it; it comes from the CIU head's December 2022 address.
- St Kitts now: all 61 stored St Kitts documents reviewed (49 complete, 12 partial; checked in the ledger).

### United States EB-5, batch 3 (pass `extract-cbi-usa3`)
- 20 documents reviewed: 19 complete, 1 partial.
- Added 9,833 numbers, 36 rules, 37 events.
  - Visa Office tables V and VI, FY2019-FY2024 (8,264 numbers): every country, every class, including
    the post-2022 set-aside categories (rural, high unemployment, infrastructure). Every table adds up.
    FY2019 and FY2020 Table V are marked provisional (printed as preliminary).
  - Federal Register: the 2019 modernization rule, 2023 Integrity Fund notice, 2024 and 2026 fee rules,
    2025 fee proposal, 2026 integrity proposal: fees, filing counts, regulatory impact estimates, events.
- Partial: the 2026 integrity proposal's cost estimates, staffing figures and small-business tables.
- Documents contradict themselves in places (fee-rule table totals, regional-centre counts 547/589/640);
  recorded as printed with notes.
- **Decisions needed:** 18 new indicators, many for regulatory impact estimates (medians, discounted
  totals): keep that kind of number or drop it? Nine new fee route names. The four largest Federal Register
  documents were read by helper agents and not re-read by the pass itself: **lower assurance** until the
  second reading covers them.

### Whistleblowing: United States, batch 2 (pass `extract-whistleblowing-usa2`)
- 20 documents reviewed: 19 complete, 1 partial.
- Added 161 cases, 71 rules, 17 numbers, 5 events, 1 programme proposal.
  - CFTC final-orders list: 156 orders not yet recorded (107 denials, 49 awards; 26 awards with an
    amount from a press release about that order alone). Anonymous, as the orders are.
  - CFTC press releases: running totals of awards and related sanctions 2021-2026, rule restatements.
  - Reward statutes: IRS (2006), Dodd-Frank (CFTC, SEC), AML Act (FinCEN, kleptocracy pilot), 2022
    omnibus. CRS report on the False Claims Act: recoveries, rules, three named court cases.
- Partial: the CRS report discusses many rulings; only one added as an event so far.
- Only 2 of the 170 CFTC orders are stored, so per-order percentages and sanctions are a gap.
- **Decisions needed:** two ids are the same 1986 law; award decisions under Dodd-Frank and the AML Act
  recorded as discretionary, unlike existing rows reading "shall pay" as mandatory; proposed programme
  for the 25 U.S.C. 201 informer qui tam.

### Fix: CFTC award orders were collapsing into one row (whistleblowing)
- Found while merging the US batch 2: cases get their id from source, date, target, amount and
  location. Every row from the CFTC orders list had the same location ("orders table"), so orders
  issued on the same day merged into one. 56 of tonight's 161 new cases were lost on first merge, and
  8 cases from an earlier research wave (October) had been lost the same way.
- Fixed by giving each row its order number (or the link to its order PDF) in the location, in both
  inbox files, and re-merging. Now: 170 orders on the CFTC list, 170 cases, each once. Two 2020 SEC
  awards on the same page (20% and 30%) were also separated.
- merge.py (both topics) now prints a warning whenever two different rows would get the same id.
  Observations were checked for every pass tonight: every inbox row is in the data.

### International documents, batch 2 (pass `extract-cbi-intl2`)
- 20 documents reviewed (EU visa-waiver acts, European Parliament resolution 2022, EPRS studies 2018
  and 2021): 18 complete, 2 partial.
- Added 109 numbers, 76 rules, 5 events: Cyprus 6,779 passports 2007-2020; Vanuatu 2023 applications
  from China (519) and Russia (237); programme shares of permits and naturalisations by country; shares
  of GDP (Malta 4.3%, St Kitts 35-40%); rejection rates; minimum investments copied by the studies.
- Partial: the 2018 study's Table 4 prints amounts without decimal points ("52 41"; confirmed on the page
  image, not guessed); the 2021 study's charts have no printed values.
- **Decisions needed:** 6 new indicators (incl. processing time in days); whether to keep minimum
  investments the studies copy from other sources (some differ from the laws, e.g. Gozo EUR 250,000 vs 220,000).

### Second reading, batches j1-j7 and y1-y2
- CBI: 545 new numbers read blind, with a heavier sample (15 per document) for the four Federal Register
  documents read by helper agents. All agree or ruled. Ruled: 5 where both figures are printed (annual vs
  ten-year totals, project cost vs this year's budget); a 13%-of-GDP row correctly filed under St Kitts in a
  Vanuatu report; "down 27 percent" recorded as -27.
- The comparison script's number cleanup was rewritten as one loop (handles "not less than HK$500 million",
  "~9.6%", "180 days", brackets...). Re-run on all 7,500+ readings: more agree, none fewer.
- Whistleblowing: 112 new CFTC numbers; two chart values checked on the page image (first reading right).
- 0 open differences in either dataset.

### Latvia, batch 1 (pass `extract-cbi-lva1`)
- 20 documents reviewed (Latvian migration office first-permit tables 2015-2022, ten versions of the
  immigration law, the 2015 annual report, a 2026 press release): all complete.
- Added 527 numbers, 3 rules, 3 events: investor permits by nationality and by route (company, property,
  bank, bonds), main applicants and family members, every non-zero cell; totals for EU/EEA and third
  countries. Replaces the earlier cut-off of nationalities with at least 5 main applicants. Every table adds up.
  Law changes: unrestricted right to work (2014), suspension power and tax-debt annulment (2016), EUR 5,000
  renewal payment (2018), 2026 renewal payments.
- **Decision needed:** zero cells by country not stored (thousands of rows; a missing row means 0 in that
  table). Store them, or leave as is?

### Vanuatu, batch 2 (pass `extract-cbi-vut2`)
- 20 documents reviewed: all complete.
- Added 155 numbers, 1 event: Constitutional Agencies revenue reports 2020-2024 (Citizenship Office
  totals and budgets, programme fees, share of the national revenue budget, investment-plan fees not taken
  before); Citizenship Office 2019 report; Treasury December and half-year updates 2019-2026; budget books
  2025-2026; IMF 2024 and 2025 projections; Ireland ending visa-free travel (March 2024).
- Documents contradict themselves (all recorded with notes): the 2019 Citizenship Office report prints three
  office budgets and two fee budgets; first-half figures are revised in the following year's update; the 2025
  half-year update gives two first-half totals and two budgets.
- **Decisions needed:** new fee-line splits that may include ordinary citizenship fees; a possibly mislabelled
  "Honorary Citizenship Program Fees" line in 2021; the Citizenship Commission's whole budget filed as
  programme costs.

### Vanuatu, batch 3 (pass `extract-cbi-vut3`)
- 1 document (VCP amending order 38 of 2020, a scan read by OCR): complete. Added the old USD 2,000
  due-diligence fee it replaced and a 27 March 2020 rule-change event.
- Vanuatu now: all 48 stored Vanuatu documents reviewed (44 complete, 3 partial, 1 not applicable;
  checked in the ledger).

### Ireland, batch 1 (pass `extract-cbi-irl1`)
- 20 documents reviewed: 16 complete, 2 partial, 2 not applicable.
- Added 162 numbers, 1 rule, 8 events.
  - The 1990s "passports for investment" scheme from Dáil records 1994-2005: cases, the 1998 review's
    appendix checks on whether early cases met the scheme's conditions, irregular naturalisations, the
    files held by the Moriarty tribunal, 1997 government decisions.
  - Immigrant Investor Programme: guideline processing times; the 2017 interim evaluation (amounts by year,
    shares by investment option, family make-up, 2016 approvals, fees, jobs); EY reviews (EUR 593m invested
    2012-2020, 3,377 jobs, sector tables, 97% of 2018 permits to Chinese nationals).
- Partial: interim evaluation charts with no printed values; one EY chart label unreadable by OCR.
- Did not add up: interim evaluation Table 3.2 (submitted amounts 2012-2016 sum to EUR 256.45m vs printed
  EUR 340.95m; Q1 2017 seems included in one total only); jobs 1,644 vs 1,619 in two tables.
- 5 new indicators proposed.

### International documents, batch 3 (pass `extract-cbi-intl3`)
- 20 documents reviewed: 19 complete, 1 partial.
- Added 37 numbers, 21 rules, 5 events: US State Department 2000 report (Dominica US$50,000/75,000 prices,
  about 500 citizenships 1996-2000, 2000 suspension and resumption; Grenada about 300 sold); the rest of
  IMF WP 15/93 (Portugal inflows up to 13% of gross foreign investment in 2014; St Kitts balances without
  programme money; development-fund-backed credit); IMF 2024 region-wide balances; FATF/OECD 2023 cases;
  the 2024 Eastern Caribbean agreement (US$200,000 minimum, one rule per signatory).
- Partial: WP 15/93's recommended buffer size (20-50% of GDP) has no measure.
- **Decision needed:** deficits printed as positive numbers recorded as printed with `category=deficit`.

### Whistleblowing: Korea, batch 1 (pass `extract-whistleblowing-kor1`)
- 20 documents reviewed (Anti-Corruption and Civil Rights Commission annual reports 2010-2025, six press
  releases): 19 complete, 1 partial.
- Added 5,244 numbers, 25 rules, 32 events, 75 cases: every whistleblowing table in each annual report
  (reports received and handled, rewards and amounts recovered, protection requests and outcomes, by year
  and category; each report reprints the history, so earlier years appear again from each source), plus
  Graft Act and Conflict of Interest Act report counts. Korean amounts read with 억 = 100,000,000 and
  만 = 10,000, recorded in the dataset's existing units.
- The new merge warning caught 19 cases colliding (several cases on one page, no target or amount); fixed by
  numbering them in order in the location and re-merging. All 75 in.
- Did not add up or look misprinted (all noted on rows): 2011 protection and preventive totals; 2023 reports
  handled (91,065 vs 91,074); the 2010 reward total printed "21,954,733,31"; the 2024 report says reports
  fell 50.6% when they rose.
- Partial: a 2020 press release's second table image (rewards by sector) isn't stored.
- **Decisions needed:** keep subsidy-fraud and public-funds-fraud reports as two series or merge; 5 new
  indicators; two 2022 case amounts that would break the KRW 3bn cap (unit probably thousand won; left empty).
