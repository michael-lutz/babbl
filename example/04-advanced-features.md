---
title: "Advanced Features"
author: "Test User"
date: "2025-01-02"
description: "Testing advanced features like TOC, CSS, and metadata"
tags: ["advanced", "features", "testing"]
category: "documentation"
---

# Advanced Features

This document demonstrates advanced features available in Babbl.

## Table of Contents

When using the `--toc` flag, this document will generate a table of contents for all H1 headings.

## Custom CSS

You can provide custom CSS files using the `--css` flag to override the default styling.

## Metadata Support

The frontmatter supports various metadata fields:

- **title**: Document title
- **author**: Document author  
- **date**: Publication date
- **description**: Document description
- **tags**: Array of tags
- **category**: Document category

## Syntax Highlighting

Code blocks support syntax highlighting for various languages:

```python
import os
from pathlib import Path

def process_files(directory: Path) -> list[str]:
    """Process all files in directory."""
    results = []
    for file in directory.glob("*.txt"):
        with open(file) as f:
            results.append(f.read())
    return results
```

```javascript
function processData(data) {
    return data
        .filter(item => item.active)
        .map(item => ({
            id: item.id,
            name: item.name.toUpperCase()
        }));
}
```

```bash
#!/bin/bash
echo "Processing files..."
for file in *.md; do
    echo "Converting $file"
    babbl render "$file"
done
```

## HTML Integration

You can embed custom HTML for advanced styling:

<div class="alert alert-info">
    <strong>Note:</strong> This is a custom HTML block with Bootstrap-like styling.
</div>

<details>
    <summary>Click to expand</summary>
    <p>This is collapsible content using HTML5 details element.</p>
</details>

## Code References with Context

Reference code with additional context:

@code-ref babbl/cli.py main

The main CLI function handles command registration and execution.

@code-ref babbl/renderer.py render_heading

The heading renderer creates anchor links for navigation.

## Mixed Content

You can mix all features together:

| Feature | Example | Code Reference |
|---------|---------|----------------|
| Tables | ✅ | @code-ref babbl/elements.py Table |
| Code Refs | ✅ | @code-ref babbl/code_ref.py CodeReferenceProcessor |
| Syntax Highlighting | ✅ | @code-ref babbl/renderer.py render_fenced_code |

## Long Content Test

This section tests how the renderer handles longer content with various elements mixed together.

### Subsection 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

```python
# This is a longer code block
def complex_function():
    """A more complex function for testing."""
    data = []
    for i in range(100):
        if i % 2 == 0:
            data.append(i * 2)
        else:
            data.append(i + 1)
    return sum(data)
```

### Subsection 2

Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

| Test | Data | Result |
|------|------|--------|
| Case 1 | Sample data | ✅ Pass |
| Case 2 | More data | ✅ Pass |
| Case 3 | Even more data | ✅ Pass |

### Subsection 3

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

> This is a blockquote with some important information that should be highlighted.

@code-ref babbl/parser.py BabblParser

The parser class handles all the custom elements and extensions. 