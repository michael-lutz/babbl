# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation and Setup
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=babbl
```

### Code Quality
```bash
# Format code
black .

# Run linting
flake8 babbl/

# Type checking
mypy babbl/
```

### Building and Distribution
```bash
# Build package
python -m build

# Install locally
pip install .
```

## Architecture Overview

Babbl is a Python-based markdown-to-HTML converter designed for research blog posts. The architecture follows a modular design:

### Core Components

1. **Parser (`babbl/parser.py`)**: Custom Marko-based parser that extends standard markdown with:
   - Table support via custom `Table` element
   - Code reference support via `CodeReference` element

2. **Renderer (`babbl/renderer.py`)**: HTML renderer with:
   - `BaseRenderer` abstract class defining all required render methods
   - `HTMLRenderer` implementation with semantic CSS classes
   - Syntax highlighting via Pygments
   - Table of contents generation for h1/h2 headings
   - Code reference rendering with collapsible sections

3. **Custom Elements (`babbl/elements.py`)**: Extended markdown elements:
   - `Table`: Full markdown table parsing and rendering
   - `CodeReference`: File-based code inclusion via markdown links
   - Various table sub-elements (TableHead, TableBody, TableRow, etc.)

4. **Utilities (`babbl/util.py`)**: Handles code extraction and file operations:
   - Function/class extraction using AST parsing
   - Line number/range extraction
   - Support for multiple programming languages
   - Base path resolution for relative file paths
   - File I/O operations
   - YAML frontmatter parsing
   - Content processing

5. **CLI Interface (`babbl/cli.py`)**: Click-based command-line interface:
   - `babbl render` - Single file rendering
   - `babbl build` - Directory-based batch processing
   - Options for CSS, TOC, and code reference base paths

6. **Defaults (`babbl/defaults.py`)**: Contains default CSS styling

### Key Features

- **Frontmatter Support**: YAML frontmatter parsing with metadata extraction
- **Table Support**: Full markdown table parsing with responsive styling
- **Code References**: Include code snippets from files using markdown link syntax
- **Syntax Highlighting**: Pygments integration for code blocks
- **Table of Contents**: Auto-generated TOC for h1/h2 headings
- **Responsive Design**: Mobile-friendly HTML output
- **Custom CSS**: Support for external CSS files

### Technology Stack

- **Core**: Python 3.8+ with setuptools build system
- **Markdown**: Marko parser with custom extensions
- **CLI**: Click for command-line interface
- **Frontend**: Jinja2 for templating, Pygments for syntax highlighting
- **File Processing**: PyYAML for frontmatter, pathspec for file patterns
- **Development**: pytest, black, flake8, mypy for testing and quality

### File Structure

```
babbl/
├── __init__.py          # Package initialization and public API
├── cli.py               # Command-line interface
├── parser.py            # Custom Marko parser
├── renderer.py          # HTML renderer implementation
├── elements.py          # Custom markdown elements
├── util.py              # File I/O utilities and code reference processor
└── defaults.py          # Default CSS and configuration
```

## Development Workflow

1. **Adding New Features**: Follow the existing pattern of extending elements or renderer methods
2. **Testing**: Use the `example/` directory for testing CLI functionality
3. **Code Style**: Use black for formatting, follow existing patterns for imports and structure
4. **Type Safety**: Use type hints consistently, especially for public APIs

## Code Reference Usage

### Markdown Link Syntax
- `[Parser class](../babbl/parser.py#BabblParser)` - Extract class
- `[Render function](../babbl/cli.py#render)` - Extract function  
- `[Line 15](../babbl/load.py#L15)` - Extract single line
- `[Lines 10-20](../babbl/renderer.py#L10-L20)` - Extract line range

### Simple Hash References
- `#HTMLRenderer` - Extract class from any file in project
- `#extract_code` - Extract function from any file in project
- `#render_code_reference` - Extract function from any file in project

**Note**: File paths in markdown links are resolved relative to the markdown file's location, not the project root. Use `../` to go up directories as needed.