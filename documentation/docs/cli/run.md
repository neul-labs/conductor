# agent run

Execute a task with a single agent.

## Synopsis

```bash
agent run [OPTIONS] PROMPT
```

## Description

The `run` command executes a single task using:

- The best-matched agent (automatic selection based on task type)
- A specific agent (via `--agent` flag)

The agent processes the prompt, performs any necessary actions (file edits, commands, etc.), and returns a result.

## Arguments

| Argument | Description |
|----------|-------------|
| `PROMPT` | The task prompt to execute (required) |

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--agent` | `-a` | Auto | Specific agent to use (claude, codex, gemini) |
| `--output-format` | `-o` | `text` | Output format: `text` or `json` |
| `--stream/--no-stream` | | `--stream` | Stream the response in real-time |
| `--timeout` | `-t` | `300` | Timeout in seconds |

## Examples

### Basic Usage

```bash
# Auto-select best agent
agent run "Fix the bug in authentication"

# The supervisor selects the most suitable agent
# based on the task type and agent capabilities
```

### Specific Agent

```bash
# Use Claude for complex refactoring
agent run --agent claude "Refactor auth.py to use dependency injection"

# Use Codex for testing
agent run --agent codex "Write unit tests for the User class"

# Use Gemini for research (when available)
agent run --agent gemini "Research GraphQL pagination patterns"
```

### Output Formats

```bash
# Text output (default) - human-readable with colors
agent run "Explain what this code does"

# JSON output - machine-readable for scripting
agent run -o json "List all API endpoints"
```

JSON output structure:

```json
{
  "success": true,
  "output": "Found 12 API endpoints:\n1. GET /users\n2. POST /users\n...",
  "actions": [
    {
      "type": "FILE_READ",
      "details": {"path": "src/routes.py"},
      "success": true
    }
  ],
  "metadata": {
    "agent": "claude",
    "duration_ms": 1523,
    "input_tokens": 450,
    "output_tokens": 890,
    "cost_usd": 0.02
  },
  "session_id": "sess_abc123"
}
```

### Streaming

```bash
# Watch the agent work in real-time (default)
agent run "Implement a binary search function"

# Disable streaming for batch operations
agent run --no-stream "Generate boilerplate code"
```

### Timeout

```bash
# Default 5-minute timeout
agent run "Fix the bug"

# Extended timeout for complex tasks
agent run -t 600 "Run the full test suite and fix failures"

# Short timeout for quick tasks
agent run -t 60 "Add a docstring to this function"
```

## Behavior

### Agent Selection

When no agent is specified, the supervisor:

1. Infers the task type from the prompt
2. Queries each agent's confidence score
3. Selects the highest-scoring agent

```bash
# "Refactor" keywords -> REFACTOR task type
# Claude scores 0.95, Codex scores 0.70
# Supervisor selects Claude
agent run "Refactor the user service"
```

### Task Execution

The agent:

1. Receives the prompt
2. Analyzes the request
3. Performs actions (reads files, edits code, runs commands)
4. Returns structured result

### Output Display

For text format:

```
Using agent: claude

[Agent's response here...]

Actions taken:
  - FILE_EDIT: src/auth.py
  - COMMAND_RUN: pytest tests/test_auth.py

Duration: 2.3s
```

## Exit Codes

| Code | Description |
|------|-------------|
| `0` | Task completed successfully |
| `1` | Task failed (agent returned error) |
| `2` | Agent not found |
| `3` | Timeout exceeded |

## Use Cases

### Bug Fixes

```bash
agent run "Fix the null pointer exception in UserService.getUser()"
```

### Code Generation

```bash
agent run "Create a REST endpoint for user registration"
```

### Documentation

```bash
agent run "Add docstrings to all public methods in api.py"
```

### Analysis

```bash
agent run "Explain the data flow in the checkout process"
```

### Refactoring

```bash
agent run "Extract the validation logic into a separate module"
```

## Tips

1. **Be specific** - Clear prompts get better results
2. **Use appropriate agents** - Claude for complex, Codex for testing
3. **Check actions** - Review what the agent actually did
4. **Use JSON for scripts** - Parse results programmatically

## See Also

- [agent orchestrate](orchestrate.md) - Multi-task orchestration
- [agent agents](agents.md) - Agent management
- [Core Concepts: Tasks](../concepts/tasks.md) - Task types and constraints
