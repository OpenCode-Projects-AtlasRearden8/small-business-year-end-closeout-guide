# STATUS.md — Small-Business Year-End Closeout Guide

## What was built

A self-contained beginner guide to closing the books on a tiny LLC or side business
(covers December bank reconciliation, categorizing a year of transactions, mileage
totals, 1099 preparation facts, W-2 vs. contractor notes, what to archive, and a
printable year-end checklist). Deliberately plain-English and **not tax advice** —
every tax-shaped judgment call is marked "→ taxes: ask a pro."

Contents:

- `README.md` — overview, table of contents, how to run the site
- `docs/` — 8 markdown chapters (00 Start Here … 07 Printable Year-End Checklist)
- `site/` — static HTML site generated from `docs/` (+ `site/LICENSE` copy);
  open `site/index.html` directly in a browser, no server needed,
  with print styles so the checklist prints on one clean page
- `build.py` — rebuilds `site/` from `docs/` **and** runs all verification checks
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`

## How to run it

Nothing to install — pure Python standard library for the build; the site itself
needs only a browser.

```bash
python3 build.py          # regenerate site/ from docs/ and run all checks
# open site/index.html in a browser
```

## Verification results

`python3 build.py` exits 0 and reports:

- 9 HTML pages + style.css built into `site/`
- all required files present and non-empty
- LICENSE contains the exact required copyright line and the standard MIT grant text
- README credits Asdale Dynamics, LLC
- every docs page opens with an H1; no emoji anywhere
- every internal link and anchor in `site/` resolves (link + anchor graph checked)
- chapter chain intact: Start Here → Reconciliation → Categorizing → Mileage →
  1099 Prep → W-2 vs. Contractor → Archive → Checklist
- `python3 -m py_compile build.py` — compiles clean
- scanned repo for secrets/API keys/personal data — clean (all examples are
  obviously fictional, no accounts, no network calls)

## Known gaps

- The markdown→HTML converter in `build.py` deliberately supports only the subset
  used by these docs (headings, tables, fenced code, lists/checkboxes, blockquotes,
  inline styles). It is not a general-purpose Markdown parser; new docs using
  nested/indented lists or multi-line list items will render imperfectly.
- Content is written for a U.S. context in spirit (1099/W-2, mileage logs) but
  mentions nothing jurisdiction-specific; retention periods are left to a
  professional, as intended.
- No automated content tests beyond the checks in `build.py` (no rendering
  screenshots/diff tests).
- The site is a flat 9-page static set; no search, no RSS, no dark mode — by design
  for a one-ritual-a-year guide.
