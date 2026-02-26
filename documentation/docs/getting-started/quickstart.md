# Quick Start

This guide walks you through your first multi-agent workflow in under 5 minutes.

## Prerequisites

Ensure you have:

- Agent installed (`pip install agent`)
- At least one AI CLI tool installed (Claude, Codex, or Gemini)

## Your First Command

Run a simple task with the best-matched agent:

```bash
agent run "Explain what this project does"
```

Agent automatically selects the most suitable agent based on the task type.

## Specify an Agent

Use a specific agent with the `--agent` flag:

```bash
# Use Claude for complex refactoring
agent run --agent claude "Refactor auth.py to use dependency injection"

# Use Codex for testing
agent run --agent codex "Write unit tests for the User class"
```

## Multi-Agent Orchestration

The real power of Agent is orchestrating multiple tasks across agents.

### Sequential Pipeline

Run tasks in sequence, with context passing forward:

```bash
agent orchestrate \
    "Research best practices for rate limiting in Python" \
    "Implement a rate limiter middleware" \
    "Write comprehensive tests for the rate limiter"
```

Each task receives context from the previous one:

```
Research -> Implement -> Test
   |            |          |
   +-- context -+- context +
```

### Parallel Execution

Run the same task across multiple agents simultaneously:

```bash
agent orchestrate --pattern parallel \
    "Review src/api.py for security vulnerabilities"
```

All available agents analyze the code independently, and results are aggregated.

### Consensus Validation

Require multiple agents to agree before proceeding:

```bash
agent orchestrate --pattern consensus --threshold 0.8 \
    "Is this database migration safe to run in production?"
```

At least 80% of agents must agree on success.

## Output Formats

### Text Output (Default)

Human-readable output with colors and formatting:

```bash
agent run "Explain the codebase structure"
```

### JSON Output

Machine-readable output for scripting:

```bash
agent run -o json "List all Python files"
```

```json
{
  "success": true,
  "output": "Found 15 Python files...",
  "actions": [
    {"type": "FILE_READ", "path": "src/main.py"}
  ],
  "metadata": {
    "agent": "claude",
    "duration_ms": 1234
  }
}
```

## Streaming

Watch the agent work in real-time:

```bash
agent run --stream "Implement a binary search function"
```

Disable streaming for batch operations:

```bash
agent run --no-stream "Generate boilerplate code"
```

## Agent Management

### List Available Agents

```bash
agent agents list
```

### Test an Agent

Verify an agent is working correctly:

```bash
agent agents test claude
```

### View Capabilities

See what each agent can do:

```bash
agent agents capabilities
```

## Python API

For programmatic control, use the Python API:

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
        Task(
            prompt="Research caching strategies",
            task_type=TaskType.RESEARCH
        ),
        Task(
            prompt="Implement Redis caching",
            task_type=TaskType.CODE_CREATE
        ),
    ]

    # Run sequential pipeline
    result = await supervisor.orchestrate(
        tasks=tasks,
        pattern=OrchestrationPattern.SEQUENTIAL,
    )

    print(f"Success: {result.success}")
    print(f"Files modified: {result.all_files_modified}")

asyncio.run(main())
```

## Common Workflows

### Development Pipeline

```bash
agent orchestrate \
    "Analyze the current implementation of user authentication" \
    "Refactor to use OAuth 2.0" \
    "Update all affected tests" \
    "Generate documentation for the changes"
```

### Code Review

```bash
agent orchestrate --pattern parallel \
    --agents claude,codex \
    "Review the pull request for bugs, security issues, and code style"
```

### Research and Implementation

```bash
agent orchestrate \
    "Research GraphQL best practices for Python" \
    "Design a GraphQL schema for our data model" \
    "Implement the GraphQL API"
```

## Next Steps

- [Core Concepts](../concepts/index.md) - Understand Agents, Tasks, and Results
- [CLI Reference](../cli/index.md) - Full command documentation
- [Orchestration Patterns](../patterns/index.md) - Deep dive into patterns
- [Python API](../api/index.md) - Programmatic usage
