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

## General principle: extract everything, decide what to show later (decided 2026-10-09)

When a figure is printed but something about it is uncertain (its unit, its label, a contradiction in the
source), we keep it, mark the uncertainty, and decide separately what pages show. Hiding is reversible; not
extracting loses information. This doesn't cover numbers the source never states (decision 2, `inferred`).

## What pages show

The data keeps everything; these rules decide what is shown. They are applied when the data is cut for the site.

| kind of figure | shown? |
|---|---|
| printed (`reading` digits, words, bound, approximate) | yes |
| `implied` | yes, as stated in words ("stated as none") |
| `inferred` | no |
| `derived` | yes, labelled "calculated by us from official records" |
| `unit_basis` inferred | with a warning (whether to show at all: open) |
| `unit_basis` guessed | with a stronger warning (whether to show at all: open) |


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

### 2. Numbers read from words (decided 2026-10-09)

**Question.** Sometimes the number isn't printed as digits: it is written as a word ("three applications"),
given as a limit ("more than 700") or rounded ("about 20"), or only implied by a sentence ("there were no
investment inflows"). Sometimes it can only be worked out by reasoning ("as in 2011, nearly 20 last year
too"). Which of these belong in the data, and how do we tell them apart?

**Decision.** Every number keeps its verbatim sentence in `quote`, and a column `reading` says how the number
was read:

| `reading` | means | example | allowed |
|---|---|---|---|
| `digits` | printed as a number (the default) | "1,583" | yes |
| `words` | the number itself is written in words | "three applications", "one million" | yes |
| `bound` | printed as a limit; stored as a range | "more than 700", "<5" | yes |
| `approximate` | printed as a rounded figure | "about 20", "nearly 60%" | yes |
| `implied` | no number printed, but the sentence states it unambiguously | "there were no investment inflows" = 0 | yes, tagged |
| `inferred` | the number depends on reasoning beyond the sentence | "as in 2011, nearly 20 last year too" = 20 for 2011 | kept, **hidden** |

Pages show `implied` figures as stated in words (e.g. "stated as none"), not as a bare number. An `inferred`
figure is kept in the data with its sentence but never shown on pages (amended 2026-10-09 under the general
principle; first decided as "not recorded").

**Why.** The sentence is the evidence, so it must travel with the number. Words, limits and rounded figures are
still what the source says. An implied zero is real information, but readers should see that no digit was
printed. An inferred number is a calculation in disguise, which decision 1 only allows in the narrow,
recalculated form of a `derived` figure.

**Applied (2026-10-09).** The column is in both topics; `scripts/reading.py` gives a first reading from the
quote and value, merge keeps reviewed readings, and `scripts/check.py` rejects `inferred` and unknown values.
Every row the classifier couldn't settle, and every row it tagged `implied` or `words`, was reviewed against the
document (809 rows). 45 `inferred` rows were removed: 39 Egyptian naturalisation counts tallied from lists of
names (the decrees print no totals), and 6 whistleblowing rows (Hungary 2011 enquiries carried over from 2012;
two Slovak counts made from descriptions; an SEC footnote taken as a yearly total; a CFTC sum of 1 + 23; an SEC
ordinal count of awards stored as people).

### 3. Derived figures from masked data (decided 2026-10-09)

**Question.** Some statistics offices add random noise to record-level data so small counts can't identify
people ("masking"). Large sums are barely affected, but a sum over a few records can be noise: it can even come
out negative (-5 permits). How do we treat derived figures from such data?

**Decision.**
- Never publish a negative count. Negative derived sums are held back and noted on the source.
- When the source is masked, derived values below 5 are stored as a range from 0 to 4 (the way publishers
  print small numbers, e.g. Australia's "<5"), with a note that the source is masked.
- Derived values of 5 and more are kept as calculated, with the masking noted on the source.

**Why.** Masking makes small sums unreliable whether or not they look wrong; a range keeps the information
without claiming a precision the source doesn't have.

### 4. Units we had to infer (decided 2026-10-09)

**Question.** Sometimes a document prints a number without its unit: a chart labelled "432,746" with no "in
thousands of pesos", or a table headed "EC$ millions" whose cells are clearly full amounts. Keep such numbers?

**Decision.** Keep them, with a warning:
- A column `unit_basis` says `printed` (the default), `inferred` (the same document settles the unit) or
  `guessed` (nothing in the document settles it; our best judgement from outside evidence, such as the
  programme's own law, with the reasoning in the notes; amended 2026-10-09).
- For `inferred`, the notes say how the unit was chosen and what supports it (e.g. "the same quantity is printed
  as ₱584,270,596 in the text, so the chart is in thousands").
- Inferred-unit figures carry a warning wherever they are shown, guessed ones a stronger one; whether pages show them at all is decided
  separately.
- When we can, we look for confirmation elsewhere (another edition, the source's methodology note, the
  agency) and switch the row to `printed` with that source, or correct it.

**Why.** A wrong unit is a factor-of-a-thousand error that looks plausible, so these figures must never pass as
ordinary. But the number itself is printed and the unit is usually clear from context, so dropping them would
lose real data.

**Applied (2026-10-09).** Column `unit_basis` in both topics (merge fills `printed` by default; `check.py`
requires notes for `inferred`). 77 CBI rows whose notes say the unit, scale or currency was chosen from context
are tagged `inferred` (Philippine charts read as thousands, tables printing "$" or no currency where the currency
was taken from the rest of the document, and similar). Rows where a bare "$" was recorded as the local currency
are left for decision 1.4. Rows that inferred a unit without saying so in their notes can't be found this way;
the extraction brief now requires the field.

### 5. The bare "$" sign (decided 2026-10-09)

**Question.** Many countries call their currency the dollar (US, Canada, Australia, New Zealand, Hong Kong,
Singapore, Bermuda, the Eastern Caribbean states). Documents often print only "$". Which currency do we record?

**Decision.** Decision 4 applied to currency:
- An official document's "$" is the dollar of the issuing government (a Grenadian budget's "$" is EC$, a
  Canadian federal document's "$" is CAD). It is recorded as that currency with `unit_basis` = `inferred` and a
  note saying why.
- US federal documents: "$" is US dollars, recorded as printed.
- Where a document mixes dollars (EC$ and US$ in one report), "$" is assigned only when the table or section
  settles it; otherwise the currency stays `unspecified`, with a note.
- `unspecified` is kept only for genuine ambiguity (e.g. a press article where "$" could be either).

**Applied (2026-10-09).** 356 CBI and 21 whistleblowing rows already recorded in the issuing government's dollar
are flagged `inferred`. Of 185 CBI rows recorded as `unspecified`, 122 got the currency their document settles
(CAD 59, NZD 49, AUD 7, USD 4, XCD 3), flagged `inferred`; 63 stay unspecified (press articles; Antigua tables
that print a bare "$" in a report that mixes EC$ and US$).

**Why.** Without a currency the number can't be compared or converted; guessing silently hides the risk of a
2.7-times error (EC$ vs US$). Recording the likely currency with a warning keeps the number usable and honest.

### 6. Zero cells (decided 2026-10-09)

**Question.** Statistical tables often list every country or month, most with 0. Does each printed 0 become a
row?

**Decision.** Yes. Every printed 0 or "-" (nil) is stored as a row like any printed figure (`reading` digits).
Blank cells are not recorded; the source's notes say what a blank means in that table ("blank = zero in this
edition", "blank = not available"). What pages show is decided separately (most charts leave zeros out).

**Why.** A zero is information ("no investors from X in 2019"). If it isn't stored, "zero", "not published"
and "not extracted" look the same, which is the silent gap the coverage ledger exists to prevent.

## Open questions

None at the moment.
