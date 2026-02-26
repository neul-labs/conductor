# Result API

The `Result` class contains everything that happened when an agent executed a task.

## Module

```python
from agent.core.result import (
    Result,
    Action,
    ActionType,
    ResultMetadata,
    OrchestratedResult,
)
```

## Result

Dataclass representing the outcome of task execution.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | Whether the task succeeded |
| `output` | `str` | The text response |
| `actions` | `list[Action]` | Actions taken |
| `metadata` | `ResultMetadata` | Execution metadata |
| `session_id` | `str \| None` | Session ID for continuation |
| `error` | `str \| None` | Error message if failed |
| `created_at` | `datetime` | When the result was created |

### Properties

#### files_modified

```python
@property
def files_modified(self) -> list[str]:
    """List of files that were modified."""
```

**Example:**
```python
for path in result.files_modified:
    print(f"Modified: {path}")
```

#### commands_run

```python
@property
def commands_run(self) -> list[str]:
    """List of commands that were executed."""
```

**Example:**
```python
for cmd in result.commands_run:
    print(f"Ran: {cmd}")
```

### Methods

#### to_dict

```python
def to_dict(self) -> dict[str, Any]:
    """Convert result to dictionary."""
```

#### to_json

```python
def to_json(self) -> str:
    """Convert result to JSON string."""
```

**Example:**
```python
import json
data = json.loads(result.to_json())
```

#### as_context

```python
def as_context(self) -> dict[str, Any]:
    """Convert result to context for next task."""
```

**Returns:**
```python
{
    "previous_output": "...",
    "files_modified": [...],
    "commands_run": [...],
    "success": True,
    "session_id": "...",
    "previous_agent": "...",
}
```

**Example:**
```python
# Pass result as context to next task
next_task = Task(
    prompt="Continue implementation",
    context=result.as_context(),
)
```

---

## Action

Dataclass representing a single action taken by an agent.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | `ActionType` | Type of action |
| `details` | `dict` | Action-specific details |
| `before` | `str \| None` | State before (for edits) |
| `after` | `str \| None` | State after (for edits) |
| `timestamp` | `datetime` | When action occurred |
| `success` | `bool` | Whether action succeeded |
| `error` | `str \| None` | Error if failed |

### Properties

#### path

```python
@property
def path(self) -> str | None:
    """Get the file path from details."""
```

#### command

```python
@property
def command(self) -> str | None:
    """Get the command from details."""
```

### Example

```python
for action in result.actions:
    print(f"{action.type}: {action.details}")

    if action.type == ActionType.FILE_EDIT:
        print(f"  Path: {action.path}")
        print(f"  Before: {action.before[:50]}...")
        print(f"  After: {action.after[:50]}...")

    if action.type == ActionType.COMMAND_RUN:
        print(f"  Command: {action.command}")
```

---

## ActionType

Enum of action types.

### Values

| Value | Description | Details Keys |
|-------|-------------|--------------|
| `FILE_CREATE` | Created a file | `path` |
| `FILE_EDIT` | Modified a file | `path`, `lines_changed` |
| `FILE_DELETE` | Deleted a file | `path` |
| `FILE_READ` | Read a file | `path` |
| `COMMAND_RUN` | Ran a command | `command`, `exit_code` |
| `GIT_COMMIT` | Made a commit | `message`, `sha` |
| `GIT_PUSH` | Pushed to remote | `branch`, `remote` |
| `GIT_BRANCH` | Created a branch | `name` |
| `WEB_FETCH` | Fetched URL | `url` |
| `WEB_SEARCH` | Searched web | `query` |
| `MCP_TOOL` | Used MCP tool | `tool`, `args` |
| `OTHER` | Other action | varies |

### Example

```python
from agent.core.result import ActionType

# Check action type
if action.type == ActionType.FILE_EDIT:
    print(f"Edited {action.path}")

# Filter actions
edits = [a for a in result.actions if a.type == ActionType.FILE_EDIT]
commands = [a for a in result.actions if a.type == ActionType.COMMAND_RUN]
```

---

## ResultMetadata

Dataclass containing execution metadata.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `agent` | `str` | Agent name |
| `duration_ms` | `int` | Execution time in ms |
| `input_tokens` | `int \| None` | Input tokens used |
| `output_tokens` | `int \| None` | Output tokens used |
| `cost_usd` | `float \| None` | Estimated cost |
| `model` | `str \| None` | Model used |
| `raw_output` | `str \| None` | Raw CLI output |

### Example

```python
meta = result.metadata

print(f"Agent: {meta.agent}")
print(f"Duration: {meta.duration_ms}ms")
print(f"Tokens: {meta.input_tokens} in, {meta.output_tokens} out")
print(f"Cost: ${meta.cost_usd:.4f}")
```

---

## OrchestratedResult

Dataclass for multi-agent orchestration results.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | `bool` | Overall success |
| `results` | `list[Result]` | Individual results |
| `pattern` | `str` | Pattern used |
| `consensus_score` | `float \| None` | Consensus score |
| `error` | `str \| None` | Error if failed |

### Properties

#### total_duration_ms

```python
@property
def total_duration_ms(self) -> int:
    """Total execution time across all agents."""
```

#### total_cost_usd

```python
@property
def total_cost_usd(self) -> float:
    """Total cost across all agents."""
```

#### all_files_modified

```python
@property
def all_files_modified(self) -> list[str]:
    """All files modified by all agents."""
```

### Example

```python
result = await supervisor.orchestrate(tasks, pattern)

print(f"Success: {result.success}")
print(f"Pattern: {result.pattern}")
print(f"Total time: {result.total_duration_ms}ms")
print(f"Total cost: ${result.total_cost_usd:.2f}")

# Individual results
for r in result.results:
    print(f"  {r.metadata.agent}: {r.success}")

# Consensus
if result.consensus_score is not None:
    print(f"Consensus: {result.consensus_score:.0%}")
```

---

## Common Patterns

### Check Success

```python
result = await agent.execute(task)

if result.success:
    print(result.output)
else:
    print(f"Failed: {result.error}")
```

### Iterate Actions

```python
for action in result.actions:
    if action.success:
        print(f"OK: {action.type}")
    else:
        print(f"FAILED: {action.type} - {action.error}")
```

### Get Files Changed

```python
files = result.files_modified
print(f"Changed {len(files)} files:")
for f in files:
    print(f"  - {f}")
```

### Chain Results

```python
# First task
result1 = await agent.execute(task1)

# Use as context for second task
task2 = Task(
    prompt="Continue...",
    context=result1.as_context(),
)
result2 = await agent.execute(task2)
```

### JSON Output

```python
# For APIs/storage
json_str = result.to_json()

# For processing
data = result.to_dict()
```

---

## Type Hints

```python
from agent.core.result import (
    Result,
    OrchestratedResult,
    Action,
    ActionType,
)

def process_result(result: Result) -> None:
    for action in result.actions:
        handle_action(action)

def handle_action(action: Action) -> None:
    if action.type == ActionType.FILE_EDIT:
        print(f"Edited: {action.path}")
```
