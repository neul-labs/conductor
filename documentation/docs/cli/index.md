# CLI Reference

Agent provides a command-line interface for running and orchestrating AI agents.

## Synopsis

```bash
agent [OPTIONS] COMMAND [ARGS]
```

## Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--version` | `-v` | Show version and exit |
| `--help` | | Show help and exit |

## Commands

| Command | Description |
|---------|-------------|
| [`run`](run.md) | Execute a task with a single agent |
| [`orchestrate`](orchestrate.md) | Orchestrate tasks across agents |
| [`agents`](agents.md) | Manage and inspect agents |

## Quick Reference

### Run a Task

```bash
# Auto-select best agent
agent run "Fix the bug in auth.py"

# Use specific agent
agent run --agent claude "Refactor the user service"

# JSON output
agent run -o json "List all endpoints"

# No streaming
agent run --no-stream "Generate documentation"

# Custom timeout
agent run -t 600 "Run comprehensive tests"
```

### Orchestrate Tasks

```bash
# Sequential pipeline
agent orchestrate "Research" "Implement" "Test"

# Parallel execution
agent orchestrate --pattern parallel "Review code"

# Consensus validation
agent orchestrate --pattern consensus --threshold 0.8 "Is this safe?"

# Specific agents
agent orchestrate --agents claude,codex "Analyze code"
```

### Manage Agents

```bash
# List agents
agent agents list

# Test an agent
agent agents test claude

# Show capabilities
agent agents capabilities
```

## Output Formats

### Text (Default)

Human-readable output with colors:

```bash
agent run "Explain this code"
```

```
Using agent: claude

This code implements a binary search algorithm...

Actions taken:
  - FILE_READ: src/search.py
```

### JSON

Machine-readable output:

```bash
agent run -o json "List files"
```

```json
{
  "success": true,
  "output": "Found 15 files...",
  "actions": [...],
  "metadata": {
    "agent": "claude",
    "duration_ms": 523
  }
}
```

## Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | Execution failed |
| `2` | Agent not found |
| `3` | Configuration error |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_DEFAULT_AGENT` | Default agent to use |
| `AGENT_OUTPUT_FORMAT` | Default output format (text/json) |
| `AGENT_TIMEOUT` | Default timeout in seconds |

## Configuration Files

Agent reads configuration from:

1. `~/.agent/config.toml` - User configuration
2. `.agent.toml` - Project configuration
3. Environment variables

See [Configuration](../configuration.md) for details.

## Examples

### Development Workflow

```bash
# Full development pipeline
agent orchestrate \
    "Research best practices for rate limiting" \
    "Implement rate limiting middleware" \
    "Write unit tests" \
    "Write integration tests" \
    "Update API documentation"
```

### Code Review

```bash
# Multi-agent review
agent orchestrate --pattern parallel \
    --agents claude,codex \
    "Review this PR for security, performance, and style issues"
```

### Validation

```bash
# Safety check before deployment
agent orchestrate --pattern consensus --threshold 0.9 \
    "Is this database migration safe for production?"
```

## Next Steps

- [agent run](run.md) - Single agent execution
- [agent orchestrate](orchestrate.md) - Multi-agent orchestration
- [agent agents](agents.md) - Agent management
