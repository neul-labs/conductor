# Parallel Pattern

Execute a single task across all agents simultaneously.

## Overview

The Parallel pattern runs one task on all available agents concurrently:

```
              Task
                |
    +-----------+-----------+
    |           |           |
 Claude      Codex       Gemini
    |           |           |
    v           v           v
 Result 1   Result 2    Result 3
    |           |           |
    +-----------+-----------+
                |
         Aggregated Result
```

All agents work independently, and results are combined.

## When to Use

- **Code review**: Get multiple perspectives on the same code
- **Analysis**: Comprehensive analysis from different viewpoints
- **Validation**: Cross-check answers before proceeding
- **Research**: Gather information from agents with different strengths

## CLI Usage

```bash
# Parallel execution on all agents
agent orchestrate --pattern parallel \
    "Review src/api.py for bugs, security issues, and performance problems"

# Parallel with specific agents
agent orchestrate --pattern parallel --agents claude,codex \
    "Analyze this pull request"
```

## Python API

```python
from agent.core.task import Task, TaskType
from agent.orchestration import Supervisor, OrchestrationPattern

supervisor = Supervisor([ClaudeAgent(), CodexAgent(), GeminiAgent()])

review_task = Task(
    prompt="Review this code for issues",
    task_type=TaskType.REVIEW,
)

result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)

# Each agent's result
for r in result.results:
    print(f"--- {r.metadata.agent} ---")
    print(r.output)
```

## Agent Independence

Each agent works independently:

- **No shared context**: Agents don't see each other's work
- **Concurrent execution**: All run at the same time
- **Independent results**: Each produces its own result

## Success Criteria

The parallel pattern succeeds if **any** agent succeeds:

```python
# 3 agents run
# 2 succeed, 1 fails
# result.success = True (any succeeded)
```

This is useful for getting diverse perspectives even if some agents struggle.

## Examples

### Comprehensive Code Review

```bash
agent orchestrate --pattern parallel \
    "Review the following code for:
     - Bugs and logic errors
     - Security vulnerabilities
     - Performance issues
     - Code style and best practices
     - Test coverage gaps"
```

Each agent provides its own analysis, giving you multiple perspectives.

### Security Audit

```bash
agent orchestrate --pattern parallel --agents claude,codex \
    "Audit src/auth/ for security vulnerabilities:
     - Authentication bypasses
     - SQL injection
     - XSS vulnerabilities
     - Insecure cryptography
     - Sensitive data exposure"
```

### Architecture Analysis

```bash
agent orchestrate --pattern parallel \
    "Analyze the architecture of this codebase:
     - Identify design patterns used
     - Find architectural issues
     - Suggest improvements"
```

### Research Task

```bash
agent orchestrate --pattern parallel \
    "Research best practices for implementing rate limiting in Python.
     Include code examples and library recommendations."
```

## Result Structure

```python
result = await supervisor.orchestrate(
    tasks=[task],
    pattern=OrchestrationPattern.PARALLEL,
)

# Overall result
print(result.success)            # True if any agent succeeded
print(result.pattern)            # "parallel"
print(result.total_duration_ms)  # Time for slowest agent
print(len(result.results))       # Number of agent results

# Individual results
for r in result.results:
    print(f"Agent: {r.metadata.agent}")
    print(f"Success: {r.success}")
    print(f"Duration: {r.metadata.duration_ms}ms")
    print(f"Output preview: {r.output[:200]}...")
    print()
```

## Filtering Agents

Limit which agents participate:

```bash
# Only Claude and Codex
agent orchestrate --pattern parallel --agents claude,codex \
    "Review this code"
```

```python
result = await supervisor.orchestrate(
    tasks=[task],
    pattern=OrchestrationPattern.PARALLEL,
    agent_names=["claude", "codex"],  # Exclude others
)
```

## Aggregating Results

Results from parallel execution can be aggregated:

```python
result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)

# Combine all outputs
combined_review = "\n\n".join([
    f"## {r.metadata.agent}\n{r.output}"
    for r in result.results
    if r.success
])

# Collect all files mentioned
all_files = set()
for r in result.results:
    all_files.update(r.files_modified)

# Find common issues (mentioned by multiple agents)
# ... custom analysis logic
```

## Performance

Parallel execution is faster than sequential for getting multiple perspectives:

```
Sequential: Agent1 (3s) → Agent2 (2s) → Agent3 (4s) = 9s total
Parallel:   All agents concurrently = 4s (slowest agent)
```

The total time equals the slowest agent's time.

## Tips

1. **Craft good prompts**: All agents see the same prompt
2. **Aggregate thoughtfully**: Consider how to combine outputs
3. **Use for reviews**: Get diverse perspectives
4. **Filter when needed**: Not all agents are needed for every task
5. **Check all results**: Even failed agents may have partial insights

## Limitations

- **Single task only**: Multiple prompts use sequential
- **No context sharing**: Agents work independently
- **Resource intensive**: Uses more API calls

## Difference from Consensus

| Aspect | Parallel | Consensus |
|--------|----------|-----------|
| **Goal** | Multiple perspectives | Agreement validation |
| **Success** | Any agent succeeds | Threshold of agreement |
| **Result** | All outputs preserved | Pass/fail decision |
| **Use case** | Reviews, analysis | Safety checks |

## See Also

- [Sequential Pattern](sequential.md) - Pipeline execution
- [Consensus Pattern](consensus.md) - Agreement validation
- [CLI: orchestrate](../cli/orchestrate.md) - Command reference
