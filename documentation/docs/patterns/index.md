# Orchestration Patterns

Orchestration patterns define how tasks are distributed and executed across agents.

## Overview

Agent supports four orchestration patterns:

| Pattern | Description | Best For |
|---------|-------------|----------|
| [Sequential](sequential.md) | Pipeline execution with context flow | Multi-step development |
| [Parallel](parallel.md) | Concurrent execution across agents | Code review, analysis |
| [Consensus](consensus.md) | Multi-agent agreement validation | Safety-critical decisions |
| [Handoff](handoff.md) | Dynamic task routing | Complex problems |

## Choosing a Pattern

```
Is this a multi-step workflow where each step depends on the previous?
├── Yes → Sequential
└── No
    └── Do you need multiple perspectives on the same task?
        ├── Yes → Do they need to agree?
        │   ├── Yes → Consensus
        │   └── No → Parallel
        └── No → Sequential (single task)
```

## Quick Reference

### Sequential

Tasks run in order, context accumulates:

```bash
agent orchestrate \
    "Research patterns" \
    "Implement solution" \
    "Write tests"
```

```
Task 1 → Task 2 → Task 3
   |         |        |
   context → context → context
```

### Parallel

Single task runs on all agents simultaneously:

```bash
agent orchestrate --pattern parallel \
    "Review this code"
```

```
          Task
            |
    +-------+-------+
    |       |       |
 Claude   Codex   Gemini
    |       |       |
    +-------+-------+
            |
     Aggregated Result
```

### Consensus

Multiple agents must agree:

```bash
agent orchestrate --pattern consensus --threshold 0.8 \
    "Is this safe?"
```

```
          Task
            |
    +-------+-------+
    |       |       |
 Claude   Codex   Gemini
    |       |       |
   Yes      Yes     Yes
    |       |       |
    +-------+-------+
            |
    Score: 1.0 (3/3)
    Threshold: 0.8
    Result: PASS
```

## Pattern Comparison

| Aspect | Sequential | Parallel | Consensus |
|--------|------------|----------|-----------|
| **Task count** | Multiple | Single | Single |
| **Execution** | One at a time | All at once | All at once |
| **Context** | Flows forward | Independent | Independent |
| **Success** | All must succeed | Any succeeds | Threshold met |
| **Speed** | Slower | Faster | Faster |
| **Use case** | Pipelines | Reviews | Validation |

## Python API

```python
from agent.orchestration import Supervisor, OrchestrationPattern

supervisor = Supervisor(agents)

# Sequential
result = await supervisor.orchestrate(
    tasks=[task1, task2, task3],
    pattern=OrchestrationPattern.SEQUENTIAL,
)

# Parallel
result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)

# Consensus
result = await supervisor.orchestrate(
    tasks=[validation_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.8,
)
```

## Combining Patterns

Complex workflows can combine patterns:

```python
# 1. Sequential: Research and implement
impl_result = await supervisor.orchestrate(
    tasks=[research_task, implement_task],
    pattern=OrchestrationPattern.SEQUENTIAL,
)

# 2. Parallel: Multi-agent review
review_result = await supervisor.orchestrate(
    tasks=[review_task],
    pattern=OrchestrationPattern.PARALLEL,
)

# 3. Consensus: Safety validation
approval_result = await supervisor.orchestrate(
    tasks=[safety_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.9,
)
```

## Next Steps

- [Sequential Pattern](sequential.md) - Pipeline execution
- [Parallel Pattern](parallel.md) - Concurrent execution
- [Consensus Pattern](consensus.md) - Agreement validation
- [Handoff Pattern](handoff.md) - Dynamic routing
