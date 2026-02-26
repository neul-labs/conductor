# Tasks

A Task defines what you want an agent to do.

## Overview

Tasks contain:

- **Prompt**: The instruction for the agent
- **Type**: The kind of work (code edit, review, test, etc.)
- **Files**: Optional files to focus on
- **Context**: Information from previous tasks
- **Constraints**: Timeout, allowed tools, etc.

## Creating Tasks

### Simple Task

```python
from agent.core.task import Task

task = Task(prompt="Fix the bug in authentication")
```

### Task with Type

```python
from agent.core.task import Task, TaskType

task = Task(
    prompt="Refactor the user service",
    task_type=TaskType.REFACTOR,
)
```

### Task with Files

```python
task = Task(
    prompt="Add input validation",
    task_type=TaskType.CODE_EDIT,
    files=["src/api/handlers.py", "src/api/validators.py"],
)
```

### Task with Constraints

```python
from agent.core.task import Task, TaskConstraints

task = Task(
    prompt="Run the test suite",
    task_type=TaskType.TEST_RUN,
    constraints=TaskConstraints(
        timeout=600,  # 10 minutes
        auto_approve=True,
    ),
)
```

## Task Types

Task types help route tasks to the right agent:

| Type | Description | Example Prompt |
|------|-------------|----------------|
| `CODE_EDIT` | Modify existing code | "Add error handling to login()" |
| `CODE_CREATE` | Create new code | "Create a cache service" |
| `REFACTOR` | Restructure code | "Extract method from this class" |
| `BUG_FIX` | Fix a defect | "Fix the null pointer exception" |
| `RESEARCH` | Investigate | "How do other projects handle auth?" |
| `REVIEW` | Evaluate code | "Review this PR for issues" |
| `ANALYZE` | Deep analysis | "Analyze performance bottlenecks" |
| `TEST_WRITE` | Write tests | "Add unit tests for UserService" |
| `TEST_RUN` | Execute tests | "Run the test suite" |
| `DOCUMENT` | Write docs | "Document the API endpoints" |
| `COMMIT` | Git commit | "Commit the authentication changes" |
| `PR_CREATE` | Pull request | "Create PR for feature branch" |
| `GENERAL` | Catch-all | Any other task |

### From Prompt

Create a task from just a prompt string:

```python
task = Task.from_prompt("Fix the authentication bug")
# task_type defaults to GENERAL
```

## Constraints

Control how tasks execute:

```python
from agent.core.task import TaskConstraints

constraints = TaskConstraints(
    timeout=300,           # Timeout in seconds (default: 300)
    allowed_tools=None,    # List of allowed tools, or None for all
    max_tokens=None,       # Token limit for response
    working_directory=".", # Working directory
    auto_approve=False,    # Auto-approve actions
    stream=True,           # Stream output
)
```

### Timeout

Set a maximum execution time:

```python
task = Task(
    prompt="Run comprehensive tests",
    constraints=TaskConstraints(timeout=600),  # 10 minutes
)
```

### Tool Allowlisting

Restrict which tools the agent can use:

```python
task = Task(
    prompt="Analyze the code structure",
    constraints=TaskConstraints(
        allowed_tools=["Read", "Glob", "Grep"],  # Read-only
    ),
)
```

### Auto-Approve

Skip confirmation prompts:

```python
task = Task(
    prompt="Format all Python files",
    constraints=TaskConstraints(auto_approve=True),
)
```

## Context

Tasks can carry context from previous tasks:

```python
# First task
task1 = Task(prompt="Research caching patterns")
result1 = await agent.execute(task1)

# Second task with context
task2 = task1.with_context({
    "previous_output": result1.output,
    "files_modified": result1.files_modified,
})
task2 = task2.with_prompt("Implement the caching strategy")
```

### Context Fields

Common context fields passed between tasks:

| Field | Description |
|-------|-------------|
| `previous_output` | Output from previous task |
| `files_modified` | Files changed by previous task |
| `commands_run` | Commands executed |
| `session_id` | Session ID for continuation |
| `previous_agent` | Name of previous agent |

## Task Factory

Create tasks programmatically:

```python
# Simple factory function
def code_task(prompt: str, files: list[str]) -> Task:
    return Task(
        prompt=prompt,
        task_type=TaskType.CODE_EDIT,
        files=files,
        constraints=TaskConstraints(
            timeout=300,
            stream=True,
        ),
    )

task = code_task("Add validation", ["src/api.py"])
```

## Serialization

Tasks can be serialized:

```python
# To dictionary
task_dict = task.to_dict()

# To JSON (via dict)
import json
task_json = json.dumps(task.to_dict())
```

## CLI to Task

The CLI creates tasks from command arguments:

```bash
agent run "Fix the bug"
# Creates: Task(prompt="Fix the bug", task_type=GENERAL)

agent run --agent claude "Refactor auth"
# Creates task and routes to Claude
```

## Next Steps

- [Agents](agents.md) - Who executes tasks
- [Results](results.md) - What tasks return
- [Patterns](../patterns/index.md) - How tasks are orchestrated
