---
kind: page

title: Elements Reference
description: A complete reference for Markdown and MDC elements available on vendor pages.
---

# My Awesome Vendor - Elements Reference

_Every element shown here renders inside the same `.vendor-content` scope, inheriting the brand styles defined on the index page._

## Headings

Headings `h1`–`h3` pick up the gradient defined in the `style` field of `index.md`. Use them to structure long pages:

```markdown
## Section Title
### Sub-section Title
```

Keep `h1` (`#`) for the page title only — the platform injects it automatically from the `title` frontmatter field when rendering the page header, so starting body content at `h2` (`##`) produces the best visual hierarchy.

---

## Text Formatting

| Syntax | Output |
| --- | --- |
| `**bold**` | **bold** |
| `_italic_` | _italic_ |
| `` `inline code` `` | `inline code` |
| `~~strikethrough~~` | ~~strikethrough~~ |
| `[link](url)` | [link](https://iximiuz.com) |

---

## Lists

Unordered lists use `-` or `*`:

- Item one
- Item two
  - Nested item
  - Another nested item
- Item three

Ordered lists:

1. First step
2. Second step
3. Third step

---

## Blockquotes

```markdown
> **Key insight:** Blockquotes are rendered with the brand accent color
> defined in the vendor `style` field.
```

> **Key insight:** Blockquotes are rendered with the brand accent color defined in the vendor `style` field.

---

## Code Blocks

Fenced code blocks support syntax highlighting. Specify the language after the opening fence:

````markdown
```yaml
key: value
nested:
  list:
    - item-a
    - item-b
```
````

Renders as:

```yaml
key: value
nested:
  list:
    - item-a
    - item-b
```

---

## Tables

Tables use standard GFM syntax:

```markdown
| Header A | Header B | Header C |
| --- | --- | --- |
| Cell 1A  | Cell 1B  | Cell 1C  |
| Cell 2A  | Cell 2B  | Cell 2C  |
```

The `style` field controls header background, cell padding, and hover state.

---

## Content Cards

The `::card` MDC component embeds a single piece of associated content. The content must be declared in the `tutorials`, `courses`, or `challenges` map in `index.md` frontmatter:

```
::card
---
:content: tutorials.my-tutorial-slug
---
::
```

The card renders exactly as it appears in the main catalog — title, description, tags, and progress state for the viewing user.

---

## Content Grids

The `::grid` component lays out multiple cards side-by-side:

```
::grid
---
items:
  - content: tutorials.slug-one
  - content: courses.slug-two
---
::
```

Items wrap onto new rows automatically. Each row maintains equal card height. Supported item types: `content` (tutorials, courses, skill paths), `challenge`.

---

## Navigation

Link between sub-pages using relative paths or absolute paths that include the vendor name:

```markdown
[← Back to overview](/v/uncloud)
[Styling Guide →](/v/uncloud/styling)
```

---

- [← Back to Overview](/v/uncloud) — return to the vendor index
- [Styling Guide →](/v/uncloud/styling) — CSS customization patterns
