# Babbl Testing Suite

This directory contains a comprehensive testing suite for Babbl that covers all library features.

## Test Files

### 01-basic-markdown.md
Tests all standard markdown features:
- Headings (H1-H6)
- Text formatting (bold, italic, inline code)
- Links and images
- Lists (ordered and unordered)
- Blockquotes
- Code blocks with syntax highlighting
- Horizontal rules
- HTML support

### 02-tables.md
Tests table functionality:
- Basic tables
- Table alignment (left, center, right)
- Complex tables with mixed content
- Tables with long content
- Empty cells

### 03-code-references.md
Tests code reference functionality:
- Function references by name
- Class references
- Method references
- Line number references
- Line range references
- Error handling for invalid references
- Multiple references in one document

### 04-advanced-features.md
Tests advanced features:
- Table of contents generation
- Custom CSS support
- Metadata handling
- Syntax highlighting for multiple languages
- HTML integration
- Mixed content scenarios
- Long content performance

### 05-cli-testing.md
Tests CLI functionality and edge cases:
- File path handling
- CSS customization
- TOC generation
- Code reference base paths
- Batch processing
- Recursive processing
- Error handling
- Edge cases and performance

## Running the Tests

### Single File Testing
```bash
# Test basic markdown
babbl render example/01-basic-markdown.md

# Test with table of contents
babbl render example/04-advanced-features.md --toc

# Test with custom CSS
babbl render example/02-tables.md --css custom.css

# Test code references with base path
babbl render example/03-code-references.md --base-path .
```

### Batch Testing
```bash
# Process all test files
babbl build example/ --pattern "*.md"

# Process recursively (if you add subdirectories)
babbl build example/ --recursive

# Process with all features enabled
babbl build example/ --toc --base-path .
```

### Expected Output
Each test file should render to HTML with:
- Proper styling and layout
- Syntax highlighting for code blocks
- Functional code reference dropdowns
- Responsive tables
- Clean typography

## Feature Coverage

This testing suite covers:

✅ **Core Markdown**: All standard markdown syntax  
✅ **Tables**: Custom table implementation with alignment  
✅ **Code References**: AST-based code extraction  
✅ **Syntax Highlighting**: Pygments integration  
✅ **Metadata**: Frontmatter parsing  
✅ **CLI**: All command-line options  
✅ **CSS**: Custom styling support  
✅ **TOC**: Table of contents generation  
✅ **Error Handling**: Graceful failure modes  
✅ **Performance**: Large content handling  

## Adding New Tests

When adding new features to Babbl:

1. Add test cases to the appropriate existing file
2. Create a new numbered test file if needed
3. Update this README with the new test coverage
4. Ensure all CLI options are tested
5. Include both success and error scenarios 