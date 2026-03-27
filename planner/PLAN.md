# Plan: Improve planner prompt with table format, line numbers, and decisive scoping

## PLAN

### 1. Requirements Analysis

**What:** Add guidelines to the planner prompt in `supervisor.py` so the planner agent produces plans that are easier for the implementer to follow.

**Why:** Implementer self-reviews across 16 runs showed that table-formatted file changes with line numbers, decisive scoping, and complete plans significantly reduce inner-loop iterations. Vague "consider" items and incomplete plans force the implementer to make design decisions or investigate independently, wasting cycles.

### 2. Implementation Steps

**File to change:** `src/ftl_sdlc_loop/supervisor.py`

| File | Lines | Change |
|------|-------|--------|
| `src/ftl_sdlc_loop/supervisor.py` | 1264-1272 | Add new guidelines section to the planner prompt between the `## PLAN` header and the existing numbered list |

The prompt at lines 1258-1284 should be modified to insert a guidelines block after `## PLAN` and before the numbered list. The guidelines should be added as a new section within the plan instructions.

**Suggested prompt addition** (insert after `## PLAN\n\n` at line 1266, before the numbered list):

```
### Output Guidelines

- **Use table format for file changes.** For each implementation step, include a table with columns: File, Line(s), Change Description. This lets the implementer go straight to the code.
- **Include line numbers for every change site.** Read the actual files and reference specific line numbers. Do not give vague locations.
- **Make decisions — do not defer to the implementer.** If a choice exists (e.g., "consider enriching X"), decide yes or no and state your reasoning. The implementer handles HOW, not WHAT.
- **Analyze both directions for matching/lookup changes.** If a change involves matching A against B, explicitly verify that B-to-A also works correctly. State your analysis.
- **Complete all plan steps.** Never truncate or abbreviate. If the plan is long, that is fine — an incomplete plan is worse than a long one.
```

Then keep the existing numbered list (requirements analysis, implementation steps, etc.) unchanged.

### 3. Key Design Decisions

1. **Add guidelines as a subsection, not replace existing structure.** The current numbered list (requirements analysis, implementation steps, key design decisions, success criteria) is good structure. The guidelines augment it — they tell the planner *how* to write each section, not *what* sections to write.

2. **Keep guidelines inside the prompt string, not as a separate file.** The prompt is self-contained in `supervisor.py`. Adding a separate file would complicate the architecture for five bullet points. Not worth it.

3. **Wording is directive, not suggestive.** Each guideline starts with a bold imperative ("Use table format", "Make decisions") rather than "Consider using" or "Try to include". This matches the feedback that vague language is the problem.

4. **No changes to effort-level prompts.** The MINIMAL/MODERATE/COMPREHENSIVE effort configs (lines 56, 68) don't need changes — the guidelines apply at all effort levels. A minimal plan with tables is still better than a minimal plan without.

### 4. Success Criteria

- The planner prompt in `supervisor.py` includes all five guidelines from the proposed solution.
- Running `uv run supervisor.py` with any task produces planner output that uses table format for file changes.
- No other behavior changes — the prompt structure (PLAN + SELF-REVIEW), effort levels, and agent flow are unaffected.

## SELF-REVIEW

1. **What went well:** The task is well-scoped — one function, one file, five bullet points to add. The issue itself provides clear before/after criteria from real implementer feedback.

2. **What information was missing:** I would have liked to see 2-3 example plan outputs (good and bad) from the 16 runs to calibrate the exact wording. The issue summarizes well but examples would help verify the guidelines produce the desired output.

3. **What would help next time:** Having the implementer feedback raw data (the self-reviews from PRs #51-66) linked or included would let me check whether the five proposed guidelines fully cover all the friction points mentioned.
