---
name: convert-plaintext-to-md
description: 'Convert plain text or PDF-extracted documents to properly formatted markdown. Use when converting controller manuals, reference guides, or any unformatted documentation into structured markdown for use as skill references or workshop materials.'
---

# Convert Plaintext to Markdown

Convert text-based documentation files (PDF extracts, plain text manuals, raw dumps) to properly formatted markdown.

## When to Use This Skill

- Converting a robot controller manual (PDF → text → markdown)
- Cleaning up raw text exports for use as skill reference material
- Formatting legacy documentation for the `docs/` folder
- Converting tree dump output into a readable reference

## Conversion Methods

1. **From explicit instructions**: Follow specific formatting rules provided with the request
2. **From reference file**: Use an already-converted markdown file as a template for formatting similar documents
3. **Auto-detect**: Analyze the text structure and apply appropriate markdown formatting

## Workflow

1. If a corresponding `.md` file already exists, treat it as the working copy
2. If one does not exist, create `<filename>.md` in the same directory
3. Apply markdown best practices:
   - Add headers based on content structure
   - Format code blocks with language hints
   - Convert tables to markdown tables
   - Preserve all technical content accurately
   - Add proper list formatting

## Guidelines for Controller Manuals

When converting robot language manuals:

- Use `## Command Name` for each command/instruction
- Put syntax in fenced code blocks with language hint (e.g., ` ```as ` for Kawasaki AS)
- Format parameter tables as markdown tables
- Preserve example code exactly as-is (only add formatting)
- Add a table of contents for documents over 100 lines
- Use `> [!NOTE]` callouts for important warnings

## Platform Target

Default: **GitHub-flavored markdown (GFM)**
- Tables, task lists, strikethrough, and alerts supported
- Fenced code blocks with language identifiers

## Quality Checklist

- [ ] All headers properly nested (no skipped levels)
- [ ] Code blocks have language hints where identifiable
- [ ] Tables are properly aligned
- [ ] No content lost from original
- [ ] Links are properly formatted
- [ ] Document is self-contained and readable
