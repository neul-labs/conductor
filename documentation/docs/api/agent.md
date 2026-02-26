# Agent API

The `Agent` class is the abstract base class for all agent implementations.

## Module

```python
from agent.core.agent import (
    Agent,
    AgentCapabilities,
    AgentInfo,
    AgentRegistry,
    get_registry,
    register_agent,
)
```

## Agent (ABC)

Abstract base class that all agents must implement.

### Properties

#### name

```python
@property
def name(self) -> str:
    """The agent's unique identifier."""
```

**Returns:** Agent name (e.g., "claude", "codex")

#### version

```python
@property
def version(self) -> str:
    """The agent's version string."""
```

**Returns:** Version string (e.g., "1.0.0")

#### description

```python
@property
def description(self) -> str:
    """Human-readable description of the agent."""
```

**Returns:** Description string

### Methods

#### capabilities

```python
def capabilities(self) -> AgentCapabilities:
    """Return the agent's capabilities as flags."""
```

**Returns:** `AgentCapabilities` flag enum

**Example:**
```python
caps = agent.capabilities()
if AgentCapabilities.FILE_EDIT in caps:
    print("Can edit files")
```

#### can_handle

```python
def can_handle(self, task: Task) -> float:
    """Score how well this agent can handle the task."""
```

**Parameters:**
- `task`: The task to evaluate

**Returns:** Confidence score (0.0-1.0)

**Example:**
```python
score = agent.can_handle(task)
if score > 0.8:
    result = await agent.execute(task)
```

#### execute

```python
async def execute(self, task: Task) -> Result:
    """Execute a task and return the result."""
```

**Parameters:**
- `task`: The task to execute

**Returns:** `Result` with output, actions, and metadata

**Example:**
```python
result = await agent.execute(task)
print(result.output)
```

#### validate

```python
async def validate(self) -> bool:
    """Check if the agent is properly configured."""
```

**Returns:** `True` if agent is ready to use

**Example:**
```python
if await agent.validate():
    result = await agent.execute(task)
else:
    print("Agent not available")
```

#### stream

```python
async def stream(self, task: Task) -> AsyncIterator[str]:
    """Stream the response in chunks."""
```

**Parameters:**
- `task`: The task to execute

**Yields:** Response chunks as strings

**Example:**
```python
async for chunk in agent.stream(task):
    print(chunk, end="", flush=True)
```

#### health_check

```python
async def health_check(self) -> bool:
    """Perform a health check on the agent."""
```

**Returns:** `True` if healthy

#### info

```python
def info(self) -> AgentInfo:
    """Get agent metadata."""
```

**Returns:** `AgentInfo` dataclass

---

## AgentCapabilities

Flag enum for agent capabilities.

### Flags

| Flag | Value | Description |
|------|-------|-------------|
| `EXECUTE` | 1 | Can execute prompts |
| `STREAM` | 2 | Can stream responses |
| `FILE_EDIT` | 4 | Can edit files |
| `FILE_CREATE` | 8 | Can create files |
| `FILE_DELETE` | 16 | Can delete files |
| `COMMAND_RUN` | 32 | Can run commands |
| `GIT_COMMIT` | 64 | Can make commits |
| `GIT_PUSH` | 128 | Can push to remote |
| `MCP` | 256 | Supports MCP tools |
| `CONTINUE_SESSION` | 512 | Can continue sessions |
| `JSON_OUTPUT` | 1024 | Can output JSON |
| `SANDBOX` | 2048 | Runs sandboxed |
| `WEB_ACCESS` | 4096 | Can access web |

### Usage

```python
from agent.core.agent import AgentCapabilities

# Single capability
caps = AgentCapabilities.EXECUTE

# Multiple capabilities
caps = (
    AgentCapabilities.EXECUTE |
    AgentCapabilities.FILE_EDIT |
    AgentCapabilities.COMMAND_RUN
)

# Check capability
if AgentCapabilities.FILE_EDIT in caps:
    print("Can edit files")

# Get preset
caps = AgentCapabilities.code_agent()
```

### Class Methods

#### code_agent

```python
@classmethod
def code_agent(cls) -> AgentCapabilities:
    """Return standard capabilities for a code agent."""
```

**Returns:** EXECUTE | STREAM | FILE_EDIT | FILE_CREATE | COMMAND_RUN | GIT_COMMIT

---

## AgentInfo

Dataclass containing agent metadata.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Agent identifier |
| `version` | `str` | Version string |
| `description` | `str` | Human-readable description |
| `capabilities` | `AgentCapabilities` | Capability flags |
| `command` | `str` | CLI command |
| `available` | `bool` | Whether agent is usable |

### Example

```python
info = agent.info()
print(f"{info.name} v{info.version}")
print(f"Available: {info.available}")
print(f"Command: {info.command}")
```

---

## AgentRegistry

Manages registered agents.

### Methods

#### register

```python
def register(self, agent: Agent) -> None:
    """Register an agent."""
```

#### get

```python
def get(self, name: str) -> Agent | None:
    """Get agent by name."""
```

#### list

```python
def list(self) -> list[str]:
    """List registered agent names."""
```

#### all

```python
def all(self) -> list[Agent]:
    """Get all registered agents."""
```

#### available

```python
def available(self) -> list[Agent]:
    """Get available (validated) agents."""
```

### Example

```python
from agent.core.agent import get_registry

registry = get_registry()

# List all
for name in registry.list():
    print(name)

# Get specific
claude = registry.get("claude")

# Get available only
for agent in registry.available():
    print(f"{agent.name} is ready")
```

---

## Helper Functions

### get_registry

```python
def get_registry() -> AgentRegistry:
    """Get the global agent registry."""
```

### register_agent

```python
def register_agent(agent: Agent) -> None:
    """Register an agent globally."""
```

**Example:**
```python
from agent.core.agent import register_agent

my_agent = MyCustomAgent()
register_agent(my_agent)
```

---

## Built-in Agents

### ClaudeAgent

```python
from agent.agents import ClaudeAgent

agent = ClaudeAgent()
```

### CodexAgent

```python
from agent.agents import CodexAgent

agent = CodexAgent()
```

### get_default_agents

```python
from agent.agents import get_default_agents

agents = get_default_agents()
# Returns [ClaudeAgent(), CodexAgent()]
```

---

## Creating Custom Agents

```python
from agent.core.agent import Agent, AgentCapabilities
from agent.core.task import Task
from agent.core.result import Result

class MyAgent(Agent):
    @property
    def name(self) -> str:
        return "my-agent"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "My custom agent"

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities.EXECUTE | AgentCapabilities.FILE_EDIT

    def can_handle(self, task: Task) -> float:
        return 0.8

    async def execute(self, task: Task) -> Result:
        # Implementation
        ...

    async def validate(self) -> bool:
        return True
```

See [Custom Agents Guide](../agents/custom.md) for details.
