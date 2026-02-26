# Agent Roadmap

This document outlines the development roadmap for Agent, the Multi-Agent CLI Orchestrator.

## Vision

Agent aims to be the definitive framework for orchestrating AI coding agents. As AI CLI tools become more capable, the need for coordination, validation, and intelligent routing between them grows. Agent provides this orchestration layer.

## Phases

### Phase 1: MVP (v0.1.0) - Foundation

**Status: Complete**

Core infrastructure for single and sequential multi-agent execution.

- [x] Core abstractions
  - [x] `Task` dataclass with types and constraints
  - [x] `Result` with actions tracking
  - [x] `Agent` ABC with capabilities
- [x] Initial agents
  - [x] Claude CLI agent
  - [x] Codex CLI agent
- [x] Orchestration
  - [x] Sequential pattern (pipeline)
  - [x] Supervisor coordinator
- [x] CLI
  - [x] `agent run` command
  - [x] `agent orchestrate` command
  - [x] `agent agents` subcommands
- [x] Documentation
  - [x] README.md
  - [x] Roadmap

---

### Phase 2: Orchestration Patterns (v0.2.0)

**Status: In Progress**

Full orchestration capabilities with parallel and consensus patterns.

- [ ] Parallel pattern
  - [ ] Concurrent agent execution with `anyio`
  - [ ] Result aggregation strategies
  - [ ] Timeout and failure handling
- [ ] Handoff pattern
  - [ ] Dynamic task routing
  - [ ] Agent confidence scoring
  - [ ] Automatic escalation
- [ ] Router
  - [ ] Task type classification
  - [ ] Agent capability matching
  - [ ] Load balancing
- [ ] Additional agents
  - [ ] Gemini CLI agent
  - [ ] Health checks for all agents
- [ ] Result aggregation
  - [ ] Merge strategies
  - [ ] Conflict detection
  - [ ] Output synthesis

---

### Phase 3: Consensus & Workflows (v1.0.0)

**Status: Planned**

Production-ready with pre-built workflows and validation patterns.

- [ ] Consensus pattern
  - [ ] Multi-agent validation
  - [ ] Configurable thresholds
  - [ ] Voting strategies (majority, unanimous, weighted)
- [ ] Pre-built workflows
  - [ ] `discover` - Research and exploration
  - [ ] `develop` - Implementation with tests
  - [ ] `deliver` - Review and documentation
  - [ ] Custom workflow definitions (YAML)
- [ ] Additional agents
  - [ ] Aider agent (with Python API)
  - [ ] Continue CLI agent
- [ ] Full documentation
  - [ ] Architecture guide
  - [ ] Agent development guide
  - [ ] Pattern reference
  - [ ] API documentation

---

### Phase 4: Advanced Features (v2.0.0)

**Status: Future**

Enterprise features and advanced orchestration.

- [ ] Magentic pattern
  - [ ] Dynamic task ledger
  - [ ] Adaptive planning
  - [ ] Goal tracking
- [ ] Human-in-the-loop
  - [ ] Approval checkpoints
  - [ ] Feedback integration
  - [ ] Interactive mode
- [ ] MCP integration
  - [ ] Tool sharing between agents
  - [ ] Custom MCP servers
  - [ ] Unified tool registry
- [ ] Plugin system
  - [ ] Custom agent plugins
  - [ ] Hook system (pre/post execution)
  - [ ] Third-party integrations
- [ ] Cost optimization
  - [ ] Token tracking
  - [ ] Cost estimation
  - [ ] Budget limits
- [ ] Observability
  - [ ] Execution logging (SQLite)
  - [ ] Metrics and tracing
  - [ ] Dashboard

---

## Feature Details

### Orchestration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Sequential** | Pipeline execution | Multi-step development |
| **Parallel** | Concurrent execution | Code review, analysis |
| **Handoff** | Dynamic routing | Complex tasks |
| **Consensus** | Multi-agent validation | Safety-critical changes |
| **Magentic** | Adaptive planning | Open-ended problems |

### Agent Capabilities

Each agent has different strengths:

| Capability | Claude | Codex | Gemini | Aider | Continue |
|------------|--------|-------|--------|-------|----------|
| File editing | Yes | Yes | Yes | Yes | Yes |
| Command execution | Yes | Sandbox | Yes | Yes | Yes |
| Git operations | Yes | No | Yes | Yes | Yes |
| Web access | Yes | No | Yes | No | No |
| MCP tools | Yes | Yes | Yes | No | No |
| Long context | Medium | Medium | High | Low | Low |

### Workflow Templates

Pre-built workflows for common development tasks:

```yaml
# discover.yaml - Research workflow
name: discover
description: Research and exploration
steps:
  - agent: gemini  # Good at research
    prompt: "Research {topic} and summarize best practices"
  - agent: claude
    prompt: "Analyze the research and create an implementation plan"

# develop.yaml - Implementation workflow
name: develop
description: Implement with tests
steps:
  - agent: claude  # Good at architecture
    prompt: "Implement {feature}"
  - agent: codex  # Good at testing
    prompt: "Write comprehensive tests"
  - agent: codex
    prompt: "Run tests and fix any failures"

# deliver.yaml - Review and ship
name: deliver
description: Review and documentation
pattern: parallel  # Run reviews concurrently
agents: [claude, codex]
prompt: "Review the implementation for issues"
```

---

## Contributing

We welcome contributions! Priority areas:

1. **Additional agents** - Gemini, Aider, Continue implementations
2. **Orchestration patterns** - Parallel and consensus patterns
3. **Documentation** - Guides, examples, API docs
4. **Testing** - Unit and integration tests

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## Timeline

| Phase | Target | Status |
|-------|--------|--------|
| v0.1.0 (MVP) | Q1 2026 | Complete |
| v0.2.0 (Patterns) | Q2 2026 | In Progress |
| v1.0.0 (Production) | Q3 2026 | Planned |
| v2.0.0 (Enterprise) | Q4 2026 | Future |

---

## References

- [Microsoft AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Datasette LLM](https://llm.datasette.io/)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [OpenAI Codex CLI](https://platform.openai.com/docs/codex)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
