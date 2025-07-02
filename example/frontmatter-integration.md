---
title: "Frontmatter Parsing"
author: "Michael Lutz"
date: "2025-07-02"
---

# Frontmatter Integration with Marko Parser

This document explains how to add YAML frontmatter support to the Marko parser system.

## Overview

The frontmatter integration provides three main approaches:

1. **FrontmatterParser**: A custom parser that extends Marko's Parser with frontmatter support
2. **FrontmatterExtractor**: A utility class for extracting frontmatter without full parsing
3. **Convenience functions**: Simple functions for common use cases

## Basic Usage

### Method 1: Parse with Frontmatter Support

```python
from babbl.frontmatter_parser import parse_with_frontmatter

content = """---
title: "My Document"
author: "John Doe"
date: "2024-01-15"
---

# My Document

This is the content.
"""

frontmatter, document = parse_with_frontmatter(content)
print(f"Title: {frontmatter['title']}")
print(f"Author: {frontmatter['author']}")
```

### Method 2: Extract Frontmatter Only

```python
from babbl.frontmatter_parser import extract_frontmatter_only

frontmatter, content_without_frontmatter = extract_frontmatter_only(content)
print(f"Frontmatter: {frontmatter}")
print(f"Content: {content_without_frontmatter}")
```

### Method 3: Use Parser Directly

```python
from babbl.frontmatter_parser import FrontmatterParser

parser = FrontmatterParser()
frontmatter, document = parser.parse_with_frontmatter(content)
```

## Integration with Existing Parser

To add frontmatter support to an existing Marko parser:

```python
from marko.parser import Parser
from babbl.frontmatter_parser import FrontmatterBlockElement

class MyCustomParser(Parser):
    def __init__(self):
        super().__init__()
        # Add frontmatter support
        self.add_element(FrontmatterBlockElement)
    
    def parse_with_frontmatter(self, text):
        document = super().parse(text)
        
        # Extract frontmatter
        frontmatter = None
        if document.children and isinstance(document.children[0], FrontmatterBlockElement):
            frontmatter = document.children[0].metadata
            document.children = document.children[1:]
        
        return frontmatter, document
```

## FrontmatterBlockElement

The `FrontmatterBlockElement` is a custom block element that:

- Has high priority (10) to parse before other elements
- Only matches at the beginning of the document (pos == 0)
- Looks for YAML content between `---` delimiters
- Parses YAML content into a metadata dictionary

### Customization

You can customize the frontmatter element:

```python
class CustomFrontmatterElement(FrontmatterBlockElement):
    priority = 15  # Higher priority
    
    @classmethod
    def match(cls, source):
        # Custom matching logic
        return super().match(source)
    
    @classmethod
    def parse(cls, source):
        # Custom parsing logic
        return super().parse(source)
```

## Error Handling

The frontmatter parser handles various error cases:

1. **Invalid YAML**: If YAML parsing fails, returns `None` for frontmatter
2. **Missing delimiters**: If no `---` delimiters found, treats as regular content
3. **Empty frontmatter**: If frontmatter is empty, returns empty dict `{}`

## Example with Renderer

```python
from babbl.frontmatter_parser import parse_with_frontmatter
from babbl.renderer import HTMLRenderer

# Parse content with frontmatter
frontmatter, document = parse_with_frontmatter(content)

# Render the document
renderer = HTMLRenderer()
html_content = renderer.render(document)

# Use frontmatter for template
title = frontmatter.get('title', 'Untitled')
author = frontmatter.get('author', 'Unknown')

final_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta name="author" content="{author}">
</head>
<body>
    {html_content}
</body>
</html>
"""
```

## Advanced Usage

### Custom Frontmatter Processing

```python
class AdvancedFrontmatterParser(FrontmatterParser):
    def parse_with_frontmatter(self, text):
        frontmatter, document = super().parse_with_frontmatter(text)
        
        # Process frontmatter
        if frontmatter:
            # Add computed fields
            frontmatter['word_count'] = len(text.split())
            frontmatter['has_code'] = '```' in text
            
            # Validate required fields
            required_fields = ['title', 'author']
            missing_fields = [field for field in required_fields if field not in frontmatter]
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
        
        return frontmatter, document
```

### Integration with Existing Systems

```python
# Integrate with existing frontmatter processing
from babbl.frontmatter import FrontmatterProcessor

class IntegratedParser(FrontmatterParser):
    def __init__(self):
        super().__init__()
        self.frontmatter_processor = FrontmatterProcessor()
    
    def parse_with_frontmatter(self, text):
        # Use existing frontmatter processor for sidecar files
        # and custom parser for inline frontmatter
        frontmatter, document = super().parse_with_frontmatter(text)
        
        # Additional processing can be added here
        return frontmatter, document
```

## Best Practices

1. **Always check for None**: Frontmatter may be `None` if not present
2. **Use .get() method**: Provides default values for missing keys
3. **Validate early**: Check required fields before processing
4. **Handle errors gracefully**: YAML parsing can fail
5. **Consider performance**: For large documents, use `extract_frontmatter_only` if you only need metadata

## Troubleshooting

### Common Issues

1. **Frontmatter not detected**: Ensure `---` delimiters are at the very beginning
2. **YAML parsing errors**: Check YAML syntax in frontmatter
3. **Parser conflicts**: Ensure frontmatter element has appropriate priority
4. **Content corruption**: Verify frontmatter is properly removed from content

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed parsing information
frontmatter, document = parse_with_frontmatter(content)
```

## Conclusion

The frontmatter integration provides a flexible way to add YAML frontmatter support to the Marko parser system. It maintains compatibility with existing code while adding powerful metadata extraction capabilities. 