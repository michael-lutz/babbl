---
title: "Code References"
author: "Test User"
date: "2025-01-02"
description: "Testing code reference functionality in Babbl"
---

# Code References

Babbl supports referencing code from Python files using markdown link syntax and simple hash references.

## Markdown Link Syntax

### Function References

Reference a function by name:

[Render function](../babbl/cli.py#render)

### Class References

Reference an entire class:

[HTML Renderer](../babbl/renderer.py#HTMLRenderer)

### Method References

Reference a specific method:

[Render fenced code](../babbl/renderer.py#render_fenced_code)

### Line Number References

Reference a specific line:

[Parser line 1](../babbl/parser.py#L1)

[Load file line 8](../babbl/load.py#L8)

### Line Range References

Reference a range of lines:

[Elements lines 1-20](../babbl/elements.py#L1-L20)

## Simple Hash References

For quick references without specifying the file path:

### Class References

#HTMLRenderer

#BabblParser

#CodeReferenceProcessor

### Function References

#extract_code

#render_code_reference

#load_file

## Error Handling

If a reference doesn't exist, you'll see an error:

[Nonexistent function](../babbl/cli.py#nonexistent_function)

## Multiple References

You can include multiple references in the same document:

[Code reference processor](../babbl/code_ref.py#CodeReferenceProcessor)

[Defaults line 1](../babbl/defaults.py#L1)

## Usage Examples

Code references are useful for:

- **Documentation**: Reference specific functions and methods
- **Code Reviews**: Point to specific lines or functions  
- **Tutorials**: Show relevant code sections inline
- **Research**: Include code examples from your codebase

## Supported Reference Types

- **Class names**: `ClassName`
- **Function names**: `function_name`
- **Method names**: `method_name`
- **Single lines**: `L25` or `line 25`
- **Line ranges**: `L10-L20`

## Syntax Examples

### Markdown Link Format
```markdown
[Description](../path/to/file.py#reference)
```

### Hash Reference Format
```markdown
#reference
```

Where `reference` can be:
- Class name: `HTMLRenderer`
- Function name: `render`
- Line number: `L25`
- Line range: `L10-L20`