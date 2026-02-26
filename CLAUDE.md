# CLAUDE.md - Agent Project Context

## Project Overview

Agent is a **Multi-Agent CLI Orchestrator** - a Python framework that coordinates AI coding agents (Claude Code, Codex, Gemini CLI, Aider, Continue) to collaborate on complex development tasks.

## Key Insight

These CLI tools are **agents that perform actions**, not just text generators:
- Edit files
- Run commands
- Make git commits
- Use MCP tools

Agent acts as a **supervisor** that delegates tasks, runs agents in parallel, and aggregates results.

## Architecture

```
src/agent/
├── core/           # Core abstractions (Agent, Task, Result)
├── agents/         # Agent implementations (Claude, Codex, etc.)
├── orchestration/  # Patterns (Sequential, Parallel, Consensus)
├── cli/            # Typer CLI interface
├── plugins/        # Plugin system (future)
└── utils/          # Utilities
```

## Core Abstractions

### Task
What we're asking agents to do:
- `prompt`: The instruction
- `task_type`: CODE_EDIT, RESEARCH, REVIEW, etc.
- `files`: Files to work on
- `constraints`: Timeout, allowed tools, etc.

### Agent (ABC)
Wraps CLI tools:
- `can_handle(task) -> float`: Confidence score (0-1)
- `execute(task) -> Result`: Run task and return result
- `capabilities()`: What the agent can do

### Result
What the agent did:
- `output`: Text response
- `actions`: Files edited, commands run, commits made
- `success`: Whether it worked
- `session_id`: For continuation

### Supervisor
Coordinates agents using patterns:
- Sequential: Pipeline (task1 → task2 → task3)
- Parallel: All agents work on same task
- Consensus: Multiple agents must agree

## CLI Commands

```bash
# Single agent
agent run "Fix the bug"
agent run --agent codex "Write tests"

# Orchestration
agent orchestrate "Research" "Implement" "Test"
agent orchestrate --pattern parallel "Review this code"
agent orchestrate --pattern consensus --threshold 0.75 "Is this safe?"

# Agent management
agent agents list
agent agents test claude
```

## Development

```bash
# Install
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/
```

## Key Files

- `src/agent/core/agent.py`: Agent ABC and capabilities
- `src/agent/core/task.py`: Task definition
- `src/agent/core/result.py`: Result with actions
- `src/agent/orchestration/supervisor.py`: Main orchestrator
- `src/agent/orchestration/patterns/sequential.py`: Sequential pattern
- `src/agent/agents/claude.py`: Claude CLI wrapper
- `src/agent/cli/main.py`: CLI entry point
