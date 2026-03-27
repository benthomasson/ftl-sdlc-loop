# Task

## Improve planner prompt with table format, line numbers, and decisive scoping

## Feature Request

**Source:** Implementer self-reviews across 16 sdlc-loop runs on ftl2 PRs #51-66.

## Problem

Implementer agents provided feedback on what helps and hinders their work. This feedback can improve planner output quality.

## Observations

### What works well
- **Table format for file changes** — plans that use tables listing file, line, and change description are easier to follow than prose
- **Accurate line numbers** — when the plan includes correct line numbers, implementers can go straight to the code without searching
- **Well-scoped plans** — plans that focus on the minimal change needed produce better results

### What causes friction
- **Incomplete plans** — one plan was cut off at Step 3, forcing the implementer to investigate independently and wasting time
- **Vague scope** — plans that suggest "consider enriching" without deciding yes/no leave implementers making design decisions that should have been made in planning
- **Missing bidirectional analysis** — a plan said "accept FQCNs in the allowlist" but did not think through symmetric matching, requiring a second implementation round

## Proposed Solution

Add planner prompt guidelines:
1. Always use table format for file changes (file, line, change)
2. Include line numbers for every change site
3. Make decisions — do not leave "consider" items for the implementer
4. For matching/lookup changes, explicitly analyze both directions
5. Ensure all plan steps are complete (no truncation)

## Priority

Medium — improves first-pass implementation success rate, reducing inner loop iterations.


Closes #1

Started: 2026-03-27T14:14:53.866859