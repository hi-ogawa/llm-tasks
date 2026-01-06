# LLM Tasks

A collection of one-off tasks and experiments, each self-contained with its own planning, scripts, and outputs.

## Structure

```
tasks/
  YYYY-MM-DD-(title)/
    plan.md              # Detailed planning and exploration
    pyproject.toml       # Python dependencies (per-task)
    scripts/             # Task-specific scripts
    data/                # Generated outputs (often git-ignored)
    .gitignore           # Ignore build artifacts, data/html, .venv
```

## Workflow

1. Create `tasks/YYYY-MM-DD-(title)/` directory
2. Write `plan.md` with problem statement, approach, and implementation steps
3. Set up `pyproject.toml` with task-specific dependencies
4. Iterate on scripts and outputs
5. Update plan.md with progress and results

## Scripting

**Toolchain**: Python with `uv` for dependency management

### Common Commands

```bash
# Navigate to task directory
cd tasks/YYYY-MM-DD-(title)/

# Install dependencies
uv sync

# Run a script
uv run scripts/script_name.py

# Add a dependency
uv add package-name
```

### Example Task Structure

See `tasks/2026-01-06-obs-document/` for a complete example:
- Web scraping with `trafilatura` and `beautifulsoup4`
- Parallel processing scripts
- Markdown generation from HTML sources
- Git-ignored data directories for large outputs