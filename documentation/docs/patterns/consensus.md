# Consensus Pattern

Require multiple agents to agree before proceeding.

## Overview

The Consensus pattern runs a task on all agents and checks if enough agree on success:

```
              Task
                |
    +-----------+-----------+
    |           |           |
 Claude      Codex       Gemini
    |           |           |
   Yes         Yes          No
    |           |           |
    +-----------+-----------+
                |
        Score: 0.67 (2/3)
        Threshold: 0.75
        Result: FAIL
```

This is useful for validation and safety-critical decisions.

## When to Use

- **Safety validation**: "Is this migration safe?"
- **Quality gates**: "Is this code ready for production?"
- **Risk assessment**: "Could this change break anything?"
- **Decision making**: Any go/no-go decision

## CLI Usage

```bash
# Default 75% threshold
agent orchestrate --pattern consensus \
    "Is this database migration safe for production?"

# Higher threshold for critical decisions
agent orchestrate --pattern consensus --threshold 0.9 \
    "Should we deploy this to production now?"

# Custom threshold
agent orchestrate --pattern consensus --threshold 0.8 \
    "Is this refactoring approach correct?"
```

## Python API

```python
from agent.core.task import Task
from agent.orchestration import Supervisor, OrchestrationPattern

supervisor = Supervisor(agents)

validation_task = Task(
    prompt="Is this database migration safe for production?",
    requires_consensus=True,
)

result = await supervisor.orchestrate(
    tasks=[validation_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.8,  # 80% must agree
)

if result.success:
    print(f"Approved! Score: {result.consensus_score:.0%}")
else:
    print(f"Not approved. Score: {result.consensus_score:.0%}")
```

## How It Works

1. **Parallel execution**: Task runs on all agents concurrently
2. **Success counting**: Count agents that returned `success=True`
3. **Score calculation**: `consensus_score = success_count / total_agents`
4. **Threshold check**: Pass if `consensus_score >= threshold`

## Threshold Guidelines

| Threshold | Use Case |
|-----------|----------|
| `0.5` | Simple majority (50%) |
| `0.67` | Two-thirds majority |
| `0.75` | Strong majority (default) |
| `0.8` | High confidence |
| `0.9` | Very high confidence |
| `1.0` | Unanimous agreement |

## Examples

### Database Migration

```bash
agent orchestrate --pattern consensus --threshold 0.9 \
    "Review this database migration:
     - Is it reversible?
     - Will it cause data loss?
     - Is there adequate rollback?
     - Will it cause downtime?"
```

### Production Deployment

```bash
agent orchestrate --pattern consensus --threshold 0.8 \
    "Is this release ready for production?
     - All tests passing?
     - No security vulnerabilities?
     - Performance acceptable?
     - Documentation updated?"
```

### Code Quality Gate

```bash
agent orchestrate --pattern consensus --threshold 0.75 \
    "Does this code meet quality standards?
     - Follows coding conventions?
     - Has adequate test coverage?
     - No obvious bugs?
     - Well documented?"
```

### Security Review

```bash
agent orchestrate --pattern consensus --threshold 0.9 \
    "Is this authentication implementation secure?
     - No hardcoded secrets?
     - Proper password hashing?
     - Session management correct?
     - CSRF protection in place?"
```

## Result Structure

```python
result = await supervisor.orchestrate(
    tasks=[task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.8,
)

# Consensus result
print(result.success)          # True if threshold met
print(result.pattern)          # "consensus"
print(result.consensus_score)  # 0.67 (2/3 agents agreed)
print(result.error)            # Reason if failed

# Individual votes
for r in result.results:
    vote = "YES" if r.success else "NO"
    print(f"{r.metadata.agent}: {vote}")
    print(f"  Reason: {r.output[:100]}...")
```

## Interpreting Agent Responses

Agents determine success/failure based on their analysis:

```python
# Claude's result
{
    "success": True,  # "Yes, it's safe"
    "output": "The migration is safe because..."
}

# Codex's result
{
    "success": False,  # "No, it's not safe"
    "output": "I found a potential issue..."
}
```

The task prompt should be phrased as a yes/no question for best results.

## Crafting Good Prompts

**Good** (clear yes/no framing):
```
"Is this database migration safe for production?"
"Should we approve this pull request?"
"Does this code meet security requirements?"
```

**Less good** (ambiguous):
```
"What do you think about this migration?"
"Review this code"
"Check for issues"
```

## Advanced Usage

### Weighted Consensus (Future)

Currently all agents have equal weight. Future versions may support:

```python
# Not yet implemented
result = await supervisor.orchestrate(
    tasks=[task],
    pattern=OrchestrationPattern.CONSENSUS,
    agent_weights={"claude": 2, "codex": 1, "gemini": 1},
)
```

### Conditional Actions

```python
result = await supervisor.orchestrate(
    tasks=[safety_task],
    pattern=OrchestrationPattern.CONSENSUS,
    consensus_threshold=0.9,
)

if result.success:
    # Proceed with deployment
    await deploy()
else:
    # Get human review
    print(f"Consensus not reached ({result.consensus_score:.0%})")
    for r in result.results:
        if not r.success:
            print(f"  {r.metadata.agent} said NO: {r.output}")
```

## Tips

1. **Phrase as yes/no**: Make questions answerable with success/failure
2. **Set appropriate thresholds**: Higher for critical decisions
3. **Review dissenting opinions**: Failed agents may have valid concerns
4. **Use multiple agents**: More agents = more robust consensus
5. **Provide context**: Include relevant code/docs in the prompt

## Limitations

- **Binary decisions**: Success/failure, not nuanced scores
- **Equal weighting**: All agents count the same
- **Single question**: One decision per orchestration

## Difference from Parallel

| Aspect | Consensus | Parallel |
|--------|-----------|----------|
| **Goal** | Agreement validation | Multiple perspectives |
| **Success** | Threshold of agreement | Any agent succeeds |
| **Result** | Pass/fail decision | All outputs preserved |
| **Score** | Consensus percentage | N/A |
| **Use case** | Safety checks | Reviews, analysis |

## See Also

- [Sequential Pattern](sequential.md) - Pipeline execution
- [Parallel Pattern](parallel.md) - Concurrent execution
- [CLI: orchestrate](../cli/orchestrate.md) - Command reference
