# Citizenship and residence by investment: a sourced dataset

Numbers on citizenship-by-investment (CBI) and golden-visa programmes in the
five Eastern Caribbean countries (Antigua and Barbuda, Dominica, Grenada,
Saint Kitts and Nevis, Saint Lucia), Malta, Greece and Turkey, with the
context around them: the end of the sugar industry in Saint Kitts, and EU,
UK and US visa and anti-money-laundering decisions.

The data is incomplete and often uncertain, because governments publish
little, change definitions, and revise their numbers heavily. So this dataset
doesn't try to give one "true" number per year. It records **every claim
separately**: who made it, in which document, on which page, in whose words,
and whether it's an outturn, an estimate, a budget or a forecast. When sources
disagree, the disagreement is part of the data.

Maintained by Oscar Leo ([oscarleo.com](https://oscarleo.com)). Last research
pass: 28 September 2026.

## What's in it

| | rows |
|---|---|
| Numbers (`data/observations.csv`) | 1,124 |
| Sources (`data/sources.csv`) | 348, of which 312 have a stored copy in `raw/` |
| Programme terms, such as minimum investment by route and date (`data/program_terms.csv`) | 137 |
| Events: launches, rule changes, visa decisions, court rulings (`data/events.csv`) | 199 |
| Programmes (`data/programs.csv`) | 13 |
| Indicators and their definitions (`data/indicators.csv`) | 65 |

Numbers per jurisdiction: Saint Kitts and Nevis 359, Grenada 138, Malta 129, Dominica 124, Saint Lucia 118, Antigua and Barbuda 103, Greece 84, Turkey 42, international 20, Vanuatu 6, Montenegro 1.

The full column-by-column description is in [docs/DATA_MODEL.md](docs/DATA_MODEL.md).

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
| `vintage` | a budget or forecast that differs from the later outturn | 23 |
| `revision` | one publisher changing its own figure in later documents (common in IMF reports) | 47 |
| `same_source` | one document giving two values, usually for two definitions | 10 |
| `conflict` | different publishers disagreeing about what happened | 18 |

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

## How the numbers were checked

- Every row has a `location` (page, table, row) and a short verbatim `quote`.
- Official documents are stored in `raw/` with their SHA-256 checksum in
  `sources.csv`, so a quote can be checked against the exact file we read,
  even if the original moves or changes. News articles and industry reports are
  linked, with an archive link where we have one, and not stored.
- `scripts/verify_quotes.py` looks for every quote in the text of the stored
  copy. Results are in `reports/quotes.csv`: of the 1,460 quoted rows, 1,376 cite a stored document; 1,217 of those quotes were found verbatim, 107 matched loosely (a table row put back together from its cells), 51 were checked by eye, and 1 points to a stored file that turned out to be the wrong page. The other 84 cite news and industry sources, which are linked rather than stored.
  Quotes from image-only tables were compared with the rendered page by eye.
  `data/quote_checks.csv` records who checked each one, when, and what they saw.
- **A blind second reading.** A different AI model (Claude Sonnet 5) was
  given each number's document, page, indicator and period, but not the
  value, and read the number itself. It read 875 numbers from stored
  documents. 840 came out the same. Most first-pass differences were tables
  that print a budget, a projection and an actual figure for the same year,
  and went away once the reader was told the status. The remaining 35 were
  checked on the page: in 31 the first reading was right (the second reader
  took a neighbouring row or column, used the wrong fiscal-year convention, or
  couldn't choose between components, as with Malta's split of revenue
  between the budget and the development fund), and in 4 the document itself
  prints two different figures, which the row notes now say. No value in the
  dataset had to be corrected. The 185 FAOSTAT rows were checked cell by cell
  by a script instead. Readings are in `data/second_read.csv`, rulings in
  `data/second_read_resolutions.csv`, and the comparison in
  `reports/second_read.csv`.
- The same pass checks page numbers. Eleven locations were off by one page
  (mostly in Dominica's budget addresses) and have been corrected.
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
