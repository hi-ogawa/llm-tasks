# Claude Code Data Structure

## File Locations

```
~/.claude/
  history.jsonl                    # Index: all prompts with metadata
  projects/<path-encoded>/         # Per-project directories
    <session-uuid>.jsonl           # Full conversation transcript
    <session-uuid>/                # Optional: session-specific data (plans, etc.)
```

## Message Types in Session JSONL

Each line is one JSON object.

| type                    | description                       |
| ----------------------- | --------------------------------- |
| `user`                  | User message or tool results      |
| `assistant`             | Assistant response                |
| `summary`               | Conversation summary (for resume) |
| `system`                | Metadata (turn_duration, etc.)    |
| `file-history-snapshot` | File backup snapshots             |

## User Message Structure

```json
{
  "type": "user",
  "message": {
    "role": "user",
    "content": "plain text string" // OR array of tool_result objects
  },
  "uuid": "...",
  "parentUuid": "...",
  "timestamp": "2026-01-15T10:14:50.233Z",
  "sessionId": "...",
  "cwd": "/path/to/project"
}
```

When `content` is array (tool results):

```json
{
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_xxx",
      "content": "result text"
    }
  ]
}
```

## Assistant Message Structure

```json
{
  "type": "assistant",
  "message": {
    "role": "assistant",
    "model": "claude-opus-4-5-20251101",
    "content": [...]  // Array of content blocks
  },
  "uuid": "...",
  "parentUuid": "...",
  "timestamp": "..."
}
```

Content block types:

- `thinking` - extended thinking (has `thinking` field)
- `text` - visible response (has `text` field)
- `tool_use` - tool invocation (has `name`, `input` fields)

## Conversation Threading

Messages link via `uuid` → `parentUuid` forming a tree (supports branching/editing).

## Quick Extraction

```bash
# User text only (skip tool results)
jq -r 'select(.type == "user") | .message.content | select(type == "string")'

# Assistant text only (skip thinking/tools)
jq -r 'select(.type == "assistant") | .message.content[] | select(.type == "text") | .text'
```
