# HTML Inclusion Examples

This document demonstrates how to include HTML content directly in your markdown documents.

## Basic HTML Inclusion

You can include HTML files using the markdown link syntax:

[Sample Interactive Chart](sample_chart.html)

The HTML content above shows an interactive Plotly chart that maintains its functionality when embedded.

## How It Works

- Use standard markdown link syntax: `[Description](file.html)`
- The HTML file is resolved relative to the markdown file location
- By default, content between `<body>` tags is extracted
- The HTML is rendered directly without escaping
- Interactive elements like JavaScript charts work normally

## Use Cases

HTML inclusion is particularly useful for:

- **Interactive visualizations** (Plotly, D3.js, etc.)
- **Complex layouts** that need custom styling
- **Embedded widgets** or third-party components
- **Rich content** that goes beyond standard markdown

## Technical Details

The HTML inclusion feature:
- Supports relative path resolution
- Extracts body content by default
- Preserves JavaScript and CSS functionality
- Applies minimal styling (no borders, padding, or background)
- Enables scrolling for overflow content