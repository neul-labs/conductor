"""Task definition - what we're asking agents to do."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any


class TaskType(Enum):
    """Types of tasks that can be delegated to agents."""

    # Code modification tasks
    CODE_EDIT = auto()       # Edit existing code
    CODE_CREATE = auto()     # Create new files/code
    REFACTOR = auto()        # Restructure code
    BUG_FIX = auto()         # Fix a specific bug

    # Analysis tasks
    RESEARCH = auto()        # Research patterns, docs, best practices
    REVIEW = auto()          # Review code for issues
    ANALYZE = auto()         # Analyze codebase structure

    # Testing tasks
    TEST_WRITE = auto()      # Write tests
    TEST_RUN = auto()        # Run existing tests

    # Documentation tasks
    DOCUMENT = auto()        # Write documentation

    # Git tasks
    COMMIT = auto()          # Create a commit
    PR_CREATE = auto()       # Create a pull request

    # General
    GENERAL = auto()         # General prompt, no specific type


@dataclass
class TaskConstraints:
    """Constraints and configuration for task execution."""

    timeout: float = 300.0                    # Max execution time in seconds
    allowed_tools: list[str] | None = None    # Allowed MCP/CLI tools (None = all)
    max_tokens: int | None = None             # Max tokens for response
    working_directory: Path | None = None     # Working directory for execution
    auto_approve: bool = False                # Auto-approve tool usage
    stream: bool = True                       # Stream output in real-time

    def to_cli_args(self) -> list[str]:
        """Convert constraints to CLI arguments (provider-specific)."""
        args: list[str] = []
        if self.allowed_tools:
            for tool in self.allowed_tools:
                args.extend(["--allowedTools", tool])
        return args


@dataclass
class Task:
    """A task to be executed by one or more agents.

    Tasks represent the work we're asking agents to do. They include:
    - The prompt/instruction
    - What type of task it is (for routing)
    - Which files to work on (if applicable)
    - Shared context from previous tasks
    - Execution constraints

    Example:
        task = Task(
            prompt="Fix the authentication bug in auth.py",
            task_type=TaskType.BUG_FIX,
            files=[Path("src/auth.py")],
            context={"error_message": "Invalid token format"},
        )
    """

    prompt: str
    task_type: TaskType = TaskType.GENERAL
    files: list[Path] | None = None
    context: dict[str, Any] = field(default_factory=dict)
    constraints: TaskConstraints = field(default_factory=TaskConstraints)
    requires_consensus: bool = False
    parent_task_id: str | None = None  # For sub-tasks in orchestration

    def __post_init__(self) -> None:
        """Validate and normalize task data."""
        if self.files:
            self.files = [Path(f) if isinstance(f, str) else f for f in self.files]

    def with_context(self, **kwargs: Any) -> Task:
        """Create a new task with additional context."""
        new_context = {**self.context, **kwargs}
        return Task(
            prompt=self.prompt,
            task_type=self.task_type,
            files=self.files,
            context=new_context,
            constraints=self.constraints,
            requires_consensus=self.requires_consensus,
            parent_task_id=self.parent_task_id,
        )

    def with_prompt(self, prompt: str) -> Task:
        """Create a new task with a different prompt."""
        return Task(
            prompt=prompt,
            task_type=self.task_type,
            files=self.files,
            context=self.context,
            constraints=self.constraints,
            requires_consensus=self.requires_consensus,
            parent_task_id=self.parent_task_id,
        )

    @classmethod
    def from_prompt(cls, prompt: str, **kwargs: Any) -> Task:
        """Create a task from a simple prompt string."""
        return cls(prompt=prompt, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            "prompt": self.prompt,
            "task_type": self.task_type.name,
            "files": [str(f) for f in self.files] if self.files else None,
            "context": self.context,
            "requires_consensus": self.requires_consensus,
        }
