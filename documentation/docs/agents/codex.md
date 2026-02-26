# Codex Agent

The Codex agent wraps [OpenAI Codex CLI](https://platform.openai.com/docs/codex), OpenAI's coding assistant.

## Overview

| Property | Value |
|----------|-------|
| **Name** | `codex` |
| **CLI Command** | `codex` |
| **Best For** | Testing, sandboxed execution, full-stack development |

## Strengths

- **Sandboxed execution**: Runs in isolated environment for safety
- **Testing expertise**: Excellent at writing and running tests
- **Broad knowledge**: Wide language and framework coverage
- **Full-stack**: Good at both frontend and backend
- **JSON output**: Clean structured output

## Capabilities

| Capability | Supported |
|------------|-----------|
| Execute prompts | Yes |
| Stream responses | Yes |
| Edit files | Yes |
| Create files | Yes |
| Run commands | Yes (sandboxed) |
| Git commits | No |
| Git push | No |
| MCP tools | Yes |
| Continue sessions | Yes |
| JSON output | Yes |
| Web access | No |
| Sandbox | Yes |

## Installation

```bash
# Install Codex CLI
npm install -g @openai/codex

# Set API key
export OPENAI_API_KEY="your-api-key"

# Verify installation
codex --version
```

## Task Routing Scores

Codex rates its confidence for different task types:

| Task Type | Score | Notes |
|-----------|-------|-------|
| `TEST_RUN` | 0.95 | Highest - testing specialty |
| `TEST_WRITE` | 0.90 | Excellent test writing |
| `CODE_CREATE` | 0.90 | Strong code generation |
| `CODE_EDIT` | 0.85 | Reliable editing |
| `BUG_FIX` | 0.85 | Good at bug fixes |
| `REVIEW` | 0.80 | Decent review |
| `ANALYZE` | 0.75 | Adequate analysis |
| `REFACTOR` | 0.70 | Lower - Claude better |
| `RESEARCH` | 0.70 | No web access |

## Usage

### CLI

```bash
# Use Codex explicitly
agent run --agent codex "Write unit tests for the API"

# Let supervisor choose (may select Codex for testing)
agent run "Run the test suite and fix any failures"
```

### Python

```python
from agent.agents import CodexAgent
from agent.core.task import Task, TaskType

agent = CodexAgent()

# Check availability
if await agent.validate():
    task = Task(
        prompt="Write comprehensive tests for UserService",
        task_type=TaskType.TEST_WRITE,
    )
    result = await agent.execute(task)
```

## Features

### Sandbox Modes

Codex supports different sandbox levels:

```python
# With auto_approve (workspace-write mode)
task = Task(
    prompt="Run the tests",
    constraints=TaskConstraints(auto_approve=True),
)

# Without auto_approve (read-only mode)
task = Task(
    prompt="Analyze the code",
    constraints=TaskConstraints(auto_approve=False),
)
```

### Streaming

Watch Codex work in real-time:

```python
async for chunk in agent.stream(task):
    print(chunk, end="", flush=True)
```

### Action Tracking

Codex's actions are tracked:

```python
result = await agent.execute(task)

for action in result.actions:
    if action.type == ActionType.COMMAND_RUN:
        print(f"Ran: {action.command}")
    elif action.type == ActionType.FILE_CREATE:
        print(f"Created: {action.path}")
```

## Configuration

Codex agent supports configuration:

```python
agent = CodexAgent(
    command="codex",  # CLI command
)
```

### Constraints

Pass constraints to control execution:

```python
task = Task(
    prompt="Run all tests",
    constraints=TaskConstraints(
        timeout=600,  # 10 minutes for test suite
        auto_approve=True,  # Allow writes
        stream=True,
    ),
)
```

## Best Practices

### Do Use Codex For

- Writing unit tests
- Running test suites
- Test-driven development
- Tasks requiring sandboxed execution
- Code generation with broad language support

### Consider Claude For

- Complex refactoring
- Multi-file architectural changes
- Tasks requiring web access

## Examples

### Test Writing

```bash
agent run --agent codex \
    "Write comprehensive unit tests for src/services/user.py
     including edge cases and error conditions"
```

### Test Running

```bash
agent run --agent codex \
    "Run the test suite in tests/ and fix any failures"
```

### Full-Stack Development

```bash
agent run --agent codex \
    "Create a REST endpoint for user registration
     with validation and tests"
```

### Code Generation

```bash
agent run --agent codex \
    "Implement a LRU cache with the following interface:
     - get(key) -> value
     - put(key, value)
     - capacity limit"
```

## Troubleshooting

### Codex Not Found

```bash
# Check installation
which codex

# Reinstall if needed
npm install -g @openai/codex
```

### API Key Issues

```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Set it if missing
export OPENAI_API_KEY="your-key"
```

### Sandbox Restrictions

If Codex can't perform an action:

```python
# Enable workspace-write mode
task = Task(
    prompt="Modify the file",
    constraints=TaskConstraints(auto_approve=True),
)
```

### Timeout on Tests

```python
# Increase timeout for test suites
task = Task(
    prompt="Run all tests",
    constraints=TaskConstraints(timeout=900),  # 15 minutes
)
```

## Comparison with Claude

| Aspect | Codex | Claude |
|--------|-------|--------|
| **Testing** | Excellent | Good |
| **Refactoring** | Good | Excellent |
| **Sandbox** | Yes | No |
| **Git ops** | No | Yes |
| **Web access** | No | Yes |
| **Best for** | Testing, TDD | Architecture, refactoring |

## See Also

- [Codex CLI Documentation](https://platform.openai.com/docs/codex)
- [Claude Agent](claude.md) - Alternative for refactoring
- [Custom Agents](custom.md) - Build your own
