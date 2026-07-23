"""Validate RedShelf's generated static site and required library assets."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DOCS = ROOT / "docs"
CONFIG_TEXT = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
SITE_URL_MATCH = re.search(r"^site_url:\s*(\S+)\s*$", CONFIG_TEXT, re.MULTILINE)
SITE_PREFIX = urlsplit(SITE_URL_MATCH.group(1) if SITE_URL_MATCH else "").path.strip("/")
REQUIRED_PDFS = {
    "cannabis-policy-example.pdf",
    "conference-proceedings-example.pdf",
    "malaysia-public-health-example.pdf",
    "netnography-example.pdf",
    "research-methods-example.pdf",
    "social-judgment-theory-example.pdf",
}


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag in {"a", "link"} and attributes.get("href"):
            self.targets.append(attributes["href"] or "")
        if tag in {"iframe", "img", "script", "source"} and attributes.get("src"):
            self.targets.append(attributes["src"] or "")


def is_external(target: str) -> bool:
    return target.startswith(
        ("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "//")
    )


def resolve_target(source: Path, target: str) -> Path | None:
    parsed = urlsplit(target)
    if not parsed.path or is_external(target):
        return None

    path = unquote(parsed.path.lstrip("/"))
    if parsed.path.startswith("/") and SITE_PREFIX:
        if path == SITE_PREFIX:
            path = ""
        elif path.startswith(f"{SITE_PREFIX}/"):
            path = path[len(SITE_PREFIX) + 1 :]
    relative = Path(path)
    candidate = (SITE / relative) if parsed.path.startswith("/") else (source.parent / relative)
    candidate = candidate.resolve()

    if candidate.is_dir() or parsed.path.endswith("/"):
        return candidate / "index.html"
    return candidate


def validate_links() -> list[str]:
    errors: list[str] = []
    for html_file in SITE.rglob("*.html"):
        parser = LinkCollector()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for target in parser.targets:
            resolved = resolve_target(html_file, target)
            if resolved is None:
                continue
            try:
                resolved.relative_to(SITE.resolve())
            except ValueError:
                errors.append(f"{html_file.relative_to(SITE)}: path escapes site: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{html_file.relative_to(SITE)}: missing target: {target}")
    return errors


def validate_required_assets() -> list[str]:
    errors: list[str] = []
    pdf_dir = DOCS / "assets" / "pdf"
    actual_pdfs = {path.name for path in pdf_dir.glob("*.pdf")}
    missing_pdfs = sorted(REQUIRED_PDFS - actual_pdfs)
    if missing_pdfs:
        errors.append(f"Missing example PDFs: {', '.join(missing_pdfs)}")

    for relative in (
        "assets/css/extra.css",
        "assets/js/extra.js",
        "assets/images/logo.svg",
        "assets/images/favicon.svg",
    ):
        if not (DOCS / relative).is_file():
            errors.append(f"Missing required asset: docs/{relative}")
    return errors


def main() -> None:
    if not SITE.is_dir():
        raise SystemExit("site/ does not exist. Run 'mkdocs build --strict' first.")

    errors = [*validate_required_assets(), *validate_links()]
    if errors:
        print("RedShelf validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    html_count = len(list(SITE.rglob("*.html")))
    print(f"RedShelf validation passed: {html_count} HTML pages and all required assets.")


if __name__ == "__main__":
    main()
