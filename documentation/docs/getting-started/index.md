# Getting Started

Welcome to Agent! This guide will help you get up and running with multi-agent orchestration.

## Overview

Agent is a framework that coordinates AI coding assistants to work together on complex tasks. Think of it as a conductor that directs an orchestra of AI agents.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- At least one AI CLI tool:
    - [Claude Code](https://docs.anthropic.com/claude-code)
    - [Codex CLI](https://platform.openai.com/docs/codex)
    - [Gemini CLI](https://github.com/google-gemini/gemini-cli)

## Quick Install

```bash
pip install neul-conductor
```

## Verify Installation

```bash
# Check version
agent --version

# List available agents
agent agents list

# Test an agent
agent agents test claude
```

## What's Next?

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Detailed installation instructions for all platforms and AI CLI tools.

    [:octicons-arrow-right-24: Installation Guide](installation.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Run your first multi-agent workflow in under 5 minutes.

    [:octicons-arrow-right-24: Quick Start](quickstart.md)

</div>

## Example: Your First Orchestration

```bash
# Run a sequential pipeline
agent orchestrate \
    "Research best practices for error handling" \
    "Implement a custom error handler" \
    "Write unit tests"
```

This command:

1. **Research** - An agent researches error handling patterns
2. **Implement** - Another agent (or the same) implements the findings
3. **Test** - Finally, tests are written for the implementation

Each step builds on the previous one's context.
