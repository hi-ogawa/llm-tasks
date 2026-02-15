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
git worktree add ../repo-wt1
```

Creates `repo-wt1` branch from current HEAD. Explicit branch optional: `-b branch-name base`.

`repo-wt1` _is_ your `main` in that worktree.

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
git checkout repo-wt1
```

## Commands

List all worktrees (from any worktree):

```bash
$ git worktree list
/path/to/repo    cf27bce [main]
/path/to/repo-wt1  52b819d [repo-wt1]
/path/to/repo-wt-2  20e00ef [repo-wt-2]
```

Remove entirely:

```bash
git worktree remove ../repo-wt1  # or: rm -rf + git worktree prune
git branch -d repo-wt1           # branch persists, delete separately
```
