#!/usr/bin/env python3
"""Render dashboard/index.html from scoreboard data. Stdlib only."""

import html
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

from scoreboard import load_scoreboard, render_methodology, render_scoreboard
from research_registry import load_research_registry


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "scoreboard"
OUT_DIR = ROOT / "dashboard"
INDEX_OUT = OUT_DIR / "index.html"
METHODOLOGY_OUT = OUT_DIR / "methodology.html"
TEMPLATE = Path(__file__).resolve().parent / "template.html"
METHODOLOGY = ROOT / "METHODOLOGY.md"
OG_SOURCE = ROOT / "assets" / "og-ai-trajectory.png"
OG_OUT = OUT_DIR / "og.png"


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


def render_page(template: str, body: str, *, title: str, description: str) -> str:
    replacements = {
        "{{TITLE}}": html.escape(title, quote=True),
        "{{DESCRIPTION}}": html.escape(description, quote=True),
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


def main() -> None:
    metrics, claims, refresh, cruxes, data_files = load_scoreboard(DATA, ROOT / "data")
    research = load_research_registry(ROOT)
    methodology = METHODOLOGY.read_text(encoding="utf-8")
    scoreboard = render_scoreboard(metrics, claims, refresh, cruxes, research, methodology, data_files)
    template = TEMPLATE.read_text(encoding="utf-8")
    index_page = render_page(
        template,
        scoreboard,
        title="AI Trajectory — Progress, Constraints, Forecasts, and Safety",
        description=(
            "A live evidence map of AI progress, constraints, forecasts, and safety questions—"
            "measured against reality."
        ),
    )
    methodology_body = f"""
      <header class="scoreboard-hero methodology-header">
        <div class="hero-mast">
          <a href="index.html" class="wordmark">AI Trajectory</a>
          <a href="#methodology">Methodology</a>
        </div>
      </header>
      <nav class="scoreboard-nav" aria-label="Methodology navigation">
        <a href="index.html">Scoreboard</a><a href="#methodology">Methodology</a>
      </nav>
      <main>{render_methodology(methodology, data_files)}</main>
    """
    methodology_page = render_page(
        template,
        methodology_body,
        title="Methodology — AI Trajectory",
        description="How AI Trajectory records observations, compares published claims, and maps unresolved safety questions.",
    )
    assert_single_escaped(index_page, "dashboard/index.html")
    assert_single_escaped(methodology_page, "dashboard/methodology.html")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_OUT.write_text(index_page, encoding="utf-8")
    METHODOLOGY_OUT.write_text(methodology_page, encoding="utf-8")
    if OG_SOURCE.exists():
        shutil.copyfile(OG_SOURCE, OG_OUT)
    word_count = visible_word_count(index_page)
    print(f"Validated {data_files['metrics']} + {data_files['claims']}")
    print(f"Validated {len(research['questions']['questions'])} research questions across three evidence lanes")
    print(f"Research-view words (details collapsed): {word_count}")
    print(f"Wrote {INDEX_OUT}")
    print(f"Wrote {METHODOLOGY_OUT}")


if __name__ == "__main__":
    main()
