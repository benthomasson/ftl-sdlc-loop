# Tester Report: Planner Prompt Guidelines

## TEST CASES

**Test file:** `tests/test_planner_prompt.py` (17 tests, all passing)

### Guideline Presence Tests (6 tests)
1. `test_output_guidelines_section_present` — `### Output Guidelines` header exists
2. `test_guideline_table_format` — table format guideline with column names present
3. `test_guideline_line_numbers` — line numbers guideline with "Do not give vague locations"
4. `test_guideline_decisive_language` — decisive language guideline with "HOW, not WHAT"
5. `test_guideline_bidirectional_analysis` — bidirectional analysis guideline with "B-to-A"
6. `test_guideline_no_truncation` — no-truncation guideline with "incomplete plan is worse"

### Structural Tests (3 tests)
7. `test_all_five_guidelines_present` — exactly 5 bullet points in guidelines section
8. `test_guidelines_before_numbered_list` — ordering: `## PLAN` < `### Output Guidelines` < numbered list
9. `test_item2_references_table_format` — item 2 says "table format above"

### Optional Section Rendering Tests (6 tests)
10. `test_prompt_without_understanding` — no shared understanding: guidelines present, no SHARED UNDERSTANDING section
11. `test_prompt_with_understanding` — shared understanding provided: both sections render
12. `test_prompt_without_feedback` — no feedback: guidelines present, no USER FEEDBACK section
13. `test_prompt_with_feedback` — feedback provided: both sections render
14. `test_prompt_with_both_understanding_and_feedback` — all sections coexist
15. `test_prompt_with_empty_string_understanding` — empty string treated as absent (Python falsy)

### Edge Cases (2 tests)
16. `test_task_with_special_characters` — quotes, ampersands, angle brackets, braces in task
17. `test_task_with_newlines` — multi-line task doesn't break guidelines ordering

## USAGE INSTRUCTIONS FOR USER

### Running the Pipeline

The planner prompt guidelines are automatically active — no configuration needed. When you run the pipeline, the planner agent will receive instructions to:

1. Use **table format** (File, Line(s), Change Description) for all file changes
2. Include **specific line numbers** for every change site
3. **Make decisions** rather than leaving "consider" items for the implementer
4. **Analyze both directions** for matching/lookup changes
5. **Never truncate** — complete all plan steps

### Example Commands

```bash
# Standard pipeline — planner guidelines are built into the prompt
uv run supervisor.py --workspace myproject "add user authentication"

# Plan-only mode — see guidelines in action without running full pipeline
uv run supervisor.py --workspace myproject --plan-only "add user authentication"

# With shared understanding — guidelines still appear after understanding section
uv run supervisor.py --workspace myproject --understanding SHARED_UNDERSTANDING.md "add feature"
```

### Expected Output

The planner's output should now consistently include:
- A table per implementation step with File, Line(s), and Change Description columns
- Specific line numbers (e.g., "lines 42-58") rather than vague references
- Definitive decisions (e.g., "Yes, add error handling because...") not suggestions ("Consider adding...")
- Bidirectional analysis for any matching/lookup changes
- Complete plans with no truncated steps

### Running Tests

```bash
cd /path/to/ftl-sdlc-loop
uv run python -m pytest tests/test_planner_prompt.py -v
```

All 17 tests should pass. Tests mock `run_agent`, `save_artifact`, and `git_commit` so they run instantly without spawning Claude CLI.

### Common Issues

- **`No module named pytest`**: Run `uv add --dev pytest` first
- **Import errors**: Ensure you're running from the project root with `uv run`
- **Tests fail after prompt edits**: If you modify the planner prompt in `supervisor.py`, update the test assertions to match

## SELF-REVIEW

1. **What was easy to test?** The prompt string content — since it's built with f-strings, mocking `run_agent` to capture the prompt was straightforward. All guideline text is deterministic.

2. **What was hard?** There's no way to test that the planner *agent* actually follows these guidelines without running a real Claude session. These tests verify the prompt contains the right instructions, not that the output improves.

3. **What information was missing?** The reviewer's feed-forward mentioned testing with "empty understanding" and "empty feedback" sections — helpful. Would have been nice to know about `patch.multiple` returning empty dicts (minor pytest gotcha).

4. **Any gaps?** No runtime gaps found. The implementation is prompt-only with no logic changes, so the risk surface is minimal. The only potential gap is that there's no integration test confirming end-to-end planner behavior improves, but that requires live agent runs and is outside scope.

## Verdict
STATUS: TESTS_PASSED
OPEN_ISSUES: none
