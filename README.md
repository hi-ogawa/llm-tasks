## Structure

```
README.md
tasks/
  YYYY-MM-DD-(title)/
    plan.md
```

## Workflow

- create tasks/YYYY-MM-DD-(title) for each task
- create plan.md, then iterate and confirm with user

## Scripting

- Use mainly python
- Use uv toolchain

### Python Setup with uv

Each task may include Python scripts. Use `uv` for dependency management:

```bash
# Install dependencies (from pyproject.toml)
uv sync

# Run a script
uv run scripts/script_name.py

# Add a dependency
uv add package-name
```

### Project Structure with Scripts

```
tasks/YYYY-MM-DD-(title)/
├── plan.md
├── pyproject.toml          # Python dependencies (if needed)
├── scripts/
│   └── script_name.py
└── docs/
    └── output/
```

**Note**: Python dependencies are defined per-task in `pyproject.toml` within each task directory.