# Supervisor API

The `Supervisor` class coordinates agents and orchestration patterns.

## Module

```python
from agent.orchestration import (
    Supervisor,
    OrchestrationPattern,
)
from agent.orchestration.patterns import (
    SequentialPattern,
    ParallelPattern,
)
```

## Supervisor

The main orchestration coordinator.

### Constructor

```python
Supervisor(agents: list[Agent])
```

**Parameters:**
- `agents`: List of agents to manage

**Example:**
```python
from agent.orchestration import Supervisor
from agent.agents import ClaudeAgent, CodexAgent

supervisor = Supervisor([ClaudeAgent(), CodexAgent()])
```

### Methods

#### orchestrate

```python
async def orchestrate(
    self,
    tasks: list[Task],
    pattern: OrchestrationPattern = OrchestrationPattern.SEQUENTIAL,
    agent_names: list[str] | None = None,
    consensus_threshold: float = 0.75,
) -> OrchestratedResult:
    """Orchestrate tasks using the specified pattern."""
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tasks` | `list[Task]` | Required | Tasks to execute |
| `pattern` | `OrchestrationPattern` | `SEQUENTIAL` | Orchestration pattern |
| `agent_names` | `list[str]` | `None` | Limit to specific agents |
| `consensus_threshold` | `float` | `0.75` | Threshold for consensus |

**Returns:** `OrchestratedResult`

**Example:**
```python
result = await supervisor.orchestrate(
    tasks=[task1, task2, task3],
    pattern=OrchestrationPattern.SEQUENTIAL,
)
```

#### run_single

```python
async def run_single(
    self,
    task: Task,
    agent_name: str | None = None,
) -> Result:
    """Run a single task with one agent."""
```

**Parameters:**
- `task`: The task to execute
- `agent_name`: Specific agent, or `None` for auto-selection

**Returns:** `Result`

**Example:**
```python
# Auto-select best agent
result = await supervisor.run_single(task)

# Use specific agent
result = await supervisor.run_single(task, agent_name="claude")
```

#### list_agents

```python
def list_agents(self) -> list[str]:
    """List names of managed agents."""
```

**Example:**
```python
for name in supervisor.list_agents():
    print(name)
```

#### validate_agents

```python
async def validate_agents(self) -> dict[str, bool]:
    """Validate all agents and return their status."""
```

**Returns:** Dict mapping agent name to availability

**Example:**
```python
status = await supervisor.validate_agents()
for name, available in status.items():
    print(f"{name}: {'OK' if available else 'UNAVAILABLE'}")
```

---

## OrchestrationPattern

Enum of orchestration patterns.

### Values

| Value | Description |
|-------|-------------|
| `SEQUENTIAL` | Tasks run in order, context flows forward |
| `PARALLEL` | Single task runs on all agents concurrently |
| `CONSENSUS` | Multiple agents must agree |
| `HANDOFF` | Dynamic routing (planned) |

### Example

```python
from agent.orchestration import OrchestrationPattern

# Sequential pipeline
result = await supervisor.orchestrate(
    tasks=tasks,
    pattern=OrchestrationPattern.SEQUENTIAL,
)

# Parallel execution
result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)

# Consensus validation
result = await supervisor.orchestrate(
    tasks=[validation_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.8,
)
```

---

## SequentialPattern

Pattern for sequential task execution.

### Constructor

```python
SequentialPattern(
    agents: list[Agent],
    stop_on_failure: bool = True,
)
```

**Parameters:**
- `agents`: Available agents
- `stop_on_failure`: Stop pipeline on first failure

### Methods

#### execute

```python
async def execute(self, tasks: list[Task]) -> OrchestratedResult:
    """Execute tasks sequentially."""
```

### Example

```python
from agent.orchestration.patterns import SequentialPattern

pattern = SequentialPattern(agents, stop_on_failure=True)
result = await pattern.execute(tasks)
```

### Context Flow

Each task receives context from the previous:

```python
# Task 1 executes, returns result
# Context created:
{
    "previous_output": "...",
    "files_modified": [...],
    "commands_run": [...],
    "success": True,
    "session_id": "...",
    "previous_agent": "claude",
}

# Task 2 receives this context
# Task 3 receives accumulated context
```

---

## ParallelPattern

Pattern for concurrent task execution.

### Constructor

```python
ParallelPattern(agents: list[Agent])
```

### Methods

#### execute

```python
async def execute(self, task: Task) -> OrchestratedResult:
    """Execute task on all agents concurrently."""
```

Note: Takes a single task, runs on all agents.

### Example

```python
from agent.orchestration.patterns import ParallelPattern

pattern = ParallelPattern(agents)
result = await pattern.execute(review_task)

# Result contains output from all agents
for r in result.results:
    print(f"{r.metadata.agent}: {r.output[:100]}")
```

---

## Common Patterns

### Sequential Pipeline

```python
tasks = [
    Task(prompt="Research patterns", task_type=TaskType.RESEARCH),
    Task(prompt="Implement solution", task_type=TaskType.CODE_CREATE),
    Task(prompt="Write tests", task_type=TaskType.TEST_WRITE),
]

result = await supervisor.orchestrate(
    tasks=tasks,
    pattern=OrchestrationPattern.SEQUENTIAL,
)
```

### Parallel Review

```python
review_task = Task(
    prompt="Review this code for issues",
    task_type=TaskType.REVIEW,
)

result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)

# Aggregate insights from all agents
for r in result.results:
    print(f"--- {r.metadata.agent} ---")
    print(r.output)
```

### Consensus Validation

```python
validation_task = Task(
    prompt="Is this migration safe for production?",
    requires_consensus=True,
)

result = await supervisor.orchestrate(
    tasks=[validation_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.9,  # 90% must agree
)

if result.success:
    print(f"Approved! (score: {result.consensus_score:.0%})")
else:
    print(f"Not approved (score: {result.consensus_score:.0%})")
```

### Agent Filtering

```python
# Only use specific agents
result = await supervisor.orchestrate(
    tasks=tasks,
    pattern=OrchestrationPattern.PARALLEL,
    agent_names=["claude", "codex"],  # Exclude others
)
```

### Error Handling

```python
try:
    result = await supervisor.orchestrate(tasks, pattern)

    if result.success:
        print("All tasks succeeded")
    else:
        print(f"Orchestration failed: {result.error}")

        # Check individual results
        for r in result.results:
            if not r.success:
                print(f"  {r.metadata.agent} failed: {r.error}")

except Exception as e:
    print(f"Error: {e}")
```

---

## Advanced Usage

### Custom Agent Selection

```python
# Get best agent for a task
task = Task(prompt="Refactor auth", task_type=TaskType.REFACTOR)

scores = []
for agent in supervisor._agents:
    score = agent.can_handle(task)
    scores.append((agent.name, score))

scores.sort(key=lambda x: x[1], reverse=True)
print("Agent scores:")
for name, score in scores:
    print(f"  {name}: {score:.2f}")
```

### Combining Patterns

```python
# Sequential for implementation
impl_result = await supervisor.orchestrate(
    tasks=[research_task, implement_task],
    pattern=OrchestrationPattern.SEQUENTIAL,
)

# Parallel for review
review_result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)

# Consensus for approval
approval_result = await supervisor.orchestrate(
    tasks=[approval_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.9,
)
```

---

## Type Hints

```python
from agent.orchestration import Supervisor, OrchestrationPattern
from agent.core.task import Task
from agent.core.result import OrchestratedResult

async def run_pipeline(
    supervisor: Supervisor,
    tasks: list[Task],
) -> OrchestratedResult:
    return await supervisor.orchestrate(
        tasks=tasks,
        pattern=OrchestrationPattern.SEQUENTIAL,
    )
```
