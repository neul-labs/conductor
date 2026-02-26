# Handoff Pattern

Dynamic task routing based on agent capabilities and task requirements.

!!! warning "Planned Feature"
    The Handoff pattern is planned for a future release (v0.2.0+). This page describes the intended design.

## Overview

The Handoff pattern enables dynamic routing of tasks between agents:

```
              Task
                |
            +-------+
            | Router|
            +---+---+
                |
    +-----------+-----------+
    |           |           |
 Claude      Codex       Gemini
    |           |           |
    +-----------+-----------+
                |
    (Routes to best agent,
     may hand off mid-task)
```

Unlike other patterns, Handoff can change agents during execution.

## When to Use

- **Complex tasks**: Problems that require multiple agent strengths
- **Escalation**: When one agent gets stuck, hand off to another
- **Specialization**: Route sub-tasks to specialists
- **Adaptive workflows**: Let agents collaborate dynamically

## Planned Features

### Confidence-Based Routing

Agents can signal when they need help:

```python
# Agent detects it's struggling
if confidence < 0.5:
    return Result(
        success=False,
        handoff_requested=True,
        handoff_reason="Need specialized testing expertise",
    )
```

### Automatic Escalation

The supervisor automatically hands off on failure:

```python
result = await supervisor.orchestrate(
    tasks=[complex_task],
    pattern=OrchestrationPattern.HANDOFF,
    max_handoffs=3,  # Limit escalation chain
)
```

### Skill-Based Routing

Route based on required capabilities:

```python
task = Task(
    prompt="Fix the bug and ensure tests pass",
    required_capabilities=[
        AgentCapabilities.FILE_EDIT,
        AgentCapabilities.TEST_RUN,
    ],
)

# Router finds agent with both capabilities
# Or chains agents: editor → tester
```

## Planned CLI Usage

```bash
# Dynamic routing
agent orchestrate --pattern handoff \
    "Implement this feature with full test coverage"

# With handoff limit
agent orchestrate --pattern handoff --max-handoffs 3 \
    "Fix this complex bug"
```

## Planned Python API

```python
from agent.orchestration import Supervisor, OrchestrationPattern

result = await supervisor.orchestrate(
    tasks=[task],
    pattern=OrchestrationPattern.HANDOFF,
    max_handoffs=3,
    handoff_threshold=0.5,  # Hand off if confidence drops below
)
```

## Design Concepts

### Handoff Chain

Track the chain of agents involved:

```python
result.handoff_chain
# ["claude", "codex", "claude"]
# Claude started, handed to Codex, returned to Claude
```

### Handoff Context

Context passed between agents:

```python
handoff_context = {
    "original_task": "Implement feature X",
    "progress": "Implemented core logic",
    "blockers": "Struggling with test setup",
    "handoff_reason": "Need testing expertise",
    "files_modified": ["src/feature.py"],
    "from_agent": "claude",
}
```

### Handoff Triggers

When handoffs occur:

1. **Explicit request**: Agent requests handoff
2. **Low confidence**: Confidence drops below threshold
3. **Task failure**: Agent fails but task is recoverable
4. **Capability mismatch**: Task needs capabilities agent lacks

## Use Cases

### Bug Fix with Testing

```
1. Claude analyzes bug → identifies fix
2. Claude implements fix → modifies code
3. Handoff to Codex (testing specialist)
4. Codex runs tests → finds edge case
5. Handoff back to Claude
6. Claude fixes edge case
7. Codex verifies all tests pass
```

### Research to Implementation

```
1. Gemini researches patterns (long context)
2. Handoff to Claude with research summary
3. Claude implements based on research
4. Handoff to Codex for testing
```

### Complex Refactoring

```
1. Claude analyzes codebase
2. Claude starts refactoring
3. Hits complexity → requests handoff
4. Different Claude session or Codex continues
5. Returns to original agent for review
```

## Configuration (Planned)

```python
handoff_config = {
    "max_handoffs": 3,
    "confidence_threshold": 0.5,
    "preferred_handoff_targets": {
        "claude": ["codex"],  # Claude prefers handing to Codex
        "codex": ["claude"],  # Codex prefers handing to Claude
    },
    "capability_routing": True,  # Route by capability matching
}
```

## Comparison with Other Patterns

| Aspect | Sequential | Parallel | Consensus | Handoff |
|--------|------------|----------|-----------|---------|
| **Routing** | Fixed order | All agents | All agents | Dynamic |
| **Mid-task change** | No | No | No | Yes |
| **Agent collaboration** | None | None | None | Active |
| **Complexity** | Low | Medium | Medium | High |

## Current Alternatives

Until Handoff is implemented, you can simulate it:

```python
# Manual handoff simulation
result1 = await supervisor.run_single(task, agent_name="claude")

if not result1.success or "need help" in result1.output.lower():
    task2 = task.with_context(result1.as_context())
    result2 = await supervisor.run_single(task2, agent_name="codex")
```

## Status

- [ ] Basic handoff mechanism
- [ ] Confidence-based triggers
- [ ] Handoff context passing
- [ ] CLI support
- [ ] Handoff chain tracking
- [ ] Capability-based routing

See the [Roadmap](../roadmap.md) for implementation timeline.

## See Also

- [Sequential Pattern](sequential.md) - Pipeline execution
- [Parallel Pattern](parallel.md) - Concurrent execution
- [Consensus Pattern](consensus.md) - Agreement validation
- [Roadmap](../roadmap.md) - Development timeline
