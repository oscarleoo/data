# Whistleblower rewards: a sourced dataset

Numbers on the programmes that pay whistleblowers a share of the money their
information helps recover: how many tips they get, how many awards they pay
and how much, the rules that set the reward, the cases behind the biggest
awards, and the laws and events that shaped them. 31 programmes: the US
False Claims Act, the IRS, the SEC, the CFTC, newer US schemes (money
laundering, car safety, the Justice Department's pilot and its antitrust
programme), and programmes outside the US (South Korea, Ontario, Canada's
offshore tax informants, the UK tax authority, competition authorities in
the UK, Hungary, Slovakia and Lithuania, and others), and the state false
claims acts of New York, California, Texas and Illinois.

Every number is a separate claim with its source, page, verbatim quote and
status, and sources that disagree (agencies revise past years heavily) are
kept side by side. Built on the same engine as `topics/cbi`. Whistleblowers
are named only when they went public themselves or a court or agency named
them.

Maintained by Oscar Leo ([oscarleo.com](https://oscarleo.com)). Research passes:
3–4 October 2026 (wave 1) and 5 October 2026 (wave 2, `docs/WAVE2_PLAN.md`).
What we looked for and couldn't find is in `docs/GAPS.md`.

## What's in it

| | rows |
|---|---|
| Numbers (`data/observations.csv`) | 4,855 |
| Cases and individual awards (`data/cases.csv`) | 1,155 |
| Reward rules over time (`data/program_rules.csv`) | 206 |
| Events (`data/events.csv`) | 189 |
| Sources (`data/sources.csv`) | 582, of which 558 have a stored copy in `raw/` |
| Programmes (`data/programs.csv`) | 31 |
| Indicators (`data/indicators.csv`) | 24 |

Numbers per programme: usa-fca-qui-tam 2059, usa-irs-wbo 1038, usa-sec-wb 1011, kor-acrc-rewards 468, usa-cftc-wb 133, gbr-hmrc-informants 24, usa-fincen-aml-wb 22, can-osc-wb 20, ltu-gp-rewards 20, can-cra-otip 17, usa-txag-tmfpa 12, hun-gvh-informant-rewards 8, svk-uoo-rewards 8, gbr-hmrc-srs 6, usa-nyag-fca 3, usa-wildlife-rewards 2, usa-nhtsa-wb 2, usa-caag-fca 1, usa-doj-cwap 1.

The column-by-column description is in [docs/DATA_MODEL.md](docs/DATA_MODEL.md).

## Coverage: what is and isn't extracted

Every number here is checked against its source, but the dataset is not a
complete extraction of every document it cites. Each source has a status in
`data/extraction_status.csv` (not reviewed, partial with a to-do, complete, or
not applicable), and nothing is marked complete without a recorded review. As of
8 October 2026, none of the 582 sources has been reviewed end to end yet; known
gaps are listed as to-dos. See [docs/COVERAGE.md](docs/COVERAGE.md).

## How it was checked

- `scripts/verify_quotes.py` looks for every quote in the stored copy. Of
  6,405 quoted rows, 5,826 were found verbatim, 406 matched as a table row
  put back together from its cells, and 114 (values printed in charts and
  image tables, and pages whose HTML splits words differently) were checked by
  hand (`data/quote_checks.csv`). The other 59 cite news, law-firm and NGO
  sources, linked rather than stored. SEC award amounts are the amounts in the
  SEC's award orders, which the SEC may raise later as more sanctions are collected.
- **A blind second reading** of a stratified sample from every stored document:
  a different AI model (Claude Sonnet 5) was given each number's document,
  page, indicator and period, but not the value, and read it itself. Of
  914 numbers, 894 came out the same (including 8 South Korean
  amounts the second reading showed had been recorded 100 times too small,
  "88억" read as 8,800 ten-thousands, and which were corrected); in 19 the first
  reading was confirmed on the page, and in 1 the document itself prints two
  figures. Readings are in `data/second_read.csv`, rulings in
  `data/second_read_resolutions.csv`.
- `scripts/check.py` validates the tables and writes `reports/validation.txt`
  and `reports/discrepancies.csv`.

Reviewed fixes to merged rows are in `data/corrections.csv`, each with its reason.

## Layout

```
data/      the tables (CSV)
raw/       stored official documents, with SHA-256 in sources.csv
docs/      DATA_MODEL.md, RESEARCH_BRIEF.md, RESEARCH_FORMAT.md, GAPS.md, WAVE2_PLAN.md
reports/   validation, discrepancies, quote and second-reading results
scripts/   merge.py (inbox -> tables), check.py, verify_quotes.py, second_read.py
_inbox/    the research files as written, merged into data/ by merge.py
```

```
python3 scripts/merge.py && python3 scripts/check.py && python3 scripts/verify_quotes.py && python3 scripts/second_read.py
```

## Using it

The tables, notes and documentation in this folder are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use them for
anything, including commercially, as long as you credit the source. Please
cite as: Oscar Leo, *Whistleblower rewards data*, oscarleo.com, with the date
you downloaded it, and cite the original source of any number you use (the
`source_id` row in `sources.csv` has the full reference).

The documents in `raw/` are copies of official publications kept so that
every number can be checked. They are not ours and remain under their
publishers' own terms.

If you find an error, or have a document we don't, please open an issue
with the source and page.
