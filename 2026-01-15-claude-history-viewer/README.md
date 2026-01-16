# Claude Code History Viewer

CLI tool to browse and pretty-print Claude Code conversation history from `~/.claude/`.

## Why

Claude Code's built-in history browser (`/resume`) works but can be clunky for:

- Searching across all sessions
- Exporting conversations
- Quick terminal-based browsing

## Data Structure

```
~/.claude/
  history.jsonl              # Index of all prompts (metadata)
  projects/<path-encoded>/   # Per-project sessions
    <session-uuid>.jsonl     # Full conversation transcript
```

Each session JSONL contains messages with:

- `type`: "user" | "assistant" | "summary"
- `message.content`: text or array with thinking/text blocks
- `timestamp`, `uuid`, `parentUuid`
