"""Markdown to HTML renderer with extensible formatting."""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Optional

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from babbl.cache import CacheManager
from babbl.frontmatter import process_file


class HTMLFormatter(ABC):
    """Abstract base class for HTML formatting."""

    @abstractmethod
    def format_heading(self, level: int, content: str, **kwargs) -> str:
        """Format a heading."""
        pass

    @abstractmethod
    def format_paragraph(self, content: str, **kwargs) -> str:
        """Format a paragraph."""
        pass

    @abstractmethod
    def format_code_block(self, code: str, language: Optional[str] = None, **kwargs) -> str:
        """Format a code block."""
        pass

    @abstractmethod
    def format_inline_code(self, code: str, **kwargs) -> str:
        """Format inline code."""
        pass

    @abstractmethod
    def format_link(self, text: str, url: str, **kwargs) -> str:
        """Format a link."""
        pass

    @abstractmethod
    def format_image(self, alt: str, src: str, title: Optional[str] = None, **kwargs) -> str:
        """Format an image."""
        pass

    @abstractmethod
    def format_list(self, items: List[str], ordered: bool = False, **kwargs) -> str:
        """Format a list."""
        pass

    @abstractmethod
    def format_blockquote(self, content: str, **kwargs) -> str:
        """Format a blockquote."""
        pass

    @abstractmethod
    def format_emphasis(self, content: str, strong: bool = False, **kwargs) -> str:
        """Format emphasis (italic/bold)."""
        pass

    @abstractmethod
    def get_css(self) -> str:
        """Get CSS for the HTML."""
        pass


class DefaultHTMLFormatter(HTMLFormatter):
    """Default HTML formatter with clean styling and syntax highlighting."""

    def __init__(self, use_syntax_highlighting: bool = True):
        """
        Initialize the formatter.

        Args:
            use_syntax_highlighting: Whether to use Pygments for syntax highlighting
        """
        self.use_syntax_highlighting = use_syntax_highlighting
        if self.use_syntax_highlighting:
            self.pygments_formatter = HtmlFormatter(style="friendly")

    def format_heading(self, level: int, content: str, **kwargs) -> str:
        """Format a heading with semantic HTML and CSS classes."""
        tag = f"h{min(level, 6)}"
        css_class = f"heading-{level}"
        return f'<{tag} class="{css_class}">{content}</{tag}>'

    def format_paragraph(self, content: str, **kwargs) -> str:
        """Format a paragraph."""
        return f'<p class="paragraph">{content}</p>'

    def format_code_block(self, code: str, language: Optional[str] = None, **kwargs) -> str:
        """Format a code block with syntax highlighting support."""
        if self.use_syntax_highlighting and language:
            lexer = get_lexer_by_name(language)
            highlighted_code = highlight(code, lexer, self.pygments_formatter)
            # Ensure the <pre> has both 'highlight' and 'code-block' classes
            highlighted_code = highlighted_code.replace(
                '<div class="highlight"><pre>', '<pre class="highlight code-block">'
            )
            highlighted_code = highlighted_code.replace("</pre></div>", "</pre>")
            return highlighted_code
        else:
            # Fallback to plain code block
            language_class = f" language-{language}" if language else ""
            import html

            escaped_code = html.escape(code)
            return f'<pre class="code-block{language_class}"><code>{escaped_code}</code></pre>'

    def format_inline_code(self, code: str, **kwargs) -> str:
        """Format inline code."""
        escaped_code = code.replace("<", "&lt;").replace(">", "&gt;")
        return f'<code class="inline-code">{escaped_code}</code>'

    def format_link(self, text: str, url: str, **kwargs) -> str:
        """Format a link."""
        return f'<a href="{url}" class="link">{text}</a>'

    def format_image(self, alt: str, src: str, title: Optional[str] = None, **kwargs) -> str:
        """Format an image."""
        title_attr = f' title="{title}"' if title else ""
        return f'<img src="{src}" alt="{alt}" class="image"{title_attr}>'

    def format_list(self, items: List[str], ordered: bool = False, **kwargs) -> str:
        """Format a list."""
        tag = "ol" if ordered else "ul"
        css_class = "ordered-list" if ordered else "unordered-list"
        items_html = "".join(f'<li class="list-item">{item}</li>' for item in items)
        return f'<{tag} class="{css_class}">{items_html}</{tag}>'

    def format_blockquote(self, content: str, **kwargs) -> str:
        """Format a blockquote."""
        return f'<blockquote class="blockquote">{content}</blockquote>'

    def format_emphasis(self, content: str, strong: bool = False, **kwargs) -> str:
        """Format emphasis (italic/bold)."""
        tag = "strong" if strong else "em"
        css_class = "strong" if strong else "emphasis"
        return f'<{tag} class="{css_class}">{content}</{tag}>'

    def get_css(self) -> str:
        """Get CSS for the HTML."""
        if self.use_syntax_highlighting:
            return self.pygments_formatter.get_style_defs(".highlight")
        return ""


class MarkdownRenderer:
    """Main markdown renderer with extensible formatting."""

    def __init__(self, formatter: Optional[HTMLFormatter] = None, cache_manager: Optional[CacheManager] = None):
        """
        Initialize the markdown renderer.

        Args:
            formatter: HTML formatter to use (defaults to DefaultHTMLFormatter)
            cache_manager: Cache manager to use (defaults to new CacheManager)
        """
        self.formatter = formatter or DefaultHTMLFormatter()
        self.cache_manager = cache_manager or CacheManager()

        # Compile regex patterns for markdown parsing
        self.patterns = {
            "heading": re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE),
            "code_block": re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL),
            "inline_code": re.compile(r"`([^`]+)`"),
            "link": re.compile(r"\[([^\]]+)\]\(([^)]+)\)"),
            "image": re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"),
            "list_item": re.compile(r"^(\s*)([\-\*\+]|\d+\.)\s+(.+)$", re.MULTILINE),
            "blockquote": re.compile(r"^>\s+(.+)$", re.MULTILINE),
            "emphasis": re.compile(r"(\*\*([^*]+)\*\*)|(\*([^*]+)\*)"),
        }

    def render_file(self, md_path: Path, output_path: Optional[Path] = None, force: bool = False) -> Path:
        """
        Render a markdown file to HTML.

        Args:
            md_path: Path to the markdown file
            output_path: Path for output HTML file (auto-generated if None)
            force: Force regeneration even if cache is valid

        Returns:
            Path to the generated HTML file
        """
        if output_path is None:
            output_path = md_path.with_suffix(".html")

        # Check cache first (unless force is True)
        if not force and not self.cache_manager.is_stale(md_path):
            cached_path = self.cache_manager.get_cached_output_path(md_path)
            if cached_path:
                return cached_path

        # Process frontmatter and content
        frontmatter, content = process_file(md_path)

        # Render markdown to HTML
        html_content = self._render_markdown(content)

        # Apply template with frontmatter
        final_html = self._apply_template(html_content, frontmatter)

        # Write output file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)

        # Update cache
        content_hash = self.cache_manager._calculate_content_hash(final_html)
        self.cache_manager.update_cache(md_path, output_path, content_hash, frontmatter)

        return output_path

    def _render_markdown(self, content: str) -> str:
        """
        Render markdown content to HTML.

        Args:
            content: Markdown content

        Returns:
            HTML content
        """
        # Step 1: Extract and replace code blocks with placeholders
        code_blocks = {}
        code_block_counter = 0

        def extract_code_block(match):
            nonlocal code_block_counter
            language = match.group(1)
            code = match.group(2)
            placeholder = f"{{{{CODEBLOCK_{code_block_counter}}}}}"
            # Preserve all whitespace in code
            code_html = self.formatter.format_code_block(code, language)
            code_blocks[placeholder] = code_html
            code_block_counter += 1
            return placeholder

        content = self.patterns["code_block"].sub(extract_code_block, content)

        # Step 2: Process other markdown elements
        content = self._process_headings(content)
        content = self._process_emphasis(content)
        content = self._process_images(content)
        content = self._process_links(content)
        content = self._process_lists(content)
        content = self._process_blockquotes(content)
        content = self._process_inline_code(content)
        content = self._process_paragraphs(content)

        # Step 3: Restore code blocks
        for placeholder, code_html in code_blocks.items():
            content = content.replace(placeholder, code_html)

        return content

    def _process_code_blocks(self, content: str) -> str:
        """Deprecated: code blocks are now handled in _render_markdown with placeholders."""
        return content

    def _process_headings(self, content: str) -> str:
        """Process headings."""

        def replace_heading(match):
            level = len(match.group(1))
            text = match.group(2)
            return self.formatter.format_heading(level, text)

        return self.patterns["heading"].sub(replace_heading, content)

    def _process_emphasis(self, content: str) -> str:
        """Process emphasis (bold/italic)."""

        def replace_emphasis(match):
            if match.group(1):  # Bold
                text = match.group(2)
                return self.formatter.format_emphasis(text, strong=True)
            else:  # Italic
                text = match.group(4)
                return self.formatter.format_emphasis(text, strong=False)

        return self.patterns["emphasis"].sub(replace_emphasis, content)

    def _process_images(self, content: str) -> str:
        """Process images."""

        def replace_image(match):
            alt = match.group(1)
            src = match.group(2)
            return self.formatter.format_image(alt, src)

        return self.patterns["image"].sub(replace_image, content)

    def _process_links(self, content: str) -> str:
        """Process links."""

        def replace_link(match):
            text = match.group(1)
            url = match.group(2)
            return self.formatter.format_link(text, url)

        return self.patterns["link"].sub(replace_link, content)

    def _process_lists(self, content: str) -> str:
        """Process lists."""
        lines = content.split("\n")
        result = []
        i = 0

        while i < len(lines):
            line = lines[i]
            list_match = self.patterns["list_item"].match(line)

            if list_match:
                items = []
                indent = len(list_match.group(1))
                marker = list_match.group(2)
                item_content = list_match.group(3)

                # Collect all items at this indent level
                while i < len(lines):
                    line = lines[i]
                    item_match = self.patterns["list_item"].match(line)

                    if not item_match or len(item_match.group(1)) != indent:
                        break

                    items.append(item_match.group(3))
                    i += 1

                # Format the list
                ordered = marker.endswith(".")
                list_html = self.formatter.format_list(items, ordered)
                result.append(list_html)
            else:
                result.append(line)
                i += 1

        return "\n".join(result)

    def _process_blockquotes(self, content: str) -> str:
        """Process blockquotes."""

        def replace_blockquote(match):
            quote_text = match.group(1)
            return self.formatter.format_blockquote(quote_text)

        return self.patterns["blockquote"].sub(replace_blockquote, content)

    def _process_inline_code(self, content: str) -> str:
        """Process inline code."""

        def replace_inline_code(match):
            code = match.group(1)
            return self.formatter.format_inline_code(code)

        return self.patterns["inline_code"].sub(replace_inline_code, content)

    def _process_paragraphs(self, content: str) -> str:
        """Process paragraphs (wrap remaining text blocks)."""
        lines = content.split("\n")
        result = []
        current_paragraph: list[str] = []

        for line in lines:
            line = line.strip()

            # Skip empty lines and already processed elements
            if not line or line.startswith("<"):
                if current_paragraph:
                    paragraph_text = " ".join(current_paragraph)
                    result.append(self.formatter.format_paragraph(paragraph_text))
                    current_paragraph = []
                if line.startswith("<"):
                    result.append(line)
            else:
                current_paragraph.append(line)

        # Handle any remaining paragraph
        if current_paragraph:
            paragraph_text = " ".join(current_paragraph)
            result.append(self.formatter.format_paragraph(paragraph_text))

        # Clean up: remove any paragraph tags that wrap code blocks
        content = "\n".join(result)
        content = re.sub(r'<p class="paragraph"><pre', "<pre", content)
        content = re.sub(r"</pre></p>", "</pre>", content)

        # Clean up: remove any paragraph tags that wrap images
        content = re.sub(r'<p class="paragraph"><img', "<img", content)
        content = re.sub(r"</img></p>", "</img>", content)

        return content

    def _apply_template(self, content: str, frontmatter: dict[str, Any]) -> str:
        """
        Apply HTML template with frontmatter.

        Args:
            content: HTML content
            frontmatter: Frontmatter data

        Returns:
            Complete HTML document
        """
        title = frontmatter.get("title", "Untitled")
        author = frontmatter.get("author", "Unknown")
        date = frontmatter.get("date", "")
        description = frontmatter.get("description", "")

        # Get Pygments CSS if available
        pygments_css = ""
        if hasattr(self.formatter, "get_css"):
            pygments_css = self.formatter.get_css()

        # Basic HTML template
        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="author" content="{author}">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            color: #333;
        }}
        .heading-1 {{ font-size: 2.5rem; margin-top: 2rem; margin-bottom: 1rem; }}
        .heading-2 {{ font-size: 2rem; margin-top: 1.5rem; margin-bottom: 0.75rem; }}
        .heading-3 {{ font-size: 1.5rem; margin-top: 1.25rem; margin-bottom: 0.5rem; }}
        .heading-4, .heading-5, .heading-6 {{ font-size: 1.25rem; margin-top: 1rem; margin-bottom: 0.5rem; }}
        .paragraph {{ margin-bottom: 1rem; }}
        .code-block {{ 
            background: #f5f5f5; 
            padding: 1rem; 
            border-radius: 4px; 
            overflow-x: auto;
            margin: 1rem 0;
        }}
        .inline-code {{ 
            background: #f5f5f5; 
            padding: 0.2rem 0.4rem; 
            border-radius: 3px; 
            font-family: 'Monaco', 'Menlo', monospace;
        }}
        .link {{ color: #0066cc; text-decoration: none; }}
        .link:hover {{ text-decoration: underline; }}
        .image {{ max-width: 100%; height: auto; margin: 1rem 0; }}
        .unordered-list, .ordered-list {{ margin: 1rem 0; padding-left: 2rem; }}
        .list-item {{ margin-bottom: 0.5rem; }}
        .blockquote {{ 
            border-left: 4px solid #ddd; 
            padding-left: 1rem; 
            margin: 1rem 0; 
            font-style: italic;
            color: #666;
        }}
        .strong {{ font-weight: bold; }}
        .emphasis {{ font-style: italic; }}
        header {{ 
            border-bottom: 2px solid #eee; 
            padding-bottom: 1rem; 
            margin-bottom: 2rem; 
        }}
        .metadata {{ 
            color: #666; 
            font-size: 0.9rem; 
            margin-bottom: 0.5rem; 
        }}
        {pygments_css}
    </style>
</head>
<body>
    <header>
        <h1 class="heading-1">{title}</h1>
        <div class="metadata">
            {f'<div>Author: {author}</div>' if author else ''}
            {f'<div>Date: {date}</div>' if date else ''}
        </div>
    </header>
    
    <main>
        {content}
    </main>
</body>
</html>"""

        return template
