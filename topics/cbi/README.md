# Citizenship and residence by investment: a sourced dataset

Numbers on the programmes that sell citizenship (citizenship by investment)
or residence ("golden visas") to people who invest or donate money:
41 citizenship and 87 residence programmes, current and closed, in
75 countries and territories: the Caribbean, Vanuatu and the Pacific,
Europe, the Gulf, Asia, Oceania, the Americas and Africa, including the
US EB-5 programme, the old and new Hong Kong schemes, and the closed UK, Irish,
Dutch and Australian schemes. The data also has
the context around them: the end of the sugar industry in Saint Kitts, court
rulings, scandals, and EU, UK and US visa and money-laundering decisions.

The data is incomplete and often uncertain, because governments publish
little, change definitions, and revise their numbers heavily. So this dataset
doesn't try to give one "true" number per year. It records **every claim
separately**: who made it, in which document, on which page, in whose words,
and whether it's an outturn, an estimate, a budget or a forecast. When sources
disagree, the disagreement is part of the data.

Maintained by Oscar Leo ([oscarleo.com](https://oscarleo.com)). Last research
pass: 3 October 2026, followed by a consistency audit (see "Corrections" in
`docs/DATA_MODEL.md`). What we looked for and could not find is listed in
`docs/GAPS.md` and in each research file's `gaps`.

## What's in it

| | rows |
|---|---|
| Numbers (`data/observations.csv`) | 6,677 |
| Sources (`data/sources.csv`) | 1,443, of which 1,267 have a stored copy in `raw/` |
| Programme terms, such as minimum investment by route and date (`data/program_terms.csv`) | 776 |
| Events: launches, rule changes, visa decisions, court rulings (`data/events.csv`) | 771 |
| Programmes (`data/programs.csv`) | 128 (41 citizenship, 87 residence) |
| Headline price per programme, checked by hand (`data/headline_prices.csv`) | 128 |
| Indicators and their definitions (`data/indicators.csv`) | 121 |

Numbers per jurisdiction (ISO codes): USA 834, PRT 646, HKG 606, LVA 462, NZL 425, KNA 390, AUS 256, IRL 249, GRC 234, CAN 211, PAN 181, MLT 175, DMA 165, GRD 157, LCA 150, GBR 138, ESP 127, ATG 112, MNE 105, VUT 99, PHL 91, HUN 90, CYP 83, AUT 74, MYS 64, BMU 60, BRA 56, INTL 46, TUR 44, BGR 37, SGP 31, COM 23, MKD 23, THA 23, ARE 18, NRU 16, KOR 14, MDA 14, CHE 13, EGY 13, IDN 12, ITA 12, TON 12, OMN 11, JOR 10, EST 9, SAU 9, KHM 7, LUX 7, MUS 6, SVK 6, MCO 5, BHR 4, BHS 3, NLD 2, POL 2, FRA 1, MHL 1, SLE 1, STP 1, VCT 1.

When a source splits a number (by nationality, investment route, applicant type), the split is in the `breakdown` column, for example `nationality=CHN` or `route=real_estate;nationality=RUS`.

The full column-by-column description is in [docs/DATA_MODEL.md](docs/DATA_MODEL.md).

## Coverage: what is and isn't extracted

Every number here is checked against its source, but the dataset is not a
complete extraction of every document it cites. Each source has a status in
`data/extraction_status.csv` (not reviewed, partial with a to-do, complete, or
not applicable), and nothing is marked complete without a recorded review. As of
8 October 2026, none of the 1,443 sources has been reviewed end to end yet; known
gaps are listed as to-dos. See [docs/COVERAGE.md](docs/COVERAGE.md).

## How to read it

**One row is one claim, not one fact.** If the IMF, the finance ministry and
the auditor each give a figure for Saint Kitts' CBI revenue in 2021, there are
three rows. To build a time series you pick rows, and which ones you pick is a
choice you should state.

**`status` says what kind of number it is.** Mixing them up is the most
common mistake with this topic:

| status | meaning | rows |
|---|---|---|
| `actual` | official outturn for a closed period (audited accounts, programme unit statistics) | 457 |
| `provisional` | official but preliminary | 40 |
| `estimate` | an estimate by the source, e.g. IMF staff estimates | 186 |
| `projection` | a forecast of a period not yet over | 49 |
| `budget` | a budgeted or target amount | 34 |
| `reported` | a figure a source reports second-hand (media, the EU quoting governments) | 334 |
| `claim` | a statement by an interested party (a minister, an agent) that we couldn't trace to data | 24 |

**Keep the definition in view.** "CBI revenue" means different things:
fees only, fees plus fund donations, net or gross of the programme unit's
costs, with or without money paid to real-estate developers. The indicator
names separate the main ones (`cbi_fiscal_revenue`, `cbi_contributions`,
`cbi_inflows`, `cbi_real_estate_inflows`…) and each row's `notes` say what's
included. When a source gives two versions in one document, both are rows.

**Values are as printed.** No rounding, no currency conversion, no
rescaling: `scale` says whether "442.6" means millions. Ranges ("3–4 percent of
GDP") have the low end in `value` and the high end in `value_high`. Fiscal
years are written `FY2022/23`; check `period_basis` and the notes for when
they start (Dominica and Saint Lucia differ).

## Where sources disagree

`reports/discrepancies.csv` puts side by side every case where rows for the
same jurisdiction, indicator, period and unit have different values, and
sorts each case into one of these groups:

| kind | meaning | cases |
|---|---|---|
| `vintage` | a budget or forecast that differs from the later outturn | 30 |
| `revision` | one publisher changing its own figure in later documents (common in IMF reports) | 85 |
| `same_source` | one document giving two values, usually for two definitions | 15 |
| `conflict` | different publishers disagreeing about what happened | 67 |

A few examples of what this shows:

- **Dominica.** IMF staff reports first put CBI revenue for FY2016/17 at
  EC$50 million (a 2016 projection). Later reports gave EC$332 million (2018)
  and then EC$491 million (2021). Early vintages underestimated the programme
  by a factor of two to three.
- **Grenada.** Government CBI revenue appears in at least four series that
  don't match: an IMF fees-only line, an IMF memo line, the ministry's gross
  series, and the ministry's older net format. For 2023 that gives
  EC$375.3m, 381.6m, 457.3m and 458.3m, all official.
- **Saint Lucia.** In one annual report the programme unit says it
  "contributed" EC$187.6 million since inception on one page and
  "transferred" EC$160.9 million to government on another.
- **Antigua and Barbuda.** The programme unit's passports-issued-by-year
  series changes between its own six-monthly reports: 2016 appears as 1,016,
  314 and 116 in different editions (the last is probably a dropped digit in
  the unit's own chart).
- **Spain.** Answers to parliament count 6,272 property-route visas for
  2013–2023; government press releases in 2024 claim 14,576 "golden visas"
  for the same years without saying what they count.
- **Montenegro.** National figures give 1,113 applications and 869
  approvals; the European Commission's figures use different, undefined
  units.
- **Portugal.** A widely repeated €6.45 billion raised is property
  investment only; the official total across all routes is €7.32 billion.

## How the numbers were checked

- Every row has a `location` (page, table, row) and a short verbatim `quote`.
- Official documents are stored in `raw/` with their SHA-256 checksum in
  `sources.csv`, so a quote can be checked against the exact file we read,
  even if the original moves or changes. News articles and industry reports are
  linked, with an archive link where we have one, and not stored.
- `scripts/verify_quotes.py` looks for every quote in the text of the stored
  copy (with OCR in 29 languages for scans). Of the 8,224 quoted rows,
  7,664 cite a stored document: 6,234 quotes were found verbatim,
  866 matched as a table row put back together from its cells,
  96 were checked by eye against the page image or text, and 465
  (quotes rebuilt from table cells or chart labels) had the number itself
  confirmed by the blind second reading below. 2 point to a stored
  file that turned out not to be the page the quote comes from, and say so;
  1 is a web page the script can't read, checked by hand.
  The other 560 cite news, NGO and industry sources, linked rather than
  stored. Results are in `reports/quotes.csv`; by-eye checks are recorded in
  `data/quote_checks.csv`.
- **A blind second reading.** A different AI model (Claude Sonnet 5) was
  given each number's document, page, indicator, period and kind of figure,
  but not the value, and read the number itself. It read 5,559
  numbers: 5,447 came out the same. The other 112
  were checked on the page: in 95 the first reading was right (the
  second reader took a neighbouring row or column, used the wrong fiscal-year
  convention, misread a scan, or wrote the same figure differently), and in
  17 the document itself prints two different figures, which the
  row notes say. No value had to be corrected; the pass did correct page
  numbers (29 so far) and turned "fewer than N" figures into ranges.
  Numbers from structured files (spreadsheets, XML, JSON) were sampled
  rather than all read twice; the FAOSTAT rows were checked cell by cell by
  a script. Readings are in `data/second_read.csv`, rulings in
  `data/second_read_resolutions.csv`, and the comparison in
  `reports/second_read.csv`.
- `scripts/check.py` validates the tables (types, references, checksums) and
  writes `reports/validation.txt`.

The research was done by AI agents working from primary documents, under the
rules in [docs/RESEARCH_FORMAT.md](docs/RESEARCH_FORMAT.md): no numbers from
memory, nothing inferred or converted, the weaker status when in doubt. The
checks above exist because that process can still misread a table. Before
publishing a number, open the stored document at the given location.

## Known gaps

- **Dominica**: no official counts of applications, approvals or passports
  at all. The IMF says it has no access to them either.
- **Saint Kitts and Nevis**: excellent fiscal data (budget estimates and
  audit reports every year), but no application or naturalisation counts
  before 2023, and no programme unit annual report, although the 2024 Act
  requires one.
- **Antigua and Barbuda**: applications received, but no approvals or
  denials.
- **Turkey**: no yearly series. Only occasional cumulative statements by
  ministers; parliamentary questions asking for yearly data have gone unanswered.
- **Greece**: detailed permit statistics, but no official figures on the
  value invested. Widely quoted totals are application counts multiplied
  by the minimum threshold.
- **UAE, Egypt, Jordan, Singapore, Cambodia**: no regular official
  statistics; counts come from ministers' statements, single decrees or
  rounded multi-year totals.
- **Residence programmes** rarely say how many permit holders later became
  citizens, and few publish the money actually invested.
- **Real-estate money** (paid to developers rather than the state) is
  almost nowhere published, so total inflows are rarely known.
- Every official document is stored. Five news articles could not be
  archived because their sites block the Wayback Machine.

Each research file in `_inbox/` ends with the gaps and leads its researcher
found. They're a good starting point for anyone reporting on this.

## Files

```
data/          the tables (CSV, UTF-8)
raw/           stored copies of official documents, named by source_id
               (the four files over 50 MB are GitHub release assets, listed with
               checksums and download links in raw/RELEASE_FILES.csv)
reports/       generated: validation, discrepancies, quote checks
docs/          data model and research rules
_inbox/        one JSON file per research pass, the input to data/
scripts/       merge.py (inbox -> tables), check.py, verify_quotes.py, second_read.py
```

To fetch the large files into `raw/`:

```
tail -n +2 raw/RELEASE_FILES.csv | while IFS=, read f bytes sha url; do curl -sSL -o "$f" "$url"; done
```

To rebuild the tables from the research files and re-run every check:

```
python3 scripts/merge.py && python3 scripts/check.py && python3 scripts/verify_quotes.py && python3 scripts/second_read.py
```

## Using it

The tables, notes and documentation in this folder are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use them for
anything, including commercially, as long as you credit the source. Please
cite as: Oscar Leo, *CBI data*, oscarleo.com, with the date you downloaded
it, and cite the original source of any number you use (the `source_id` row
in `sources.csv` has the full reference).

The documents in `raw/` are copies of official publications kept so that
every number can be checked. They are not ours and remain under their
publishers' own terms.

If you find an error, or have a document we don't, please open an issue
with the source and page.
