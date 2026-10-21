# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-10-21

### ✨ Added

#### Foundation — one contract for every node

* `Markdown` — the abstract base of every node; a node implements one method,
  `to_lines()`, and gets `to_text()`, `str()`, `repr()` and the `+` operator from it
* `InlineMarkdown` — the shortcut base for nodes that live inside a line; a node writes
  `to_inline()` and gets the rest
* `NodeLevel` — `INLINE` or `BLOCK`, the one tag the operators and the containers decide by;
  `Footnote` and `Html` carry it as a property because one class can stand on either level
* `+` composition — inline with inline gives an `InlineJoin`, anything with a block gives a
  `Document`; a string next to an inline node becomes escaped `Text`, next to a block a `Paragraph`

#### Inline — nodes inside a line

* `Text` — plain text with every character that Markdown could read as formatting escaped,
  including the marks that matter only at the start of a line; `escape=False` is the explicit
  escape hatch
* `Emphasis` — emphasis, strong, both and strike-through in one node (`EmphasisKind`,
  `EmphasisMarker`); whitespace at the edges moves outside the markers
* `InlineCode` — a code span whose delimiter and padding are chosen to fit any content
* `Link` — six forms (inline, reference, collapsed, shortcut, autolink, bare URL) times
  link or image, in one node (`LinkKind`); destinations and titles are written in the form that
  cannot end early
* `Entity` — an HTML entity by name or by code point; the name is checked against the HTML5 list
* `Math` — an inline or display formula
* `Reference` — a mention, a team, an issue, a repository issue, a commit and an emoji
  (`ReferenceKind`); the shape of the value is checked and the error says what a valid one looks like
* `LineBreak` — a hard break in three styles (`LineBreakStyle`)
* `InlineJoin` — several inline nodes in a row; always flat

#### Blocks — nodes that are lines of their own

* `Paragraph` — lines of inline content, with an optional hard-break style; a line that would
  start a block is escaped
* `Heading` — levels 1–6 in three styles (`HeadingStyle`: ATX, closed ATX, setext); a trailing
  `#` is escaped
* `CodeBlock` — fenced (backtick or tilde, `FenceChar`) or indented; the fence grows to fit the
  code it holds
* `ThematicBreak` — a horizontal rule (`BreakChar`)
* `BlankLine` — explicit empty lines that replace the separator instead of adding to it
* `LinkDefinition` — `[label]: destination "title"` with a normalized label
* `Footnote` — the marker or the note itself (`FootnoteRole`)
* `Frontmatter` — a YAML header written by a small, strict writer; an unsupported value is a
  `ConversionError` card where the data is passed
* `Html` — a block, an inline tag or a comment (`HtmlMode`) with validated tag and attribute
  names and escaped attribute values

#### Containers — nodes that hold other blocks

* `Document` — blocks separated by a chosen number of blank lines, with an optional final newline;
  documents never nest
* `Quote` — a block quote or a GitHub alert (`AlertKind`)
* `List` and `ListItem` — bullet and ordered lists in one node (`ListMarker`), tight or loose,
  with checkboxes and indentation that follows the marker's width
* `Table` — a GFM table with per-column alignment (`TableAlign`); rows of the wrong width are an
  error, not a silently padded row
* Nesting is prefixing: all containers are built on `separate_blocks` and `prefix_lines`

#### Output

* `MarkdownText` — the finished text of a node, rendered once: `text`, `lines`, `str()`,
  iteration, `len()` and `to_file()`
* `to_file(source, path, *, overwrite=True, **write_options)` — one call from a string, a node
  or a `MarkdownText` to a file, written through `simplibs-file` (atomic, UTF-8, `"\n"` line endings)

#### Presets — `simplibs.markdown.presets`

* Alerts: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`
* Code: `MERMAID`, `GEOJSON`, `TOPOJSON`, `STL`, `MATH_BLOCK`
* Emphasis: `BOLD`, `ITALIC`, `BOLD_ITALIC`, `STRIKETHROUGH`
* Headings: `H1` – `H6`
* HTML: `DETAILS`, `SUP`, `SUB`, `MARK`, `KBD`, `COMMENT`, `ANCHOR`
* Links: `IMAGE`, `AUTOLINK`, `BARE_URL`
* Lists: `BULLET_LIST`, `NUMBERED_LIST`, `TASK_ITEM`, `DONE_ITEM`
* References: `MENTION`, `ISSUE_REF`, `COMMIT_REF`, `EMOJI`, `COLOR_CHIP`
* Spacing: `EMPTY_LINE`, `RULE`, `HARD_BREAK`
* A preset only calls a node; every check and every error card comes from the node

#### Safe by construction

* Strings are content, never Markdown: everything passed as a string is escaped
* Structure is checked when a node is built — a heading inside bold text, a table inside a link,
  a setext heading of level 3, a list marker that does not fit the kind of list, a wrong row
  width — and every mistake is a `ParamError` card with a stable error name
* Every error name is prefixed `MARKDOWN_` and documented next to the node that raises it

#### Package Layout

* `simplibs.markdown` exports the nodes, the base classes, the enums, the output layer,
  and all presets directly for convenience; presets are also available in `simplibs.markdown.presets`
* Layers, each importing only from those before it:
  `_common` ← `base_class` ← `inline` ← `blocks` ← `containers` ← `output` ← `presets`

#### Documentation

* Main `README.md` with quick start, package structure and an overview of every node
* Detailed reference for each part under `docs/`: base classes, inline nodes, blocks, containers,
  output and presets — each node documented with parameters, raised errors, examples and the
  logic behind it

#### Quality Assurance

* Comprehensive test suite of 5,551 tests mirroring the source layout, covering nodes,
  helpers, composition, and structured error diagnostics
* Round-trip parser integration tests via `markdown-it-py` verifying clean Markdown generation
  for paragraphs, headings, code fences, lists, tables, and complex documents

#### Dependencies

* `simplibs-exception` — structured exceptions for every diagnostic (`ParamError`,
  `ConversionError`)
* `simplibs-file` — the atomic file write behind `MarkdownText.to_file` and `to_file`; the only
  place in the library that touches the disk

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality (not used yet in this
  project)
* 🗑️ **Removed** — removed functionality (not used yet in this project)
