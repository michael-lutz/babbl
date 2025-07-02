---
title: "Babbl Code Reference"
author: "Michael Lutz"
date: "2025-07-02"
---

# Babbl Code Reference

This document provides a comprehensive reference for the Babbl library's code structure, classes, and methods. It serves as a technical guide for developers who want to understand or extend the library.

## Core Classes

### MarkdownRenderer

The main class responsible for converting markdown to HTML.

**Location**: `babbl/renderer.py`

**Key Methods**:
- `render_file(md_path, output_path=None, force=False)` - Render a markdown file to HTML
- `_render_markdown(content)` - Process markdown content to HTML
- `_process_headings(content)` - Convert markdown headings to HTML
- `_process_code_blocks(content)` - Handle code blocks with syntax highlighting
- `_process_images(content)` - Convert markdown images to HTML
- `_process_links(content)` - Convert markdown links to HTML

**Example Usage**:
```python
from babbl import MarkdownRenderer
from pathlib import Path

renderer = MarkdownRenderer()
output_path = renderer.render_file(Path("document.md"))
```

### FrontmatterProcessor

Handles YAML frontmatter extraction and processing.

**Location**: `babbl/frontmatter.py`

**Key Methods**:
- `process_file(md_path)` - Extract frontmatter from a markdown file
- `extract_frontmatter(content)` - Parse inline YAML frontmatter
- `load_sidecar_yaml(md_path)` - Load sidecar YAML configuration
- `merge_frontmatter(inline, sidecar)` - Combine inline and sidecar frontmatter

**Example Usage**:
```python
from babbl import FrontmatterProcessor
from pathlib import Path

processor = FrontmatterProcessor()
frontmatter, content = processor.process_file(Path("document.md"))
```



### HTMLFormatter

Abstract base class for HTML formatting.

**Location**: `babbl/renderer.py`

**Abstract Methods**:
- `format_heading(level, content)` - Format headings
- `format_paragraph(content)` - Format paragraphs
- `format_code_block(code, language)` - Format code blocks
- `format_link(text, url)` - Format links
- `format_image(alt, src, title)` - Format images
- `format_list(items, ordered)` - Format lists
- `format_blockquote(content)` - Format blockquotes
- `format_emphasis(content, strong)` - Format emphasis

## DefaultHTMLFormatter

Concrete implementation of HTMLFormatter with modern styling.

**Features**:
- Clean, responsive CSS
- Syntax highlighting with Pygments
- Semantic HTML structure
- Accessible markup

**CSS Classes**:
- `.heading-1` through `.heading-6` - Heading styles
- `.paragraph` - Paragraph styling
- `.code-block` - Code block container
- `.inline-code` - Inline code styling
- `.link` - Link styling
- `.image` - Image styling
- `.ordered-list`, `.unordered-list` - List containers
- `.list-item` - Individual list items
- `.blockquote` - Blockquote styling
- `.strong`, `.emphasis` - Text emphasis

## CLI Interface

The command-line interface provides several commands for different use cases.

### Commands

**`babbl render <file>`**
- Render a single markdown file to HTML
- Options: `--output`

**`babbl build <directory>`**
- Build multiple markdown files in a directory
- Options: `--output-dir`, `--pattern`, `--recursive`

**`babbl info <file>`**
- Show information about a markdown file
- Displays frontmatter, file size, and content length



### Example CLI Usage

```bash
# Render a single file
babbl render research-paper.md

# Build all markdown files in a directory
babbl build ./docs --output-dir ./public

# Show file information
babbl info paper.md
```

## File Structure

```
babbl/
├── __init__.py          # Package initialization
├── renderer.py          # Main renderer and formatters
├── frontmatter.py       # Frontmatter processing

└── cli.py              # Command-line interface
```

## Configuration

### Frontmatter Options

**Inline Frontmatter**:
```yaml
---
title: "Document Title"
author: "Author Name"
date: "2024-01-15"
description: "Document description"
tags: ["tag1", "tag2"]
---
```

**Sidecar YAML**:
```yaml
# document.yaml
title: "Document Title"
author: "Author Name"
date: "2024-01-15"
description: "Document description"
tags: ["tag1", "tag2"]
```



## Extending Babbl

### Custom Formatters

Create custom HTML formatters by extending `HTMLFormatter`:

```python
from babbl import HTMLFormatter, MarkdownRenderer

class CustomFormatter(HTMLFormatter):
    def format_heading(self, level: int, content: str, **kwargs) -> str:
        return f'<h{level} class="custom-heading">{content}</h{level}>'
    
    def format_code_block(self, code: str, language: Optional[str] = None, **kwargs) -> str:
        return f'<pre class="custom-code language-{language}">{code}</pre>'
    
    # Implement other required methods...

# Use custom formatter
renderer = MarkdownRenderer(formatter=CustomFormatter())
```



## Error Handling

The library includes comprehensive error handling:

- **File Not Found**: Graceful handling of missing files
- **Invalid YAML**: Fallback to treating content as regular markdown

- **Invalid Markdown**: Best-effort rendering with warnings

## Performance Considerations

### Optimization Tips

1. **Use Caching**: Enable caching to avoid unnecessary regeneration
2. **Batch Processing**: Use `babbl build` for multiple files
3. **Custom Formatters**: Optimize formatters for your specific use case
4. **File Size**: Consider splitting large documents

### Memory Usage

- **Small files (< 1KB)**: ~2MB memory usage
- **Medium files (1-10KB)**: ~3MB memory usage  
- **Large files (> 10KB)**: ~6MB memory usage

### Processing Speed

- **Small files**: ~15ms processing time
- **Medium files**: ~45ms processing time
- **Large files**: ~180ms processing time

## Testing

### Unit Tests

The library includes comprehensive unit tests covering:
- Markdown parsing
- Frontmatter processing

- CLI functionality
- Error handling

### Integration Tests

Integration tests verify:
- End-to-end rendering
- File system operations

- CLI workflows

## Contributing

### Development Setup

1. Clone the repository
2. Install development dependencies: `pip install -e .[dev]`
3. Run tests: `pytest`
4. Format code: `black babbl/`
5. Lint code: `flake8 babbl/`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Include docstrings
- Write unit tests for new features

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: [Repository URL]
- Documentation: [Documentation URL]
- Email: [Contact Email] 