# Data model: citizenship and residency by investment

This dataset collects numbers about citizenship-by-investment (CBI) and
residency-by-investment programs from many sources, and keeps every claim
separate and traceable. It does not try to produce one "true" number: many
figures in this field are estimates, disagree between sources, or are
published only once. The aim is that a journalist or researcher can see, for
any number, where it came from, how reliable it is, and what other sources say.

## Principles

1. **One row per claim.** An observation is one number, from one source,
   about one thing and one period. Two sources giving numbers for the same
   thing are two rows, even when they agree.
2. **Nothing is overwritten.** Corrections add a row and mark the old one
   `superseded_by`; they don't edit the value.
3. **Every number points to its evidence:** a source, a location in it (page,
   table, paragraph) and a short verbatim quote.
4. **Status says what kind of number it is** (see below). A budget target is
   not an outturn, and a minister's claim is not audited accounts.
5. **Official documents are kept.** Government, IMF, EU, court and legislative
   documents are stored in `raw/` with a SHA-256 checksum. Media and industry
   sources are linked (plus an archive.org copy) and quoted briefly, not copied.

## Tables (`data/`, CSV, UTF-8)

### `sources.csv`: where claims come from

| column | meaning |
|---|---|
| `source_id` | stable id, e.g. `kn-imf-art4-2024` (jurisdiction, publisher, document, year) |
| `title`, `publisher`, `author` | as printed on the document |
| `source_type` | `government`, `legislation`, `imf`, `world_bank`, `eu`, `court`, `international_org`, `academic`, `ngo`, `media`, `industry` |
| `jurisdiction` | ISO 3166 alpha-3 (`KNA`, `DMA`…), or `INTL` |
| `published_date` | as precise as known: `2024-06-12`, `2024-06`, `2024` |
| `accessed_date` | when we retrieved it |
| `url`, `archive_url` | original link, and a Wayback Machine or other archive link |
| `raw_file` | path under `raw/` when a copy is kept, else empty |
| `sha256` | checksum of `raw_file` |
| `notes` | anything a reader should know about the source itself |

### `observations.csv`: the numbers

| column | meaning |
|---|---|
| `obs_id` | stable id |
| `jurisdiction` | ISO alpha-3 |
| `program_id` | from `programs.csv`, when the number is about one program |
| `indicator` | from `indicators.csv`, e.g. `cbi_inflows` |
| `breakdown` | empty for a total; otherwise the split as `key=value`: `nationality=CHN` (ISO alpha-3), `route=real_estate`, `applicant=family`, `sex=F`, `category=` (an applicant group the source defines, not a nationality), `residence=` (country of residence), `country=` (the source doesn't say whether nationality or residence), `destination=` (region of settlement), `item=` (a single document, e.g. one decree). When the source splits two ways at once, join them with `;` in this order: route, applicant, nationality, sex (e.g. `route=real_estate;nationality=RUS`) |
| `period` | what the number covers: `2023`, `FY2023/24`, `2023-Q1`, `2014-2023` |
| `period_basis` | `calendar_year`, `fiscal_year`, `cumulative`, `as_of_date`… |
| `value` | the number as given (no rounding, no conversion); for a range, the low end |
| `value_high` | only for a range ("3–4 percent of GDP"): the high end. Empty otherwise |
| `unit` | `XCD`, `USD`, `EUR`, `percent_of_gdp`, `persons`, `applications`… |
| `scale` | `1`, `thousand`, `million`, as in the source |
| `status` | see below |
| `source_id` | from `sources.csv` |
| `location` | where in the source: `p. 14, Table 3`, `para 21` |
| `quote` | verbatim text supporting the number (short) |
| `notes` | caveats: definitions, what's included, known issues |
| `superseded_by` | `obs_id` of a correction, if any |
| `added_date`, `added_by` | provenance of the row itself |

### `status` values

| status | means | example |
|---|---|---|
| `actual` | official outturn for a closed period | audited fiscal accounts |
| `provisional` | official but preliminary | "preliminary 2024 outturn" |
| `estimate` | an estimate by the source | IMF staff estimate of CBI inflows |
| `projection` | a forecast of future periods | IMF medium-term projection |
| `budget` | a plan or target | budget estimate of CBI receipts |
| `reported` | a secondary report of someone else's figure | a newspaper citing the ministry |
| `claim` | an unverified statement | a politician's or industry figure |

Rules applied across the dataset:

- An official international body's table that repeats a government's past
  outturns (an IMF table column not marked estimate, projection or
  preliminary) is `actual`; the notes say it is relayed.
- A rounded or spoken official figure ("about 450", "more than 35,400") takes
  the status of the figure it rounds; the notes say it is rounded. `claim` is
  for statements nobody can check.
- A plan or forecast passed on by the press is `budget` or `projection`, never
  `reported`, so it can't be mistaken for an outturn.
- On an application indicator, unit `persons` means people included in the
  applications (main applicants and family); unit `applications` counts
  applications.
- Masked small counts are recorded as a range: Australian "<5" cells (which
  print true zeros as 0) are `value` 1, `value_high` 4; "fewer than N" wording
  elsewhere is 0 to N.
- A bare "$" is never read as US dollars: the unit or currency is
  `unspecified` unless the document says which dollar.

### `indicators.csv`: what numbers mean

`indicator`, `name`, `definition`, `unit_kind`, `notes`. Definitions matter
here: "CBI revenue" can mean all inflows (fund contributions plus real estate),
only what reaches the government, or only fees. Each is its own indicator.

### `programs.csv`: the programs

`program_id`, `jurisdiction`, `name`, `kind` (`citizenship`, `residency`),
`launched`, `ended`, `status`, `notes`, `source_ids`.

`ended` is the last day new applications were accepted. `status` is `active`,
`closed`, `not_operational` (a legal basis but no operating programme or price)
or empty when the current state could not be confirmed. `launched` is filled
only from a document.

### `program_terms.csv`: what it costs, and when

One row per route and period of validity: `program_id`, `route`
(`donation`, `real_estate`, `bonds`…), `valid_from`, `valid_to`,
`min_amount`, `currency`, `applies_to` (e.g. `single applicant`),
`source_id`, `location`, `quote`, `notes`.

### `events.csv`: the timeline

`event_id`, `date`, `date_precision` (`day`, `month`, `year`), `jurisdiction`,
`program_id`, `category` (`launch`, `price_change`, `rule_change`,
`visa_access`, `legal`, `scandal`, `closure`, `context`), `title`,
`description`, `source_id`, `location`, `quote`.

## Corrections

Reviewed fixes to merged rows live in `data/corrections.csv` (`table`, `id`,
`field`, `value`, `reason`, `by`; field `_delete` removes a row).
`scripts/merge.py` applies them after merging the inbox, so re-merging never
undoes a fix, and every change to a row keeps its reason.

## Headline prices

`data/headline_prices.csv` gives, per programme, the minimum a single
applicant must invest or donate on the main route today (or on the day a
closed programme stopped taking applications), excluding fees, with the
`term_id`s it rests on and a note on the choice. It was set by hand from the
rules, because an automatic minimum mixes up family prices, add-on fees and
discounted niche routes. Empty amounts say why in the note.

## Disagreements

`scripts/check.py` validates the tables and writes `reports/discrepancies.csv`:
every jurisdiction, indicator and period where sources give different values,
side by side with their statuses. Differences are expected; they are data, not
errors to be cleaned away.

## Research inbox

New research lands in `_inbox/` as JSON (see `RESEARCH_FORMAT.md`), is checked,
and is then merged into the tables. The inbox is not part of the published
dataset.
