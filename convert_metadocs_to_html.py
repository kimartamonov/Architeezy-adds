from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "metadoc-pages"
OUTPUT_DIR = ROOT / "metadocs-html"
STRUCTURE_FILE = ROOT / "meta-doc-structure.md"
CSS_FILE = OUTPUT_DIR / "styles.css"


@dataclass(frozen=True)
class PageInfo:
    section: str
    title: str
    source_name: str
    output_name: str


INLINE_CODE_RE = re.compile(r"`([^`]+)`")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SCREENSHOT_RE = re.compile(r"^\[Скриншот\s+\d+\s+-\s+.+\]$")


def read_title(markdown_path: Path) -> str:
    text = markdown_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"Cannot find title in {markdown_path}")


def parse_structure() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in STRUCTURE_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 2:
            continue
        if cells[0] in {"Раздел документации", "---"} or cells[1] in {"Страница документации", "---"}:
            continue
        if set(cells[0]) == {"-"} or set(cells[1]) == {"-"}:
            continue
        rows.append((cells[0], cells[1]))
    return rows


def build_pages() -> list[PageInfo]:
    title_to_source: dict[str, str] = {}
    for markdown_path in SOURCE_DIR.glob("*.md"):
        title_to_source[read_title(markdown_path)] = markdown_path.name

    pages: list[PageInfo] = []
    for section, title in parse_structure():
        source_name = title_to_source.get(title)
        if not source_name:
            raise ValueError(f"Cannot map structure title to file: {title}")
        pages.append(
            PageInfo(
                section=section,
                title=title,
                source_name=source_name,
                output_name=Path(source_name).with_suffix(".html").name,
            )
        )
    return pages


def slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
    slug = re.sub(r"[\s_]+", "-", slug, flags=re.UNICODE).strip("-")
    return slug or "section"


def unique_anchor(base_anchor: str, used_anchors: dict[str, int]) -> str:
    count = used_anchors.get(base_anchor, 0)
    used_anchors[base_anchor] = count + 1
    if count == 0:
        return base_anchor
    return f"{base_anchor}-{count + 1}"


def render_inline(text: str, title_to_output: dict[str, str]) -> str:
    placeholders: list[str] = []

    def stash(value: str) -> str:
        token = f"@@PLACEHOLDER{len(placeholders)}@@"
        placeholders.append(value)
        return token

    def replace_md_link(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        href = target
        if href.endswith(".md"):
            href = href[:-3] + ".html"
        elif ".md#" in href:
            href = href.replace(".md#", ".html#")
        return stash(f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')

    text = MARKDOWN_LINK_RE.sub(replace_md_link, text)

    def replace_inline_code(match: re.Match[str]) -> str:
        code_value = match.group(1)
        target = title_to_output.get(code_value)
        if target:
            return stash(
                f'<a class="inline-page-link" href="{html.escape(target, quote=True)}"><code>{html.escape(code_value)}</code></a>'
            )
        return stash(f"<code>{html.escape(code_value)}</code>")

    text = INLINE_CODE_RE.sub(replace_inline_code, text)
    escaped = html.escape(text)

    for index, placeholder in enumerate(placeholders):
        escaped = escaped.replace(f"@@PLACEHOLDER{index}@@", placeholder)

    return escaped


def render_markdown(markdown_text: str, title_to_output: dict[str, str]) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown_text.splitlines()
    html_parts: list[str] = []
    headings: list[tuple[int, str, str]] = []
    used_anchors: dict[str, int] = {}
    in_ul = False
    in_ol = False
    in_paragraph = False
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal in_paragraph, paragraph_lines
        if paragraph_lines:
            text = " ".join(part.strip() for part in paragraph_lines if part.strip())
            if SCREENSHOT_RE.match(text):
                html_parts.append(f'<div class="screenshot-placeholder">{render_inline(text, title_to_output)}</div>')
            else:
                html_parts.append(f"<p>{render_inline(text, title_to_output)}</p>")
        paragraph_lines = []
        in_paragraph = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        ul_match = re.match(r"^[-*]\s+(.*)$", stripped)
        ol_match = re.match(r"^(\d+)\.\s+(.*)$", stripped)

        if not stripped:
            flush_paragraph()
            close_lists()
            continue

        if heading_match:
            flush_paragraph()
            close_lists()
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            anchor = unique_anchor(slugify(title), used_anchors)
            headings.append((level, title, anchor))
            html_parts.append(f'<h{level} id="{anchor}">{render_inline(title, title_to_output)}</h{level}>')
            continue

        if ul_match:
            flush_paragraph()
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            html_parts.append(f"<li>{render_inline(ul_match.group(1).strip(), title_to_output)}</li>")
            continue

        if ol_match:
            flush_paragraph()
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True
            html_parts.append(f"<li>{render_inline(ol_match.group(2).strip(), title_to_output)}</li>")
            continue

        if not in_paragraph:
            in_paragraph = True
        paragraph_lines.append(stripped)

    flush_paragraph()
    close_lists()
    return "\n".join(html_parts), headings


def build_section_map(pages: list[PageInfo]) -> dict[str, list[PageInfo]]:
    section_map: dict[str, list[PageInfo]] = {}
    for page in pages:
        section_map.setdefault(page.section, []).append(page)
    return section_map


def render_sidebar(current_output_name: str, sections: dict[str, list[PageInfo]]) -> str:
    parts = ['<nav class="sidebar">', '<a class="home-link" href="index.html">Все страницы</a>']
    for section, pages in sections.items():
        parts.append(f"<div class=\"nav-section\"><div class=\"nav-section-title\">{html.escape(section)}</div><ul>")
        for page in pages:
            class_name = "current" if page.output_name == current_output_name else ""
            parts.append(
                f'<li><a class="{class_name}" href="{html.escape(page.output_name, quote=True)}">{html.escape(page.title)}</a></li>'
            )
        parts.append("</ul></div>")
    parts.append("</nav>")
    return "\n".join(parts)


def render_prev_next(pages: list[PageInfo], current_page: PageInfo) -> str:
    index = pages.index(current_page)
    prev_link = ""
    next_link = ""
    if index > 0:
        prev_page = pages[index - 1]
        prev_link = (
            f'<a class="pager-link" href="{html.escape(prev_page.output_name, quote=True)}">'
            f"&larr; {html.escape(prev_page.title)}</a>"
        )
    if index < len(pages) - 1:
        next_page = pages[index + 1]
        next_link = (
            f'<a class="pager-link" href="{html.escape(next_page.output_name, quote=True)}">'
            f"{html.escape(next_page.title)} &rarr;</a>"
        )
    if not prev_link and not next_link:
        return ""
    return f'<div class="pager">{prev_link}<span class="pager-spacer"></span>{next_link}</div>'


def render_toc(headings: list[tuple[int, str, str]]) -> str:
    visible = [(level, title, anchor) for level, title, anchor in headings if level in {2, 3}]
    if not visible:
        return ""
    parts = ['<aside class="toc"><div class="toc-title">На странице</div><ul>']
    for level, title, anchor in visible:
        css_class = "toc-level-3" if level == 3 else "toc-level-2"
        parts.append(
            f'<li class="{css_class}"><a href="#{html.escape(anchor, quote=True)}">{html.escape(title)}</a></li>'
        )
    parts.append("</ul></aside>")
    return "\n".join(parts)


def render_layout(
    *,
    page_title: str,
    main_title: str,
    content_html: str,
    sidebar_html: str,
    toc_html: str,
    pager_html: str,
) -> str:
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="layout">
    {sidebar_html}
    <main class="content">
      <header class="page-header">
        <h1>{html.escape(main_title)}</h1>
      </header>
      {toc_html}
      <article class="article">
        {content_html}
      </article>
      {pager_html}
    </main>
  </div>
</body>
</html>
"""


def build_css() -> str:
    return """body {
  margin: 0;
  font-family: "Segoe UI", Arial, sans-serif;
  color: #1f2933;
  background: #f4f7fb;
  line-height: 1.65;
}

a {
  color: #0b63c8;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code {
  font-family: Consolas, "Courier New", monospace;
  background: #eef3f8;
  padding: 0.12rem 0.35rem;
  border-radius: 0.3rem;
  font-size: 0.94em;
}

.layout {
  max-width: 1440px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 24px;
  padding: 24px;
}

.sidebar {
  position: sticky;
  top: 0;
  align-self: start;
  max-height: 100vh;
  overflow-y: auto;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #d9e2ec;
  border-radius: 16px;
}

.home-link {
  display: inline-block;
  margin-bottom: 16px;
  font-weight: 700;
}

.nav-section {
  margin-bottom: 18px;
}

.nav-section-title {
  margin-bottom: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #52606d;
  text-transform: uppercase;
}

.nav-section ul,
.toc ul,
.index-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-section li {
  margin: 0 0 8px;
}

.nav-section a {
  display: block;
  padding: 8px 10px;
  border-radius: 10px;
  color: #243b53;
}

.nav-section a.current,
.nav-section a:hover {
  background: #e6f0fb;
}

.content {
  min-width: 0;
}

.page-header,
.article,
.toc,
.pager,
.index-card {
  background: #ffffff;
  border: 1px solid #d9e2ec;
  border-radius: 16px;
}

.page-header,
.article,
.toc,
.pager,
.index-card {
  padding: 24px 28px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  line-height: 1.2;
}

.toc {
  margin-bottom: 20px;
}

.toc-title {
  margin-bottom: 12px;
  font-weight: 700;
}

.toc li {
  margin: 0 0 8px;
}

.toc-level-3 {
  padding-left: 14px;
}

.article h1:first-child {
  display: none;
}

.article h2,
.article h3,
.article h4 {
  margin-top: 1.8em;
  line-height: 1.25;
}

.article p,
.article ul,
.article ol {
  margin: 1em 0;
}

.article ul,
.article ol {
  padding-left: 1.5rem;
}

.article li + li {
  margin-top: 0.35rem;
}

.screenshot-placeholder {
  margin: 1.25rem 0;
  padding: 1rem 1.1rem;
  border: 2px dashed #9fb3c8;
  border-radius: 14px;
  background: #f8fbff;
  color: #486581;
}

.inline-page-link code {
  color: #0b63c8;
}

.pager {
  margin-top: 20px;
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
}

.pager-spacer {
  flex: 1 1 auto;
}

.pager-link {
  font-weight: 600;
}

.index-card {
  margin: 24px auto;
  max-width: 980px;
}

.index-card h1 {
  margin-top: 0;
}

.index-list > li {
  margin-bottom: 18px;
}

.index-list strong {
  display: block;
  margin-bottom: 8px;
}

.index-list ul li + li {
  margin-top: 6px;
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
    max-height: none;
  }
}
"""


def render_index(pages: list[PageInfo], sections: dict[str, list[PageInfo]]) -> str:
    intro = (
        "<p>HTML-версия документации по метамоделям Architeezy, собранная из исходных markdown-файлов. "
        "Все внутренние переходы между страницами используют относительные ссылки на <code>.html</code>-файлы.</p>"
    )
    items: list[str] = ['<div class="index-card">', "<h1>Документация по метамоделям</h1>", intro, '<ol class="index-list">']
    for section, section_pages in sections.items():
        items.append(f"<li><strong>{html.escape(section)}</strong><ul>")
        for page in section_pages:
            items.append(
                f'<li><a href="{html.escape(page.output_name, quote=True)}">{html.escape(page.title)}</a></li>'
            )
        items.append("</ul></li>")
    items.append("</ol></div>")

    sidebar = render_sidebar("", sections)
    return render_layout(
        page_title="Документация по метамоделям",
        main_title="Документация по метамоделям",
        content_html="\n".join(items),
        sidebar_html=sidebar,
        toc_html="",
        pager_html="",
    )


def main() -> None:
    pages = build_pages()
    sections = build_section_map(pages)
    title_to_output = {page.title: page.output_name for page in pages}

    OUTPUT_DIR.mkdir(exist_ok=True)
    CSS_FILE.write_text(build_css(), encoding="utf-8")

    for page in pages:
        source_path = SOURCE_DIR / page.source_name
        markdown_text = source_path.read_text(encoding="utf-8")
        content_html, headings = render_markdown(markdown_text, title_to_output)
        sidebar = render_sidebar(page.output_name, sections)
        toc = render_toc(headings)
        pager = render_prev_next(pages, page)
        output_html = render_layout(
            page_title=page.title,
            main_title=page.title,
            content_html=content_html,
            sidebar_html=sidebar,
            toc_html=toc,
            pager_html=pager,
        )
        (OUTPUT_DIR / page.output_name).write_text(output_html, encoding="utf-8")

    (OUTPUT_DIR / "index.html").write_text(render_index(pages, sections), encoding="utf-8")


if __name__ == "__main__":
    main()
