# Sequential Pattern

Execute tasks in a pipeline, with context flowing forward between steps.

## Overview

The Sequential pattern runs tasks one after another:

```
Task 1 → Task 2 → Task 3 → Task 4
   |         |        |        |
   +-- ctx --+-- ctx -+-- ctx -+
```

Each task receives context from all previous tasks, enabling complex multi-step workflows.

## When to Use

- **Development pipelines**: Research → Implement → Test → Document
- **Refactoring workflows**: Analyze → Plan → Execute → Verify
- **Step-by-step processes**: Any workflow where steps depend on previous results

## CLI Usage

```bash
# Basic sequential pipeline
agent orchestrate \
    "Research authentication best practices" \
    "Implement JWT authentication" \
    "Write comprehensive tests" \
    "Document the API"

# Each prompt becomes a task executed in order
```

## Python API

```python
from agent.core.task import Task, TaskType
from agent.orchestration import Supervisor, OrchestrationPattern

supervisor = Supervisor(agents)

tasks = [
    Task(prompt="Research caching strategies", task_type=TaskType.RESEARCH),
    Task(prompt="Implement Redis caching", task_type=TaskType.CODE_CREATE),
    Task(prompt="Write integration tests", task_type=TaskType.TEST_WRITE),
    Task(prompt="Update documentation", task_type=TaskType.DOCUMENT),
]

result = await supervisor.orchestrate(
    tasks=tasks,
    pattern=OrchestrationPattern.SEQUENTIAL,
)
```

## Context Flow

Context accumulates through the pipeline:

### After Task 1

```python
context = {
    "previous_output": "Research findings: JWT is recommended...",
    "files_modified": [],
    "commands_run": [],
    "success": True,
    "previous_agent": "claude",
}
```

### After Task 2

```python
context = {
    "previous_output": "Implemented JWT auth in src/auth.py...",
    "files_modified": ["src/auth.py", "src/models/token.py"],
    "commands_run": [],
    "success": True,
    "session_id": "sess_123",
    "previous_agent": "claude",
}
```

### After Task 3

```python
context = {
    "previous_output": "Tests written and passing...",
    "files_modified": ["src/auth.py", "src/models/token.py", "tests/test_auth.py"],
    "commands_run": ["pytest tests/test_auth.py"],
    "success": True,
    "session_id": "sess_456",
    "previous_agent": "codex",
}
```

## Agent Selection

For each task, the supervisor selects the best agent:

```python
# Task 1: RESEARCH → Gemini (0.90) or Claude (0.85)
# Task 2: CODE_CREATE → Claude (0.85) or Codex (0.90)
# Task 3: TEST_WRITE → Codex (0.90)
# Task 4: DOCUMENT → Claude (0.85)
```

Different agents may handle different tasks based on their strengths.

## Stop on Failure

By default, the pipeline stops if any task fails:

```python
# If Task 2 fails:
# - Task 3 and 4 are skipped
# - result.success = False
# - result.error contains failure reason
```

Using the pattern directly:

```python
from agent.orchestration.patterns import SequentialPattern

pattern = SequentialPattern(
    agents=agents,
    stop_on_failure=True,  # Default
)

result = await pattern.execute(tasks)
```

Set `stop_on_failure=False` to continue despite failures:

```python
pattern = SequentialPattern(
    agents=agents,
    stop_on_failure=False,  # Continue on failure
)
```

## Examples

### Development Pipeline

```bash
agent orchestrate \
    "Analyze the current authentication implementation" \
    "Design improvements using OAuth 2.0" \
    "Implement the OAuth integration" \
    "Add comprehensive test coverage" \
    "Update the API documentation"
```

### Bug Fix Workflow

```bash
agent orchestrate \
    "Investigate the null pointer exception in UserService" \
    "Implement a fix for the issue" \
    "Add a regression test" \
    "Verify all existing tests still pass"
```

### Refactoring Pipeline

```bash
agent orchestrate \
    "Analyze the monolithic service for extraction candidates" \
    "Extract the payment logic into a separate module" \
    "Update all imports and references" \
    "Run the test suite and fix any failures"
```

### Code Review Process

```bash
agent orchestrate \
    "Read and understand the changes in this PR" \
    "Identify potential bugs or issues" \
    "Check for security vulnerabilities" \
    "Suggest improvements and optimizations"
```

## Result Structure

```python
result = await supervisor.orchestrate(tasks, OrchestrationPattern.SEQUENTIAL)

# Overall result
print(result.success)           # True if all tasks succeeded
print(result.pattern)           # "sequential"
print(result.total_duration_ms) # Sum of all task durations
print(result.total_cost_usd)    # Sum of all task costs
print(result.all_files_modified) # All files changed across tasks

# Individual task results
for i, task_result in enumerate(result.results):
    print(f"Task {i+1}:")
    print(f"  Agent: {task_result.metadata.agent}")
    print(f"  Success: {task_result.success}")
    print(f"  Output: {task_result.output[:100]}...")
    print(f"  Files: {task_result.files_modified}")
```

## Tips

1. **Order matters**: Place dependent tasks after their dependencies
2. **Be specific**: Clear prompts help agents understand context
3. **Check intermediate results**: Each task result is available
4. **Use task types**: Help with agent routing
5. **Handle failures**: Check `result.success` and individual results

## Limitations

- **No parallelism**: Tasks run sequentially, not concurrently
- **Single path**: No branching or conditional execution
- **Context size**: Very long pipelines may have large context

## See Also

- [Parallel Pattern](parallel.md) - Concurrent execution
- [Consensus Pattern](consensus.md) - Multi-agent agreement
- [CLI: orchestrate](../cli/orchestrate.md) - Command reference
