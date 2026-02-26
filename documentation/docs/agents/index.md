# Agents

Agent supports multiple AI coding assistants, each with unique strengths.

## Overview

| Agent | CLI Tool | Strengths | Status |
|-------|----------|-----------|--------|
| [Claude](claude.md) | `claude` | Complex refactoring, multi-file changes | Available |
| [Codex](codex.md) | `codex` | Sandboxed execution, testing | Available |
| Gemini | `gemini` | Long context, research | Planned |
| Aider | `aider` | Git-integrated edits | Planned |
| Continue | `continue` | CI/CD integration | Planned |

## Agent Comparison

### Capabilities

| Capability | Claude | Codex | Gemini | Aider | Continue |
|------------|--------|-------|--------|-------|----------|
| File editing | Yes | Yes | Yes | Yes | Yes |
| Command execution | Yes | Sandbox | Yes | Yes | Yes |
| Git operations | Yes | No | Yes | Yes | Yes |
| Web access | Yes | No | Yes | No | No |
| MCP tools | Yes | Yes | Yes | No | No |
| Long context | Medium | Medium | High | Low | Low |
| Streaming | Yes | Yes | Yes | Yes | Yes |

### Task Routing Scores

Each agent rates its confidence for different task types:

| Task Type | Claude | Codex |
|-----------|--------|-------|
| `REFACTOR` | 0.95 | 0.70 |
| `ANALYZE` | 0.90 | 0.75 |
| `REVIEW` | 0.85 | 0.80 |
| `CODE_EDIT` | 0.85 | 0.85 |
| `CODE_CREATE` | 0.85 | 0.90 |
| `TEST_WRITE` | 0.75 | 0.90 |
| `TEST_RUN` | 0.70 | 0.95 |
| `RESEARCH` | 0.80 | 0.70 |

Higher scores indicate better suitability for that task type.

## Choosing an Agent

### Claude

Best for:
- Complex refactoring across multiple files
- Architectural decisions
- Code analysis and review
- Tasks requiring deep reasoning

```bash
agent run --agent claude "Refactor the authentication module"
```

### Codex

Best for:
- Testing and test-driven development
- Sandboxed execution
- Full-stack development
- Tasks requiring isolated environments

```bash
agent run --agent codex "Write unit tests for the API"
```

### Auto-Selection

Let the supervisor choose:

```bash
# Supervisor picks best agent based on task type
agent run "Fix the bug in auth.py"
```

## Checking Agent Status

### List Agents

```bash
agent agents list
```

```
+----------+---------+------------------------------------------+-----------+
| Name     | Version | Description                              | Available |
+----------+---------+------------------------------------------+-----------+
| claude   | 1.0.0   | Claude Code - complex refactoring        | Yes       |
| codex    | 1.0.0   | Codex CLI - sandboxed execution          | Yes       |
+----------+---------+------------------------------------------+-----------+
```

### Test Agent

```bash
agent agents test claude
```

### View Capabilities

```bash
agent agents capabilities
```

## Using Multiple Agents

### Sequential

Different agents for different tasks:

```bash
agent orchestrate \
    "Research authentication patterns" \  # May use Gemini
    "Implement JWT auth" \                 # May use Claude
    "Write comprehensive tests"            # May use Codex
```

### Parallel

Same task, multiple perspectives:

```bash
agent orchestrate --pattern parallel --agents claude,codex \
    "Review this code for issues"
```

### Consensus

Agreement across agents:

```bash
agent orchestrate --pattern consensus --agents claude,codex \
    "Is this migration safe?"
```

## Custom Agents

Build your own agent to wrap any CLI tool:

```python
from agent.core.agent import Agent, AgentCapabilities

class MyAgent(Agent):
    @property
    def name(self) -> str:
        return "my-agent"

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities.EXECUTE | AgentCapabilities.FILE_EDIT

    async def execute(self, task: Task) -> Result:
        # Implementation
        ...
```

See [Creating Custom Agents](custom.md) for details.

## Next Steps

- [Claude Agent](claude.md) - Claude Code details
- [Codex Agent](codex.md) - Codex CLI details
- [Custom Agents](custom.md) - Build your own
- [Core Concepts: Agents](../concepts/agents.md) - Agent architecture
