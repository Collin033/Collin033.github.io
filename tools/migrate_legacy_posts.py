"""Recover Hexo post sources from the generated HTML in the legacy site.

The original Markdown sources were lost. This script deliberately converts
Hexo's rendered article body back to readable Markdown while preserving code
blocks exactly. Images that were embedded in HTML or committed to Git are
recovered; image paths that only referenced the old computer are replaced by
an explicit note instead of leaving a broken image on the rebuilt site.
"""

from __future__ import annotations

import base64
import html
import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag


LEGACY_ROOT = Path(r"D:\blog")
SOURCE_ROOT = Path(r"D:\blog-source")
POSTS_ROOT = SOURCE_ROOT / "source" / "_posts"
CHINA_TZ = timezone(timedelta(hours=8))


@dataclass
class MigrationResult:
    title: str
    slug: str
    source: str
    recovered_images: list[str] = field(default_factory=list)
    missing_images: list[str] = field(default_factory=list)
    code_blocks: int = 0


def yaml_string(value: str) -> str:
    """JSON strings are valid YAML strings and handle punctuation safely."""
    return json.dumps(value, ensure_ascii=False)


def parse_hexo_time(value: str | None, fallback: datetime) -> datetime:
    if not value:
        return fallback
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(CHINA_TZ)


def normalize_inline_text(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    return re.sub(r"[\t\r\n ]+", " ", value)


def code_fence(code: str, language: str = "text") -> str:
    code = code.rstrip("\n")
    fence = "````" if "```" in code else "```"
    return f"{fence}{language}\n{code}\n{fence}"


def repair_malformed_links(markdown: str) -> str:
    """Repair a small number of malformed links in the rendered legacy HTML.

    One old source contained literal Markdown brackets around an HTML anchor,
    so Hexo emitted a link nested inside another link. Keep the useful target
    and the explanatory text after it, while producing valid Markdown.
    """
    pattern = re.compile(
        r"^\[([^\]]+)\]\(\[?(https?://[^\]\s]+)\]\((https?://[^)]+)\)(.*)\)$"
    )
    repaired: list[str] = []
    for line in markdown.splitlines():
        match = pattern.match(line.strip())
        if match:
            line = f"[{match.group(1)}]({match.group(2)}){match.group(4)}"
        repaired.append(line)
    return "\n".join(repaired)


class ArticleRenderer:
    def __init__(self, legacy_file: Path, slug: str, result: MigrationResult):
        self.legacy_file = legacy_file
        self.slug = slug
        self.result = result
        self.asset_dir = POSTS_ROOT / slug
        self.image_index = 0

    def render(self, entry: Tag) -> str:
        for reward in entry.select(".page-reward"):
            reward.decompose()

        blocks: list[str] = []
        for child in entry.children:
            rendered = self.render_block(child).strip()
            if rendered:
                blocks.append(rendered)

        markdown = "\n\n".join(blocks)
        markdown = repair_malformed_links(markdown)
        markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)
        return markdown.strip() + "\n"

    def render_block(self, node: object) -> str:
        if isinstance(node, NavigableString):
            return normalize_inline_text(str(node)).strip()
        if not isinstance(node, Tag):
            return ""

        name = node.name.lower()
        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(name[1])
            return f"{'#' * level} {self.render_inline_children(node).strip()}"
        if name == "p":
            return self.render_inline_children(node).strip()
        if name == "figure" and "highlight" in node.get("class", []):
            return self.render_highlight(node)
        if name == "pre":
            return code_fence(node.get_text("", strip=False), "text")
        if name in {"ul", "ol"}:
            return self.render_list(node, ordered=name == "ol")
        if name == "blockquote":
            text = self.render_inline_children(node).strip()
            return "\n".join(f"> {line}" for line in text.splitlines())
        if name == "hr":
            return "---"
        if name == "span" and node.get("id") == "more":
            return "<!-- more -->"
        return self.render_inline(node).strip()

    def render_inline_children(self, node: Tag) -> str:
        return "".join(self.render_inline(child) for child in node.children)

    def render_inline(self, node: object) -> str:
        if isinstance(node, NavigableString):
            return normalize_inline_text(str(node))
        if not isinstance(node, Tag):
            return ""

        name = node.name.lower()
        if name == "a":
            if "headerlink" in node.get("class", []):
                return ""
            label = self.render_inline_children(node).strip()
            href = node.get("href", "").strip()
            if not href or not label:
                return label
            title = node.get("title")
            suffix = f' "{title}"' if title else ""
            return f"[{label}]({href}{suffix})"
        if name == "img":
            return self.render_image(node)
        if name == "br":
            return "\n"
        if name in {"strong", "b"}:
            return f"**{self.render_inline_children(node).strip()}**"
        if name in {"em", "i"}:
            return f"*{self.render_inline_children(node).strip()}*"
        if name in {"del", "s", "strike"}:
            return f"~~{self.render_inline_children(node).strip()}~~"
        if name == "code":
            value = node.get_text("", strip=False)
            marker = "``" if "`" in value else "`"
            return f"{marker}{value}{marker}"
        if name == "span" and node.get("id") == "more":
            return "\n\n<!-- more -->\n\n"
        if name in {"ul", "ol", "blockquote", "figure", "pre"}:
            return f"\n\n{self.render_block(node)}\n\n"
        return self.render_inline_children(node)

    def render_list(self, node: Tag, ordered: bool) -> str:
        lines: list[str] = []
        for index, item in enumerate(node.find_all("li", recursive=False), start=1):
            prefix = f"{index}." if ordered else "-"
            text = self.render_inline_children(item).strip()
            text = text.replace("\n", "\n  ")
            lines.append(f"{prefix} {text}")
        return "\n".join(lines)

    def render_highlight(self, figure: Tag) -> str:
        classes = figure.get("class", [])
        language = next((item for item in classes if item != "highlight"), "text")
        language = {"c++": "cpp", "plaintext": "text", "plain": "text"}.get(
            language, language
        )

        code_node = figure.select_one("td.code pre") or figure.select_one("pre")
        if code_node is None:
            return ""

        lines = code_node.select("span.line")
        if lines:
            code = "\n".join(line.get_text("", strip=False) for line in lines)
        else:
            code = code_node.get_text("", strip=False)

        self.result.code_blocks += 1
        return code_fence(code.replace("\xa0", " "), language)

    def render_image(self, image: Tag) -> str:
        src = unquote(image.get("src", "").strip())
        alt = image.get("alt", "图片").strip() or "图片"
        if not src:
            return ""

        if src.startswith("data:image/"):
            return self.recover_data_image(src, alt)

        if src.startswith(("https://", "http://", "//")):
            return f"![{alt}]({src})"

        basename = Path(src.replace("\\", "/")).name
        candidates = [
            self.legacy_file.parent / basename,
            LEGACY_ROOT / "assets" / basename,
        ]
        candidates.extend(LEGACY_ROOT.rglob(basename))
        source = next((path for path in candidates if path.is_file()), None)

        if source is not None:
            self.asset_dir.mkdir(parents=True, exist_ok=True)
            target = self.asset_dir / basename
            if source.resolve() != target.resolve():
                shutil.copy2(source, target)
            self.result.recovered_images.append(basename)
            return f"{{% asset_img {basename} {alt} %}}"

        self.result.missing_images.append(src)
        return f"**历史图片缺失：{alt}（原图片未进入 Git 仓库，现已移除失效链接）**"

    def recover_data_image(self, src: str, alt: str) -> str:
        match = re.match(r"data:image/([^;,]+);base64,(.+)", src, re.DOTALL)
        if not match:
            self.result.missing_images.append("无法解析的内嵌图片")
            return "**历史内嵌图片无法解析**"

        extension = {"jpeg": "jpg", "svg+xml": "svg"}.get(match.group(1), match.group(1))
        self.image_index += 1
        filename = f"embedded-image-{self.image_index}.{extension}"
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        (self.asset_dir / filename).write_bytes(base64.b64decode(match.group(2)))
        self.result.recovered_images.append(filename)
        return f"{{% asset_img {filename} {alt} %}}"


def front_matter(
    title: str,
    published: datetime,
    updated: datetime,
    tags: list[str],
    source_path: str,
) -> str:
    lines = [
        "---",
        f"title: {yaml_string(title)}",
        f"date: {published.strftime('%Y-%m-%d %H:%M:%S')}",
        f"updated: {updated.strftime('%Y-%m-%d %H:%M:%S')}",
        "tags:",
    ]
    if tags:
        lines.extend(f"  - {yaml_string(tag)}" for tag in tags)
    else:
        lines.append("  - 算法")
    lines.extend(
        [
            "categories:",
            "  - 学习笔记",
            "toc: true",
            f"legacy_source: {yaml_string(source_path)}",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def article_files() -> list[Path]:
    files: list[Path] = []
    for year in ("2022", "2023"):
        files.extend((LEGACY_ROOT / year).rglob("index.html"))
    return sorted(files)


def migrate_file(path: Path) -> MigrationResult:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title_node = soup.select_one("h1.article-title")
    entry = soup.select_one(".article-entry")
    if title_node is None or entry is None:
        raise RuntimeError(f"Cannot find article title/body in {path}")

    title = title_node.get_text(" ", strip=True)
    slug = path.parent.name
    relative_source = path.relative_to(LEGACY_ROOT).as_posix()
    result = MigrationResult(title=title, slug=slug, source=relative_source)

    published_node = soup.select_one("time[datetime]")
    published_raw = published_node.get("datetime") if published_node else None
    fallback = datetime.fromtimestamp(path.stat().st_mtime, tz=CHINA_TZ)
    published = parse_hexo_time(published_raw, fallback)

    modified_node = soup.select_one('meta[property="article:modified_time"]')
    modified_raw = modified_node.get("content") if modified_node else None
    updated = parse_hexo_time(modified_raw, published)

    tags = [node.get_text(" ", strip=True) for node in soup.select(".article-tag-list-link")]
    renderer = ArticleRenderer(path, slug, result)
    markdown = renderer.render(entry)

    target = POSTS_ROOT / f"{slug}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        front_matter(title, published, updated, tags, relative_source) + markdown,
        encoding="utf-8",
        newline="\n",
    )
    return result


def write_report(results: list[MigrationResult]) -> None:
    missing_count = sum(len(item.missing_images) for item in results)
    recovered_count = sum(len(item.recovered_images) for item in results)
    code_count = sum(item.code_blocks for item in results)
    lines = [
        "# 旧博客迁移报告",
        "",
        f"- 恢复文章：{len(results)} 篇",
        f"- 恢复代码块：{code_count} 个",
        f"- 恢复图片：{recovered_count} 张",
        f"- 无法恢复的历史图片：{missing_count} 张",
        "",
        "无法恢复的图片原本只引用旧电脑本地路径，从未提交到 Git。迁移稿已用文字提示替代死链。",
        "",
        "| 文章 | 恢复图片 | 缺失图片 | 原页面 |",
        "| --- | ---: | ---: | --- |",
    ]
    for item in results:
        lines.append(
            f"| {item.title} | {len(item.recovered_images)} | "
            f"{len(item.missing_images)} | `{item.source}` |"
        )

    missing = [
        (item.title, source)
        for item in results
        for source in item.missing_images
    ]
    if missing:
        lines.extend(["", "## 缺失图片清单", ""])
        for title, source in missing:
            lines.append(f"- **{title}**：`{source}`")

    (SOURCE_ROOT / "MIGRATION_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )


def main() -> None:
    POSTS_ROOT.mkdir(parents=True, exist_ok=True)
    results = [migrate_file(path) for path in article_files()]
    write_report(results)
    print(
        json.dumps(
            {
                "posts": len(results),
                "code_blocks": sum(item.code_blocks for item in results),
                "recovered_images": sum(len(item.recovered_images) for item in results),
                "missing_images": sum(len(item.missing_images) for item in results),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
