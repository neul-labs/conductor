# Core Concepts

Understanding Agent's core abstractions is key to using it effectively.

## Overview

Agent is built around four core concepts:

```
+--------+     +-----------+     +--------+
|  Task  | --> |   Agent   | --> | Result |
+--------+     +-----------+     +--------+
                    ^
                    |
              +-----------+
              | Supervisor|
              +-----------+
```

| Concept | Description |
|---------|-------------|
| [Task](tasks.md) | What you want done - the prompt, type, and constraints |
| [Agent](agents.md) | Who does the work - wraps an AI CLI tool |
| [Result](results.md) | What happened - output, actions, and metadata |
| [Supervisor](supervisor.md) | The orchestrator - coordinates agents and patterns |

## How It Works

### 1. Define a Task

A Task describes what you want to accomplish:

```python
from agent.core.task import Task, TaskType

task = Task(
    prompt="Implement user authentication",
    task_type=TaskType.CODE_CREATE,
    files=["src/auth.py"],
)
```

### 2. Agent Executes

The Supervisor routes the task to the best-suited Agent:

```python
from agent.agents import ClaudeAgent

agent = ClaudeAgent()
result = await agent.execute(task)
```

### 3. Result Returned

The Result contains everything that happened:

```python
print(result.success)          # True
print(result.output)           # "Implemented JWT auth..."
print(result.files_modified)   # ["src/auth.py"]
print(result.actions)          # [Action(FILE_EDIT, ...), ...]
```

## The Supervisor

The Supervisor is the brain of Agent. It:

1. **Routes** tasks to the best agent based on capabilities
2. **Orchestrates** complex workflows using patterns
3. **Aggregates** results from multiple agents

```python
from agent.orchestration import Supervisor, OrchestrationPattern
from agent.agents import ClaudeAgent, CodexAgent

supervisor = Supervisor([ClaudeAgent(), CodexAgent()])

# Single task - supervisor picks best agent
result = await supervisor.run_single(task)

# Multiple tasks - supervisor orchestrates
result = await supervisor.orchestrate(
    tasks=[task1, task2, task3],
    pattern=OrchestrationPattern.SEQUENTIAL,
)
```

## Capabilities

Each agent declares its capabilities:

| Capability | Description |
|------------|-------------|
| `EXECUTE` | Can execute prompts |
| `STREAM` | Can stream responses |
| `FILE_EDIT` | Can edit existing files |
| `FILE_CREATE` | Can create new files |
| `COMMAND_RUN` | Can run shell commands |
| `GIT_COMMIT` | Can make git commits |
| `MCP` | Supports MCP tools |
| `WEB_ACCESS` | Can access the web |
| `SANDBOX` | Runs in isolated environment |

The Supervisor uses these to route tasks intelligently.

## Task Types

Tasks have types that help with routing:

| Type | Description | Best Agent |
|------|-------------|------------|
| `CODE_EDIT` | Modify existing code | Claude |
| `CODE_CREATE` | Create new code | Claude, Codex |
| `REFACTOR` | Restructure code | Claude |
| `RESEARCH` | Investigate a topic | Gemini |
| `REVIEW` | Review code quality | Claude |
| `TEST_WRITE` | Write tests | Codex |
| `TEST_RUN` | Run tests | Codex |
| `DOCUMENT` | Write documentation | Claude |

## Next Steps

Dive deeper into each concept:

- [Agents](agents.md) - How agents work and their capabilities
- [Tasks](tasks.md) - Task types, constraints, and context
- [Results](results.md) - Actions, metadata, and error handling
- [Supervisor](supervisor.md) - Orchestration and pattern selection
