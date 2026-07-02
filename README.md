# Conductor

[![PyPI version](https://img.shields.io/pypi/v/neul-conductor.svg)](https://pypi.org/project/neul-conductor/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**Orchestrate AI coding agents like a conductor leads an orchestra.**

Conductor coordinates Claude, Codex, Gemini, and other AI CLI tools to tackle complex development tasks through intelligent delegation, parallel execution, and result aggregation.

[Repository](https://github.com/neul-labs/conductor) | [Neul Labs](https://www.neullabs.com) | [Quick Start](#quick-start)

---

## Why Conductor?

AI CLI tools like Claude Code and Codex are not just text generators - they are **agents that perform actions**: editing files, running commands, making commits, and using tools.

Conductor acts as a **supervisor** that:

- **Delegates** tasks to the best-suited agent
- **Orchestrates** complex workflows across multiple agents
- **Aggregates** results and tracks all actions taken

```
                    ┌─────────────────┐
                    │   Supervisor    │
                    │   (Orchestrator)│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Claude Agent │    │  Codex Agent  │    │  Gemini Agent │
│  (Refactoring)│    │  (Testing)    │    │  (Research)   │
└───────────────┘    └───────────────┘    └───────────────┘
```

---

## Quick Start

### Installation

```bash
pip install neul-conductor
```

> Installs the `agent` command-line tool.

### Run Your First Task

```bash
# Best-matched agent handles the task
agent run "Fix the authentication bug in auth.py"

# Use a specific agent
agent run --agent codex "Write tests for the API"
```

### Orchestrate Multi-Agent Workflows

```bash
# Sequential pipeline
agent orchestrate \
    "Research best practices for rate limiting" \
    "Implement rate limiting middleware" \
    "Write comprehensive tests"

# Parallel review from multiple perspectives
agent orchestrate --pattern parallel \
    "Review src/api.py for security, performance, and maintainability"

# Consensus validation
agent orchestrate --pattern consensus --threshold 0.8 \
    "Is this database migration safe for production?"
```

---

## Features

### Orchestration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Sequential** | Pipeline execution with context flow | Multi-step development |
| **Parallel** | Concurrent execution across agents | Code review, analysis |
| **Consensus** | Multi-agent validation | Safety-critical changes |
| **Handoff** | Dynamic task routing | Complex problems |

### Supported Agents

| Agent | Strengths | Best For |
|-------|-----------|----------|
| **Claude** | Complex refactoring, multi-file changes | Architecture, synthesis |
| **Codex** | Broad knowledge, sandbox execution | Full-stack, testing |
| **Gemini** | Long context (1M tokens) | Research, large codebases |

---

## Python API

```python
import asyncio
from agent.core.task import Task, TaskType
from agent.agents import ClaudeAgent, CodexAgent
from agent.orchestration import Supervisor, OrchestrationPattern

async def main():
    supervisor = Supervisor([ClaudeAgent(), CodexAgent()])

    result = await supervisor.orchestrate(
        tasks=[
            Task(prompt="Research auth patterns", task_type=TaskType.RESEARCH),
            Task(prompt="Implement JWT auth", task_type=TaskType.CODE_CREATE),
            Task(prompt="Write tests", task_type=TaskType.TEST_WRITE),
        ],
        pattern=OrchestrationPattern.SEQUENTIAL,
    )

    print(f"Success: {result.success}")
    print(f"Files modified: {result.all_files_modified}")

asyncio.run(main())
```

---

## Documentation

- [Getting Started](documentation/docs/getting-started/) - Installation and quick start
- [Core Concepts](documentation/docs/concepts/) - Agents, Tasks, Results
- [CLI Reference](documentation/docs/cli/) - All commands with examples
- [Python API](documentation/docs/api/) - Full API documentation
- [Orchestration Patterns](documentation/docs/patterns/) - Sequential, Parallel, Consensus
- [Creating Custom Agents](documentation/docs/agents/custom.md) - Extend with your own agents

### Build Documentation Locally

```bash
pip install -e ".[docs]"
cd documentation && mkdocs serve
```

---

## Requirements

- Python 3.11+
- At least one AI CLI tool:
  - [Claude Code](https://docs.anthropic.com/claude-code)
  - [Codex CLI](https://platform.openai.com/docs/codex)
  - [Gemini CLI](https://github.com/google-gemini/gemini-cli)

---

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/

# Type check
mypy src/
```

---

## Contributing

Contributions welcome! See [Contributing Guide](documentation/docs/contributing.md) for guidelines.

Priority areas:

- Additional agent implementations (Gemini, Aider, Continue)
- Orchestration patterns (Handoff, Magentic)
- Documentation and examples

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Credits

Inspired by:

- [Datasette LLM](https://llm.datasette.io/) - Plugin architecture
- [Microsoft Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

---

## Part of the Neul Labs toolchain

Conductor is part of the Neul Labs orchestration toolchain:

| Project | Description |
|---------|-------------|
| [brat](https://github.com/neul-labs/brat) | Multi-agent harness for AI coding tools — crash-safe state, parallel execution. |
| [ringlet](https://github.com/neul-labs/ringlet) | One CLI to rule all your coding agents. |
| [fastworker](https://github.com/neul-labs/fastworker) | Background tasks in Python with zero infrastructure — no Redis, no RabbitMQ. |
| [m9m](https://github.com/neul-labs/m9m) | The n8n alternative without the bugs — one Go binary. |

Learn more at [neullabs.com](https://www.neullabs.com).
