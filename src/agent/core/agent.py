"""Agent abstract base class - wraps AI CLI tools."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from enum import Flag, auto
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from agent.core.task import Task
    from agent.core.result import Result


class AgentCapabilities(Flag):
    """Capabilities that an agent may support."""

    NONE = 0

    # Execution modes
    EXECUTE = auto()              # Can execute prompts
    STREAM = auto()               # Can stream responses

    # Code operations
    FILE_EDIT = auto()            # Can edit files
    FILE_CREATE = auto()          # Can create files
    COMMAND_RUN = auto()          # Can run shell commands

    # Git operations
    GIT_COMMIT = auto()           # Can make commits
    GIT_PUSH = auto()             # Can push to remote

    # Special features
    MCP = auto()                  # Supports MCP tools
    CONTINUE_SESSION = auto()     # Can continue previous sessions
    JSON_OUTPUT = auto()          # Supports JSON output format
    SANDBOX = auto()              # Runs in sandbox/isolated environment
    WEB_ACCESS = auto()           # Can access the web

    @classmethod
    def all(cls) -> AgentCapabilities:
        """Return all capabilities."""
        result = cls.NONE
        for cap in cls:
            if cap != cls.NONE:
                result |= cap
        return result

    @classmethod
    def code_agent(cls) -> AgentCapabilities:
        """Standard capabilities for a code agent."""
        return (
            cls.EXECUTE | cls.STREAM | cls.FILE_EDIT |
            cls.FILE_CREATE | cls.COMMAND_RUN | cls.JSON_OUTPUT
        )


@dataclass
class AgentInfo:
    """Information about an agent."""

    name: str
    version: str
    description: str
    capabilities: AgentCapabilities
    command: str | list[str]     # CLI command to invoke
    available: bool = True


class Agent(ABC):
    """Abstract base class for AI CLI agents.

    Agents wrap external CLI tools (Claude, Codex, Gemini, etc.)
    and expose a unified interface for executing tasks.

    Example implementation:
        class ClaudeAgent(Agent):
            @property
            def name(self) -> str:
                return "claude"

            def can_handle(self, task: Task) -> float:
                # Claude is good at complex refactoring
                if task.task_type == TaskType.REFACTOR:
                    return 0.9
                return 0.7

            async def execute(self, task: Task) -> Result:
                # Run claude -p "prompt" and parse output
                ...
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this agent."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the CLI tool (or 'unknown')."""
        ...

    @property
    def description(self) -> str:
        """Human-readable description of this agent."""
        return f"{self.name} agent"

    @abstractmethod
    def capabilities(self) -> AgentCapabilities:
        """Return the capabilities this agent supports."""
        ...

    def supports(self, capability: AgentCapabilities) -> bool:
        """Check if this agent supports a specific capability."""
        return bool(self.capabilities() & capability)

    @abstractmethod
    def can_handle(self, task: Task) -> float:
        """Return confidence score (0-1) for handling this task.

        Higher scores indicate better suitability. The router uses
        these scores to select the best agent for a task.

        Args:
            task: The task to evaluate

        Returns:
            Confidence score between 0.0 and 1.0
        """
        ...

    @abstractmethod
    async def execute(self, task: Task) -> Result:
        """Execute a task and return the result.

        This is the main entry point for running tasks. The agent
        should invoke its CLI tool and parse the output.

        Args:
            task: The task to execute

        Returns:
            Result with output and actions taken
        """
        ...

    async def stream(self, task: Task) -> AsyncIterator[str]:
        """Stream response chunks as they arrive.

        Default implementation executes and yields the full output.
        Override for true streaming support.

        Args:
            task: The task to execute

        Yields:
            Response chunks as strings
        """
        result = await self.execute(task)
        yield result.output

    @abstractmethod
    async def validate(self) -> bool:
        """Check if this agent is properly configured and available.

        Should verify the CLI tool is installed and accessible.

        Returns:
            True if the agent is ready to use
        """
        ...

    async def health_check(self) -> dict[str, Any]:
        """Perform a health check on this agent.

        Returns:
            Dict with health status information
        """
        available = await self.validate()
        return {
            "name": self.name,
            "version": self.version,
            "available": available,
            "capabilities": str(self.capabilities()),
        }

    def info(self) -> AgentInfo:
        """Get information about this agent."""
        return AgentInfo(
            name=self.name,
            version=self.version,
            description=self.description,
            capabilities=self.capabilities(),
            command=self._get_command(),
        )

    def _get_command(self) -> str | list[str]:
        """Get the CLI command for this agent."""
        return self.name


class AgentRegistry:
    """Registry of available agents."""

    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        """Register an agent."""
        self._agents[agent.name] = agent

    def get(self, name: str) -> Agent | None:
        """Get an agent by name."""
        return self._agents.get(name)

    def list(self) -> list[str]:
        """List all registered agent names."""
        return list(self._agents.keys())

    def all(self) -> list[Agent]:
        """Get all registered agents."""
        return list(self._agents.values())

    async def available(self) -> list[Agent]:
        """Get all available (validated) agents."""
        result = []
        for agent in self._agents.values():
            if await agent.validate():
                result.append(agent)
        return result


# Global registry instance
_registry: AgentRegistry | None = None


def get_registry() -> AgentRegistry:
    """Get the global agent registry."""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry


def register_agent(agent: Agent) -> None:
    """Register an agent with the global registry."""
    get_registry().register(agent)
