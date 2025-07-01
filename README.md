# The Library of Babbl

Turn markdown into beautiful research blog posts.

## Features

- **Custom Markdown Renderer**: Built from scratch with extensible HTML formatting
- **Frontmatter Support**: YAML frontmatter in markdown files or sidecar YAML files
- **Smart Caching**: MD5-based caching to avoid unnecessary regeneration
- **Beautiful Templates**: Clean, responsive HTML output with modern styling
- **CLI Interface**: Easy-to-use command-line tools
- **Extensible**: Custom formatters for different styling needs

## Installation

```bash
pip install babbl
```

## Quick Start

### Render a single markdown file:

```bash
babbl render example.md
```

### Build multiple files in a directory:

```bash
babbl build ./docs --output-dir ./public
```

### Show file information:

```bash
babbl info example.md
```

## Usage

### Python API

```python
from babbl import MarkdownRenderer
from pathlib import Path

# Initialize renderer
renderer = MarkdownRenderer()

# Render a markdown file
output_path = renderer.render_file(Path("example.md"))
print(f"Generated: {output_path}")
```

### Frontmatter Support

Babbl supports YAML frontmatter both inline and in sidecar files:

**Inline frontmatter:**
```markdown
---
title: "My Research Paper"
author: "Dr. Jane Smith"
date: "2024-01-15"
description: "A groundbreaking study"
---

# Content here...
```

**Sidecar YAML file (`example.yaml`):**
```yaml
title: "My Research Paper"
author: "Dr. Jane Smith"
date: "2024-01-15"
description: "A groundbreaking study"
```

### Custom Formatting

Create custom HTML formatters by extending the `HTMLFormatter` class:

```python
from babbl import HTMLFormatter, MarkdownRenderer

class CustomFormatter(HTMLFormatter):
    def format_heading(self, level: int, content: str, **kwargs) -> str:
        return f'<h{level} class="my-custom-heading">{content}</h{level}>'
    
    # Implement other methods...

# Use custom formatter
renderer = MarkdownRenderer(formatter=CustomFormatter())
```

## CLI Commands

### `babbl render <file>`
Render a single markdown file to HTML.

Options:
- `--output, -o`: Specify output file path
- `--cache-dir`: Custom cache directory
- `--force, -f`: Force regeneration (ignore cache)
- `--clear-cache`: Clear cache before processing

### `babbl build <directory>`
Build multiple markdown files in a directory.

Options:
- `--output-dir, -o`: Output directory
- `--pattern`: File pattern to match (default: `*.md`)
- `--recursive, -r`: Process subdirectories
- `--force, -f`: Force regeneration

### `babbl info <file>`
Show information about a markdown file including frontmatter.

### `babbl clear-cache`
Clear the cache.

## Supported Markdown Features

- **Headings**: `# ## ###` etc.
- **Code blocks**: ```python with syntax highlighting
- **Inline code**: `code`
- **Links**: `[text](url)`
- **Images**: `![alt](src)`
- **Lists**: Ordered and unordered
- **Blockquotes**: `> quote`
- **Emphasis**: **bold** and *italic*
- **Paragraphs**: Automatic wrapping

## Caching

Babbl uses MD5 hashing to cache generated files. Files are only regenerated when:
- The source markdown file has changed
- The cache is cleared
- The `--force` flag is used

## License

MIT License
