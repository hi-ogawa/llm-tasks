#!/usr/bin/env python3
"""Web UI for browsing Claude Code conversation history."""

import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"


def get_projects():
    """Get all projects with session counts."""
    projects = []
    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if project_dir.is_dir():
            sessions = list(project_dir.glob("*.jsonl"))
            if sessions:
                # Get most recent session time
                latest = max(s.stat().st_mtime for s in sessions)
                projects.append({
                    "encoded": project_dir.name,
                    "path": "/" + project_dir.name.replace("-", "/"),
                    "session_count": len(sessions),
                    "latest": datetime.fromtimestamp(latest),
                })
    # Sort by most recent activity
    return sorted(projects, key=lambda p: p["latest"], reverse=True)


def get_sessions(encoded_project: str):
    """Get sessions for a project."""
    project_dir = PROJECTS_DIR / encoded_project
    if not project_dir.exists():
        return []

    sessions = []
    for session_file in sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        size_kb = session_file.stat().st_size // 1024

        # Get first user message as preview
        preview = ""
        try:
            with open(session_file) as f:
                for line in f:
                    msg = json.loads(line)
                    if msg.get("type") == "user":
                        content = msg.get("message", {}).get("content", "")
                        if isinstance(content, str):
                            preview = content[:100].replace("\n", " ")
                            break
        except:
            pass

        sessions.append({
            "id": session_file.stem,
            "date": mtime,
            "size_kb": size_kb,
            "preview": preview,
        })
    return sessions


def get_session_messages(session_id: str):
    """Get all messages from a session."""
    # Find the session file
    session_file = None
    project_encoded = None
    for project_dir in PROJECTS_DIR.iterdir():
        candidate = project_dir / f"{session_id}.jsonl"
        if candidate.exists():
            session_file = candidate
            project_encoded = project_dir.name
            break
        # Try partial match
        for f in project_dir.glob(f"{session_id}*.jsonl"):
            session_file = f
            project_encoded = project_dir.name
            break
        if session_file:
            break

    if not session_file:
        return None, None

    messages = []
    with open(session_file) as f:
        for line in f:
            msg = json.loads(line)
            msg_type = msg.get("type")

            if msg_type == "user":
                content = msg.get("message", {}).get("content", "")
                if isinstance(content, str):
                    messages.append({
                        "role": "user",
                        "content": content,
                        "timestamp": msg.get("timestamp"),
                    })
                else:
                    # Tool results - collect them
                    tool_results = []
                    for item in content:
                        if item.get("type") == "tool_result":
                            tool_results.append(item.get("content", ""))
                    if tool_results:
                        messages.append({
                            "role": "tool_result",
                            "results": tool_results,
                            "timestamp": msg.get("timestamp"),
                        })

            elif msg_type == "assistant":
                content = msg.get("message", {}).get("content", [])
                blocks = []
                for block in content:
                    block_type = block.get("type")
                    if block_type == "thinking":
                        blocks.append({"type": "thinking", "content": block.get("thinking", "")})
                    elif block_type == "text":
                        blocks.append({"type": "text", "content": block.get("text", "")})
                    elif block_type == "tool_use":
                        blocks.append({
                            "type": "tool_use",
                            "name": block.get("name", ""),
                            "input": json.dumps(block.get("input", {}), indent=2),
                        })
                if blocks:
                    messages.append({
                        "role": "assistant",
                        "blocks": blocks,
                        "timestamp": msg.get("timestamp"),
                    })

    return messages, project_encoded


def search_history(query: str, limit: int = 50):
    """Search history.jsonl for matching prompts."""
    history_file = CLAUDE_DIR / "history.jsonl"
    if not history_file.exists():
        return []

    matches = []
    with open(history_file) as f:
        for line in f:
            entry = json.loads(line)
            display = entry.get("display", "")
            if query.lower() in display.lower():
                matches.append({
                    "timestamp": datetime.fromtimestamp(entry.get("timestamp", 0) / 1000),
                    "session_id": entry.get("sessionId", ""),
                    "display": display[:150],
                    "project": entry.get("project", ""),
                })

    # Return most recent first
    return matches[-limit:][::-1]


@app.route("/")
def index():
    """List all projects."""
    projects = get_projects()
    return render_template("projects.html", projects=projects)


@app.route("/project/<path:encoded>")
def project(encoded):
    """List sessions for a project."""
    sessions = get_sessions(encoded)
    decoded_path = "/" + encoded.replace("-", "/")
    return render_template("sessions.html", sessions=sessions, project_path=decoded_path, project_encoded=encoded)


@app.route("/session/<session_id>")
def session(session_id):
    """View a session's conversation."""
    messages, project_encoded = get_session_messages(session_id)
    if messages is None:
        return "Session not found", 404
    return render_template("session.html", messages=messages, session_id=session_id, project_encoded=project_encoded)


@app.route("/search")
def search():
    """Search history."""
    query = request.args.get("q", "")
    results = search_history(query) if query else []
    return render_template("search.html", results=results, query=query)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
