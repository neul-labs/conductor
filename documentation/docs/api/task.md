# Task API

The `Task` class defines what an agent should do.

## Module

```python
from agent.core.task import (
    Task,
    TaskType,
    TaskConstraints,
)
```

## Task

Dataclass representing a task for an agent to execute.

### Constructor

```python
Task(
    prompt: str,
    task_type: TaskType = TaskType.GENERAL,
    files: list[str] | None = None,
    context: dict[str, Any] | None = None,
    constraints: TaskConstraints | None = None,
    requires_consensus: bool = False,
    parent_task_id: str | None = None,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | Required | The instruction for the agent |
| `task_type` | `TaskType` | `GENERAL` | Type of task for routing |
| `files` | `list[str]` | `None` | Files to focus on |
| `context` | `dict` | `None` | Context from previous tasks |
| `constraints` | `TaskConstraints` | `None` | Execution constraints |
| `requires_consensus` | `bool` | `False` | Requires multi-agent agreement |
| `parent_task_id` | `str` | `None` | ID of parent task |

### Example

```python
from agent.core.task import Task, TaskType, TaskConstraints

task = Task(
    prompt="Implement user authentication",
    task_type=TaskType.CODE_CREATE,
    files=["src/auth.py", "src/models/user.py"],
    constraints=TaskConstraints(timeout=600),
)
```

### Methods

#### with_context

```python
def with_context(self, context: dict[str, Any]) -> Task:
    """Return a new Task with additional context."""
```

**Example:**
```python
task_with_ctx = task.with_context({
    "previous_output": "Research findings...",
    "files_modified": ["src/utils.py"],
})
```

#### with_prompt

```python
def with_prompt(self, prompt: str) -> Task:
    """Return a new Task with a different prompt."""
```

**Example:**
```python
new_task = task.with_prompt("Now implement the tests")
```

#### to_dict

```python
def to_dict(self) -> dict[str, Any]:
    """Convert task to dictionary."""
```

### Class Methods

#### from_prompt

```python
@classmethod
def from_prompt(cls, prompt: str) -> Task:
    """Create a Task from just a prompt string."""
```

**Example:**
```python
task = Task.from_prompt("Fix the authentication bug")
# task_type defaults to GENERAL
```

---

## TaskType

Enum of task types for routing.

### Values

| Value | Description |
|-------|-------------|
| `CODE_EDIT` | Modify existing code |
| `CODE_CREATE` | Create new code |
| `REFACTOR` | Restructure code |
| `BUG_FIX` | Fix a defect |
| `RESEARCH` | Investigate a topic |
| `REVIEW` | Evaluate code quality |
| `ANALYZE` | Deep analysis |
| `TEST_WRITE` | Write tests |
| `TEST_RUN` | Execute tests |
| `DOCUMENT` | Write documentation |
| `COMMIT` | Git commit |
| `PR_CREATE` | Create pull request |
| `GENERAL` | Catch-all |

### Example

```python
from agent.core.task import TaskType

# Use in task creation
task = Task(
    prompt="Add unit tests",
    task_type=TaskType.TEST_WRITE,
)

# Check task type
if task.task_type == TaskType.REFACTOR:
    print("This is a refactoring task")
```

### Routing Scores

Agents score tasks based on type:

| Agent | CODE_EDIT | REFACTOR | TEST_WRITE |
|-------|-----------|----------|------------|
| Claude | 0.85 | 0.95 | 0.75 |
| Codex | 0.85 | 0.70 | 0.90 |

---

## TaskConstraints

Dataclass for execution constraints.

### Constructor

```python
TaskConstraints(
    timeout: float = 300.0,
    allowed_tools: list[str] | None = None,
    max_tokens: int | None = None,
    working_directory: str = ".",
    auto_approve: bool = False,
    stream: bool = True,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `float` | `300.0` | Timeout in seconds |
| `allowed_tools` | `list[str]` | `None` | Allowed tools (None = all) |
| `max_tokens` | `int` | `None` | Token limit |
| `working_directory` | `str` | `"."` | Working directory |
| `auto_approve` | `bool` | `False` | Auto-approve actions |
| `stream` | `bool` | `True` | Stream output |

### Example

```python
from agent.core.task import TaskConstraints

# Read-only constraints
constraints = TaskConstraints(
    allowed_tools=["Read", "Glob", "Grep"],
    timeout=60,
)

# Auto-approve for automation
constraints = TaskConstraints(
    auto_approve=True,
    timeout=600,
)
```

### Methods

#### to_cli_args

```python
def to_cli_args(self) -> list[str]:
    """Convert constraints to CLI arguments."""
```

---

## Common Patterns

### Simple Task

```python
task = Task(prompt="Fix the bug")
```

### Typed Task

```python
task = Task(
    prompt="Refactor the authentication module",
    task_type=TaskType.REFACTOR,
)
```

### Task with Files

```python
task = Task(
    prompt="Add input validation",
    task_type=TaskType.CODE_EDIT,
    files=["src/handlers.py", "src/validators.py"],
)
```

### Constrained Task

```python
task = Task(
    prompt="Run the full test suite",
    task_type=TaskType.TEST_RUN,
    constraints=TaskConstraints(
        timeout=600,
        auto_approve=True,
    ),
)
```

### Task with Context

```python
# From previous result
context = result.as_context()

task = Task(
    prompt="Now implement the solution",
    context=context,
)

# Or manually
task = Task(
    prompt="Continue the implementation",
    context={
        "previous_output": "Analysis complete...",
        "files_modified": ["src/auth.py"],
        "session_id": "sess_123",
    },
)
```

### Chained Tasks

```python
# Original task
task1 = Task(prompt="Research patterns")
result1 = await agent.execute(task1)

# Create follow-up with context
task2 = task1.with_context(result1.as_context())
task2 = task2.with_prompt("Implement the patterns")
```

---

## Type Hints

```python
from agent.core.task import Task, TaskType, TaskConstraints

def create_refactor_task(
    prompt: str,
    files: list[str],
    timeout: float = 300.0,
) -> Task:
    return Task(
        prompt=prompt,
        task_type=TaskType.REFACTOR,
        files=files,
        constraints=TaskConstraints(timeout=timeout),
    )
```
