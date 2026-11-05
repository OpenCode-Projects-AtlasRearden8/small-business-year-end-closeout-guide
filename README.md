# Small-Business Year-End Closeout Guide

A plain-English, step-by-step companion for closing the books on a tiny LLC or side business — no panic, no jargon, no tax advice. Just a calm ritual you can run every December so January-you doesn't inherit a shoebox of mystery.

Built by **Asdale Dynamics, LLC** as part of the same friendly series as *The Massive AI Manual* — everything explained "like a friend would": clear, warm, and never condescending.

## Who this is for

- A single-member LLC that made a little money on the side
- An eBay/Amazon reseller, book royalty earner, or gig worker
- Anyone whose "bookkeeping" is currently a spreadsheet (or a drawer)

If you already have a CPA and proper accounting software, this guide will still be useful — as the December checklist you hand them instead of a shoebox.

## What's inside

| Page | What it covers |
| --- | --- |
| [Start Here](docs/00-start-here.md) | What "closing the books" actually means, and the full route map |
| [The December Bank Reconciliation Ritual](docs/01-bank-reconciliation-december-ritual.md) | Making every bank figure match your records, line by line |
| [Categorizing a Year of Transactions](docs/02-categorizing-a-year-of-transactions.md) | Turning 400 mystery rows into a handful of meaningful numbers |
| [Mileage Totals](docs/03-mileage-totals.md) | Reconstructing a year of driving without guesswork |
| [1099 Prep](docs/04-1099-prep.md) | What 1099s are, who might need to send them, and what to gather now |
| [W-2 vs. Contractor Notes](docs/05-w2-vs-contractor-notes.md) | The difference between hiring someone and paying for a service |
| [What to Archive](docs/06-what-to-archive.md) | What to keep, in what form, for how long — and what you can safely toss |
| [Printable Year-End Checklist](docs/07-year-end-checklist.md) | One page you can print and physically check off |

## How to use it

- **Read it in order** from Start Here if this is your first year-end ever.
- **Or grab the checklist** in `docs/07-year-end-checklist.md` and work through it, peeking back at chapters as you go.
- **Print-friendly** every page in the HTML site (`site/index.html`) is styled for printing, and the checklist is one clean sheet.

## Running the companion site

The `site/` folder is a fully static HTML site built from the markdown in `docs/`. To rebuild it from scratch and verify everything:

```bash
python3 build.py      # regenerates site/ from docs/ and runs all checks
```

To just view the site, open `site/index.html` in a browser — no server, no build tools, no internet needed. It's local-first by design.

## Important notes

- **This is not tax advice.** This guide explains *mechanics* — what things are called, what a reconciliation is, what a 1099-NEC looks like. It never tells you what to file, deduct, or owe. For that, use a qualified tax professional or official IRS/state resources.
- All examples use obviously fictional names and round numbers.
- Nothing in this repo connects to the internet, asks for accounts, or collects data.

## Credits

Written and maintained by **Asdale Dynamics, LLC** — Dylan Asdale's Indiana LLC for beginner-friendly books, guides, and tools. See [dylanasdale.github.io](https://dylanasdale.github.io).

Licensed under the MIT License — see [LICENSE](LICENSE).
