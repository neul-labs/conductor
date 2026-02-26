# Agents

Agents are wrappers around AI CLI tools that provide a unified interface for task execution.

## Overview

An Agent:

- Wraps an external AI CLI tool (Claude, Codex, Gemini, etc.)
- Declares its capabilities and strengths
- Scores its confidence for handling specific tasks
- Executes tasks and returns structured results

## The Agent Interface

All agents implement the `Agent` abstract base class:

```python
from agent.core.agent import Agent, AgentCapabilities
from agent.core.task import Task
from agent.core.result import Result

class MyAgent(Agent):
    @property
    def name(self) -> str:
        return "my-agent"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "My custom agent"

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities.EXECUTE | AgentCapabilities.FILE_EDIT

    def can_handle(self, task: Task) -> float:
        # Return confidence score 0.0-1.0
        return 0.8

    async def execute(self, task: Task) -> Result:
        # Execute the task
        ...

    async def validate(self) -> bool:
        # Check if CLI tool is available
        ...
```

## Capabilities

Agents declare their capabilities using bitwise flags:

```python
from agent.core.agent import AgentCapabilities

# Single capability
caps = AgentCapabilities.EXECUTE

# Multiple capabilities
caps = (
    AgentCapabilities.EXECUTE |
    AgentCapabilities.FILE_EDIT |
    AgentCapabilities.COMMAND_RUN
)

# Check capability
if AgentCapabilities.FILE_EDIT in agent.capabilities():
    print("Agent can edit files")
```

### Available Capabilities

| Flag | Description |
|------|-------------|
| `EXECUTE` | Can execute prompts |
| `STREAM` | Can stream responses in real-time |
| `FILE_EDIT` | Can edit existing files |
| `FILE_CREATE` | Can create new files |
| `FILE_DELETE` | Can delete files |
| `COMMAND_RUN` | Can run shell commands |
| `GIT_COMMIT` | Can make git commits |
| `GIT_PUSH` | Can push to remote |
| `MCP` | Supports MCP (Model Context Protocol) tools |
| `CONTINUE_SESSION` | Can continue from previous session |
| `JSON_OUTPUT` | Can output structured JSON |
| `SANDBOX` | Runs in isolated environment |
| `WEB_ACCESS` | Can fetch web content |

### Preset Capabilities

Use presets for common agent types:

```python
# Standard code agent capabilities
caps = AgentCapabilities.code_agent()
# Includes: EXECUTE, STREAM, FILE_EDIT, FILE_CREATE, COMMAND_RUN, GIT_COMMIT
```

## Task Routing

The `can_handle()` method returns a confidence score (0.0-1.0) for a task:

```python
def can_handle(self, task: Task) -> float:
    """Score this agent's ability to handle the task."""
    scores = {
        TaskType.REFACTOR: 0.95,    # Excellent at refactoring
        TaskType.REVIEW: 0.90,       # Great at code review
        TaskType.CODE_EDIT: 0.85,    # Good at editing
        TaskType.TEST_WRITE: 0.70,   # Decent at tests
    }
    return scores.get(task.task_type, 0.6)  # Default score
```

The Supervisor selects the agent with the highest score:

```python
# Given task with type=REFACTOR:
# - Claude scores 0.95
# - Codex scores 0.75
# Supervisor selects Claude
```

## Built-in Agents

### Claude Agent

Wraps Claude Code CLI. Best for complex reasoning and multi-file changes.

```python
from agent.agents import ClaudeAgent

agent = ClaudeAgent()
print(agent.name)         # "claude"
print(agent.capabilities())  # EXECUTE, STREAM, FILE_EDIT, ...
```

**Strengths:**

- Complex refactoring
- Multi-file changes
- Architectural decisions
- Code synthesis

**Task Scores:**

| Task Type | Score |
|-----------|-------|
| REFACTOR | 0.95 |
| ANALYZE | 0.90 |
| REVIEW | 0.85 |
| CODE_EDIT | 0.85 |
| CODE_CREATE | 0.85 |

### Codex Agent

Wraps OpenAI Codex CLI. Best for testing and isolated work.

```python
from agent.agents import CodexAgent

agent = CodexAgent()
print(agent.name)         # "codex"
print(agent.capabilities())  # EXECUTE, STREAM, FILE_EDIT, SANDBOX, ...
```

**Strengths:**

- Sandboxed execution
- Testing and test-driven development
- Broad language knowledge
- Full-stack development

**Task Scores:**

| Task Type | Score |
|-----------|-------|
| TEST_RUN | 0.95 |
| TEST_WRITE | 0.90 |
| CODE_CREATE | 0.90 |
| CODE_EDIT | 0.85 |
| BUG_FIX | 0.85 |

## Agent Info

Get metadata about an agent:

```python
info = agent.info()
print(info.name)         # "claude"
print(info.version)      # "1.0.0"
print(info.description)  # "Claude Code - complex refactoring..."
print(info.available)    # True (CLI tool is installed)
print(info.command)      # "claude"
```

## Agent Registry

Agents can be registered globally:

```python
from agent.core.agent import get_registry, register_agent

# Get the global registry
registry = get_registry()

# Register a custom agent
register_agent(my_agent)

# Get agent by name
claude = registry.get("claude")

# List all agents
for agent in registry.all():
    print(agent.name)

# List available agents (CLI tool installed)
for agent in registry.available():
    print(f"{agent.name} is ready")
```

## Validation

Check if an agent is properly configured:

```python
# Check single agent
if await agent.validate():
    print("Agent is ready")
else:
    print("Agent CLI tool not found")

# Check via info
info = agent.info()
if info.available:
    print("CLI tool is installed")
```

## Streaming

Agents with `STREAM` capability can stream responses:

```python
if AgentCapabilities.STREAM in agent.capabilities():
    async for chunk in agent.stream(task):
        print(chunk, end="", flush=True)
else:
    result = await agent.execute(task)
    print(result.output)
```

## Next Steps

- [Tasks](tasks.md) - Define what agents should do
- [Results](results.md) - Understand what agents return
- [Custom Agents](../agents/custom.md) - Build your own agent
