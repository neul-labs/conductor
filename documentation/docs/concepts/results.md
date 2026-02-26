# Results

Results capture everything that happened when an agent executed a task.

## Overview

A Result contains:

- **Success**: Whether the task succeeded
- **Output**: The text response from the agent
- **Actions**: All actions taken (file edits, commands, etc.)
- **Metadata**: Agent name, duration, tokens, cost
- **Session ID**: For continuing sessions

## Result Structure

```python
from agent.core.result import Result

result = await agent.execute(task)

print(result.success)        # True or False
print(result.output)         # "I've implemented the feature..."
print(result.error)          # None or error message
print(result.session_id)     # "abc123" for session continuation
print(result.created_at)     # datetime when created
```

## Actions

Actions track exactly what the agent did:

```python
for action in result.actions:
    print(f"{action.type}: {action.details}")
```

### Action Types

| Type | Description | Details |
|------|-------------|---------|
| `FILE_CREATE` | Created a file | `{"path": "..."}` |
| `FILE_EDIT` | Modified a file | `{"path": "...", "before": "...", "after": "..."}` |
| `FILE_DELETE` | Deleted a file | `{"path": "..."}` |
| `FILE_READ` | Read a file | `{"path": "..."}` |
| `COMMAND_RUN` | Ran a command | `{"command": "..."}` |
| `GIT_COMMIT` | Made a commit | `{"message": "...", "sha": "..."}` |
| `GIT_PUSH` | Pushed to remote | `{"branch": "..."}` |
| `GIT_BRANCH` | Created a branch | `{"name": "..."}` |
| `WEB_FETCH` | Fetched URL | `{"url": "..."}` |
| `WEB_SEARCH` | Searched web | `{"query": "..."}` |
| `MCP_TOOL` | Used MCP tool | `{"tool": "...", "args": {...}}` |

### Action Details

Each action has detailed information:

```python
from agent.core.result import Action, ActionType

action = Action(
    type=ActionType.FILE_EDIT,
    details={"path": "src/auth.py", "lines_changed": 15},
    before="def login():\n    pass",
    after="def login(username, password):\n    ...",
    timestamp=datetime.now(),
    success=True,
    error=None,
)

# Convenient properties
print(action.path)     # "src/auth.py"
print(action.command)  # None (only for COMMAND_RUN)
```

## Convenience Properties

Results provide shortcuts for common queries:

```python
# Files modified
print(result.files_modified)
# ["src/auth.py", "src/models/user.py"]

# Commands run
print(result.commands_run)
# ["pytest tests/", "ruff check src/"]
```

## Metadata

Results include execution metadata:

```python
meta = result.metadata

print(meta.agent)         # "claude"
print(meta.duration_ms)   # 1234
print(meta.input_tokens)  # 500
print(meta.output_tokens) # 1200
print(meta.cost_usd)      # 0.05
print(meta.model)         # "claude-3-5-sonnet"
print(meta.raw_output)    # Raw CLI output (for debugging)
```

## Serialization

Results can be serialized for storage or transmission:

```python
# To dictionary
result_dict = result.to_dict()

# To JSON
result_json = result.to_json()
```

## Context for Next Task

Convert a result to context for the next task:

```python
# Get context dict
context = result.as_context()
# {
#     "previous_output": "...",
#     "files_modified": [...],
#     "commands_run": [...],
#     "success": True,
#     "session_id": "abc123",
#     "previous_agent": "claude",
# }

# Use in next task
next_task = task.with_context(context)
```

## Orchestrated Results

When orchestrating multiple agents, results are aggregated:

```python
from agent.core.result import OrchestratedResult

orch_result: OrchestratedResult = await supervisor.orchestrate(tasks, pattern)

print(orch_result.success)          # Overall success
print(orch_result.pattern)          # "sequential" or "parallel"
print(orch_result.consensus_score)  # 0.8 (for consensus pattern)
print(orch_result.error)            # None or error message

# Individual results
for result in orch_result.results:
    print(f"{result.metadata.agent}: {result.success}")

# Aggregated metrics
print(orch_result.total_duration_ms)   # 5000
print(orch_result.total_cost_usd)      # 0.15
print(orch_result.all_files_modified)  # ["a.py", "b.py", ...]
```

## Error Handling

Handle failures gracefully:

```python
result = await agent.execute(task)

if result.success:
    print("Task completed successfully")
    print(result.output)
else:
    print(f"Task failed: {result.error}")

    # Check which actions failed
    for action in result.actions:
        if not action.success:
            print(f"Failed: {action.type} - {action.error}")
```

## JSON Output

For programmatic use, request JSON output:

```python
task = Task(
    prompt="List all Python files",
    constraints=TaskConstraints(stream=False),
)

result = await agent.execute(task)
print(result.to_json())
```

```json
{
  "success": true,
  "output": "Found 15 Python files in src/",
  "actions": [
    {
      "type": "FILE_READ",
      "details": {"path": "src/"},
      "success": true
    }
  ],
  "metadata": {
    "agent": "claude",
    "duration_ms": 523,
    "model": "claude-3-5-sonnet"
  },
  "session_id": "sess_abc123"
}
```

## Next Steps

- [Supervisor](supervisor.md) - How results flow through orchestration
- [Patterns](../patterns/index.md) - Result aggregation strategies
- [CLI Reference](../cli/index.md) - Output formats
