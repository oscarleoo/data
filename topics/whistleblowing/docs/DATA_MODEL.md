# Data model: whistleblower reward programmes

This dataset collects numbers about programmes that pay whistleblowers a
reward (a share of the money recovered or the sanctions imposed): how many
tips they get, how many awards they pay and how much, how much money those
cases bring in, the rules that set the reward, and the cases themselves. It
uses the same principles and engine as the citizenship-by-investment dataset
in `topics/cbi`: one row per claim, every number traceable to a page and a
verbatim quote, and disagreeing sources kept side by side.

## Principles

1. **One row per claim.** Two sources giving numbers for the same thing are
   two rows, even when they agree.
2. **Every number points to its evidence:** a source, a location in it (page,
   table, paragraph) and a short verbatim quote.
3. **Status says what kind of number it is.** A budget is not an outturn, and
   a law firm's claim is not an agency report.
4. **Official documents are kept** in `raw/` with a SHA-256 checksum. Media,
   law-firm and NGO sources are linked and quoted briefly, not copied.
5. **People's privacy.** Most whistleblowers are anonymous by law. Record a
   whistleblower's name only when they went public themselves or a court or
   agency published it; never try to identify an anonymous one.

## Tables (`data/`, CSV, UTF-8)

### `sources.csv`: where claims come from

| column | meaning |
|---|---|
| `source_id` | stable id, e.g. `usa-irs-wbo-ar-2023` (jurisdiction, publisher, document, year) |
| `title`, `publisher`, `author` | as printed on the document |
| `source_type` | `government`, `legislation`, `imf`, `world_bank`, `eu`, `court`, `international_org`, `academic`, `ngo`, `media`, `industry` |
| `jurisdiction` | ISO 3166 alpha-3 (`USA`, `KOR`…), or `INTL` |
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
| `indicator` | from `indicators.csv`, e.g. `awards_paid_amount` |
| `breakdown` | empty for a total; otherwise the split as `key=value`: `category=` (type of wrongdoing as the source names it, e.g. `category=offering_fraud`, `category=healthcare`), `country=` (country the tip came from, ISO alpha-3), `subsection=` (legal basis, e.g. `subsection=7623b`), `agency=` (agency involved), `item=` (a single document). Join two splits with `;` (e.g. `category=healthcare;agency=HHS`) |
| `period` | what the number covers: `2023`, `FY2023/24`, `2023-Q1`, `2014-2023` |
| `period_basis` | `calendar_year`, `fiscal_year`, `cumulative`, `as_of_date`… |
| `value` | the number as given (no rounding, no conversion); for a range, the low end |
| `value_high` | only for a range ("3–4 percent of GDP"): the high end. Empty otherwise |
| `unit` | `USD`, `KRW`, `percent`, `tips`, `awards`, `cases`, `persons`, `days`… |
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

### `programs.csv`: the programmes

`program_id` (e.g. `usa-irs-wbo`, `usa-sec-wb`, `usa-fca-qui-tam`,
`kor-acrc-rewards`), `jurisdiction`, `name`, `kind` (`reward`: pays a share
of money recovered; `protection_only`: protects but doesn't pay, included for
context), `launched`, `ended`, `status` (`active`, `closed`, empty if unclear),
`notes`, `source_ids`. `ended` is the last day new claims were accepted.

### `program_rules.csv`: how the reward is set, and when

One row per rule and period of validity: `program_id`, `rule`, `valid_from`,
`valid_to`, `value`, `unit`, `applies_to`, `source_id`, `location`, `quote`,
`notes`. Rules:

| rule | meaning |
|---|---|
| `award_pct_min`, `award_pct_max` | the share of the money collected paid to the whistleblower (unit `percent`); `applies_to` says when (e.g. "government intervenes") |
| `sanctions_threshold` | minimum sanctions or amount in dispute for an award (currency) |
| `income_threshold` | e.g. the IRS gross-income test for the individual (currency) |
| `award_cap` | maximum award (currency or percent) |
| `discretionary` | 1 if awards are discretionary, 0 if mandatory |
| `anonymous_filing` | 1 if a claim can be filed anonymously (often through a lawyer) |
| `filing_deadline_days` | time to claim an award after a notice |

Propose another rule in `notes` if none fits.

### `cases.csv`: individual awards and cases

One row per award or case as a source describes it: `case_id`,
`jurisdiction`, `program_id`, `date` and `date_precision`, `whistleblower`
(name only if public, see principle 5; otherwise empty), `target` (company or
defendant, if published), `summary` (plain words), `sanctions_amount`
(money the government collected or the settlement), `award_amount`,
`award_pct` (only if the source states it), `currency`, `outcome`
(`awarded`, `denied`, `settled`, `pending`, `reported`), `source_id`,
`location`, `quote`, `notes`. Anonymous SEC/CFTC award orders count as cases
(the order number goes in `notes`).

### `events.csv`: the timeline

`event_id`, `date`, `date_precision`, `jurisdiction`, `program_id`,
`category` (`launch`, `rule_change`, `legal`, `award`, `scandal`, `closure`,
`context`), `title`, `description`, `source_id`, `location`, `quote`.

## Currency

A bare "$" in an official US document (an agency report, a law, a court
record) is recorded as `USD`; `scripts/merge.py` applies this. Anywhere else a
bare "$" is `unspecified` unless the document says which dollar.

## Corrections

Reviewed fixes to merged rows go in `data/corrections.csv` (`table`, `id`,
`field`, `value`, `reason`, `by`; field `_delete` removes a row);
`scripts/merge.py` applies them last.

## Disagreements

Sources often disagree (agency reports revise earlier years, law firms round
up). Differences are data, not errors to be cleaned away.
