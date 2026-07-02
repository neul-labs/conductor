# Agent

**Orchestrate AI coding agents like a conductor leads an orchestra.**

Agent coordinates Claude, Codex, Gemini, and other AI CLI tools to tackle complex development tasks through intelligent delegation, parallel execution, and result aggregation.

[Get Started](getting-started/index.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/neul-labs/conductor){ .md-button }

---

## What is Agent?

AI CLI tools like Claude Code, Codex, and Gemini CLI are not just text generators - they are **agents that perform actions**: editing files, running commands, making commits, and using tools.

Agent acts as a **supervisor** that:

- **Delegates** tasks to the best-suited agent
- **Orchestrates** complex workflows across multiple agents
- **Aggregates** results and tracks all actions taken

```
                    +------------------+
                    |    Supervisor    |
                    |   (Orchestrator) |
                    +--------+---------+
                             |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
+---------------+    +---------------+    +---------------+
|  Claude Agent |    |  Codex Agent  |    |  Gemini Agent |
|  (Refactoring)|    |   (Testing)   |    |  (Research)   |
+---------------+    +---------------+    +---------------+
```

---

## Quick Example

```bash
# Sequential pipeline: research -> implement -> test
agent orchestrate \
    "Research authentication patterns" \
    "Implement JWT authentication" \
    "Write comprehensive tests"

# Parallel review from multiple agents
agent orchestrate --pattern parallel \
    "Review src/auth.py for issues"

# Consensus validation (75% must agree)
agent orchestrate --pattern consensus --threshold 0.75 \
    "Is this migration safe for production?"
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
| **Aider** | Git-integrated, autonomous commits | Focused edits |
| **Continue** | CI/CD integration | Automation pipelines |

---

## Why Agent?

### The Problem

Modern development involves multiple AI coding assistants, each with unique strengths:

- Claude excels at complex refactoring
- Codex is great for sandboxed testing
- Gemini handles massive context windows

But coordinating them manually is tedious and error-prone.

### The Solution

Agent provides a unified orchestration layer:

```python
from agent.orchestration import Supervisor, OrchestrationPattern
from agent.agents import ClaudeAgent, CodexAgent

supervisor = Supervisor([ClaudeAgent(), CodexAgent()])

result = await supervisor.orchestrate(
    tasks=[research_task, implement_task, test_task],
    pattern=OrchestrationPattern.SEQUENTIAL,
)
```

---

## Next Steps

- [Installation](getting-started/installation.md) - Get Agent up and running
- [Quick Start](getting-started/quickstart.md) - Your first multi-agent workflow
- [Core Concepts](concepts/index.md) - Understand Agents, Tasks, and Results
- [CLI Reference](cli/index.md) - All available commands
