# Creating Custom Agents

Build your own agent to wrap any AI CLI tool.

## Overview

Custom agents allow you to:

- Integrate any AI CLI tool into Agent
- Define custom capabilities and routing
- Implement specialized behavior
- Extend the Agent ecosystem

## Basic Implementation

### Minimal Agent

```python
from agent.core.agent import Agent, AgentCapabilities, AgentInfo
from agent.core.task import Task, TaskType
from agent.core.result import Result, ResultMetadata
from agent.utils.process import run_command, is_available

class MyAgent(Agent):
    """Agent that wraps my-cli-tool."""

    def __init__(self, command: str = "my-cli") -> None:
        self._command = command

    @property
    def name(self) -> str:
        return "my-agent"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "My custom AI agent"

    def capabilities(self) -> AgentCapabilities:
        return AgentCapabilities.EXECUTE | AgentCapabilities.FILE_EDIT

    def can_handle(self, task: Task) -> float:
        return 0.7  # Default confidence

    async def validate(self) -> bool:
        return is_available(self._command)

    async def execute(self, task: Task) -> Result:
        cmd = [self._command, "--prompt", task.prompt]
        result = await run_command(cmd, timeout=task.constraints.timeout)

        return Result(
            success=result.success,
            output=result.stdout,
            error=result.stderr if not result.success else None,
            metadata=ResultMetadata(agent=self.name),
        )
```

## Step-by-Step Guide

### 1. Define Properties

```python
@property
def name(self) -> str:
    """Unique identifier for the agent."""
    return "my-agent"

@property
def version(self) -> str:
    """Agent version string."""
    return "1.0.0"

@property
def description(self) -> str:
    """Human-readable description."""
    return "My agent for specialized tasks"
```

### 2. Declare Capabilities

```python
def capabilities(self) -> AgentCapabilities:
    """What the agent can do."""
    return (
        AgentCapabilities.EXECUTE |
        AgentCapabilities.STREAM |
        AgentCapabilities.FILE_EDIT |
        AgentCapabilities.FILE_CREATE |
        AgentCapabilities.COMMAND_RUN
    )
```

### 3. Implement Task Scoring

```python
def can_handle(self, task: Task) -> float:
    """Score confidence for handling this task (0.0-1.0)."""
    scores = {
        TaskType.CODE_EDIT: 0.85,
        TaskType.CODE_CREATE: 0.90,
        TaskType.TEST_WRITE: 0.80,
        TaskType.REFACTOR: 0.75,
    }
    return scores.get(task.task_type, 0.6)
```

### 4. Implement Validation

```python
async def validate(self) -> bool:
    """Check if CLI tool is available."""
    return is_available(self._command)
```

### 5. Implement Execution

```python
async def execute(self, task: Task) -> Result:
    """Execute the task and return result."""
    # Build command
    cmd = self._build_command(task)

    # Run command
    result = await run_command(
        cmd,
        timeout=task.constraints.timeout,
        cwd=task.constraints.working_directory,
    )

    # Parse output
    return self._parse_result(result)
```

## Advanced Features

### Streaming Support

```python
from collections.abc import AsyncIterator
from agent.utils.process import stream_command

async def stream(self, task: Task) -> AsyncIterator[str]:
    """Stream response chunks."""
    cmd = self._build_command(task, stream=True)

    async for chunk in stream_command(cmd):
        yield chunk
```

### Action Tracking

```python
from agent.core.result import Action, ActionType

def _parse_result(self, cmd_result) -> Result:
    """Parse CLI output and extract actions."""
    actions = []

    # Parse file edits
    for edit in self._extract_edits(cmd_result.stdout):
        actions.append(Action(
            type=ActionType.FILE_EDIT,
            details={"path": edit["path"]},
            before=edit.get("before"),
            after=edit.get("after"),
            success=True,
        ))

    # Parse commands
    for cmd in self._extract_commands(cmd_result.stdout):
        actions.append(Action(
            type=ActionType.COMMAND_RUN,
            details={"command": cmd},
            success=True,
        ))

    return Result(
        success=cmd_result.success,
        output=cmd_result.stdout,
        actions=actions,
        metadata=ResultMetadata(
            agent=self.name,
            duration_ms=cmd_result.duration_ms,
        ),
    )
```

### Session Continuation

```python
async def execute(self, task: Task) -> Result:
    cmd = self._build_command(task)

    # Resume session if provided
    if task.context and task.context.get("session_id"):
        cmd.extend(["--session", task.context["session_id"]])

    result = await run_command(cmd)

    return Result(
        success=result.success,
        output=result.stdout,
        session_id=self._extract_session_id(result.stdout),
        metadata=ResultMetadata(agent=self.name),
    )
```

### JSON Output Parsing

```python
import json

def _parse_result(self, cmd_result) -> Result:
    """Parse JSON output from CLI."""
    try:
        data = json.loads(cmd_result.stdout)
        return Result(
            success=data.get("success", True),
            output=data.get("output", ""),
            actions=self._parse_actions(data.get("actions", [])),
            metadata=ResultMetadata(
                agent=self.name,
                input_tokens=data.get("input_tokens"),
                output_tokens=data.get("output_tokens"),
                cost_usd=data.get("cost_usd"),
            ),
        )
    except json.JSONDecodeError:
        # Fallback to raw output
        return Result(
            success=cmd_result.success,
            output=cmd_result.stdout,
            metadata=ResultMetadata(agent=self.name),
        )
```

## Registration

### Global Registration

```python
from agent.core.agent import register_agent

# Create and register
my_agent = MyAgent()
register_agent(my_agent)

# Now available globally
from agent.core.agent import get_registry
registry = get_registry()
agent = registry.get("my-agent")
```

### With Supervisor

```python
from agent.orchestration import Supervisor
from agent.agents import ClaudeAgent, CodexAgent

supervisor = Supervisor([
    ClaudeAgent(),
    CodexAgent(),
    MyAgent(),  # Add custom agent
])
```

## Testing

### Unit Tests

```python
import pytest
from agent.core.task import Task, TaskType

@pytest.mark.asyncio
async def test_my_agent_validate():
    agent = MyAgent()
    # Assuming CLI tool is installed
    assert await agent.validate()

@pytest.mark.asyncio
async def test_my_agent_execute():
    agent = MyAgent()
    task = Task(
        prompt="Hello, agent!",
        task_type=TaskType.GENERAL,
    )

    result = await agent.execute(task)

    assert result.success
    assert result.metadata.agent == "my-agent"

def test_my_agent_can_handle():
    agent = MyAgent()

    task = Task(prompt="Edit code", task_type=TaskType.CODE_EDIT)
    score = agent.can_handle(task)

    assert 0.0 <= score <= 1.0
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_my_agent_in_supervisor():
    supervisor = Supervisor([MyAgent()])

    task = Task(prompt="Test task")
    result = await supervisor.run_single(task)

    assert result.success
```

## Complete Example

```python
"""Custom agent for wrapping a hypothetical AI CLI tool."""

from collections.abc import AsyncIterator
from datetime import datetime
import json

from agent.core.agent import Agent, AgentCapabilities, AgentInfo
from agent.core.task import Task, TaskType
from agent.core.result import (
    Result,
    Action,
    ActionType,
    ResultMetadata,
)
from agent.utils.process import run_command, stream_command, is_available


class CustomAIAgent(Agent):
    """Agent wrapping custom-ai CLI tool."""

    def __init__(self, command: str = "custom-ai") -> None:
        self._command = command

    @property
    def name(self) -> str:
        return "custom-ai"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Custom AI agent for specialized tasks"

    def capabilities(self) -> AgentCapabilities:
        return (
            AgentCapabilities.EXECUTE |
            AgentCapabilities.STREAM |
            AgentCapabilities.FILE_EDIT |
            AgentCapabilities.FILE_CREATE |
            AgentCapabilities.COMMAND_RUN |
            AgentCapabilities.JSON_OUTPUT
        )

    def can_handle(self, task: Task) -> float:
        scores = {
            TaskType.CODE_EDIT: 0.85,
            TaskType.CODE_CREATE: 0.90,
            TaskType.TEST_WRITE: 0.80,
            TaskType.REFACTOR: 0.75,
            TaskType.REVIEW: 0.80,
        }
        return scores.get(task.task_type, 0.65)

    async def validate(self) -> bool:
        return is_available(self._command)

    async def execute(self, task: Task) -> Result:
        cmd = self._build_command(task)

        start_time = datetime.now()
        cmd_result = await run_command(
            cmd,
            timeout=task.constraints.timeout,
            cwd=task.constraints.working_directory,
        )
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

        return self._parse_result(cmd_result, duration_ms)

    async def stream(self, task: Task) -> AsyncIterator[str]:
        cmd = self._build_command(task, stream=True)
        async for chunk in stream_command(cmd):
            yield chunk

    def _build_command(self, task: Task, stream: bool = False) -> list[str]:
        cmd = [self._command, "run"]

        if stream:
            cmd.append("--stream")

        if task.constraints.auto_approve:
            cmd.append("--auto-approve")

        cmd.extend(["--prompt", task.prompt])

        if task.files:
            for f in task.files:
                cmd.extend(["--file", f])

        return cmd

    def _parse_result(self, cmd_result, duration_ms: int) -> Result:
        try:
            data = json.loads(cmd_result.stdout)
            actions = [
                Action(
                    type=ActionType[a["type"]],
                    details=a.get("details", {}),
                    success=a.get("success", True),
                )
                for a in data.get("actions", [])
            ]

            return Result(
                success=data.get("success", cmd_result.success),
                output=data.get("output", ""),
                actions=actions,
                session_id=data.get("session_id"),
                metadata=ResultMetadata(
                    agent=self.name,
                    duration_ms=duration_ms,
                    input_tokens=data.get("input_tokens"),
                    output_tokens=data.get("output_tokens"),
                    cost_usd=data.get("cost_usd"),
                ),
            )
        except json.JSONDecodeError:
            return Result(
                success=cmd_result.success,
                output=cmd_result.stdout,
                error=cmd_result.stderr if not cmd_result.success else None,
                metadata=ResultMetadata(
                    agent=self.name,
                    duration_ms=duration_ms,
                ),
            )
```

## See Also

- [Agent API Reference](../api/agent.md) - Full API documentation
- [Claude Agent](claude.md) - Reference implementation
- [Codex Agent](codex.md) - Reference implementation
