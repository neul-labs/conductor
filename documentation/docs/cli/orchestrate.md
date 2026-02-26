# agent orchestrate

Orchestrate tasks across multiple agents using coordination patterns.

## Synopsis

```bash
agent orchestrate [OPTIONS] PROMPTS...
```

## Description

The `orchestrate` command runs multiple tasks using orchestration patterns:

- **Sequential**: Tasks run in order, context flows forward
- **Parallel**: Single task runs across all agents simultaneously
- **Consensus**: Multiple agents must agree on success
- **Handoff**: Dynamic routing based on task requirements

## Arguments

| Argument | Description |
|----------|-------------|
| `PROMPTS...` | One or more task prompts (required) |

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--pattern` | `-p` | `sequential` | Orchestration pattern |
| `--agents` | `-a` | All | Comma-separated agent names |
| `--threshold` | | `0.75` | Consensus threshold (0.0-1.0) |
| `--output-format` | `-o` | `text` | Output format: `text` or `json` |

### Pattern Values

| Pattern | Description |
|---------|-------------|
| `sequential` | Run tasks in order, pass context forward |
| `parallel` | Run single task on all agents concurrently |
| `consensus` | Require agent agreement above threshold |
| `handoff` | Dynamic routing (planned) |

## Examples

### Sequential Pipeline

Run tasks in order with context passing:

```bash
agent orchestrate \
    "Research authentication best practices" \
    "Implement JWT authentication" \
    "Write comprehensive tests" \
    "Document the implementation"
```

Flow:
```
Research -> Implement -> Test -> Document
   |            |          |         |
   +-- context -+- context +- context +
```

Each task receives the output and actions from the previous task.

### Parallel Execution

Run a single task across all agents simultaneously:

```bash
agent orchestrate --pattern parallel \
    "Review src/api.py for potential issues"
```

All available agents analyze independently, results are aggregated.

### Specific Agents

Limit which agents participate:

```bash
# Only use Claude and Codex
agent orchestrate --agents claude,codex \
    "Analyze the codebase" \
    "Create implementation plan"

# Parallel with specific agents
agent orchestrate --pattern parallel --agents claude,codex \
    "Review this code"
```

### Consensus Validation

Require multiple agents to agree:

```bash
# Default 75% threshold
agent orchestrate --pattern consensus \
    "Is this database migration safe for production?"

# Higher threshold for critical decisions
agent orchestrate --pattern consensus --threshold 0.9 \
    "Should we deploy this to production?"

# Custom threshold
agent orchestrate --pattern consensus --threshold 0.8 \
    "Is this refactoring approach correct?"
```

### JSON Output

Get machine-readable results:

```bash
agent orchestrate -o json \
    "Research" "Implement" "Test"
```

```json
{
  "success": true,
  "pattern": "sequential",
  "results": [
    {
      "success": true,
      "output": "Research findings...",
      "metadata": {"agent": "claude", "duration_ms": 2000}
    },
    {
      "success": true,
      "output": "Implementation complete...",
      "metadata": {"agent": "claude", "duration_ms": 3500}
    },
    {
      "success": true,
      "output": "Tests written...",
      "metadata": {"agent": "codex", "duration_ms": 2500}
    }
  ],
  "total_duration_ms": 8000,
  "total_cost_usd": 0.15
}
```

## Patterns in Detail

### Sequential Pattern

Best for development pipelines where each step builds on the previous:

```bash
agent orchestrate --pattern sequential \
    "Analyze the current code structure" \
    "Identify refactoring opportunities" \
    "Implement the refactoring" \
    "Verify tests still pass"
```

**Characteristics:**
- Tasks run one at a time
- Context accumulates through the pipeline
- Fails fast if `stop_on_failure=True` (default)
- Best agent selected for each task

### Parallel Pattern

Best for getting multiple perspectives on a single task:

```bash
agent orchestrate --pattern parallel \
    "Review this PR for bugs, security issues, and performance problems"
```

**Characteristics:**
- Single task runs on all agents concurrently
- Results are aggregated
- Success if any agent succeeds
- Useful for comprehensive reviews

### Consensus Pattern

Best for validation and safety-critical decisions:

```bash
agent orchestrate --pattern consensus --threshold 0.8 \
    "Is this change backwards compatible?"
```

**Characteristics:**
- Runs parallel first
- Calculates consensus score (success_count / total)
- Passes if score >= threshold
- Useful for go/no-go decisions

## Output Format

### Text Output

```
Pattern: sequential

Task 1/3: Research authentication patterns
Using agent: claude
[Output...]
Actions: FILE_READ x 3

Task 2/3: Implement JWT authentication
Using agent: claude
[Output...]
Actions: FILE_EDIT x 2, COMMAND_RUN x 1

Task 3/3: Write tests
Using agent: codex
[Output...]
Actions: FILE_CREATE x 1, COMMAND_RUN x 2

---
Summary:
  Success: Yes
  Total duration: 8.5s
  Total cost: $0.15
  Files modified: src/auth.py, tests/test_auth.py
```

### Consensus Output

```
Pattern: consensus (threshold: 0.8)

Running task on 3 agents...

  claude: SUCCESS - "Yes, the migration is safe..."
  codex:  SUCCESS - "Migration looks safe..."
  gemini: SUCCESS - "Safe to proceed..."

Consensus score: 1.0 (3/3 agree)
Threshold: 0.8
Result: PASSED
```

## Exit Codes

| Code | Description |
|------|-------------|
| `0` | All tasks succeeded (or consensus passed) |
| `1` | One or more tasks failed |
| `2` | Consensus threshold not met |
| `3` | No agents available |

## Use Cases

### Development Pipeline

```bash
agent orchestrate \
    "Research best practices for error handling" \
    "Implement custom exception hierarchy" \
    "Add error handling to API endpoints" \
    "Write tests for error scenarios" \
    "Update error documentation"
```

### Code Review

```bash
agent orchestrate --pattern parallel \
    --agents claude,codex,gemini \
    "Review this pull request for:
     - Code quality and style
     - Potential bugs
     - Security vulnerabilities
     - Performance issues
     - Test coverage"
```

### Safety Validation

```bash
agent orchestrate --pattern consensus --threshold 0.9 \
    "Analyze this deployment script. Is it safe to run in production?
     Consider: data loss, downtime, rollback capability, dependencies."
```

### Feature Implementation

```bash
agent orchestrate \
    "Design database schema for user preferences" \
    "Create migration scripts" \
    "Implement preference service" \
    "Add API endpoints" \
    "Write integration tests"
```

## Tips

1. **Sequential for workflows** - Use when tasks depend on each other
2. **Parallel for reviews** - Get multiple perspectives quickly
3. **Consensus for safety** - Validate critical decisions
4. **Specific agents** - Use `--agents` when you know which are best
5. **High thresholds** - Use 0.9+ for critical consensus decisions

## See Also

- [agent run](run.md) - Single task execution
- [Orchestration Patterns](../patterns/index.md) - Pattern deep dive
- [Core Concepts: Supervisor](../concepts/supervisor.md) - How orchestration works
