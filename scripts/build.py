#!/usr/bin/env python3
"""Render dashboard/index.html from scoreboard data. Stdlib only."""

import html
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from scoreboard import load_scoreboard, render_site_pages
from research_registry import load_research_registry


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "scoreboard"
OUT_DIR = ROOT / "dashboard"
TEMPLATE = Path(__file__).resolve().parent / "template.html"
METHODOLOGY = ROOT / "METHODOLOGY.md"
OG_SOURCE = ROOT / "assets" / "og-ai-trajectory.png"
OG_OUT = OUT_DIR / "og.png"
STATIC_ASSETS = (
    (ROOT / "assets" / "favicon.svg", OUT_DIR / "favicon.svg"),
    (ROOT / "assets" / "favicon.ico", OUT_DIR / "favicon.ico"),
    (ROOT / "assets" / "apple-touch-icon.png", OUT_DIR / "apple-touch-icon.png"),
)


class VisibleWordCounter(HTMLParser):
    """Count default-visible prose, excluding details content and SVG labels."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.words = 0
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"head", "script", "style", "title", "details", "svg"}:
            self.ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"head", "script", "style", "title", "details", "svg"}:
            self.ignored_depth = max(0, self.ignored_depth - 1)

    def handle_data(self, data: str) -> None:
        if self.ignored_depth:
            return
        self.words += len(re.findall(r"\b[\w’'-]+\b", html.unescape(data)))


class PageAudit(HTMLParser):
    """Collect the structural contracts that make the generated pages navigable."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.h1_count = 0
        self.current_page_links = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if values.get("href"):
            self.hrefs.append(str(values["href"]))
        if tag == "h1":
            self.h1_count += 1
        if values.get("aria-current") == "page":
            self.current_page_links += 1


def render_page(template: str, body: str, *, title: str, description: str, page_url: str) -> str:
    replacements = {
        "{{TITLE}}": html.escape(title, quote=True),
        "{{DESCRIPTION}}": html.escape(description, quote=True),
        "{{PAGE_URL}}": html.escape(page_url, quote=True),
        "{{PAGE}}": body,
    }
    for placeholder, value in replacements.items():
        if template.count(placeholder) < 1:
            raise ValueError(f"scripts/template.html must contain at least one {placeholder} placeholder")
        template = template.replace(placeholder, value)
    return template


DOUBLE_ESCAPED = re.compile(
    r"&amp;(?:#x?[0-9a-fA-F]+|amp|lt|gt|quot|apos|nbsp|mdash|ndash|hellip|rarr|middot);"
)


def assert_single_escaped(page: str, name: str) -> None:
    """Catch text that was escaped twice — it renders as a literal `&#x27;` on the page.

    Happens when a tooltip or label is assembled from pieces that were already
    escaped and then escaped again at insertion. Build tooltip strings from raw
    values and escape exactly once, at the point they enter the markup.
    """
    hits = DOUBLE_ESCAPED.findall(page)
    if hits:
        counts = ", ".join(f"{h} x{hits.count(h)}" for h in sorted(set(hits)))
        raise ValueError(
            f"{name}: {len(hits)} double-escaped entities ({counts}). "
            "Assemble the string from raw values and call esc() once, at insertion."
        )


def visible_word_count(page: str) -> int:
    counter = VisibleWordCounter()
    counter.feed(page)
    counter.close()
    return counter.words


def validate_site(pages: dict[str, str]) -> None:
    """Fail the build when a generated destination or fragment becomes orphaned."""
    audits: dict[str, PageAudit] = {}
    for filename, page in pages.items():
        audit = PageAudit()
        audit.feed(page)
        audit.close()
        audits[filename] = audit
        duplicate_ids = sorted({item for item in audit.ids if audit.ids.count(item) > 1})
        if duplicate_ids:
            raise ValueError(f"dashboard/{filename}: duplicate ids: {', '.join(duplicate_ids)}")
        if audit.h1_count != 1:
            raise ValueError(f"dashboard/{filename}: expected exactly one h1; found {audit.h1_count}")
        if audit.current_page_links != 1:
            raise ValueError(
                f"dashboard/{filename}: expected one aria-current=page link; found {audit.current_page_links}"
            )

    for filename, audit in audits.items():
        for href in audit.hrefs:
            if href.startswith(("http:", "https:", "mailto:", "/")):
                continue
            target = urlsplit(href)
            target_page = target.path or filename
            if target_page not in audits:
                raise ValueError(f"dashboard/{filename}: internal link targets missing page {href}")
            if target.fragment and target.fragment not in audits[target_page].ids:
                raise ValueError(f"dashboard/{filename}: internal link targets missing fragment {href}")


def main() -> None:
    metrics, claims, refresh, cruxes, data_files = load_scoreboard(DATA, ROOT / "data")
    research = load_research_registry(ROOT)
    methodology = METHODOLOGY.read_text(encoding="utf-8")
    bodies = render_site_pages(metrics, claims, refresh, cruxes, research, methodology, data_files)
    template = TEMPLATE.read_text(encoding="utf-8")
    metadata = {
        "index.html": (
            "AI Trajectory — Progress, Constraints, Forecasts, and Safety",
            "A concise map of AI progress, constraints, forecasts, and safety questions—measured against reality.",
            "https://ai-trajectory.vercel.app/",
        ),
        "evidence.html": (
            "Evidence — AI Trajectory",
            "Reality lines, source-backed measurements, AI R&D evidence, and visible data gaps.",
            "https://ai-trajectory.vercel.app/evidence.html",
        ),
        "forecasts.html": (
            "Forecasts — AI Trajectory",
            "Upcoming AI forecast tests, comparisons with later evidence, shared milestones, and revisions.",
            "https://ai-trajectory.vercel.app/forecasts.html",
        ),
        "safety.html": (
            "Safety Questions — AI Trajectory",
            "Eight source-backed questions tracing frontier AI risk from hazardous behavior through recovery.",
            "https://ai-trajectory.vercel.app/safety.html",
        ),
        "questions.html": (
            "Research Map — AI Trajectory",
            "Ten cross-cutting AI trajectory questions organized by the evidence needed to answer them.",
            "https://ai-trajectory.vercel.app/questions.html",
        ),
        "methodology.html": (
            "Methodology — AI Trajectory",
            "How AI Trajectory records observations, compares published claims, and maps unresolved safety questions.",
            "https://ai-trajectory.vercel.app/methodology.html",
        ),
    }
    pages = {}
    for filename, body in bodies.items():
        title, description, page_url = metadata[filename]
        pages[filename] = render_page(
            template,
            body,
            title=title,
            description=description,
            page_url=page_url,
        )
        assert_single_escaped(pages[filename], f"dashboard/{filename}")
    validate_site(pages)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, page in pages.items():
        (OUT_DIR / filename).write_text(page, encoding="utf-8")
    if OG_SOURCE.exists():
        shutil.copyfile(OG_SOURCE, OG_OUT)
    for source, destination in STATIC_ASSETS:
        if not source.exists():
            raise FileNotFoundError(f"Missing required public asset: {source}")
        shutil.copyfile(source, destination)
    word_counts = {filename: visible_word_count(page) for filename, page in pages.items()}
    print(f"Validated {data_files['metrics']} + {data_files['claims']}")
    print(f"Validated {len(research['questions']['questions'])} research questions across three evidence lanes")
    print("Visible words (details collapsed): " + ", ".join(f"{name}={count}" for name, count in word_counts.items()))
    for filename in pages:
        print(f"Wrote {OUT_DIR / filename}")


if __name__ == "__main__":
    main()
