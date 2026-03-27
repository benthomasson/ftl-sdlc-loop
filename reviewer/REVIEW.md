# Code Review: Improve planner prompt with table format, line numbers, and decisive scoping

## FEEDBACK FOR IMPLEMENTER

**Correctness:** The implementation fulfills all five requirements from the task:
1. Table format for file changes — addressed by guideline 1
2. Line numbers for every change site — addressed by guideline 2
3. Decisive language (no "consider" items) — addressed by guideline 3
4. Bidirectional analysis for matching/lookup — addressed by guideline 4
5. Complete plans, no truncation — addressed by guideline 5

The guidelines are inserted at the right location (after `## PLAN`, before the numbered list) and the numbered list item 2 was updated to reference the table format ("using table format above"), which ties the guidelines to the existing structure.

**The truncated sentence completion is reasonable.** The plan itself was truncated at "If the plan is long" — the implementer completed it with "that is fine — an incomplete plan is worse than a long one." This is a good phrasing that directly reinforces the anti-truncation guideline. Ironic that the plan about preventing truncation was itself truncated, but the fix is sound.

**No issues found.** The change is a prompt-only modification — no logic, no control flow, no risk of runtime errors. The f-string interpolation is unchanged. The guidelines are clear and actionable.

## FEED-FORWARD FOR TESTER

**Key behaviors to test:**
- The planner prompt string includes all five guidelines when rendered
- The `### Output Guidelines` section appears between `## PLAN` and the numbered list
- Item 2 in the numbered list references "using table format above"
- The prompt still renders correctly with and without `understanding_section` and `feedback_section` content

**Edge cases:**
- Empty `understanding_section` (no shared understanding provided) — verify no blank lines break formatting
- Empty `feedback_section` (first iteration) — same concern
- Both sections populated — verify guidelines don't get lost in a long prompt

**Suggested test scenarios:**
1. Unit test: call the planner function (or extract the prompt construction) and assert the guidelines text is present in the prompt string
2. String assertion: verify "Output Guidelines" appears after "## PLAN" and before "1. Requirements analysis"
3. Verify the numbered list item 2 contains "table format above"

**Areas of concern:** This is a prompt text change, so functional testing is mostly about verifying string content. No behavioral regression risk beyond prompt quality.

## SELF-REVIEW

1. **What was easy to review:** This change is entirely within a single prompt string — no logic changes, no new imports, no side effects. The diff is small and self-contained. Easy to verify correctness by reading.
2. **What made review difficult:** Not being able to see the git diff directly (permission issues) meant I had to compare the current file state against my knowledge of the original. For prompt-only changes this is fine, but for logic changes it would be harder.
3. **What would make my job easier next time:** Having the diff provided inline in the review task context rather than needing to reconstruct it.
4. **What the implementer should know:** Good judgment call on completing the truncated sentence. The change is clean and minimal — no unnecessary refactoring or scope creep.

## Verdict
STATUS: APPROVED
OPEN_ISSUES: none
