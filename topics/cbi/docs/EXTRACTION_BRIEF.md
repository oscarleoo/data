# Extraction brief: getting everything out of documents we already store

Read with `DATA_MODEL.md`, `RESEARCH_FORMAT.md` and `COVERAGE.md`. This pass adds no new sources:
it works through stored documents and records what is in them, so the ledger
(`data/extraction_status.csv`) can say honestly what is and isn't extracted.

## For each document you are given

1. **Read all of it.** Every page, every table, every chart with printed values. For spreadsheets,
   every sheet.
2. **List what it contains** (`contains`, plain words): e.g. "Applications by country and by
   investment route for 1 Jan-30 Jun 2019; NDF contributions; passports issued by year 2014-2019;
   disbursements".
3. **Extract everything in scope** into observations (and rules or events where relevant), using
   the existing indicators and `breakdown` keys (`nationality=ISO3`, `route=`, `applicant=`...).
   In scope: any number about the programme (applications, approvals, rejections, people,
   passports, permits, money, by any split the document gives). Out of scope: numbers about other
   things (general immigration, unrelated budget lines); say so in `contains`.
4. **Check before you write:** where a table prints a total, the parts must add up to it (or the
   difference is explained in notes). Every number needs location, verbatim quote, status.
5. **Skip what is already in the data:** check `data/observations.csv` for the document's
   `source_id` and don't add a row that is already there (same indicator, breakdown and period).
6. **Set the ledger status** for the document in your inbox file under `ledger`:
   - `complete`: everything in scope is now extracted.
   - `partial`: something in scope is left; `to_do` says exactly what and why (e.g. "chart on p. 7
     has no printed values").
   - `not_applicable`: nothing in it belongs in the tables; `contains` says what it is.
   Never mark `complete` if anything in scope is left.

## How each number was read (METHODOLOGY.md decisions 2 and 4)

Every observation needs `reading` (`digits`, `words`, `bound`, `approximate` or `implied`; never record a number
the document doesn't state: that would be `inferred`) and `unit_basis` (`printed`, or `inferred` when you chose
the unit, scale or currency from context: then say in `notes` how, and what supports it).

## Output

`_inbox/<slug>.json` in the format of `RESEARCH_FORMAT.md`, plus:

```json
"ledger": [
  {"source_id": "atg-ciu-6m-2019h1", "status": "complete", "contains": "...", "to_do": ""}
]
```

The main session applies the ledger rows with `reviewed_by` = the pass name and
`reviewed_on` = the date, and runs the quote check and a blind second reading on the new numbers.

## Rules

No web access is needed or allowed in this pass (the documents are local). Don't use the browser.
Don't edit `data/` or `scripts/`; write only your inbox file and temporary files in your scratch
folder. Names of individuals only under the dataset's existing rules.
