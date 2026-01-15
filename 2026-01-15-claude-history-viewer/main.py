#!/usr/bin/env python3
"""Browse Claude Code conversation history."""

import json
import argparse
from pathlib import Path
from datetime import datetime

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"


def list_projects():
    """List all projects with sessions."""
    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if project_dir.is_dir():
            sessions = list(project_dir.glob("*.jsonl"))
            # Decode path: -home-user-code becomes /home/user/code
            decoded = "/" + project_dir.name.replace("-", "/")
            print(f"{decoded}  ({len(sessions)} sessions)")


def list_sessions(project_path: str):
    """List sessions for a project."""
    # Encode path: /home/user/code becomes -home-user-code
    encoded = project_path.replace("/", "-").lstrip("-")
    project_dir = PROJECTS_DIR / encoded

    if not project_dir.exists():
        # Try partial match
        matches = [p for p in PROJECTS_DIR.iterdir() if encoded in p.name]
        if matches:
            project_dir = matches[0]
        else:
            print(f"Project not found: {project_path}")
            return

    sessions = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    for session_file in sessions:
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        size_kb = session_file.stat().st_size // 1024

        # Get first user message as preview
        preview = ""
        with open(session_file) as f:
            for line in f:
                msg = json.loads(line)
                if msg.get("type") == "user":
                    content = msg.get("message", {}).get("content", "")
                    if isinstance(content, str):
                        preview = content[:60].replace("\n", " ")
                        break

        print(f"{session_file.stem}  {mtime:%Y-%m-%d %H:%M}  {size_kb:>4}KB  {preview}...")


def print_session(session_id: str, show_thinking: bool = False, show_tools: bool = False):
    """Pretty print a session's conversation."""
    # Find the session file
    session_file = None
    for project_dir in PROJECTS_DIR.iterdir():
        candidate = project_dir / f"{session_id}.jsonl"
        if candidate.exists():
            session_file = candidate
            break
        # Try partial match
        for f in project_dir.glob(f"{session_id}*.jsonl"):
            session_file = f
            break

    if not session_file:
        print(f"Session not found: {session_id}")
        return

    with open(session_file) as f:
        for line in f:
            msg = json.loads(line)
            msg_type = msg.get("type")

            if msg_type == "user":
                content = msg.get("message", {}).get("content", "")
                if isinstance(content, str):
                    print(f"\n{'='*60}")
                    print("USER:")
                    print(content)
                elif show_tools:
                    # Tool results
                    for item in content:
                        if item.get("type") == "tool_result":
                            result = item.get("content", "")[:200]
                            print(f"\n[tool_result: {result}...]")

            elif msg_type == "assistant":
                content = msg.get("message", {}).get("content", [])
                for block in content:
                    block_type = block.get("type")

                    if block_type == "thinking" and show_thinking:
                        print(f"\n<thinking>\n{block.get('thinking', '')}\n</thinking>")

                    elif block_type == "text":
                        print(f"\n{'-'*60}")
                        print("ASSISTANT:")
                        print(block.get("text", ""))

                    elif block_type == "tool_use" and show_tools:
                        name = block.get("name", "")
                        inp = json.dumps(block.get("input", {}), indent=2)[:200]
                        print(f"\n[tool: {name}]\n{inp}")


def search_history(query: str, limit: int = 20):
    """Search history.jsonl for matching prompts."""
    history_file = CLAUDE_DIR / "history.jsonl"
    if not history_file.exists():
        print("history.jsonl not found")
        return

    matches = []
    with open(history_file) as f:
        for line in f:
            entry = json.loads(line)
            display = entry.get("display", "")
            if query.lower() in display.lower():
                matches.append(entry)

    # Show most recent first
    for entry in matches[-limit:]:
        ts = datetime.fromtimestamp(entry.get("timestamp", 0) / 1000)
        session = entry.get("sessionId", "")[:8]
        display = entry.get("display", "")[:80].replace("\n", " ")
        print(f"{ts:%Y-%m-%d %H:%M}  {session}  {display}")


def main():
    parser = argparse.ArgumentParser(description="Browse Claude Code history")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("projects", help="List projects")

    ls = sub.add_parser("ls", help="List sessions for a project")
    ls.add_argument("project", help="Project path (e.g., /home/user/code)")

    show = sub.add_parser("show", help="Show a session")
    show.add_argument("session", help="Session ID (can be partial)")
    show.add_argument("-t", "--thinking", action="store_true", help="Show thinking")
    show.add_argument("-T", "--tools", action="store_true", help="Show tool calls")

    search = sub.add_parser("search", help="Search history")
    search.add_argument("query", help="Search term")
    search.add_argument("-n", "--limit", type=int, default=20, help="Max results")

    args = parser.parse_args()

    if args.command == "projects":
        list_projects()
    elif args.command == "ls":
        list_sessions(args.project)
    elif args.command == "show":
        print_session(args.session, args.thinking, args.tools)
    elif args.command == "search":
        search_history(args.query, args.limit)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
