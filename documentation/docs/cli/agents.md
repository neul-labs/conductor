# agent agents

Manage and inspect available agents.

## Synopsis

```bash
agent agents COMMAND [OPTIONS]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all registered agents |
| `test` | Test a specific agent |
| `capabilities` | Show agent capabilities |

---

## agent agents list

List all registered agents with their status.

### Synopsis

```bash
agent agents list [OPTIONS]
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--json` | `-j` | Output in JSON format |

### Examples

```bash
# Table output (default)
agent agents list
```

```
+----------+---------+------------------------------------------+-----------+
| Name     | Version | Description                              | Available |
+----------+---------+------------------------------------------+-----------+
| claude   | 1.0.0   | Claude Code - complex refactoring        | Yes       |
| codex    | 1.0.0   | Codex CLI - sandboxed execution          | Yes       |
| gemini   | 1.0.0   | Gemini CLI - long context research       | No        |
+----------+---------+------------------------------------------+-----------+
```

```bash
# JSON output
agent agents list --json
```

```json
[
  {
    "name": "claude",
    "version": "1.0.0",
    "description": "Claude Code - complex refactoring, multi-file changes",
    "available": true,
    "command": "claude"
  },
  {
    "name": "codex",
    "version": "1.0.0",
    "description": "Codex CLI - sandboxed execution, testing",
    "available": true,
    "command": "codex"
  }
]
```

### Availability

An agent is "Available" when:

1. The CLI tool is installed (`which claude` succeeds)
2. Required environment variables are set
3. The agent passes its validation check

---

## agent agents test

Test a specific agent to verify it's working correctly.

### Synopsis

```bash
agent agents test NAME
```

### Arguments

| Argument | Description |
|----------|-------------|
| `NAME` | Agent name to test (claude, codex, gemini) |

### Examples

```bash
# Test Claude agent
agent agents test claude
```

```
Testing agent: claude

Checking availability... OK
Running test prompt... OK

Test result:
  Agent: claude
  Response: "Hello! I'm Claude, ready to help with coding tasks."
  Duration: 523ms

Agent claude is working correctly.
```

```bash
# Test unavailable agent
agent agents test gemini
```

```
Testing agent: gemini

Checking availability... FAILED

Error: gemini CLI not found. Install with:
  npm install -g @google/gemini-cli
```

### What It Tests

1. **Availability**: Checks if the CLI tool is installed
2. **Execution**: Runs a simple test prompt
3. **Response**: Verifies the agent responds correctly

---

## agent agents capabilities

Show detailed capabilities for all agents.

### Synopsis

```bash
agent agents capabilities
```

### Example

```bash
agent agents capabilities
```

```
Agent Capabilities
==================

claude:
  - EXECUTE         Run prompts
  - STREAM          Stream responses
  - FILE_EDIT       Edit existing files
  - FILE_CREATE     Create new files
  - COMMAND_RUN     Run shell commands
  - GIT_COMMIT      Make git commits
  - MCP             Use MCP tools
  - CONTINUE_SESSION Continue sessions
  - JSON_OUTPUT     Structured output
  - WEB_ACCESS      Fetch web content

codex:
  - EXECUTE         Run prompts
  - STREAM          Stream responses
  - FILE_EDIT       Edit existing files
  - FILE_CREATE     Create new files
  - COMMAND_RUN     Run shell commands
  - MCP             Use MCP tools
  - JSON_OUTPUT     Structured output
  - SANDBOX         Isolated execution
```

### Capability Reference

| Capability | Description |
|------------|-------------|
| `EXECUTE` | Can execute prompts |
| `STREAM` | Can stream responses in real-time |
| `FILE_EDIT` | Can modify existing files |
| `FILE_CREATE` | Can create new files |
| `FILE_DELETE` | Can delete files |
| `COMMAND_RUN` | Can run shell commands |
| `GIT_COMMIT` | Can make git commits |
| `GIT_PUSH` | Can push to remote |
| `MCP` | Supports Model Context Protocol tools |
| `CONTINUE_SESSION` | Can resume previous sessions |
| `JSON_OUTPUT` | Can output structured JSON |
| `SANDBOX` | Runs in isolated environment |
| `WEB_ACCESS` | Can fetch web content |

---

## Use Cases

### Verify Setup

After installation, verify agents are working:

```bash
# List what's available
agent agents list

# Test each agent
agent agents test claude
agent agents test codex
```

### Check Capabilities

Before running a task, check if an agent supports needed capabilities:

```bash
agent agents capabilities
```

For example, if you need git operations, look for `GIT_COMMIT` capability.

### Debugging

If tasks are failing, test the agent directly:

```bash
agent agents test claude
```

### CI/CD Integration

Check agents in CI pipelines:

```bash
# JSON output for parsing
AGENTS=$(agent agents list --json)
if echo "$AGENTS" | jq -e '.[] | select(.name=="claude" and .available==true)' > /dev/null; then
    echo "Claude is available"
fi
```

## See Also

- [agent run](run.md) - Execute tasks
- [Core Concepts: Agents](../concepts/agents.md) - Agent architecture
- [Configuration](../configuration.md) - Agent configuration
