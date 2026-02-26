# Supervisor

The Supervisor is the orchestration brain of Agent, coordinating agents and patterns.

## Overview

The Supervisor:

- **Routes** tasks to the best-suited agent
- **Orchestrates** multi-task workflows using patterns
- **Aggregates** results from multiple agents
- **Manages** agent lifecycle and validation

## Creating a Supervisor

```python
from agent.orchestration import Supervisor
from agent.agents import ClaudeAgent, CodexAgent

# Create with agents
supervisor = Supervisor([ClaudeAgent(), CodexAgent()])

# Or get default agents
from agent.agents import get_default_agents
supervisor = Supervisor(get_default_agents())
```

## Single Task Execution

Run a single task with automatic agent selection:

```python
from agent.core.task import Task

task = Task(prompt="Refactor the authentication module")

# Supervisor picks the best agent
result = await supervisor.run_single(task)

print(f"Agent used: {result.metadata.agent}")
print(f"Success: {result.success}")
```

### Specify an Agent

```python
# Use a specific agent by name
result = await supervisor.run_single(task, agent_name="claude")
```

## Multi-Task Orchestration

Orchestrate multiple tasks using a pattern:

```python
from agent.orchestration import OrchestrationPattern

tasks = [
    Task(prompt="Research caching strategies"),
    Task(prompt="Implement Redis caching"),
    Task(prompt="Write integration tests"),
]

result = await supervisor.orchestrate(
    tasks=tasks,
    pattern=OrchestrationPattern.SEQUENTIAL,
)
```

### Patterns

| Pattern | Description |
|---------|-------------|
| `SEQUENTIAL` | Tasks run one after another, context flows forward |
| `PARALLEL` | Single task runs across all agents simultaneously |
| `CONSENSUS` | Multiple agents must agree on success |
| `HANDOFF` | Dynamic routing based on task requirements |

See [Orchestration Patterns](../patterns/index.md) for details.

## Agent Selection

The Supervisor selects agents based on confidence scores:

```python
# Each agent scores the task
# claude.can_handle(task) -> 0.95
# codex.can_handle(task) -> 0.75

# Supervisor picks highest scoring agent
result = await supervisor.run_single(task)
# Uses claude (0.95 > 0.75)
```

### Selection Algorithm

1. Get all available agents
2. Call `can_handle(task)` on each
3. Select agent with highest score
4. Execute task with selected agent

```python
def _select_best_agent(self, task: Task) -> Agent:
    """Select the best agent for a task."""
    scores = []
    for agent in self._agents:
        if await agent.validate():
            score = agent.can_handle(task)
            scores.append((agent, score))

    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[0][0]  # Highest scoring agent
```

## Agent Filtering

Limit which agents can be used:

```python
# Only use specific agents
result = await supervisor.orchestrate(
    tasks=tasks,
    pattern=OrchestrationPattern.PARALLEL,
    agent_names=["claude", "codex"],  # Exclude gemini
)
```

## Validation

Check all agents are available:

```python
# Validate all agents
validation = await supervisor.validate_agents()

for agent_name, is_valid in validation.items():
    status = "ready" if is_valid else "not available"
    print(f"{agent_name}: {status}")
```

## List Agents

Get information about registered agents:

```python
# List agent names
names = supervisor.list_agents()
print(names)  # ["claude", "codex"]

# Get detailed info
for name in names:
    agent = supervisor._agents[name]
    info = agent.info()
    print(f"{info.name} v{info.version}: {info.description}")
```

## Consensus Configuration

For consensus pattern, configure the threshold:

```python
result = await supervisor.orchestrate(
    tasks=[Task(prompt="Is this migration safe?")],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.8,  # 80% must agree
)

print(f"Consensus score: {result.consensus_score}")
print(f"Passed threshold: {result.success}")
```

## Error Handling

The Supervisor handles agent failures gracefully:

```python
try:
    result = await supervisor.orchestrate(tasks, pattern)
except Exception as e:
    print(f"Orchestration failed: {e}")

# Or check result for partial failures
if not result.success:
    print(f"Error: {result.error}")
    for r in result.results:
        if not r.success:
            print(f"{r.metadata.agent} failed: {r.error}")
```

## Context Flow

In sequential pattern, context flows automatically:

```python
# Task 1 executes, returns result
# Task 2 receives context from Task 1
# Task 3 receives context from Task 2

result = await supervisor.orchestrate(
    tasks=[task1, task2, task3],
    pattern=OrchestrationPattern.SEQUENTIAL,
)

# Each task knew about previous results
```

### Context Contents

```python
context = {
    "previous_output": "Output from previous task...",
    "files_modified": ["src/a.py", "src/b.py"],
    "commands_run": ["pytest tests/"],
    "success": True,
    "session_id": "sess_abc123",
    "previous_agent": "claude",
}
```

## CLI Integration

The CLI uses the Supervisor internally:

```bash
# Creates Supervisor, runs single task
agent run "Fix the bug"

# Creates Supervisor, orchestrates sequential
agent orchestrate "Research" "Implement" "Test"

# Creates Supervisor, orchestrates parallel
agent orchestrate --pattern parallel "Review code"
```

## Architecture

```
+----------------+
|   Supervisor   |
+-------+--------+
        |
        v
+-------+--------+
|   Pattern      |  (Sequential, Parallel, Consensus)
+-------+--------+
        |
        v
+-------+--------+
|   Agents       |  [Claude, Codex, Gemini, ...]
+----------------+
```

## Next Steps

- [Orchestration Patterns](../patterns/index.md) - Deep dive into patterns
- [CLI Reference](../cli/index.md) - Command-line usage
- [Python API](../api/index.md) - Full API documentation
