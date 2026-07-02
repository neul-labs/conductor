# Conductor Documentation

Welcome to the Conductor documentation - the Multi-Agent CLI Orchestrator.

## What is Conductor?

Conductor is a Python framework that orchestrates AI coding agents (Claude Code, Codex, Gemini CLI, Aider, Continue) to collaborate on complex development tasks.

Unlike simple wrappers, Conductor treats these CLI tools as **agents that perform actions**:
- Editing files in your codebase
- Executing shell commands
- Making git commits
- Using MCP tools

Conductor acts as a **supervisor** - delegating tasks, running agents in parallel, and aggregating results.

## Quick Start

```bash
# Install
pip install neul-conductor

# Run a task
agent run "Fix the bug in auth.py"

# Orchestrate multiple tasks
agent orchestrate "Research auth patterns" "Implement JWT" "Write tests"
```

## Documentation

- [Getting Started](getting-started.md) - Installation and first steps
- [Orchestration Patterns](orchestration/patterns.md) - Sequential, Parallel, Consensus
- [Agent Reference](agents/) - Supported agents and their capabilities
- [Roadmap](roadmap.md) - Development roadmap

## Core Concepts

### Tasks

Tasks represent what you want agents to do. They include:
- A prompt/instruction
- Task type (CODE_EDIT, RESEARCH, REVIEW, etc.)
- Files to work on
- Execution constraints

### Agents

Agents wrap AI CLI tools and expose a unified interface:
- `can_handle(task)` - How well can this agent handle the task?
- `execute(task)` - Run the task and return results
- `capabilities()` - What can this agent do?

### Results

Results capture what agents did:
- Text output
- Actions taken (files edited, commands run)
- Success/failure status
- Session ID for continuation

### Supervisor

The Supervisor coordinates agents using patterns:
- **Sequential**: Pipeline execution
- **Parallel**: Concurrent execution
- **Consensus**: Multi-agent validation

## Example

```python
from agent.core.task import Task
from agent.agents import ClaudeAgent, CodexAgent
from agent.orchestration import Supervisor, OrchestrationPattern

# Create agents
agents = [ClaudeAgent(), CodexAgent()]
supervisor = Supervisor(agents)

# Run a pipeline
tasks = [
    Task(prompt="Research authentication patterns"),
    Task(prompt="Implement JWT authentication"),
    Task(prompt="Write comprehensive tests"),
]

result = await supervisor.orchestrate(
    tasks=tasks,
    pattern=OrchestrationPattern.SEQUENTIAL,
)

print(f"Success: {result.success}")
```

## Getting Help

- [GitHub Issues](https://github.com/neul-labs/conductor/issues)
- [Roadmap](roadmap.md)
