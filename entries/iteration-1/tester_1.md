All 17 tests pass. Here's the summary:

## TEST CASES

**17 tests** in `tests/test_planner_prompt.py`, all passing:
- **6 guideline presence tests** — each of the 5 guidelines is present with key phrases, plus the section header
- **3 structural tests** — correct ordering (PLAN > Guidelines > numbered list), exactly 5 bullets, item 2 references "table format above"
- **6 rendering tests** — prompt works with/without shared understanding and feedback, including both populated simultaneously
- **2 edge cases** — special characters and multi-line tasks don't break the structure

## USAGE INSTRUCTIONS FOR USER

No configuration needed — the guidelines are built into the planner prompt. Run the pipeline as usual:

```bash
uv run supervisor.py --workspace myproject "your task here"
```

Run tests with:
```bash
uv run python -m pytest tests/test_planner_prompt.py -v
```

## SELF-REVIEW

1. **Easy:** Testing prompt string content — mock `run_agent`, capture the prompt, assert on substrings
2. **Hard:** Can't verify the planner *agent* actually follows guidelines without live runs
3. **Missing:** Nothing critical — reviewer feed-forward was helpful for edge cases
4. **Gaps:** None found — prompt-only change with no logic risk

## Verdict
STATUS: TESTS_PASSED
OPEN_ISSUES: none

[Committed changes to tester branch]