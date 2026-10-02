# Research brief: extending the dataset worldwide

Read this together with `DATA_MODEL.md` (the tables and what each column
means) and `RESEARCH_FORMAT.md` (the inbox file you write). This page adds the
rules for the worldwide extension. The bar is the same as for the first pass:
every number traceable to a page of a document, and a reader can see how far
to trust it.

## What to collect, for each programme

1. **The programme itself** (`programs`): official name, `kind`
   (`citizenship` or `residency`), when it started and ended (with the legal
   act that did it), current status, and a short note on how it works,
   including how many years of residence lead to citizenship for residence
   programmes.
2. **Rules and prices over time** (`program_terms`): every investment route
   (donation, property, funds, bonds, deposits, business, education…) with
   its minimum amount, currency, who it covers (single applicant, family of
   four…), and the date it applied from and until. Each change is a new row.
   Fees count too (government, due diligence, processing).
3. **Numbers** (`observations`): applications received, approved, rejected;
   people and investors approved; permits issued, valid and renewed;
   passports issued; citizenships revoked; money raised (government income,
   total investment, fund contributions); anything else the programme or its
   overseers publish. Split by nationality or route when the source does,
   using `breakdown` (see `DATA_MODEL.md`), not new indicators.
4. **Events** (`events`): launch, rule and price changes, suspensions,
   closures, court rulings, scandals and investigations, and decisions by
   other countries about visas or money-laundering risk that cite the
   programme.

## Where to look, in this order

1. The law and its amendments (official gazette, legislation database).
2. The programme's own reports and statistics, and the ministry in charge.
3. Parliament: answers to questions, committee reports, audit reports.
4. International bodies: European Commission reports and decisions, IMF
   country reports, OECD, FATF/MONEYVAL, US Treasury (FinCEN), EU court.
5. Courts.
6. Serious investigative journalism (OCCRP, ICIJ, Al Jazeera, national
   press) for what official sources leave out, recorded as `reported`.
7. Industry sources only as a last resort for what nobody else publishes,
   recorded as `reported` with a note.

Search in the country's own language as well as English.

## Rules

- **Only numbers you read in the document**, with `location` (PDF page,
  table, row) and a verbatim `quote`. Nothing from memory; nothing calculated.
- **Status:** `actual` only for official outturns of a closed period;
  `reported` for anything passed on second-hand; when unsure, the weaker one,
  explained in `notes`.
- **Keep amounts as printed**, with their currency. Never assume `$` means
  US dollars: say which currency the document uses, or that it doesn't say.
- **Store official documents** in `raw/<source_id>.<ext>` (government, law,
  IMF, EU, courts, international organisations). If a site blocks downloads,
  still record the source with its URL, leave `raw_file` empty and write
  `download blocked` in its notes; they will be fetched another way.
  Don't store news or industry articles.
- **One row per claim.** Two sources with the same number are two rows.
- **Plain notes.** `notes` are read by journalists: say what's included and
  what isn't, and anything odd, in plain words.

## Ids and names

- `program_id`: `<iso3 lowercase>-<short name>`, e.g. `prt-golden-visa`,
  `cyp-cip`, `usa-eb5`. Reuse an existing id if the programme is already in
  `data/programs.csv`.
- `source_id`: `<iso3 lowercase>-<publisher>-<document>-<year>`, e.g.
  `cyp-audit-cip-2021`. It must be unique across the whole dataset; check
  `data/sources.csv` before choosing one.
- `jurisdiction`: ISO alpha-3, or `INTL` for documents about several.
- Use indicators from `data/indicators.csv`. Propose a new one in
  `new_indicators` only when nothing there fits, with a precise definition.

## Done means

- Every programme in your brief has a `programs` row and its rules over time.
- Every number has a quote, a location and a status.
- The inbox file ends with honest `gaps` (what you looked for and couldn't
  find) and `leads` (promising sources not yet read, with URLs).
- `python3 -c "import json; json.load(open('_inbox/<slug>.json'))"` passes.

Don't edit anything in `data/`; the merge does that. Don't use the web
browser (Chrome) at all; blocked documents are fetched separately.
