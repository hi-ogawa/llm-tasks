# .dev-notes Convention

A personal convention for local-only documentation in any codebase. Globally gitignored by personal [dotfiles/.gitignore-global](https://github.com/hi-ogawa/dotfiles/blob/main/.gitignore-global), so it works across all repos without polluting them.

## Purpose

Keep working notes, investigations, and references alongside code without committing them:

- PR reviews and code analysis
- Bug investigation notes
- Architecture explorations
- Scratch files and experiments

## Directory Structure

```
.dev-notes/
  dist/           # Escape hatch from linting/formatting
    <topic>.md
  <topic>.md      # Topic-specific notes
```

### The `dist/` Trick

Many repos have aggressive linting/formatting on `**/*.md`. Nesting under `dist/` often escapes these rules since build outputs are typically excluded. Adjust based on repo's tooling:

- `.dev-notes/dist/*.md` - if repo lints markdown
- `.dev-notes/*.md` - if no lint rules apply
- Check `.eslintignore`, `.prettierignore`, etc.

## Clickable Source Links

Use relative markdown links with line anchors for navigation:

```markdown
**Location:** [packages/runner/src/suite.ts#L918](../../packages/runner/src/suite.ts#L918)
```

- Path is relative from the markdown file to the source
- Single line `#L123` works in VS Code
- Ranges `#L123-L456` break VS Code jump (works on GitHub though)
- Ctrl+Click in VS Code markdown preview to jump

From `.dev-notes/dist/*.md`, use `../../` to reach repo root.

## Benefits

- **Local-only** - never pollutes the repo, no PR noise
- **Portable** - works in any repo with global gitignore
- **Navigable** - clickable links in VS Code
- **Persistent** - survives branch switches (untracked)
- **Searchable** - grep/ripgrep works on local notes
