# Configuration

Agent can be configured through files, environment variables, and command-line options.

## Configuration Sources

Agent reads configuration from (in order of precedence):

1. **Command-line options** - Highest priority
2. **Environment variables** - `AGENT_*` prefix
3. **Project config** - `.agent.toml` in current directory
4. **User config** - `~/.agent/config.toml`

## Configuration File

### Location

```bash
# User configuration
~/.agent/config.toml

# Project configuration (overrides user config)
.agent.toml
```

### Format

Configuration uses TOML format:

```toml
# ~/.agent/config.toml

# Default agent to use when none specified
default_agent = "claude"

# Default output format
output_format = "text"  # "text" or "json"

# Default timeout in seconds
timeout = 300

# Enable streaming by default
stream = true

# Agent-specific configuration
[agents.claude]
timeout = 600
# allowed_tools = ["Read", "Write", "Edit", "Bash"]

[agents.codex]
timeout = 300
sandbox = "workspace-write"

# Orchestration defaults
[orchestration]
default_pattern = "sequential"
consensus_threshold = 0.75
stop_on_failure = true
```

## Environment Variables

All configuration can be set via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `AGENT_DEFAULT_AGENT` | Default agent name | Auto-select |
| `AGENT_OUTPUT_FORMAT` | Output format (text/json) | `text` |
| `AGENT_TIMEOUT` | Default timeout (seconds) | `300` |
| `AGENT_STREAM` | Enable streaming | `true` |

### API Keys

AI CLI tools require their own API keys:

```bash
# Claude Code
export ANTHROPIC_API_KEY="sk-ant-..."

# Codex CLI
export OPENAI_API_KEY="sk-..."

# Gemini CLI
export GOOGLE_API_KEY="..."
```

## Command-Line Options

Options override all other configuration:

```bash
# Override agent
agent run --agent codex "Write tests"

# Override output format
agent run -o json "List files"

# Override timeout
agent run -t 600 "Complex task"

# Override streaming
agent run --no-stream "Generate code"
```

## Agent Configuration

### Claude Agent

```toml
[agents.claude]
# Timeout for Claude tasks
timeout = 600

# Allowed tools (optional, default: all)
# allowed_tools = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]

# Auto-approve actions
auto_approve = false
```

### Codex Agent

```toml
[agents.codex]
# Timeout for Codex tasks
timeout = 300

# Sandbox mode: "workspace-write" or "read-only"
sandbox = "workspace-write"

# Auto-approve actions
auto_approve = false
```

## Orchestration Configuration

```toml
[orchestration]
# Default pattern for orchestrate command
default_pattern = "sequential"  # sequential, parallel, consensus

# Consensus threshold (0.0-1.0)
consensus_threshold = 0.75

# Stop sequential pipeline on failure
stop_on_failure = true

# Maximum parallel agents
max_parallel = 5
```

## Task Constraints

Default task constraints:

```toml
[constraints]
# Default timeout in seconds
timeout = 300

# Default working directory (empty = current)
working_directory = ""

# Stream output by default
stream = true

# Auto-approve by default
auto_approve = false
```

## Logging

Configure logging output:

```toml
[logging]
# Log level: debug, info, warning, error
level = "info"

# Log file (optional)
# file = "~/.agent/agent.log"

# Show timestamps
timestamps = true
```

## Example Configurations

### Development Setup

```toml
# .agent.toml (project root)

default_agent = "claude"
output_format = "text"
stream = true

[agents.claude]
timeout = 600

[agents.codex]
timeout = 300
sandbox = "workspace-write"

[orchestration]
default_pattern = "sequential"
stop_on_failure = true
```

### CI/CD Setup

```toml
# .agent.toml for CI environment

default_agent = "codex"
output_format = "json"
stream = false

[constraints]
timeout = 900
auto_approve = true

[orchestration]
stop_on_failure = true
```

### Research Setup

```toml
# Configuration for research tasks

default_agent = "gemini"  # Long context
output_format = "text"
stream = true

[agents.gemini]
timeout = 900

[orchestration]
default_pattern = "parallel"
```

## Configuration Precedence

When the same option is set in multiple places:

```
CLI option > Environment variable > Project config > User config > Default
```

Example:

```bash
# User config sets timeout = 300
# Project config sets timeout = 600
# CLI sets --timeout 900

# Result: timeout = 900 (CLI wins)
```

## Validating Configuration

Check your configuration:

```bash
# List agents with current config
agent agents list

# Test with verbose output
agent run --agent claude "Test" 2>&1 | head -20
```

## Troubleshooting

### Config Not Loading

```bash
# Check config file exists
cat ~/.agent/config.toml

# Check project config
cat .agent.toml
```

### Environment Variables Not Working

```bash
# Verify variables are set
env | grep AGENT_

# Verify API keys
env | grep -E "(ANTHROPIC|OPENAI|GOOGLE)_API_KEY"
```

### Agent Not Using Expected Settings

Remember precedence order:

1. Check CLI options
2. Check environment variables
3. Check project `.agent.toml`
4. Check user `~/.agent/config.toml`

## See Also

- [Installation](getting-started/installation.md) - Initial setup
- [CLI Reference](cli/index.md) - Command-line options
- [Agents](agents/index.md) - Agent-specific configuration
