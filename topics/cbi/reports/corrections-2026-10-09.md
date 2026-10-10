# CBI corrections run, 2026-10-09

Decision 12 in practice: 108 suspected errors in existing rows (collected from audits, extraction passes and second
readings) were each drafted by one reader against the cited page, then checked blind by a second reader who saw only
the current rows, the proposed change and the location (not the drafter's verdict or reasoning). Only fixes both
readers support are in `data/corrections.csv` (749 lines, `by` = "corrections 2026-10-09 ..."); each line's reason
holds the drafter's reason, the cited quote and the second reader's quote and comment.

| Outcome | Items |
|---|---|
| Applied in full | 74 |
| Applied in part (see below) | 5 |
| Indicator definitions fixed directly earlier (q059, q060) | 2 |
| No change needed (drafter found the row right) | 18 |
| Rejected by the second reader, not applied | 1 (q058) |
| Left for a person | 8 |

## Applied in part

- **q053** rounded official figures: only the two Singapore rows became `actual`. The Saint Kitts speech figure stays a `claim`, and the Turkish figure is printed exactly, so the rounding rule doesn't apply (second reader).
- **q081** Grenada: the source note was fixed; the Grenada event was **not** deleted (see open question A).
- **q074** Dominica and **q078/q080** Saint Kitts: duplicate sources merged, but the country-tagged events were kept and pointed at the surviving source (open question A).
- **q078** was rejected as drafted because 10 rows would have pointed at a deleted source; those 10 are exactly the rows q079 (confirmed) deletes as duplicates, so both were applied together.

## Rejected (not applied)

- **q058** Uruguay "UI" -> "UYI": the decree prints "UI"; changing 4 of 10 rows would split one unit into two labels. If we want ISO codes, that's a rule for all rows.

## Left for a person

Open question A, events: when a duplicate pair is one country-tagged event and one region-wide event ("the five
Eastern Caribbean countries"), do we keep both (one per country page) or only the region-wide one? Held for
Grenada, Dominica and Saint Kitts and Nevis; my suggestion is to keep the country copies, since country pages need them.

- **q016** Malta 2018 report: the printed label says 'till 30th June 2017' but the figures are cumulative to 30 June 2018 (each equals the 2017 report's cumulative plus the 2017/18 distribution). Draft: period 2014/2018-06, printed label kept in notes. Held for Oscar: it overrides a printed label using arithmetic.
- **q055** North Macedonia: is the 'launch' the 1992 citizenship law or the 2005 criteria decree? The documents don't settle it.
- **q056** Grenada launch: the blog source isn't stored; the stored INCSR 2000 points to the 1997 Act.
- **q024** Seven Canadian counts (tax filers, survey respondents) filed as a share: they need a count indicator that doesn't exist yet.
- **q034** Grenada IMF adjustment (-4.5% of GDP, stored as +4.5) filed as agents' income: needs a new indicator, and the sign fixed.
- **q036** Two percentage changes in fees (-14.7%, +70.7%) filed in a money indicator: need a percent-change indicator.
- **q046** Turks and Caicos Home Owner's Permit is a separate permit filed under the investor permit: needs a new programme row.
- **q089** Grenada fee quote comes from a 2015 Fees page we never stored; needs fetching (web) before it can be fixed.

## Follow-ups noticed by the readers

- Ledger rows of the 9 merged-away sources disappear automatically (coverage.py lists only current sources); their raw files stay in `raw/` as exact copies.
- 21 second readings now point at deleted duplicate rows; second_read.py reports and ignores them.
- q045: the 2025 Malta row o-bdb6fe9a8c has the same problem as the fixed 2024 row; not yet queued.
- q038: CBI-funded homes approved in plans sit in an indicator for homes built; a planned-homes indicator would be cleaner.
- q092: Bermuda t-af75965433's new quote no longer contains the removal sentence behind valid_to 2024-06-09 (the notes still state it).
- q079: two deleted rows' interpretive notes were not carried over (the surviving rows have equivalent notes).

## Checks after applying (2026-10-10)

- `merge.py`, `check.py`: 0 errors. Every one of the 749 lines took effect; no other row changed; nothing points at a
  deleted source or rule.
- Quote check: of the 31 rows whose quote or location was corrected, 23 match automatically and 8 were checked by
  hand (table layout, line breaks, a scanned page, a Word file, a companion web page, Khmer OCR) and recorded in
  `data/quote_checks.csv`.
- Second reading: 8 Australian figures reopened by the decision 3 change to a 0-4 range; each second reading falls
  inside the range, resolved. 0 open.

## Gap-fill merged (extract-gapfill-2026-10-09)

1,344 printed zeros from the Malta regulator reports and 12 rules stated by a single source (Mauritius, New Zealand,
Panama). Quotes: all 1,344 match (1,261 verbatim, 83 as table rows). No duplicates: rows that looked like duplicates
were the old programme (IIP) and the new one (GCES) in the same report. Blind second reading of 120 sampled zeros: 60
agree; in the other 60 (2016-2019 bought/leased-by-locality tables) the reader gave the figure from the neighbouring
column, which is already stored as that locality's other row with the same value, so the zeros stand.
Left: 2023 "rabat_malta" vs 2024 "rabat" for the same locality; old notes on the 2016-2019 and 2022 locality tables
still say zeros aren't recorded; Image 4 zeros (2023, 2024) and the 2024 combined Table 29 not extracted.

## Found while checking: quotes the automatic check can't match

The full quote check (first run since 9 Oct 02:38) finds 15,020 rows whose quote it can't match in the stored text,
up from 6,321. 8,836 of them are rows added by the overnight passes, mostly the zero passes (4,777, extract-zeros-b)
and the UK spreadsheets (3,124, extract-cbi-gbr1). These rows are not wrong as far as we know (many are table rows put
back together from cells, which the checker matches poorly), but they are not verified either. To do: sample them by
eye per pass, then either improve the checker for spreadsheet rows or record checks.

## 2026-10-10 follow-ups

- Decision 13 (one event per joint action): the Grenada, Dominica and Saint Kitts and Nevis country copies deleted;
  their region events list the countries in the new `countries` column.
- q089 resolved: the Grenada Fees page archived 29 June 2015 is stored (`grd-cbiunit-web-fees-2015`), the
  government-fee rule cites it, and its 7 other fees are extracted. Blind second reader: 7 confirm; the application
  fee's "per application" was an inference, so the row now says the page prints no unit.
- Oscar's answers (2026-10-10): q016 applied (Malta 2018 period to June 2018; sums shown above check out); q055 and
  q056 settled by decision 14 (keep both dates / both accounts); q024, q034, q036, q046 moved to three new
  indicators (programme_migrants_counted, cbi_agent_commission_outflows_pct_gdp, fee_change_pct) and a new programme
  (tca-home-owner-permit). The Grenada IMF figure is now stored as printed, -4.5. No items from this run remain open.
