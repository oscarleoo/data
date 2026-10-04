# Whistleblower rewards: a sourced dataset

Numbers on the programmes that pay whistleblowers a share of the money their
information helps recover: how many tips they get, how many awards they pay
and how much, the rules that set the reward, the cases behind the biggest
awards, and the laws and events that shaped them. 22 programmes: the US
False Claims Act, the IRS, the SEC, the CFTC, newer US schemes (money
laundering, car safety, the Justice Department's pilot and its antitrust
programme), and programmes outside the US (South Korea, Ontario, Canada's
offshore tax informants, the UK tax authority and others).

Every number is a separate claim with its source, page, verbatim quote and
status, and sources that disagree (agencies revise past years heavily) are
kept side by side. Built on the same engine as `topics/cbi`. Whistleblowers
are named only when they went public themselves or a court or agency named
them.

Maintained by Oscar Leo ([oscarleo.com](https://oscarleo.com)). First
research pass: 3–4 October 2026. What we looked for and couldn't find is in
`docs/GAPS.md`; the next pass is planned in `docs/WAVE2_PLAN.md`.

## What's in it

| | rows |
|---|---|
| Numbers (`data/observations.csv`) | 4,224 |
| Cases and individual awards (`data/cases.csv`) | 222 |
| Reward rules over time (`data/program_rules.csv`) | 152 |
| Events (`data/events.csv`) | 150 |
| Sources (`data/sources.csv`) | 215, of which 192 have a stored copy in `raw/` |
| Programmes (`data/programs.csv`) | 22 |
| Indicators (`data/indicators.csv`) | 22 |

Numbers per programme: usa-fca-qui-tam 2000, usa-sec-wb 1011, usa-irs-wbo 965, usa-cftc-wb 133, kor-acrc-rewards 28, usa-fincen-aml-wb 22, can-cra-otip 17, ltu-gp-rewards 13, can-osc-wb 12, gbr-hmrc-informants 10, svk-uoo-rewards 8, usa-wildlife-rewards 2, usa-nhtsa-wb 2, usa-doj-cwap 1.

The column-by-column description is in [docs/DATA_MODEL.md](docs/DATA_MODEL.md).

## How it was checked

- `scripts/verify_quotes.py` looks for every quote in the stored copy. Of
  4,748 quoted rows, 4,245 were found verbatim, 366 matched as a table row
  put back together from its cells, and 80 (values printed in charts and
  image tables) were checked by eye on the rendered page (`data/quote_checks.csv`).
  The other 57 cite news, law-firm and NGO sources, linked rather than stored.
- **A blind second reading** of a stratified sample: a different AI model
  (Claude Sonnet 5) was given each number's document, page, indicator and
  period, but not the value, and read it itself. Of 614 numbers across
  all stored documents, 600 came out the same; in the other 14 the first
  reading was confirmed on the page (images the second reader's OCR couldn't
  read, a count of applications decided taken for applications received, or
  the same figure written differently). No value had to be corrected.
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
