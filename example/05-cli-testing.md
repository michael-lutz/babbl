---
title: "CLI Testing"
author: "Test User"
date: "2025-01-02"
description: "Testing CLI functionality and edge cases"
---

# CLI Testing

This document tests various CLI scenarios and edge cases.

## Basic Rendering

This document should render correctly with the basic `babbl render` command.

## File Paths

Testing various file path scenarios:

- Relative paths: `babbl render example/05-cli-testing.md`
- Absolute paths: `babbl render /full/path/to/file.md`
- Output specification: `babbl render input.md -o output.html`

## CSS Customization

Test custom CSS with: `babbl render input.md --css custom.css`

## Table of Contents

Test TOC generation with: `babbl render input.md --toc`

## Code Reference Base Path

Test code references with custom base path: `babbl render input.md --base-path /path/to/project`

## Batch Processing

Test batch processing with: `babbl build example/ --pattern "*.md"`

## Recursive Processing

Test recursive processing with: `babbl build example/ --recursive`

## Error Handling

This document tests various error scenarios:

### Invalid Code References

@code-ref nonexistent/file.py function

### Invalid Line Numbers

@code-ref babbl/cli.py line 999

### Invalid Line Ranges

@code-ref babbl/cli.py lines 999-1000

## Edge Cases

### Empty Code Blocks

```


```

### Tables with Irregular Data

| Col1 | Col2 | Col3 |
|------|------|------|
| Data | | More Data |
| | Missing | |
| | | |

### Mixed Content Types

This paragraph contains **bold**, *italic*, `code`, and [links](https://example.com).

> Blockquote with **formatting** and `code`.

- List with **bold** items
- List with *italic* items  
- List with `code` items

## Performance Testing

This section contains a lot of content to test rendering performance:

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.

Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.

Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?

## Code References in Lists

- Function: @code-ref babbl/cli.py render
- Class: @code-ref babbl/renderer.py HTMLRenderer
- Method: @code-ref babbl/elements.py parse_table_from_text

## Tables with Code References

| Component | File | Reference |
|-----------|------|-----------|
| Parser | babbl/parser.py | @code-ref babbl/parser.py BabblParser |
| Renderer | babbl/renderer.py | @code-ref babbl/renderer.py HTMLRenderer |
| CLI | babbl/cli.py | @code-ref babbl/cli.py main | 