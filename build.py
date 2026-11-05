#!/usr/bin/env python3
"""Build the site/ static HTML pages from docs/ markdown, then verify them.

Standard library only. Run: python3 build.py
"""

import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

# ------------------------------------------------------------------- markdown

def inline(text: str) -> str:
    """Inline markdown -> HTML: code spans, links, bold, italics."""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{_href(m.group(2))}">{m.group(1)}</a>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)\*([^*\s][^*]*)\*(?!\w)", r"<em>\1</em>", text)
    return text


def _href(url: str) -> str:
    """Rewrite local .md link targets to .html so the site survives the build."""
    if re.match(r"[a-z]+://", url) or url.startswith("#") or url.endswith(".html"):
        return url
    if url.endswith(".md"):
        return url[:-3] + ".html"
    return url


def md_to_html(md_text: str) -> str:
    out: list[str] = []
    open_kind: str | None = None  # "ul" | "ol" | "cb"

    def element_for(kind: str) -> str:
        return "ol" if kind == "ol" else "ul"

    def close_list() -> None:
        nonlocal open_kind
        if open_kind:
            out.append(f"</{element_for(open_kind)}>")
            open_kind = None

    lines = md_text.splitlines()
    i, n = 0, len(lines)

    while i < n:
        line = lines[i]

        if line.startswith("```"):  # fenced code block
            close_list()
            out.append("<pre><code>")
            i += 1
            while i < n and not lines[i].startswith("```"):
                out.append(html.escape(lines[i]))
                i += 1
            out.append("</code></pre>")
            i += 1
            continue

        stripped = line.strip()
        if not stripped:
            close_list()
            i += 1
            continue

        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            close_list()
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_list()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # table (header | separator-with-dashes | rows)
        if stripped.startswith("|") and i + 1 < n:
            sep = lines[i + 1].strip().replace(" ", "")
            if re.fullmatch(r"\|(:?-{2,}:?\|)+", sep):
                close_list()
                headers = [c.strip() for c in stripped.strip("|").split("|")]
                out.append("<table><thead><tr>")
                out.extend(f"<th>{inline(h)}</th>" for h in headers)
                out.append("</tr></thead><tbody>")
                i += 2
                while i < n and lines[i].strip().startswith("|"):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
                    i += 1
                out.append("</tbody></table>")
                continue

        if stripped.startswith(">"):
            close_list()
            out.append(f"<blockquote><p>{inline(stripped.lstrip('> ').strip())}</p></blockquote>")
            i += 1
            continue

        m = re.match(r"^- \[( |x)\]\s+(.*)$", stripped)
        if m:
            if open_kind != "cb":
                close_list()
                open_kind = "cb"
                out.append('<ul class="cb">')
            checked = " checked" if m.group(1) == "x" else ""
            out.append(
                f'<li><label><input type="checkbox"{checked} disabled> {inline(m.group(2))}</label></li>'
            )
            i += 1
            continue

        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            if open_kind not in ("ul", "cb"):
                close_list()
                open_kind = "ul"
                out.append("<ul>")
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue

        m = re.match(r"^\d+\.\s+(.*)$", stripped)
        if m:
            if open_kind != "ol":
                close_list()
                open_kind = "ol"
                out.append("<ol>")
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue

        close_list()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


# ------------------------------------------------------------------- template

PAGES = [
    ("00-start-here.md", "Start Here"),
    ("01-bank-reconciliation-december-ritual.md", "Bank Reconciliation Ritual"),
    ("02-categorizing-a-year-of-transactions.md", "Categorizing a Year"),
    ("03-mileage-totals.md", "Mileage Totals"),
    ("04-1099-prep.md", "1099 Prep"),
    ("05-w2-vs-contractor-notes.md", "W-2 vs. Contractor"),
    ("06-what-to-archive.md", "What to Archive"),
    ("07-year-end-checklist.md", "Printable Checklist"),
]

PAGE_STEMS = [fname[:-3] for fname, _ in PAGES]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Small-Business Year-End Closeout Guide</title>
<meta name="description" content="A plain-English year-end closeout ritual for tiny LLCs and side businesses. Bookkeeping mechanics only, not tax advice.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-head">
  <p class="masthead"><a href="index.html">Small-Business Year-End Closeout Guide</a></p>
  <p class="tagline">Plain English, step by step, never condescending. From Asdale Dynamics, LLC.</p>
  <nav aria-label="Chapters"><a href="index.html"{a0}>Overview</a>{navlinks}</nav>
</header>
<main>
<article>
{body}
</article>
</main>
<footer>
<p><em>Small-Business Year-End Closeout Guide</em> · Asdale Dynamics, LLC · MIT License.<br>
Educational bookkeeping mechanics only — not tax, legal, or financial advice.</p>
</footer>
</body>
</html>
"""

CSS = """:root {
  --ink: #21262d;
  --paper: #fdfcf8;
  --accent: #0e6b5c;
  --accent-soft: #eaf4f1;
  --line: #ddd8cf;
}
* { box-sizing: border-box; }
html { font-size: 17px; }
body {
  margin: 0;
  font-family: Georgia, "Iowan Old Style", "Times New Roman", serif;
  line-height: 1.65;
  color: var(--ink);
  background: var(--paper);
}
.site-head {
  border-bottom: 3px double var(--accent);
  padding: 1.4rem 1.5rem 1rem;
  background: linear-gradient(180deg, var(--accent-soft), var(--paper));
}
.masthead { margin: 0; font-size: 1.35rem; font-weight: 700; }
.masthead a { color: var(--accent); text-decoration: none; }
.tagline { margin: .15rem 0 .7rem; font-size: .92rem; color: #5a6069; font-style: italic; }
.site-head nav { display: flex; flex-wrap: wrap; gap: .35rem .95rem; }
.site-head nav a {
  font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: .85rem;
  text-decoration: none;
  color: var(--ink);
  border-bottom: 2px solid transparent;
  padding-bottom: 1px;
}
.site-head nav a:hover { color: var(--accent); }
.site-head nav a[aria-current="page"] { color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }
main { max-width: 44rem; margin: 0 auto; padding: 2rem 1.5rem 3rem; }
a { color: var(--accent); }
code {
  font-family: "SF Mono", ui-monospace, Menlo, Consolas, monospace;
  font-size: .86em;
  background: #f1ede5;
  padding: .1em .35em;
  border-radius: 4px;
}
pre {
  background: #f6f3ec;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: .9rem 1.1rem;
  overflow-x: auto;
}
pre code { background: none; padding: 0; font-size: .84em; }
h1 { font-size: 1.75rem; line-height: 1.25; margin: 0 0 1rem; color: var(--accent); }
h2 { font-size: 1.25rem; margin-top: 2.2rem; border-bottom: 1px solid var(--line); padding-bottom: .25rem; }
h3 { font-size: 1.05rem; margin-top: 1.6rem; }
blockquote {
  margin: 1rem 0;
  padding: .2rem 1rem;
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  font-style: italic;
}
table { border-collapse: collapse; width: 100%; margin: 1.2rem 0; font-size: .95rem; }
th, td { border: 1px solid var(--line); padding: .45rem .7rem; text-align: left; vertical-align: top; }
th { background: var(--accent-soft); font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; font-size: .85rem; }
tr:nth-child(even) td { background: #faf7f1; }
ul { padding-left: 1.4rem; }
li { margin: .3rem 0; }
ul.cb { list-style: none; padding-left: 0; }
ul.cb li { margin: .45rem 0; }
ul.cb label { display: block; cursor: default; }
ul.cb input[type="checkbox"] { margin-right: .45rem; accent-color: var(--accent); }
ul.cb input[type="checkbox"]:disabled { opacity: 1; }
footer {
  border-top: 1px solid var(--line);
  padding: 1rem 1.5rem 2rem;
  font-size: .82rem;
  color: #6b7078;
  text-align: center;
}
@media print {
  .site-head nav, footer { display: none; }
  body { background: #fff; font-size: 11.5pt; }
  .site-head { border-bottom: 2px solid #000; background: none; }
  main { max-width: 100%; padding: 0; }
  ul.cb li { page-break-inside: avoid; }
}
"""


def render(src: Path, nav_current: str, title: str) -> str:
    body = md_to_html(src.read_text(encoding="utf-8"))
    if nav_current == "index":
        # README lives at the repo root and links docs/xxx.md; the site is flat,
        # so index.html links straight to the page files.
        body = body.replace('href="docs/', 'href="')
    def nav_item(stem: str, href: str, label: str) -> str:
        if stem == nav_current:
            return f'<a href="{href}" aria-current="page">{label}</a>'
        return f'<a href="{href}">{label}</a>'

    navlinks = ""
    for (fname, label), stem in zip(PAGES, PAGE_STEMS):
        navlinks += nav_item(stem, f"{stem}.html", label)
    a0 = ' aria-current="page"' if nav_current == "index" else ""
    return TEMPLATE.format(title=title, body=body, navlinks=navlinks, a0=a0)


# -------------------------------------------------------------------- checks

def check_all(source_pages: dict[str, Path], site_files: dict[str, Path]) -> list[str]:
    problems: list[str] = []

    required = [
        "LICENSE",
        "README.md",
        "build.py",
        *(f"docs/{fname}" for fname, _ in PAGES),
        *(f"site/{stem}.html" for stem in PAGE_STEMS),
        "site/index.html",
        "site/style.css",
        "site/LICENSE",
    ]
    for rel in required:
        path = ROOT / rel
        if not path.exists():
            problems.append(f"missing file: {rel}")
        elif path.stat().st_size == 0:
            problems.append(f"empty file: {rel}")

    license_path = ROOT / "LICENSE"
    if license_path.exists():
        lic = license_path.read_text(encoding="utf-8")
        if "Copyright (c) 2026 Asdale Dynamics, LLC" not in lic:
            problems.append("LICENSE missing exact copyright line")
        if "Permission is hereby granted" not in lic:
            problems.append("LICENSE missing MIT grant text")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "Asdale Dynamics, LLC" not in readme:
        problems.append("README does not credit Asdale Dynamics, LLC")

    for rel, src in source_pages.items():
        text = src.read_text(encoding="utf-8")
        first_heading = next((l for l in text.splitlines() if l.startswith("#")), "")
        if not first_heading.startswith("# "):
            problems.append(f"{rel}: first heading is not an H1")
        if any(ord(ch) >= 0x1F300 for ch in text):
            problems.append(f"{rel}: contains emoji")

    for rel, path in site_files.items():
        text = path.read_text(encoding="utf-8")
        if "<h1" not in text:
            problems.append(f"{rel}: no <h1> in HTML page")
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            url = m.group(1)
            if re.match(r"[a-z]+://", url) or url.startswith("#") or url.startswith("mailto:"):
                continue
            frag = None
            if "#" in url:
                path_part, frag = url.split("#", 1)
            else:
                path_part = url
            target = (path.parent / path_part).resolve() if path_part else path.parent
            if not target.exists():
                problems.append(f"{rel}: broken link {url}")
                continue
            if frag:
                doc = text if target == path.resolve() else target.read_text(encoding="utf-8", errors="replace")
                if f'id="{frag}"' not in doc and f"id='{frag}'" not in doc:
                    problems.append(f"{rel}: missing anchor {url}")

    chain = PAGE_STEMS
    for stem_a, stem_b in zip(chain, chain[1:]):
        text = source_pages[f"{stem_a}.md"].read_text(encoding="utf-8")
        if f"{stem_b}.md" not in text:
            problems.append(f"{stem_a}.md: does not link to next chapter {stem_b}.md")

    return problems


# ---------------------------------------------------------------------- main

def main() -> int:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    (SITE / "style.css").write_text(CSS, encoding="utf-8")

    site_files: dict[str, Path] = {}
    (SITE / "index.html").write_text(
        render(ROOT / "README.md", "index", "Overview"), encoding="utf-8"
    )
    site_files["site/index.html"] = SITE / "index.html"
    (SITE / "LICENSE").write_text((ROOT / "LICENSE").read_text(encoding="utf-8"), encoding="utf-8")

    source_pages: dict[str, Path] = {}
    for fname, label in PAGES:
        src = DOCS / fname
        stem = fname[:-3]
        out = SITE / f"{stem}.html"
        out.write_text(render(src, stem, label), encoding="utf-8")
        source_pages[fname] = src
        site_files[f"site/{out.name}"] = out

    problems = check_all(source_pages, site_files)

    print(f"Built {len(site_files)} HTML pages + style.css into site/")
    if problems:
        print("\nPROBLEMS FOUND:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("All checks passed:")
    print("  - all required files present and non-empty")
    print("  - LICENSE carries the exact copyright line and MIT grant text")
    print("  - README credits Asdale Dynamics, LLC")
    print("  - every markdown page opens with an H1; no emoji anywhere")
    print("  - every internal link and anchor on the site resolves")
    print("  - the Start Here -> Checklist chapter chain is intact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
