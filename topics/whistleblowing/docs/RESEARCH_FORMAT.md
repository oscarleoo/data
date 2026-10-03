# Research inbox format

Each research pass writes one file: `_inbox/<slug>.json`, and downloads
official documents to `raw/<source_id>.<ext>`.

The values in this example are invented to show the shape; don't copy them.

```json
{
  "slug": "irs",
  "researched_on": "2026-10-03",
  "summary": "Two or three sentences: what exists, how good it is.",
  "sources": [
    {
      "source_id": "usa-irs-wbo-ar-2023",
      "title": "IRS Whistleblower Program Fiscal Year 2023 Annual Report to Congress",
      "publisher": "Internal Revenue Service",
      "author": "",
      "source_type": "government",
      "jurisdiction": "USA",
      "published_date": "2024",
      "accessed_date": "2026-10-03",
      "url": "https://...",
      "archive_url": "",
      "raw_file": "raw/usa-irs-wbo-ar-2023.pdf",
      "covers": "What data it has, for which years",
      "notes": "Reliability, definitions, anything odd"
    }
  ],
  "observations": [
    {
      "jurisdiction": "USA",
      "program_id": "usa-irs-wbo",
      "indicator": "awards_paid_amount",
      "period": "FY2023",
      "period_basis": "fiscal_year",
      "value": "88.8",
      "unit": "USD",
      "scale": "million",
      "status": "actual",
      "source_id": "usa-irs-wbo-ar-2023",
      "location": "p. 12, Table 3",
      "quote": "Amount of awards paid ... $88.8",
      "notes": ""
    }
  ],
  "program_rules": [],
  "cases": [],
  "events": [],
  "programs": [],
  "new_indicators": [],
  "gaps": ["What we looked for and couldn't find"],
  "leads": ["Promising sources not yet read, with URLs"]
}
```

Rules:
- Only include a number you read in the document yourself, with its location
  and a verbatim quote. No numbers from memory; nothing inferred or converted.
- Keep the value exactly as printed (units, scale, currency).
- Pick `status` carefully (see DATA_MODEL.md). When in doubt, choose the
  weaker one (`reported` over `actual`) and explain in `notes`.
- Two sources, two rows, even if they agree.
- Download official documents (government, legislation, courts, international
  organisations) into `raw/`. Don't store copies of news articles or paywalled or
  industry reports; link them and quote at most ~25 words.
