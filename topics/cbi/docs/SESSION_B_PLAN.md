# Session B: gap filling and consistency audit (to run in a fresh session)

Waves 1 and 2 are merged, verified and published (5,873 numbers, 1,322
sources, 122 programmes). Two wave 2 briefs were not run because the
session's web-search budget (about 200 searches, shared by every agent in a
session) ran out: `pacific-gaps` and `cross-cutting`. Every agent's list of
what it could not find is in `GAPS.md` (356 items).

## How to run it

Same rules as waves 1 and 2: each research agent reads `DATA_MODEL.md`,
`RESEARCH_FORMAT.md` and `RESEARCH_BRIEF.md`, checks `data/programs.csv`,
`data/indicators.csv` and `data/sources.csv` so it adds only what is new,
writes `_inbox/<slug>.json`, stores documents in `raw/`, and has its own
scratch folder. Agents must not use the web browser (Chrome); the main
session fetches blocked documents afterwards, one new tab per download, and
never gets past bot checks or CAPTCHAs.

Four research agents share the search budget: tell each to use **at most
45 web searches** and to prefer fetching known official URLs over searching.
The fifth agent (the audit) works only from the local files and needs no
searches.

Then merge (`scripts/merge.py`), validate (`scripts/check.py`), check quotes
(`scripts/verify_quotes.py`), fetch blocked documents, and run the blind
second read (`scripts/second_read.py`), as in `README.md`.

## Briefs

| slug | scope |
|---|---|
| `pacific-gaps` | Marshall Islands, Samoa, Cape Verde and Papua New Guinea (citizenship schemes reported but never checked), Nauru's amending Act and any official Nauru figures, Sierra Leone and other reported African citizenship plans if `africa-indian-ocean` left them open |
| `cross-cutting` | European Commission: 2019 report on investor citizenship and residence, 2022 recommendation, visa-suspension-mechanism reports, infringement case against Malta and the 2025 Court of Justice ruling; OECD 2018 list of schemes posing a risk of tax evasion; FATF and MONEYVAL; Transparency International and Global Witness reports; parliamentary material wave 1 missed (Italy, Australian Senate, Latvian Saeima, Cyprus House) |
| `gaps-americas-gulf` | The items under `gulf`, `americas-residence`, `caribbean-residence`, the five Caribbean citizenship briefs (`antigua-barbuda`, `dominica`, `grenada`, `saint-lucia`, `st-kitts-nevis`), `panama` and `usa-eb5` in `GAPS.md`: notably Qatar, Saudi official texts, Paraguay, Mexico, Brazil legal texts, small Caribbean territories, missing budget and annual-report years |
| `gaps-europe-asia-africa` | The items under every other brief in `GAPS.md` (Europe, Turkey, Egypt and Jordan, Asia, Hong Kong, Singapore, Oceania, Vanuatu, Africa and the Indian Ocean, historical, closed Western schemes, context timeline) |
| `audit` | No web searches. A consistency check across agents: (1) the same kind of figure uses the same indicator and status everywhere (e.g. budget vs actual revenue, applications vs approvals); (2) each programme's open/closed status, launch and end dates agree with its events and rules; (3) a hand-checked headline price per programme: the minimum a single applicant pays on the main route today, with the rule ids it rests on, written to `data/headline_prices.csv` (programme_id, amount, currency, route, term_ids, note). Report proposed fixes in `_inbox/audit.json`; the main session applies them after review. |

The two gap briefs should work down their part of `GAPS.md` in order of how
much the missing item matters to a reader (official counts and revenue
first, then legal texts behind prices, then everything else), and say which
gaps they closed and which remain.
