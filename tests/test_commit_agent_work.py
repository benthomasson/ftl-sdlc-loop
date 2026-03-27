"""Tests for commit_agent_work staging behavior.

Uses real git repos in temp directories to verify that source-modifying agents
(implementer, tester) commit source file changes, while non-source-modifying
agents (planner, reviewer) only commit files in their own subdirectory.
"""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run a git command in the given directory."""
    return subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True,
        env={"GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@test",
             "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@test",
             "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )


def _init_workspace(tmp_path: Path) -> Path:
    """Create a git repo with an initial commit and agent subdirectories."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _git(["init"], workspace)
    _git(["config", "user.email", "test@test"], workspace)
    _git(["config", "user.name", "test"], workspace)
    (workspace / "src").mkdir()
    (workspace / "src" / "main.py").write_text("print('hello')\n")
    for role in ("planner", "implementer", "reviewer", "tester", "user"):
        (workspace / role).mkdir()
    _git(["add", "-A"], workspace)
    _git(["commit", "-m", "initial"], workspace)
    # Create a branch for the agent to work on
    _git(["checkout", "-b", "implementer"], workspace)
    _git(["checkout", "-b", "tester"], workspace)
    _git(["checkout", "-b", "planner"], workspace)
    _git(["checkout", "main"], workspace)
    return workspace


def _committed_files(workspace: Path) -> list[str]:
    """Return list of files changed in the last commit."""
    result = _git(["diff", "--name-only", "HEAD~1", "HEAD"], workspace)
    return sorted(result.stdout.strip().split("\n")) if result.stdout.strip() else []


def test_implementer_commits_source_files(tmp_path):
    """Implementer should commit both its subdirectory files and source files."""
    workspace = _init_workspace(tmp_path)
    _git(["checkout", "implementer"], workspace)

    # Simulate implementer editing a source file and writing to its own dir
    (workspace / "src" / "main.py").write_text("print('modified')\n")
    (workspace / "implementer" / "notes.md").write_text("implementation notes\n")

    with patch("ftl_sdlc_loop.agent.get_workspace_dir", return_value=workspace):
        from ftl_sdlc_loop.agent import commit_agent_work
        result = commit_agent_work("implementer", "test commit")

    assert result is True
    files = _committed_files(workspace)
    assert "src/main.py" in files
    assert "implementer/notes.md" in files


def test_implementer_excludes_other_agent_dirs(tmp_path):
    """Implementer should not stage files in other agents' subdirectories."""
    workspace = _init_workspace(tmp_path)
    _git(["checkout", "implementer"], workspace)

    # Simulate another agent leaving uncommitted work
    (workspace / "reviewer" / "REVIEW.md").write_text("review notes\n")
    (workspace / "planner" / "PLAN.md").write_text("plan notes\n")
    # Implementer edits source
    (workspace / "src" / "main.py").write_text("print('modified')\n")

    with patch("ftl_sdlc_loop.agent.get_workspace_dir", return_value=workspace):
        from ftl_sdlc_loop.agent import commit_agent_work
        result = commit_agent_work("implementer", "test commit")

    assert result is True
    files = _committed_files(workspace)
    assert "src/main.py" in files
    assert "reviewer/REVIEW.md" not in files
    assert "planner/PLAN.md" not in files


def test_tester_commits_source_files(tmp_path):
    """Tester should commit both its subdirectory files and source files."""
    workspace = _init_workspace(tmp_path)
    _git(["checkout", "tester"], workspace)

    (workspace / "src" / "main.py").write_text("print('tested')\n")
    (workspace / "tester" / "report.md").write_text("test report\n")

    with patch("ftl_sdlc_loop.agent.get_workspace_dir", return_value=workspace):
        from ftl_sdlc_loop.agent import commit_agent_work
        result = commit_agent_work("tester", "test commit")

    assert result is True
    files = _committed_files(workspace)
    assert "src/main.py" in files
    assert "tester/report.md" in files


def test_planner_only_commits_own_directory(tmp_path):
    """Planner should only commit files in planner/, not source files."""
    workspace = _init_workspace(tmp_path)
    _git(["checkout", "planner"], workspace)

    # Planner writes to its directory; a source file is also modified (shouldn't be staged)
    (workspace / "planner" / "PLAN.md").write_text("the plan\n")
    (workspace / "src" / "main.py").write_text("print('should not be committed')\n")

    with patch("ftl_sdlc_loop.agent.get_workspace_dir", return_value=workspace):
        from ftl_sdlc_loop.agent import commit_agent_work
        result = commit_agent_work("planner", "test commit")

    assert result is True
    files = _committed_files(workspace)
    assert "planner/PLAN.md" in files
    assert "src/main.py" not in files


def test_no_changes_returns_false(tmp_path):
    """commit_agent_work should return False when there are no changes."""
    workspace = _init_workspace(tmp_path)
    _git(["checkout", "implementer"], workspace)

    with patch("ftl_sdlc_loop.agent.get_workspace_dir", return_value=workspace):
        from ftl_sdlc_loop.agent import commit_agent_work
        result = commit_agent_work("implementer", "nothing to commit")

    assert result is False
