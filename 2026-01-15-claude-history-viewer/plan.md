# Plan: Claude Code History Viewer

## Goal

Browse Claude Code conversation history from `~/.claude/` via CLI and web UI.

## Phase 1: CLI (done)

Simple Python CLI with argparse, zero external deps.

```bash
uv run python main.py projects           # list all projects
uv run python main.py ls llm-tasks       # list sessions (partial match)
uv run python main.py show 00746d3b      # view conversation
uv run python main.py show 00746d3b -t   # include thinking
uv run python main.py show 00746d3b -T   # include tool calls
uv run python main.py search "keyword"   # search all history
```

## Phase 2: Web UI (done)

Flask + vanilla HTML/CSS/JS.

### Routes

| Route               | Description               |
| ------------------- | ------------------------- |
| `/`                 | List projects             |
| `/project/<path>`   | List sessions for project |
| `/session/<id>`     | View conversation         |
| `/search?q=<query>` | Search results            |

### Features

- Markdown rendering (marked.js via CDN)
- Toggle thinking blocks (collapsed by default)
- Toggle tool calls (collapsible `<details>`)
- Search across history.jsonl

### Files Created

- `web.py` - Flask app
- `templates/base.html` - layout with nav, search
- `templates/projects.html` - project list
- `templates/sessions.html` - session list
- `templates/session.html` - conversation with markdown
- `templates/search.html` - search results
- `static/style.css` - minimal styling

## Follow-up

See `notes/prd.md` for bugs and future improvements.

## Data Structure Reference

See `notes/data-structure.md` for JSONL format details.

## Run

```bash
uv run python web.py   # starts on http://localhost:5000
```
