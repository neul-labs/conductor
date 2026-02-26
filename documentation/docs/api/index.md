# Python API Reference

Agent provides a full Python API for programmatic control over agent orchestration.

## Installation

```bash
pip install agent
```

## Quick Start

```python
import asyncio
from agent.core.task import Task, TaskType
from agent.agents import ClaudeAgent, CodexAgent
from agent.orchestration import Supervisor, OrchestrationPattern

async def main():
    # Create supervisor with agents
    supervisor = Supervisor([ClaudeAgent(), CodexAgent()])

    # Define tasks
    tasks = [
        Task(prompt="Research caching patterns", task_type=TaskType.RESEARCH),
        Task(prompt="Implement Redis caching", task_type=TaskType.CODE_CREATE),
        Task(prompt="Write tests", task_type=TaskType.TEST_WRITE),
    ]

    # Run orchestration
    result = await supervisor.orchestrate(
        tasks=tasks,
        pattern=OrchestrationPattern.SEQUENTIAL,
    )

    print(f"Success: {result.success}")
    print(f"Files modified: {result.all_files_modified}")
    print(f"Total cost: ${result.total_cost_usd:.2f}")

asyncio.run(main())
```

## Module Structure

```
agent/
├── core/
│   ├── agent.py      # Agent ABC, capabilities, registry
│   ├── task.py       # Task, TaskType, TaskConstraints
│   └── result.py     # Result, Action, OrchestratedResult
├── agents/
│   ├── claude.py     # ClaudeAgent
│   └── codex.py      # CodexAgent
├── orchestration/
│   ├── supervisor.py # Supervisor, OrchestrationPattern
│   └── patterns/     # Sequential, Parallel patterns
└── utils/
    └── process.py    # Command execution utilities
```

## API Reference

| Module | Description |
|--------|-------------|
| [Agent](agent.md) | Agent base class and capabilities |
| [Task](task.md) | Task definition and types |
| [Result](result.md) | Result and action tracking |
| [Supervisor](supervisor.md) | Orchestration coordinator |

## Core Classes

### Agent

Abstract base class for all agents:

```python
from agent.core.agent import Agent, AgentCapabilities

class MyAgent(Agent):
    @property
    def name(self) -> str:
        return "my-agent"

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities.EXECUTE | AgentCapabilities.FILE_EDIT

    async def execute(self, task: Task) -> Result:
        ...
```

### Task

Defines what an agent should do:

```python
from agent.core.task import Task, TaskType, TaskConstraints

task = Task(
    prompt="Implement feature X",
    task_type=TaskType.CODE_CREATE,
    files=["src/feature.py"],
    constraints=TaskConstraints(timeout=600),
)
```

### Result

Contains execution outcome:

```python
from agent.core.result import Result

result = await agent.execute(task)
print(result.success)
print(result.output)
print(result.files_modified)
```

### Supervisor

Coordinates agents and patterns:

```python
from agent.orchestration import Supervisor, OrchestrationPattern

supervisor = Supervisor(agents)
result = await supervisor.orchestrate(tasks, OrchestrationPattern.PARALLEL)
```

## Common Patterns

### Single Task Execution

```python
from agent.agents import ClaudeAgent
from agent.core.task import Task

agent = ClaudeAgent()
task = Task(prompt="Fix the bug")
result = await agent.execute(task)
```

### Sequential Pipeline

```python
from agent.orchestration import Supervisor, OrchestrationPattern

result = await supervisor.orchestrate(
    tasks=[task1, task2, task3],
    pattern=OrchestrationPattern.SEQUENTIAL,
)
```

### Parallel Review

```python
result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)
```

### Consensus Validation

```python
result = await supervisor.orchestrate(
    tasks=[validation_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.8,
)
```

## Error Handling

```python
try:
    result = await supervisor.orchestrate(tasks, pattern)
    if result.success:
        print("Success!")
    else:
        print(f"Failed: {result.error}")
except Exception as e:
    print(f"Orchestration error: {e}")
```

## Async Context

All execution methods are async:

```python
import asyncio

async def main():
    result = await supervisor.orchestrate(tasks, pattern)
    return result

# Run with asyncio
result = asyncio.run(main())
```

## Type Hints

Agent is fully typed with Python type hints:

```python
from agent.core.task import Task
from agent.core.result import Result, OrchestratedResult

async def run_task(task: Task) -> Result:
    return await agent.execute(task)

async def orchestrate(tasks: list[Task]) -> OrchestratedResult:
    return await supervisor.orchestrate(tasks, pattern)
```

## Next Steps

- [Agent API](agent.md) - Agent class reference
- [Task API](task.md) - Task class reference
- [Result API](result.md) - Result class reference
- [Supervisor API](supervisor.md) - Supervisor class reference
