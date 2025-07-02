# The Library of Babbl

Turn markdown into beautiful research blog posts.

![Babbl](assets/babel_img.jpg)

## Features

- **Custom Markdown Renderer**: Built from scratch with extensible HTML formatting
- **Frontmatter Support**: YAML frontmatter in markdown files or sidecar YAML files
- **Beautiful Templates**: Clean, responsive HTML output with modern styling
- **Fully Customizable CSS**: Complete control over styling through CSS files
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

### Generate a default CSS file:

```bash
babbl init-css
```

### Render with custom CSS file:

```bash
babbl render example.md --css my-styles.css
```

## Usage

### Python API

```python
from babbl import HTMLRenderer
from pathlib import Path
from marko import Markdown

# Initialize renderer
markdown = Markdown(renderer=HTMLRenderer)

# Render a markdown file
with open("example.md", "r") as f:
    content = f.read()
html = markdown(content)
print(f"Generated HTML: {html}")
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
from babbl import HTMLFormatter, HTMLRenderer

class CustomFormatter(HTMLFormatter):
    def format_heading(self, level: int, content: str, **kwargs) -> str:
        return f'<h{level} class="my-custom-heading">{content}</h{level}>'
    
    # Implement other methods...

# Use custom formatter
renderer = HTMLRenderer(formatter=CustomFormatter())
```

### CSS Customization

Babbl provides complete control over styling through CSS files:

**Generate a default CSS file:**
```bash
babbl init-css my-styles.css
```

**Customize your styles:**
```css
/* my-styles.css */
body {
    font-family: "Georgia", serif;
    background-color: #f5f5f5;
    color: #333;
}

.heading-1 {
    color: #2c3e50;
    font-size: 2.5rem;
    border-bottom: 2px solid #3498db;
}

.code-block {
    background: #2c3e50;
    color: #ecf0f1;
    border-radius: 8px;
}
```

**Use your custom styles:**
```bash
babbl render example.md --css my-styles.css
```

The CSS system supports all standard CSS properties for:
- Body and section styling
- All heading levels (h1-h6)
- Paragraphs and text
- Code blocks and inline code
- Links and images
- Lists and blockquotes
- Emphasis (bold/italic)
- Responsive design
- Syntax highlighting

## CLI Commands

### `babbl render <file>`
Render a single markdown file to HTML.

Options:
- `--output, -o`: Specify output file path
- `--css`: Path to CSS file

### `babbl build <directory>`
Build multiple markdown files in a directory.

Options:
- `--output-dir, -o`: Output directory
- `--pattern`: File pattern to match (default: `*.md`)
- `--recursive, -r`: Process subdirectories
- `--css`: Path to CSS file

### `babbl init-css [file]`
Generate a default CSS file.

Options:
- `--force, -f`: Overwrite existing file

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

## License

MIT License
