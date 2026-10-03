# Research brief: whistleblower reward programmes (wave 1)

Read this with `DATA_MODEL.md` (tables and columns) and `RESEARCH_FORMAT.md`
(the inbox file you write). The bar is the same as the citizenship dataset in
`topics/cbi`: every number traceable to a page of a document, and a reader can
see how far to trust it.

## What to collect, for each programme

1. **The programme** (`programs`): official name, legal basis, when it began
   (and ended), who runs it, and a short plain note on how it works.
2. **Reward rules over time** (`program_rules`): percentage ranges, thresholds,
   caps, whether awards are mandatory, anonymous filing; each change a new row.
3. **Numbers** (`observations`): tips received, claims closed, awards paid
   (number and amount), denials, money collected thanks to whistleblowers,
   processing time, fund balances; every year the agency reports, using the
   indicators in `data/indicators.csv` and `breakdown` for splits (type of
   wrongdoing, country of the tipster). Propose a new indicator only if none
   fits.
4. **Cases** (`cases`): individual awards and notable cases with the amount
   recovered and the award, from agency orders, press releases and court
   documents. Names only under principle 5 of DATA_MODEL.md.
5. **Events** (`events`): laws and amendments, launches, rule changes,
   record awards, scandals, court rulings.

## Where to look, in this order

1. The law and regulations (US Code, Federal Register, eCFR; national
   legislation databases).
2. The programme's own annual reports and statistics (many US programmes must
   report to Congress every year: get every year available, not a sample).
3. Agency press releases and award orders; Justice Department statistics.
4. Oversight: GAO, inspectors general (e.g. TIGTA for the IRS), congressional
   hearings and reports.
5. Courts (dockets and opinions, e.g. CourtListener, justice.gov).
6. Serious journalism for what agencies leave out, recorded as `reported`.
7. Law firms and advocacy groups only as a last resort, as `claim` or
   `reported`, with a note (they have an interest in big numbers).

## Rules

- **Only numbers you read in the document**, with `location` and a verbatim
  `quote`. Nothing from memory, nothing calculated.
- **Status:** `actual` for an agency's own figures for a closed period;
  `provisional` for a year not yet closed; `reported` for second-hand;
  `claim` for law-firm or advocacy figures nobody can check.
- **Amounts as printed**, with currency and scale ("$1.2 million" is value
  1.2, scale million).
- **Fiscal years:** say which (US federal FY runs October to September), in
  `period` (`FY2023`) and `period_basis` (`fiscal_year`).
- **Store official documents** in `raw/<source_id>.<ext>` (download with
  curl). If a site blocks downloads, record the source with its URL, leave
  `raw_file` empty and write `download blocked` in notes; never try to get
  past bot checks or CAPTCHAs. Don't store news, law-firm or paywalled
  material, or anything whose terms forbid redistribution.
- **Do NOT use the web browser (Chrome, any mcp__claude-in-chrome tool).**
  Use WebSearch, WebFetch and curl.
- **Web searches are shared across all agents in this session and limited:
  use at most 18.** Prefer fetching known official URLs and following links
  from index pages (annual-report archives) over searching.
- **One row per claim**; plain-language notes for journalists.

## Ids

- `program_id`: `<iso3 lowercase>-<agency>-<short>`, e.g. `usa-irs-wbo`,
  `usa-sec-wb`, `usa-cftc-wb`, `usa-fca-qui-tam`, `usa-fincen-aml-wb`,
  `kor-acrc-rewards`. Check `data/programs.csv` and the other agents' briefs
  so the same programme gets the same id.
- `source_id`: `<iso3 lowercase>-<publisher>-<document>-<year>`, unique.

## Done means

Every programme in your brief has a `programs` row, its rules over time, every
year of numbers its agency publishes, its main cases and events, and a
`gaps` list of what you looked for and couldn't find.
