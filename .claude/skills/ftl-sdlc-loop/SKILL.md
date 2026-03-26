---
name: ftl-sdlc-loop
description: Run autonomous multi-agent SDLC pipeline — plan, implement, review, test, and ship code changes
argument-hint: "[task description] [options]"
allowed-tools: Bash(ftl-sdlc-loop *), Bash(uv run ftl-sdlc-loop *), Bash(uv run supervisor.py *), Read
---

You are running the autonomous multi-agent SDLC pipeline using the `ftl-sdlc-loop` CLI tool. This tool orchestrates multiple Claude agents (planner, implementer, reviewer, tester, user) to collaboratively build software with real feedback loops.

## Why Use This Tool

**Autonomous development with real feedback.** Instead of a single agent writing code and hoping it works, this pipeline has separate agents plan, implement, review, test, and actually run the code — catching real issues through structured iteration.

**Claude is the user.** The key insight: the User agent actually runs the generated code, discovers real errors, and provides structured feedback. This creates genuine feedback loops, not simulated ones.

**Structured verdicts and exit gates.** Each agent emits APPROVED/NEEDS_CHANGES/TESTS_PASSED/TESTS_FAILED/SATISFIED/NEEDS_IMPROVEMENT verdicts. The supervisor validates these — if an agent says APPROVED but lists open issues, it overrides the verdict.

## How to Run

First run `ftl-sdlc-loop --help` to see all available options and examples.

Try these in order until one works:
1. `ftl-sdlc-loop $ARGUMENTS` (if installed via uv/pip)
2. `uv run ftl-sdlc-loop $ARGUMENTS` (if in the multiagent-loop repo)
3. `uv run supervisor.py $ARGUMENTS` (direct script invocation)

## Common Workflows

### Simple task
```bash
ftl-sdlc-loop "write a function to check if a number is prime"
ftl-sdlc-loop --effort minimal "solve two-sum"
```

### Work on an existing codebase
```bash
ftl-sdlc-loop --workspace myproject --init-from /path/to/repo "add caching layer"
ftl-sdlc-loop --workspace myproject --init-from git@github.com:user/repo.git "fix auth bug"
```

### GitHub issue workflow — fix issue, create PR, review
```bash
ftl-sdlc-loop --workspace issue-42 --init-from ~/git/repo --github-issue 42 --github-repo owner/repo --github-pr --code-review --effort moderate --no-questions --clean
```

### GitLab issue workflow — fix issue, create MR
```bash
ftl-sdlc-loop --workspace issue-285 --init-from ~/git/repo.git --gitlab-remote git@gitlab.com:org/repo.git --gitlab-issue 285 --effort minimal
ftl-sdlc-loop --workspace issue-285 --gitlab-mr --push
```

### Push or create PR after completion
```bash
ftl-sdlc-loop --workspace myproject --push          # Push to remote
ftl-sdlc-loop --workspace myproject --pr             # Create GitHub PR
ftl-sdlc-loop --workspace myproject --push --clean   # Push, strip SDLC artifacts
```

### Feature branch development
```bash
ftl-sdlc-loop --workspace feature-x --init-from /path/to/repo --branch feature-x "implement feature"
ftl-sdlc-loop --workspace feature-x --branch feature-x --push
```

### Plan review workflow
```bash
ftl-sdlc-loop --workspace myproject --plan-only "build feature X"    # Generate plan, exit
# (human reviews PLAN.md)
ftl-sdlc-loop --workspace myproject --plan workspaces/myproject/PLAN.md "build feature X"
```

### Continue a previous run
```bash
ftl-sdlc-loop --workspace myproject --continue "fix the bug from last run"
```

### Continuous batch mode
```bash
ftl-sdlc-loop --continuous                    # Process queue.txt
ftl-sdlc-loop --continuous --queue tasks.txt  # Custom queue file
```

### With environment variables (secrets)
```bash
ftl-sdlc-loop --workspace myproject --env ~/.secrets/myproject.env "build API integration"
```

## Effort Levels

- **minimal** — Fast (~5-15 min): planner, implementer, tester. Skips review and user stages.
- **moderate** — Balanced (~30-60 min): full pipeline with review. Default.
- **maximum** — Production (~2-3 hours): comprehensive testing, multiple iterations.

## Key Concepts

- **Workspace**: Named directory under `workspaces/` containing the git repo and all artifacts. Reuse a workspace name to continue working on the same codebase.
- **`--init-from`**: Clones a repo (local path or git URL) into the workspace. Only needed the first time.
- **`--clean`**: Strips SDLC artifacts (PLAN.md, REVIEW.md, etc.) before push/PR. Use for clean deliverables.
- **`--no-questions`**: Fully autonomous — no interactive prompts. Required for unattended runs.
- **`--code-review`**: Runs multi-model code review after PR creation. Requires `--github-pr`.
- **FINAL_REPORT.md**: Human-readable summary generated at the end of each run.

## Converting Natural Language to Commands

When the user describes what they want, map it to flags:
- "fix issue 42 on my repo" → `--workspace issue-42 --init-from <repo> --github-issue 42`
- "create a PR when done" → add `--github-pr --push`
- "run a code review too" → add `--code-review`
- "quick/fast" → `--effort minimal`
- "thorough/production" → `--effort maximum`
- "no prompts" → `--no-questions`
- "clean up artifacts" → `--clean`

## After Any Command

- The pipeline runs autonomously and may take minutes to hours depending on effort level
- When complete, read `FINAL_REPORT.md` in the workspace for the summary
- If the user wants to see what happened, check `workspaces/<name>/entries/` for full agent outputs
