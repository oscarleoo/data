# Research inbox format

Each research pass writes one file: `_inbox/<slug>.json`, and downloads
official documents to `raw/<source_id>.<ext>`.

```json
{
  "slug": "st-kitts-nevis",
  "researched_on": "2026-09-28",
  "summary": "Two or three sentences: what exists, how good it is.",
  "sources": [
    {
      "source_id": "kna-imf-art4-2024",
      "title": "St. Kitts and Nevis: 2024 Article IV Consultation - Staff Report",
      "publisher": "International Monetary Fund",
      "author": "",
      "source_type": "imf",
      "jurisdiction": "KNA",
      "published_date": "2024-06",
      "accessed_date": "2026-09-28",
      "url": "https://...",
      "archive_url": "",
      "raw_file": "raw/kna-imf-art4-2024.pdf",
      "covers": "What data it has, for which years",
      "notes": "Reliability, definitions, anything odd"
    }
  ],
  "observations": [
    {
      "jurisdiction": "KNA",
      "program_id": "kna-cbi",
      "indicator": "cbi_inflows_pct_gdp",
      "period": "2023",
      "period_basis": "calendar_year",
      "value": "20.1",
      "unit": "percent_of_gdp",
      "scale": "1",
      "status": "estimate",
      "source_id": "kna-imf-art4-2024",
      "location": "p. 5, Table 1",
      "quote": "CBI inflows ... 20.1",
      "notes": ""
    }
  ],
  "program_terms": [],
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
- Download official documents (government, legislation, IMF, World Bank, EU,
  courts) into `raw/`. Don't store copies of news articles or paywalled or
  industry reports; link them and quote at most ~25 words.
