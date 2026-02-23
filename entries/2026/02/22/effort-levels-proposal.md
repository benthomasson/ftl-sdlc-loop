# Effort Levels Proposal

**Date:** 2026-02-22
**Time:** 20:23

## Overview

Proposal to add configurable effort levels to multiagent-loop via `--effort` flag, enabling fast execution for LeetCode problems (~5-15 min) vs production-quality code (~2-3 hours).

**Problem**: Current system optimized for production quality is overkill for LeetCode practice problems (2-3 hours per problem with 40+ tests, READMEs, verification scripts).

**Solution**: Three effort levels - minimal, moderate, maximum - controlling which agents run and how thorough they are.

## Details

### Proposed Effort Levels

#### 1. MINIMAL (for LeetCode, quick prototypes)
- **Goal**: Working solution, fast execution (~5-15 minutes)
- **Pipeline**: Planner → Implementer → Tester (3 agents, no review loops)
- **Max iterations**: 1
- **Skip**: Reviewer, User
- **Output**: ~80-130 lines (solution.py + test_solution.py)

**Changes per agent**:
- **Planner**: Brief plan (1-2 paragraphs), skip architectural discussions
- **Implementer**: Basic solution, minimal docstring, no extra files, type hints optional
- **Tester**: 5-10 test cases, no usage guide

#### 2. MODERATE (balanced, good for most tasks)
- **Goal**: Solid solution with good practices (~30-60 minutes)
- **Pipeline**: Planner → Implementer → Reviewer → Tester (4 agents, 1 review loop max)
- **Max iterations**: 1
- **Skip**: User agent
- **Output**: ~190-300 lines (solution.py + tests + USAGE.md)

**Changes per agent**:
- Standard plan with key decisions
- Clean solution with good docstring, type hints required
- Focused review (1 round max)
- 10-20 test cases with basic usage guide

#### 3. MAXIMUM (production quality, current behavior)
- **Goal**: Production-ready code (~2-3 hours)
- **Pipeline**: Full 5-agent pipeline with all feedback loops
- **Max iterations**: 2-3
- **Output**: 400+ lines (comprehensive docs, verification scripts, 40+ tests)

### Implementation Strategy

```python
EFFORT_CONFIGS = {
    'minimal': {
        'agents': ['planner', 'implementer', 'tester'],
        'max_iterations': 1,
        'skip_review': True,
        'skip_user': True,
        'planner_prompt_suffix': '\nIMPORTANT: Keep plan brief (2-3 paragraphs max).',
        'implementer_prompt_suffix': '\nIMPORTANT: Minimal implementation - basic solution.',
        'tester_prompt_suffix': '\nIMPORTANT: 5-10 test cases.',
        'reviewer_max_rounds': 0,
    },
    'moderate': {
        'agents': ['planner', 'implementer', 'reviewer', 'tester'],
        'max_iterations': 1,
        'skip_user': True,
        'reviewer_max_rounds': 1,
    },
    'maximum': {
        'agents': ['planner', 'implementer', 'reviewer', 'tester', 'user'],
        'max_iterations': 2,
        'skip_review': False,
        'skip_user': False,
        'reviewer_max_rounds': 3,
    }
}
```

### Expected Performance

| Effort | Time/Problem | Code Quality | Use Case |
|--------|--------------|--------------|----------|
| Minimal | 5-15 min | Working solution | LeetCode, quick prototypes |
| Moderate | 30-60 min | Good practices | Learning, side projects |
| Maximum | 2-3 hours | Production ready | Real software, critical code |

### Usage Examples

```bash
# Quick and dirty
uv run supervisor.py --effort minimal "solve two-sum"

# Balanced (default)
uv run supervisor.py --effort moderate "solve two-sum"

# Production quality
uv run supervisor.py --effort maximum "solve two-sum"

# Batch processing
./process_leetcode_batch.sh --effort minimal
# Process 10 problems in ~1-2 hours instead of 20-25 hours
```

### Benefits

1. **Speed**: Minimal effort = 10-20x faster than current
2. **Flexibility**: Choose appropriate level for task
3. **Cost**: Less API usage for simple tasks
4. **Practicality**: Makes multiagent-loop viable for LeetCode/practice
5. **Backward compatible**: Default to 'moderate', 'maximum' preserves current behavior

## Next Steps

### Implementation Phases

1. **Phase 1**: Add basic effort flag and configs (1-2 hours)
2. **Phase 2**: Implement prompt modifications (2-3 hours)
3. **Phase 3**: Test and tune each level (3-4 hours)
4. **Phase 4**: Update batch script and docs (1 hour)

**Total effort to implement**: ~1 day of development

### Open Questions

1. Should minimal skip type hints entirely, or require them?
2. Should minimal allow some input validation (TypeError) but skip ValueError?
3. Should we have a 4th level "ultra-minimal" with no tests at all?
4. How to handle continuous mode - should it auto-select effort based on task?

## Related

- Current behavior observed in fibonacci-number run (2h 40min)
- LeetCode batch processing needs
- process_leetcode_batch.sh script to be updated
