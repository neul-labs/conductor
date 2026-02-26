# Contributing

Thank you for your interest in contributing to Agent! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- At least one AI CLI tool (Claude, Codex, etc.)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/dipankarsarkar/agent.git
cd agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"

# Verify installation
agent --version
pytest
```

## Development Workflow

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check code style
ruff check src/

# Auto-fix issues
ruff check --fix src/

# Format code
ruff format src/
```

### Type Checking

We use [mypy](https://mypy.readthedocs.io/) for type checking:

```bash
# Run type checker
mypy src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agent

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::test_agent_execute
```

### Pre-commit Checks

Before committing, ensure:

```bash
# All checks pass
ruff check src/
mypy src/
pytest
```

## Making Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

Examples:

```
feat(agents): add Gemini agent implementation

Implements GeminiAgent class with support for long context
and research tasks.

Closes #123
```

```
fix(orchestration): handle timeout in parallel pattern

Previously, parallel pattern didn't properly handle agent
timeouts. Now uses anyio timeout wrapper.
```

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Update documentation if needed
6. Submit PR

PR checklist:

- [ ] Tests pass (`pytest`)
- [ ] Linting passes (`ruff check src/`)
- [ ] Types check (`mypy src/`)
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow convention

## Priority Areas

We especially welcome contributions in these areas:

### 1. New Agents

Implement wrappers for additional AI CLI tools:

- **Gemini CLI** - Google's AI with long context
- **Aider** - Git-integrated coding assistant
- **Continue** - CI/CD integration

See [Creating Custom Agents](agents/custom.md) for guidance.

### 2. Orchestration Patterns

Improve existing patterns or add new ones:

- **Handoff pattern** - Dynamic task routing
- **Magentic pattern** - Adaptive planning
- **Human-in-the-loop** - Approval checkpoints

### 3. Documentation

- Tutorials and guides
- API documentation improvements
- Example workflows
- Video walkthroughs

### 4. Testing

- Unit tests for all modules
- Integration tests
- End-to-end tests
- Performance benchmarks

## Code Structure

```
src/agent/
├── core/           # Core abstractions
│   ├── agent.py    # Agent ABC
│   ├── task.py     # Task definition
│   └── result.py   # Result handling
├── agents/         # Agent implementations
│   ├── claude.py   # Claude agent
│   └── codex.py    # Codex agent
├── orchestration/  # Orchestration logic
│   ├── supervisor.py
│   └── patterns/
├── cli/            # CLI interface
│   └── main.py
└── utils/          # Utilities
    └── process.py
```

## Adding a New Agent

1. Create agent file in `src/agent/agents/`:

```python
# src/agent/agents/my_agent.py
from agent.core.agent import Agent, AgentCapabilities
from agent.core.task import Task
from agent.core.result import Result

class MyAgent(Agent):
    @property
    def name(self) -> str:
        return "my-agent"

    # ... implement required methods
```

2. Export in `src/agent/agents/__init__.py`:

```python
from .my_agent import MyAgent
```

3. Add to default agents:

```python
def get_default_agents() -> list[Agent]:
    return [ClaudeAgent(), CodexAgent(), MyAgent()]
```

4. Add tests in `tests/`:

```python
# tests/test_my_agent.py
import pytest
from agent.agents import MyAgent

@pytest.mark.asyncio
async def test_my_agent():
    agent = MyAgent()
    # ... tests
```

5. Add documentation in `documentation/docs/agents/`:

## Reporting Issues

### Bug Reports

Include:

- Agent version (`agent --version`)
- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

### Feature Requests

Include:

- Use case description
- Proposed solution
- Alternative solutions considered
- Willingness to implement

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the issue, not the person

## Getting Help

- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - Questions and ideas
- **Pull Requests** - Code contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Every contribution helps make Agent better. Whether it's:

- Fixing a typo
- Improving documentation
- Adding a test
- Implementing a feature

We appreciate your help!
