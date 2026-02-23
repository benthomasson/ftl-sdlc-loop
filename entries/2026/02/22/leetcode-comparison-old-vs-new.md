# LeetCode Comparison Old vs New

**Date:** 2026-02-22
**Time:** 20:23

## Overview

Comparison of LeetCode problem processing between old script-based experiment (~/data/leetcode) and new multiagent-loop system. Shows massive improvement in code quality, testing, and completeness - from proof-of-concept to production-ready autonomous development system.

## Details

### Architecture Comparison

| Aspect | Old Experiment | New Multiagent-Loop |
|--------|----------------|---------------------|
| **Architecture** | Script-based with `ftl-*-agent` tools | Multi-agent with Claude CLI instances |
| **Agents** | 3 specialized tools | 5 autonomous agents |
| **Coordination** | Bash script orchestration | Git-based with commits per stage |
| **Feedback Loops** | None - linear pipeline | 3 loops (Reviewer→Implementer, Tester→Implementer, User→Planner) |
| **Documentation** | Docstrings only | Planning + reviews + usage guides |
| **Testing** | Auto-generated pytest | Comprehensive + manual verification |
| **Iteration** | Single pass | Multiple iterations until satisfied |
| **Audit Trail** | Processing logs in .txt | Git commits + structured artifacts |

### Feature Comparison

**Old Experiment Generated:**
- ✅ Basic function implementation
- ✅ Type hints (ftl-doc-agent3)
- ✅ Google-style docstrings (ftl-doc-agent)
- ✅ Pytest tests (ftl-pytest-agent2)
- ✅ Coverage reports
- ⚠️ No planning phase
- ⚠️ No code review
- ⚠️ No usage verification
- ⚠️ No error handling
- ⚠️ No iterative improvement

**Multiagent-Loop Generated:**
- ✅ Comprehensive planning (PLAN.md)
- ✅ Type hints AND docstrings
- ✅ **Input validation and error handling**
- ✅ **Code review with feedback** (REVIEW.md)
- ✅ **Comprehensive test cases** (base, edge, invalid, properties)
- ✅ **Actual execution and usage verification**
- ✅ **Usage guide with examples** (USAGE.md)
- ✅ **User feedback** (USER_FEEDBACK.md)
- ✅ **Complete audit trail** (git log)
- ✅ **Self-review from every agent**
- ✅ **Beliefs tracking**
- ✅ **Iterative improvement**

### File Structure Comparison

**Old Experiment (two-sum):**
```
two-sum/
├── two-sum.py          # Original
├── code.py             # Basic
├── code2.py            # + type hints
├── code3.py            # + docstrings
├── code3.py,cover      # Coverage
├── test_twoSum.py      # Auto-generated
├── test_twoSum.txt     # Test output
├── output.txt          # Log
├── run.sh              # Pipeline
├── .coverage
├── coverage_total.txt
└── function_name.txt
```

**Multiagent-Loop (climbing-stairs):**
```
workspace/
├── TASK.md
├── PLAN.md                        # Planner output
├── IMPLEMENTATION.md              # Implementer notes
├── REVIEW.md                      # Reviewer feedback
├── USAGE.md                       # Tester guide
├── USER_FEEDBACK.md               # User report
├── ITERATION_1_UNDERSTANDING.md   # Cumulative knowledge
├── ITERATION_1_HUMAN_REVIEW.md
├── FINAL_REPORT.md
├── beliefs.md
├── implementer/
│   ├── climbing_stairs.py         # Production code
│   └── test_climbing_stairs.py    # 13 tests
├── tester/
│   ├── TEST_REPORT.md
│   ├── USAGE_GUIDE.md
│   └── manual_test.py
├── user/
│   └── test_usage.py
├── entries/iteration-1/
│   ├── planner.md
│   ├── implementer.md
│   ├── reviewer.md
│   ├── tester.md
│   └── user.md
└── .git/
```

### Code Quality Comparison

**Old Experiment (two-sum/code3.py):**
```python
def twoSum(nums: List[int], target: int) -> List[int]:
    """Finds two distinct indices..."""
    map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in map:
            return [map[complement], i]
        map[num] = i
    return []  # Empty on failure
```

**Issues:**
- ⚠️ No input validation
- ⚠️ No error handling
- ⚠️ Returns empty list on failure (not explicit)

**Multiagent-Loop (climbing_stairs.py):**
```python
def climbStairs(n: int) -> int:
    """Calculate distinct ways to climb n stairs.

    Mathematical explanation: Maps to Fibonacci...
    Time Complexity: O(n)
    Space Complexity: O(1)

    Examples:
        >>> climbStairs(1)
        1
    """
    # Input validation
    if not isinstance(n, int):
        raise ValueError(f"n must be integer, got {type(n).__name__}")
    if n < 1 or n > 45:
        raise ValueError(f"n must be [1,45], got {n}")

    # Base cases
    if n == 1: return 1
    if n == 2: return 2

    # Iterative DP with O(1) space
    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1
```

**Improvements:**
- ✅ Complexity analysis documented
- ✅ Mathematical explanation
- ✅ Input validation with type checking
- ✅ Range validation
- ✅ Clear error messages
- ✅ Explicit exception raising

### Test Quality Comparison

**Old Experiment:**
- Basic assertions (1-3 test cases)
- No edge cases
- No invalid input testing

**Multiagent-Loop (13 test cases):**
- Base cases (n=1, n=2)
- Problem examples
- Small/medium/large values
- Maximum constraint (n=45)
- **Invalid inputs** (too small, too large, wrong type)
- **Mathematical properties** (Fibonacci recurrence)
- **Sequential consistency**

## Next Steps

The multiagent-loop represents a massive upgrade:

1. **Quality**: Production-ready with error handling
2. **Completeness**: Full SDLC pipeline
3. **Documentation**: Comprehensive at every stage
4. **Testing**: Thorough edge case coverage
5. **Feedback**: Multiple review loops
6. **Audit Trail**: Full git history
7. **Self-Improvement**: Friction point identification
8. **Iteration**: User feedback incorporation

**Verdict**: Old = proof-of-concept. New = **complete autonomous software development system**.

## Related

- Old experiment location: `~/data/leetcode/leetcode/`
- New system: `~/git/multiagent-loop/`
- See: `effort-levels-implemented.md` (speed optimization)
- Example runs: fibonacci-number (2h 40min), plus-one (2min minimal)
