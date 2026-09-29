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

### `indicators.csv`: what numbers mean

`indicator`, `name`, `definition`, `unit_kind`, `notes`. Definitions matter
here: "CBI revenue" can mean all inflows (fund contributions plus real estate),
only what reaches the government, or only fees. Each is its own indicator.

### `programs.csv`: the programs

`program_id`, `jurisdiction`, `name`, `kind` (`citizenship`, `residency`),
`launched`, `ended`, `status`, `notes`, `source_ids`.

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

## Disagreements

`scripts/check.py` validates the tables and writes `reports/discrepancies.csv`:
every jurisdiction, indicator and period where sources give different values,
side by side with their statuses. Differences are expected; they are data, not
errors to be cleaned away.

## Research inbox

New research lands in `_inbox/` as JSON (see `RESEARCH_FORMAT.md`), is checked,
and is then merged into the tables. The inbox is not part of the published
dataset.
