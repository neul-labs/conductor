# Claude Agent

The Claude agent wraps [Claude Code](https://docs.anthropic.com/claude-code), Anthropic's official CLI.

## Overview

| Property | Value |
|----------|-------|
| **Name** | `claude` |
| **CLI Command** | `claude` |
| **Best For** | Complex refactoring, multi-file changes, architecture |

## Strengths

- **Complex refactoring**: Excels at restructuring code across multiple files
- **Multi-file changes**: Understands and modifies related files together
- **Architectural work**: Can reason about system design and patterns
- **Deep analysis**: Provides thorough code analysis and explanations
- **Session continuation**: Can resume previous sessions

## Capabilities

| Capability | Supported |
|------------|-----------|
| Execute prompts | Yes |
| Stream responses | Yes |
| Edit files | Yes |
| Create files | Yes |
| Run commands | Yes |
| Git commits | Yes |
| Git push | No |
| MCP tools | Yes |
| Continue sessions | Yes |
| JSON output | Yes |
| Web access | Yes |
| Sandbox | No |

## Installation

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Set API key
export ANTHROPIC_API_KEY="your-api-key"

# Verify installation
claude --version
```

## Task Routing Scores

Claude rates its confidence for different task types:

| Task Type | Score | Notes |
|-----------|-------|-------|
| `REFACTOR` | 0.95 | Highest - refactoring specialty |
| `ANALYZE` | 0.90 | Strong analytical capabilities |
| `REVIEW` | 0.85 | Good code review |
| `CODE_EDIT` | 0.85 | Reliable editing |
| `CODE_CREATE` | 0.85 | Good code generation |
| `RESEARCH` | 0.80 | Can access web |
| `TEST_WRITE` | 0.75 | Decent at tests |
| `TEST_RUN` | 0.70 | Lower - Codex better |
| `DOCUMENT` | 0.85 | Good documentation |

## Usage

### CLI

```bash
# Use Claude explicitly
agent run --agent claude "Refactor the user service"

# Let supervisor choose (may select Claude for refactoring)
agent run "Refactor the authentication module"
```

### Python

```python
from agent.agents import ClaudeAgent
from agent.core.task import Task, TaskType

agent = ClaudeAgent()

# Check availability
if await agent.validate():
    task = Task(
        prompt="Refactor the authentication system",
        task_type=TaskType.REFACTOR,
    )
    result = await agent.execute(task)
```

## Features

### Session Continuation

Resume previous sessions:

```python
# First execution
result1 = await agent.execute(task1)
session_id = result1.session_id

# Continue with context
task2 = Task(
    prompt="Continue the refactoring",
    context={"session_id": session_id},
)
result2 = await agent.execute(task2)
```

### Streaming

Watch Claude work in real-time:

```python
async for chunk in agent.stream(task):
    print(chunk, end="", flush=True)
```

### MCP Tools

Claude supports Model Context Protocol tools:

```python
# Tools available through Claude's MCP integration
# - Read files
# - Write files
# - Edit files
# - Run Bash commands
# - Web fetch
# - Web search
```

### Action Tracking

Claude's actions are tracked:

```python
result = await agent.execute(task)

for action in result.actions:
    if action.type == ActionType.FILE_EDIT:
        print(f"Edited: {action.path}")
    elif action.type == ActionType.COMMAND_RUN:
        print(f"Ran: {action.command}")
```

## Configuration

Claude agent supports configuration:

```python
agent = ClaudeAgent(
    command="claude",  # CLI command
)
```

### Constraints

Pass constraints to control execution:

```python
task = Task(
    prompt="Analyze this code",
    constraints=TaskConstraints(
        timeout=600,  # 10 minutes
        allowed_tools=["Read", "Glob", "Grep"],  # Read-only
        stream=True,
    ),
)
```

## Best Practices

### Do Use Claude For

- Complex refactoring spanning multiple files
- Architectural analysis and recommendations
- Code review with detailed explanations
- Tasks requiring deep reasoning
- Multi-step implementations

### Consider Codex For

- Running tests (Codex has sandbox)
- Test-driven development
- Isolated execution requirements

## Examples

### Refactoring

```bash
agent run --agent claude \
    "Refactor the monolithic UserService into separate services:
     - AuthenticationService for login/logout
     - ProfileService for user data
     - PreferencesService for settings"
```

### Architecture Review

```bash
agent run --agent claude \
    "Analyze the architecture of src/ and suggest improvements
     for scalability and maintainability"
```

### Multi-File Changes

```bash
agent run --agent claude \
    "Add comprehensive error handling across all API endpoints
     in src/api/"
```

## Troubleshooting

### Claude Not Found

```bash
# Check installation
which claude

# Reinstall if needed
npm install -g @anthropic-ai/claude-code
```

### API Key Issues

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Set it if missing
export ANTHROPIC_API_KEY="your-key"
```

### Timeout Issues

```python
# Increase timeout for complex tasks
task = Task(
    prompt="Complex refactoring...",
    constraints=TaskConstraints(timeout=900),  # 15 minutes
)
```

## See Also

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Codex Agent](codex.md) - Alternative for testing
- [Custom Agents](custom.md) - Build your own
