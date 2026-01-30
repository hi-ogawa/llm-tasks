# Parallel Claude Code Agents with Git Worktree

Run multiple Claude Code agents simultaneously on the same repository using git worktrees for isolation.

## Core Concept

Worktrees are like hard copies, except:

|            | Hard copy          | Worktree                     |
| ---------- | ------------------ | ---------------------------- |
| Disk       | Full duplicate     | Shared `.git` objects        |
| Branch     | Any branch anytime | Must differ across worktrees |
| Visibility | None               | `git worktree list`          |

Same ergonomics otherwise - `cd` in, work normally.

## One-Time Setup

```bash
git worktree add ../repo-wt-1
```

Creates `repo-wt-1` branch from current HEAD. Explicit branch optional: `-b branch-name base`.

`repo-wt-1` _is_ your `main` in that worktree.

## Workflow

Normal git, except to sync with main:

```bash
git reset --hard origin/main  # instead of `git pull`
```

Full cycle:

```bash
git fetch origin
git reset --hard origin/main
git checkout -b feature/x
# work, commit, push, PR...
git checkout worktree-1
```

## Commands

List all worktrees (from any worktree):

```bash
$ git worktree list
/path/to/repo    cf27bce [main]
/path/to/repo-wt-1  52b819d [repo-wt-1]
/path/to/repo-wt-2  20e00ef [repo-wt-2]
```

Remove entirely:

```bash
git worktree remove ../repo-wt-1
git branch -d worktree-1  # branch persists, delete separately
```
