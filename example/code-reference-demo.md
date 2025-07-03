---
title: "Code Reference Demo"
author: "Michael Lutz"
date: "2025-01-02"
description: "Demonstrating the new code reference feature in Babbl"
---

# Code Reference Demo

This document demonstrates the new code reference feature in Babbl, which allows you to reference specific code elements from Python files and automatically generate dropdowns with the referenced code.

## Function References

You can reference functions by name:

@code-ref babbl/renderer.py HTMLRenderer

This will show the entire HTMLRenderer class definition.

## Method References

You can also reference specific methods:

@code-ref babbl/renderer.py render_fenced_code

This shows the render_fenced_code method implementation.

## Line Number References

Reference specific lines:

@code-ref babbl/cli.py line 25

This shows line 25 from the CLI file.

## Line Range References

Reference a range of lines:

@code-ref babbl/elements.py lines 1-20

This shows the first 20 lines of the elements file.

## Class References

Reference entire classes:

@code-ref babbl/code_ref.py CodeReferenceProcessor

This shows the complete CodeReferenceProcessor class.

## Error Handling

If a reference is not found, you'll see an error message:

@code-ref babbl/renderer.py nonexistent_function

## Multiple References

You can include multiple references in the same document:

@code-ref babbl/parser.py BabblParser

@code-ref babbl/cli.py render

## Usage in Documentation

This feature is particularly useful for:

- **API Documentation**: Reference specific functions and methods
- **Code Reviews**: Point to specific lines or functions
- **Tutorials**: Show relevant code sections inline
- **Research Papers**: Include code examples from your codebase

## How It Works

The code reference system:

1. **Parses** the markdown for `@code-ref` directives
2. **Extracts** code from the specified file using AST parsing
3. **Generates** collapsible dropdowns with syntax highlighting
4. **Handles** various reference types (functions, classes, line numbers, ranges)

## Supported Reference Types

- **Function names**: `function_name`
- **Class names**: `ClassName`
- **Method names**: `method_name`
- **Single lines**: `line 42`
- **Line ranges**: `lines 10-20` or `lines 10:20`

## File Support

Currently supports Python files with automatic syntax highlighting. The system can be extended to support other languages by adding appropriate lexers to the language mapping. 