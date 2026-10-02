# Wave 2: remaining programmes (to run in a fresh session)

Wave 1 (October 2026) covered every citizenship programme found, current and
closed, plus Portugal, Spain, Italy, Hungary, Latvia, the UAE, US EB-5,
Panama, Singapore and the closed UK, Irish and Australian schemes. Wave 2
covers the remaining residence-by-investment programmes and the gaps wave 1
left because its web-search budget (shared by all agents in a session, about
200 searches) ran out.

## How to run it

One research agent per brief below, in parallel, each given the same prompt
as wave 1: read `DATA_MODEL.md`, `RESEARCH_FORMAT.md` and
`RESEARCH_BRIEF.md`, check `data/programs.csv`, `data/indicators.csv` and
`data/sources.csv`, write `_inbox/<slug>.json` and store documents in `raw/`.
Give each agent its own scratch folder (agents sharing one overwrote each
other's files in wave 1). Agents must not use the web browser.

Keep it to about 8 to 10 agents per session so the search budget lasts.
Then merge (`scripts/merge.py`), validate (`scripts/check.py`), check quotes
(`scripts/verify_quotes.py`), fetch blocked documents separately, and run the
blind second read (`scripts/second_read.py`, see `README.md`).

## Briefs

| slug | scope |
|---|---|
| `gulf` | Saudi Arabia (Premium Residency), Bahrain (golden residency), Oman (investor residence), Qatar (property residence) |
| `hong-kong-taiwan` | Hong Kong: Capital Investment Entrant Scheme (2003–2015) and New Capital Investment Entrant Scheme (from 2024), with official application and approval figures |
| `asia` | Malaysia (MM2H), Thailand (Elite / Privilege, LTR), Indonesia (golden visa 2024), Philippines (SRRV), South Korea (immigrant investor) |
| `oceania` | New Zealand (Investor 1/2, Active Investor Plus 2022 and the 2025 revamp), plus Australia's Premium Investor and pre-2012 schemes left out in wave 1 |
| `americas-residence` | Costa Rica, Uruguay, Paraguay, Brazil, Argentina (residence), Mexico, Canada (federal Immigrant Investor, Quebec Investor Program) |
| `caribbean-residence` | The Bahamas, Cayman Islands, Turks and Caicos, Bermuda, plus any Caribbean residence routes not yet in the data |
| `europe-rest` | Switzerland (lump-sum taxation and residence), Monaco, the Netherlands (closed 2024), Malta's residence programmes (MPRP top-up), Lithuania, Estonia, Croatia and others found |
| `africa-indian-ocean` | Mauritius (residence for investors and retirees), Seychelles, plus Sierra Leone and other reported African citizenship plans left unchecked in wave 1 |
| `pacific-gaps` | Marshall Islands, Samoa, Cape Verde and Papua New Guinea (citizenship schemes left unchecked in wave 1), Nauru's amending Act |
| `cross-cutting` | European Commission reports (2019 report, 2022 recommendation, visa-suspension reports), OECD 2018 list of schemes risking tax evasion, FATF/MONEYVAL, Transparency International and Global Witness reports, parliamentary material wave 1 missed (Italy, Australian Senate, Saeima, Cyprus) |
