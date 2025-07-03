---
title: "Code References"
author: "Test User"
date: "2025-01-02"
description: "Testing code reference functionality in Babbl"
---

# Code References

Babbl supports referencing code from Python files using the `@code-ref` directive.

## Function References

Reference a function by name:

```markdown
@code-ref babbl/cli.py render
```

@code-ref babbl/cli.py render

## Class References

Reference an entire class:

@code-ref babbl/renderer.py HTMLRenderer

## Method References

Reference a specific method:

@code-ref babbl/renderer.py render_fenced_code

## Line Number References

Reference a specific line:

@code-ref babbl/parser.py line 1

## Line Range References

Reference a range of lines:

@code-ref babbl/elements.py lines 1-20

## Error Handling

If a reference doesn't exist, you'll see an error:

@code-ref babbl/cli.py nonexistent_function

## Multiple References

You can include multiple references in the same document:

@code-ref babbl/code_ref.py CodeReferenceProcessor

@code-ref babbl/defaults.py line 1

## Usage Examples

Code references are useful for:

- **Documentation**: Reference specific functions and methods
- **Code Reviews**: Point to specific lines or functions  
- **Tutorials**: Show relevant code sections inline
- **Research**: Include code examples from your codebase

## Supported Reference Types

- **Function names**: `function_name`
- **Class names**: `ClassName` 
- **Method names**: `method_name`
- **Single lines**: `line 42`
- **Line ranges**: `lines 10-20` or `lines 10:20` 