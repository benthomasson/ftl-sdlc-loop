"""Tests for planner prompt guidelines (table format, line numbers, decisive scoping).

Validates that the planner prompt in supervisor.py includes the five Output Guidelines
added per issue #1, and that they render correctly under various input combinations.
"""

import re
from unittest.mock import patch, MagicMock


def _call_planner(**kwargs):
    """Call planner() with all side-effects mocked; return the prompt string passed to run_agent."""
    defaults = {"task": "test task", "iteration": 1}
    defaults.update(kwargs)
    mock_run_agent = MagicMock(return_value="mocked response")
    with patch("ftl_sdlc_loop.supervisor.run_agent", mock_run_agent), \
         patch("ftl_sdlc_loop.supervisor.save_artifact"), \
         patch("ftl_sdlc_loop.supervisor.git_commit"):
        from ftl_sdlc_loop.supervisor import planner
        planner(**defaults)
        # run_agent is called as run_agent("planner", prompt, continue_session=...)
        call_args = mock_run_agent.call_args
        prompt = call_args[0][1]  # second positional arg
        return prompt


# --- Guideline presence tests ---

def test_output_guidelines_section_present():
    """The prompt must contain the '### Output Guidelines' header."""
    prompt = _call_planner()
    assert "### Output Guidelines" in prompt


def test_guideline_table_format():
    """Guideline 1: Use table format for file changes."""
    prompt = _call_planner()
    assert "table format for file changes" in prompt
    assert "File, Line(s), Change Description" in prompt


def test_guideline_line_numbers():
    """Guideline 2: Include line numbers for every change site."""
    prompt = _call_planner()
    assert "Include line numbers for every change site" in prompt
    assert "Do not give vague locations" in prompt


def test_guideline_decisive_language():
    """Guideline 3: Make decisions, do not defer to the implementer."""
    prompt = _call_planner()
    assert "Make decisions" in prompt
    assert "do not defer to the implementer" in prompt
    assert "The implementer handles HOW, not WHAT" in prompt


def test_guideline_bidirectional_analysis():
    """Guideline 4: Analyze both directions for matching/lookup changes."""
    prompt = _call_planner()
    assert "Analyze both directions" in prompt
    assert "B-to-A" in prompt


def test_guideline_no_truncation():
    """Guideline 5: Complete all plan steps, never truncate."""
    prompt = _call_planner()
    assert "Complete all plan steps" in prompt
    assert "Never truncate or abbreviate" in prompt
    assert "incomplete plan is worse than a long one" in prompt


def test_all_five_guidelines_present():
    """All five guideline bullet points must appear as a group."""
    prompt = _call_planner()
    # Each guideline starts with "- **"
    guidelines_section = prompt.split("### Output Guidelines")[1].split("\n1.")[0]
    bullets = [line.strip() for line in guidelines_section.strip().split("\n") if line.strip().startswith("- **")]
    assert len(bullets) == 5, f"Expected 5 guideline bullets, got {len(bullets)}: {bullets}"


# --- Ordering tests ---

def test_guidelines_before_numbered_list():
    """Output Guidelines must appear between '## PLAN' and the numbered list."""
    prompt = _call_planner()
    plan_pos = prompt.index("## PLAN")
    guidelines_pos = prompt.index("### Output Guidelines")
    numbered_list_pos = prompt.index("1. Requirements analysis")
    assert plan_pos < guidelines_pos < numbered_list_pos


def test_item2_references_table_format():
    """Numbered item 2 should reference 'table format above'."""
    prompt = _call_planner()
    # Find item 2 in the numbered list
    match = re.search(r"2\.\s+Implementation steps.*", prompt)
    assert match, "Could not find item 2 in the numbered list"
    assert "table format above" in match.group(0), \
        f"Item 2 does not reference table format: {match.group(0)}"


# --- Rendering with optional sections ---

def test_prompt_without_understanding():
    """Prompt renders correctly when no shared_understanding is provided."""
    prompt = _call_planner(shared_understanding=None)
    assert "### Output Guidelines" in prompt
    assert "SHARED UNDERSTANDING" not in prompt
    # Guidelines should still be well-formed
    assert "table format for file changes" in prompt


def test_prompt_with_understanding():
    """Prompt renders correctly when shared_understanding is provided."""
    prompt = _call_planner(shared_understanding="We are building a REST API.")
    assert "### Output Guidelines" in prompt
    assert "SHARED UNDERSTANDING" in prompt
    assert "We are building a REST API." in prompt
    # Guidelines must still be present after understanding section
    assert "table format for file changes" in prompt


def test_prompt_without_feedback():
    """Prompt renders correctly when no user_feedback is provided (first iteration)."""
    prompt = _call_planner(user_feedback=None)
    assert "### Output Guidelines" in prompt
    assert "USER FEEDBACK" not in prompt


def test_prompt_with_feedback():
    """Prompt renders correctly when user_feedback is provided."""
    prompt = _call_planner(user_feedback="Please add error handling.")
    assert "### Output Guidelines" in prompt
    assert "USER FEEDBACK" in prompt
    assert "Please add error handling." in prompt


def test_prompt_with_both_understanding_and_feedback():
    """Prompt renders correctly with both optional sections populated."""
    prompt = _call_planner(
        shared_understanding="Build a CLI tool.",
        user_feedback="Add --verbose flag.",
    )
    assert "### Output Guidelines" in prompt
    assert "SHARED UNDERSTANDING" in prompt
    assert "USER FEEDBACK" in prompt
    # Verify guidelines are not lost between the two sections
    guidelines_pos = prompt.index("### Output Guidelines")
    assert guidelines_pos > 0


def test_prompt_with_empty_string_understanding():
    """Empty string for shared_understanding is falsy, so the section should be omitted."""
    prompt = _call_planner(shared_understanding="")
    assert "### Output Guidelines" in prompt
    assert "SHARED UNDERSTANDING" not in prompt


# --- Task content does not break guidelines ---

def test_task_with_special_characters():
    """Task containing special characters doesn't break the prompt structure."""
    prompt = _call_planner(task='Fix "quoting" & <angle> brackets {braces}')
    assert "### Output Guidelines" in prompt
    assert "table format for file changes" in prompt
    assert 'Fix "quoting"' in prompt


def test_task_with_newlines():
    """Multi-line task doesn't break the guidelines section."""
    prompt = _call_planner(task="Line 1\nLine 2\nLine 3")
    assert "### Output Guidelines" in prompt
    # Guidelines should still be between PLAN and numbered list
    plan_pos = prompt.index("## PLAN")
    guidelines_pos = prompt.index("### Output Guidelines")
    numbered_list_pos = prompt.index("1. Requirements analysis")
    assert plan_pos < guidelines_pos < numbered_list_pos
