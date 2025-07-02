"""HTML renderer extends Marko's Renderer class."""

from __future__ import annotations

import html
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, cast
from urllib.parse import quote

from marko import Renderer

from babbl.defaults import DEFAULT_CSS
from babbl.utils import load_file

if TYPE_CHECKING:
    from marko import block, element, inline


class BaseRenderer(ABC, Renderer):
    """Strictly specified Renderer base class that plugs into Marko."""

    @abstractmethod
    def render_paragraph(self, element: block.Paragraph) -> str:
        """Render a paragraph element"""
        pass

    @abstractmethod
    def render_list(self, element: block.List) -> str:
        """Render a list element (ordered or unordered)"""
        pass

    @abstractmethod
    def render_list_item(self, element: block.ListItem) -> str:
        """Render a list item element"""
        pass

    @abstractmethod
    def render_quote(self, element: block.Quote) -> str:
        """Render a blockquote element"""
        pass

    @abstractmethod
    def render_fenced_code(self, element: block.FencedCode) -> str:
        """Render a fenced code block"""
        pass

    @abstractmethod
    def render_code_block(self, element: block.CodeBlock) -> str:
        """Render a code block"""
        pass

    @abstractmethod
    def render_html_block(self, element: block.HTMLBlock) -> str:
        """Render an HTML block"""
        pass

    @abstractmethod
    def render_thematic_break(self, element: block.ThematicBreak) -> str:
        """Render a thematic break (horizontal rule)"""
        pass

    @abstractmethod
    def render_heading(self, element: block.Heading) -> str:
        """Render a heading element"""
        pass

    @abstractmethod
    def render_setext_heading(self, element: block.SetextHeading) -> str:
        """Render a setext heading"""
        pass

    @abstractmethod
    def render_blank_line(self, element: block.BlankLine) -> str:
        """Render a blank line"""
        pass

    @abstractmethod
    def render_link_ref_def(self, element: block.LinkRefDef) -> str:
        """Render a link reference definition"""
        pass

    @abstractmethod
    def render_emphasis(self, element: inline.Emphasis) -> str:
        """Render emphasis (italic) text"""
        pass

    @abstractmethod
    def render_strong_emphasis(self, element: inline.StrongEmphasis) -> str:
        """Render strong emphasis (bold) text"""
        pass

    @abstractmethod
    def render_inline_html(self, element: inline.InlineHTML) -> str:
        """Render inline HTML"""
        pass

    @abstractmethod
    def render_plain_text(self, element: Any) -> str:
        """Render plain text"""
        pass

    @abstractmethod
    def render_link(self, element: inline.Link) -> str:
        """Render a link"""
        pass

    @abstractmethod
    def render_auto_link(self, element: inline.AutoLink) -> str:
        """Render an auto link"""
        pass

    @abstractmethod
    def render_image(self, element: inline.Image) -> str:
        """Render an image"""
        pass

    @abstractmethod
    def render_literal(self, element: inline.Literal) -> str:
        """Render literal text"""
        pass

    @abstractmethod
    def render_raw_text(self, element: inline.RawText) -> str:
        """Render raw text"""
        pass

    @abstractmethod
    def render_line_break(self, element: inline.LineBreak) -> str:
        """Render a line break"""
        pass

    @abstractmethod
    def render_code_span(self, element: inline.CodeSpan) -> str:
        """Render inline code"""
        pass

    @abstractmethod
    def render_table(self, element: Any) -> str:
        """Render a table element"""
        pass

    @abstractmethod
    def render_table_head(self, element: Any) -> str:
        """Render a table head element"""
        pass

    @abstractmethod
    def render_table_body(self, element: Any) -> str:
        """Render a table body element"""
        pass

    @abstractmethod
    def render_table_row(self, element: Any) -> str:
        """Render a table row element"""
        pass

    @abstractmethod
    def render_table_cell(self, element: Any) -> str:
        """Render a table cell element"""
        pass

    @abstractmethod
    def render_table_head_cell(self, element: Any) -> str:
        """Render a table header cell element"""
        pass


class HTMLRenderer(BaseRenderer):
    """Beautiful HTML renderer with clean styling and semantic classes."""

    def __init__(self, highlight_syntax: bool = True, css_file_path: Optional[Path] = None):
        """
        Initialize the HTML renderer.

        Args:
            highlight_syntax: Whether to use Pygments for syntax highlighting
            css_file_path: Path to CSS file
        """
        super().__init__()
        self.highlight_syntax = highlight_syntax
        self.pygments_formatter = None

        if css_file_path:
            self.base_css = load_file(css_file_path)
        else:
            self.base_css = DEFAULT_CSS

        if self.highlight_syntax:
            try:
                from pygments import highlight  # type: ignore
                from pygments.formatters import HtmlFormatter  # type: ignore
                from pygments.lexers import get_lexer_by_name  # type: ignore

                self.highlight = highlight
                self.get_lexer_by_name = get_lexer_by_name
                self.pygments_formatter = HtmlFormatter(style="friendly")
            except ImportError:
                self.highlight_syntax = False

    @staticmethod
    def escape_html(raw: str) -> str:
        """Replaces unsafe HTML characters with their escaped equivalents."""
        return html.escape(html.unescape(raw)).replace("&#x27;", "'")

    @staticmethod
    def escape_url(raw: str) -> str:
        """Escape urls to prevent code injection craziness."""
        return html.escape(quote(html.unescape(raw), safe="/#:()*?=%@+,&"))

    def html(self, element: element.Element, metadata: dict[str, str] | None) -> str:
        """Converts the base element to HTML with full document structure."""
        content = super().render(element)
        meta_str = (
            "\n".join(f"<meta name={key} content={value}>" for key, value in metadata.items()) if metadata else ""
        )

        # create complete HTML document
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{meta_str}
{f"<title>{metadata.get('title', 'Document')}</title>" if metadata else ""}
<style>
{self.get_css()}
</style>
</head>
<body>
<section>
{self.get_header(metadata) if metadata else ""}
{content}
</section>
</body>
</html>"""

    def get_css(self) -> str:
        """Get CSS for the rendered HTML."""
        css = self.base_css

        # add Pygments CSS if available
        if self.highlight_syntax and self.pygments_formatter:
            pygments_css = self.pygments_formatter.get_style_defs(".highlight")
            css += (
                "\n"
                + pygments_css
                + """
.highlight {
    background: #f5f5f5;
    border: none;
    margin: 1rem 0;
}
.highlight pre {
    margin: 0;
    padding: 1rem;
    overflow-x: auto;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.4;
}"""
            )

        return css

    def get_header(self, metadata: dict[str, str]) -> str:
        """Get the header of the document."""
        meta = metadata.copy()
        res = "<header>\n"
        if "title" in meta:
            res += f'<h1 class="title">{meta["title"]}</h1>\n'
            meta.pop("title")
        res += "<div class='metadata'>\n"
        if "author" in meta:
            res += f'<div class="meta-field">Author: {meta["author"]}</div>\n'
            meta.pop("author")
        if "date" in meta:
            res += f'<div class="meta-field">Date: {meta["date"]}</div>\n'
            meta.pop("date")
        if "summary" in meta:
            res += f'<div class="meta-field">Summary: {meta["summary"]}</div>\n'
            meta.pop("summary")
        if "description" in meta:
            res += f'<div class="meta-field">Description: {meta["description"]}</div>\n'
            meta.pop("description")
        if "tags" in meta:
            res += f'<div class="meta-field">Tags: {", ".join(meta["tags"])}</div>\n'
            meta.pop("tags")
        if "categories" in meta:
            res += f'<div class="meta-field">Categories: {meta["categories"]}</div>\n'
            meta.pop("categories")
        if "slug" in meta:
            res += f'<div class="meta-field">Slug: {meta["slug"]}</div>\n'
            meta.pop("slug")
        if "layout" in meta:
            res += f'<div class="meta-field">Layout: {meta["layout"]}</div>\n'
            meta.pop("layout")
        if "draft" in meta:
            res += f'<div class="meta-field">Draft: {meta["draft"]}</div>\n'
            meta.pop("draft")
        for key, value in meta.items():
            res += f'<div class="meta-field">{key}: {value}</div>\n'
        res += "</div>\n"
        res += "<hr />\n"
        res += "</header>\n"
        return res

    def render_paragraph(self, element: block.Paragraph) -> str:
        children = self.render_children(element)
        if element._tight:  # type: ignore
            return children
        else:
            return f'<p class="paragraph">{children}</p>\n'

    def render_list(self, element: block.List) -> str:
        if element.ordered:
            tag = "ol"
            css_class = "ordered-list"
            extra = f' start="{element.start}"' if element.start != 1 else ""
        else:
            tag = "ul"
            css_class = "unordered-list"
            extra = ""
        return f'<{tag} class="{css_class}"{extra}>\n{self.render_children(element)}</{tag}>\n'

    def render_list_item(self, element: block.ListItem) -> str:
        if len(element.children) == 1 and getattr(element.children[0], "_tight", False):  # type: ignore
            sep = ""
        else:
            sep = "\n"
        return f'<li class="list-item">{sep}{self.render_children(element)}</li>\n'

    def render_quote(self, element: block.Quote) -> str:
        return f'<blockquote class="blockquote">\n{self.render_children(element)}</blockquote>\n'

    def render_fenced_code(self, element: block.FencedCode) -> str:
        code_content = element.children[0].children  # type: ignore

        if self.highlight_syntax and element.lang and self.pygments_formatter:
            try:
                lexer = self.get_lexer_by_name(element.lang)
                highlighted_code = self.highlight(code_content, lexer, self.pygments_formatter)  # type: ignore
                # ensure proper class structure
                highlighted_code = highlighted_code.replace(
                    '<div class="highlight"><pre>', '<div class="highlight"><pre class="code-block">'
                )
                return highlighted_code + "\n"
            except:
                # fallback to plain code block
                pass

        # plain code block
        lang_class = f' class="language-{self.escape_html(element.lang)}"' if element.lang else ""
        escaped_code = html.escape(code_content)
        return f'<pre class="code-block"{lang_class}><code>{escaped_code}</code></pre>\n'

    def render_code_block(self, element: block.CodeBlock) -> str:
        return self.render_fenced_code(cast("block.FencedCode", element))

    def render_html_block(self, element: block.HTMLBlock) -> str:
        return element.body

    def render_thematic_break(self, element: block.ThematicBreak) -> str:
        return "<hr />\n"

    def render_heading(self, element: block.Heading) -> str:
        css_class = f"heading-{element.level}"
        return f'<h{element.level} class="{css_class}">{self.render_children(element)}</h{element.level}>\n'

    def render_setext_heading(self, element: block.SetextHeading) -> str:
        return self.render_heading(cast("block.Heading", element))

    def render_blank_line(self, element: block.BlankLine) -> str:
        return ""

    def render_link_ref_def(self, element: block.LinkRefDef) -> str:
        return ""

    def render_emphasis(self, element: inline.Emphasis) -> str:
        return f'<em class="emphasis">{self.render_children(element)}</em>'

    def render_strong_emphasis(self, element: inline.StrongEmphasis) -> str:
        return f'<strong class="strong">{self.render_children(element)}</strong>'

    def render_inline_html(self, element: inline.InlineHTML) -> str:
        return cast(str, element.children)

    def render_plain_text(self, element: Any) -> str:
        if isinstance(element.children, str):
            return self.escape_html(element.children)
        return self.render_children(element)

    def render_link(self, element: inline.Link) -> str:
        template = '<a href="{}" class="link"{}>{}</a>'
        title = f' title="{self.escape_html(element.title)}"' if element.title else ""
        url = self.escape_url(element.dest)
        body = self.render_children(element)
        return template.format(url, title, body)

    def render_auto_link(self, element: inline.AutoLink) -> str:
        return self.render_link(cast("inline.Link", element))

    def render_image(self, element: inline.Image) -> str:
        template = '<img src="{}" alt="{}" class="image"{} />'
        title = f' title="{self.escape_html(element.title)}"' if element.title else ""
        url = self.escape_url(element.dest)
        render_func = self.render
        self.render = self.render_plain_text  # type: ignore
        body = self.render_children(element)
        self.render = render_func  # type: ignore
        return template.format(url, body, title)

    def render_literal(self, element: inline.Literal) -> str:
        return self.render_raw_text(cast("inline.RawText", element))

    def render_raw_text(self, element: inline.RawText) -> str:
        return self.escape_html(element.children)

    def render_line_break(self, element: inline.LineBreak) -> str:
        if element.soft:
            return "\n"
        return "<br />\n"

    def render_code_span(self, element: inline.CodeSpan) -> str:
        escaped_code = html.escape(cast(str, element.children))
        return f'<code class="inline-code">{escaped_code}</code>'

    def render_table(self, element: Any) -> str:
        """Render a table element."""
        # Handle our custom Table element
        if hasattr(element, "headers") and hasattr(element, "rows"):
            html = '<div class="table-container">\n<table class="table">\n'

            # Render header
            html += "<thead>\n<tr>\n"
            for header in element.headers:
                html += f"<th>{self.escape_html(header)}</th>\n"
            html += "</tr>\n</thead>\n"

            # Render body
            html += "<tbody>\n"
            for row in element.rows:
                html += "<tr>\n"
                for cell in row:
                    html += f"<td>{self.escape_html(cell)}</td>\n"
                html += "</tr>\n"
            html += "</tbody>\n"

            html += "</table>\n</div>\n"
            return html

        # Fallback to generic table rendering
        return (
            f'<div class="table-container">\n<table class="table">\n{self.render_children(element)}</table>\n</div>\n'
        )

    def render_table_head(self, element: Any) -> str:
        """Render a table head element."""
        return f"<thead>\n{self.render_children(element)}</thead>\n"

    def render_table_body(self, element: Any) -> str:
        """Render a table body element."""
        return f"<tbody>\n{self.render_children(element)}</tbody>\n"

    def render_table_row(self, element: Any) -> str:
        """Render a table row element."""
        return f"<tr>\n{self.render_children(element)}</tr>\n"

    def render_table_cell(self, element: Any) -> str:
        """Render a table cell element."""
        return f"<td>{self.render_children(element)}</td>\n"

    def render_table_head_cell(self, element: Any) -> str:
        """Render a table header cell element."""
        return f"<th>{self.render_children(element)}</th>\n"

    # def render_frontmatter(self, element: Frontmatter) -> str:
    #     """Render frontmatter metadata as HTML."""
    #     if not hasattr(element, "metadata") or not element.metadata:
    #         return ""

    #     metadata = element.metadata
    #     metadata_html = []

    #     if "title" in metadata:
    #         metadata_html.append(f'<meta name="title" content="{self.escape_html(str(metadata["title"]))}">')

    #     if "author" in metadata:
    #         metadata_html.append(f'<meta name="author" content="{self.escape_html(str(metadata["author"]))}">')

    #     if "date" in metadata:
    #         metadata_html.append(f'<meta name="date" content="{self.escape_html(str(metadata["date"]))}">')

    #     if "summary" in metadata:
    #         metadata_html.append(f'<meta name="description" content="{self.escape_html(str(metadata["summary"]))}">')
    #     elif "description" in metadata:
    #         metadata_html.append(
    #             f'<meta name="description" content="{self.escape_html(str(metadata["description"]))}">'
    #         )

    #     if "tags" in metadata and metadata["tags"]:
    #         if isinstance(metadata["tags"], list):
    #             tags_str = ", ".join(str(tag) for tag in metadata["tags"])
    #         else:
    #             tags_str = str(metadata["tags"])
    #         metadata_html.append(f'<meta name="keywords" content="{self.escape_html(tags_str)}">')

    #     if "categories" in metadata and metadata["categories"]:
    #         if isinstance(metadata["categories"], list):
    #             categories_str = ", ".join(str(cat) for cat in metadata["categories"])
    #         else:
    #             categories_str = str(metadata["categories"])
    #         metadata_html.append(f'<meta name="categories" content="{self.escape_html(categories_str)}">')

    #     if "slug" in metadata:
    #         metadata_html.append(f'<meta name="slug" content="{self.escape_html(str(metadata["slug"]))}">')

    #     if "layout" in metadata:
    #         metadata_html.append(f'<meta name="layout" content="{self.escape_html(str(metadata["layout"]))}">')

    #     if "draft" in metadata:
    #         draft_status = "true" if metadata["draft"] else "false"
    #         metadata_html.append(f'<meta name="draft" content="{draft_status}">')

    #     for key, value in metadata.items():
    #         if key not in [
    #             "title",
    #             "author",
    #             "date",
    #             "summary",
    #             "description",
    #             "tags",
    #             "categories",
    #             "slug",
    #             "layout",
    #             "draft",
    #         ]:
    #             metadata_html.append(
    #                 f'<meta name="{self.escape_html(str(key))}" content="{self.escape_html(str(value))}">'
    #             )

    #     if metadata_html:
    #         return "\n".join(metadata_html) + "\n"

    #     return ""
