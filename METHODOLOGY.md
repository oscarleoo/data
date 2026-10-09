# Methodology

How every dataset in this repository is built. Each topic (`topics/cbi`, `topics/whistleblowing`, and any
future one) follows these rules. Each rule records a decision: the question, what we decided, and why. When
a new kind of case comes up, the answer is added here before the data is changed.

The topic folders hold the details that are specific to one subject (`docs/DATA_MODEL.md`), the coverage
ledger (`docs/COVERAGE.md`, `data/extraction_status.csv`) and the work logs (`reports/`).

## Basic principle

Every number comes from a stored source document. Each one carries the document, the place in it, a verbatim
quote and a status saying what kind of figure it is. Sources that disagree are kept side by side. We record
what documents say; we don't correct, estimate or fill gaps ourselves.

## Decisions

### 1. Numbers derived from an official source's raw records (decided 2026-10-09)

**Question.** Some official sources publish raw records instead of finished tables: a spreadsheet with one row
per batch of permits (Greece), or a pivot-table workbook whose visible sheet shows only totals while the
breakdowns appear only after setting filters (Australia, Home Affairs BP0068). The figure you want, for
example permits by nationality in a year, is printed nowhere; it exists only once someone adds up the
records. Do such figures belong in the dataset?

**Decision.** Yes, but only as a separate, clearly marked kind of figure:

- Status `derived`. Never `actual` or any other status reserved for printed figures.
- Only simple sums or counts of one official source's own records, as the source publishes them (rows of its
  data sheet, records in its pivot table). No estimates, rates, shares, averages, currency conversions or
  combining of different sources.
- Every derived number carries its recipe: the file, the sheet or table, and the exact filters or rows that
  were summed, so anyone can repeat it. The recipe is written in `notes`, starting with `Recipe:`.
- Before a derived number enters the data, a second, independent calculation from the raw file must give the
  same result.
- Pages and summaries show derived figures as "calculated by us from official records", never as quotes, and
  leave them out wherever only printed figures are claimed.

**Why.** These are often the only source for figures that matter (who buys, by nationality), and the
arithmetic is plain and repeatable from official records. But they are not printed, so there is no page to
check them against. Marking them, keeping the recipe and recalculating independently keeps the line clear
between "printed in the source" and "calculated by us from the source".

**Applied (2026-10-09).** Greek permit spreadsheets 2016-2019: 497 figures `derived`, 6 printed summary cells
kept as printed; all 503 matched an independent recalculation. Australian BP0068 workbook: 3,547 figures
`derived` (3,511 new, 36 older rows converted); all matched an independent recalculation, which also reproduced
every cell of the workbook's visible table. Ten Australian sums come out negative because the source data is
masked (privacy perturbation); they are held back (open question 1a below).

## Open questions

- **1a. Masked data that sums to a negative number.** Some official datasets perturb small counts for privacy,
  so a derived sum can be negative (e.g. -1 permits). Proposal: never publish a negative count; hold such
  figures back and note the masking on the source. Not yet decided.
