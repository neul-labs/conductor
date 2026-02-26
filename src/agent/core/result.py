"""Result definition - what agents did and produced."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any
import json


class ActionType(Enum):
    """Types of actions an agent can perform."""

    # File operations
    FILE_CREATE = auto()     # Created a new file
    FILE_EDIT = auto()       # Edited an existing file
    FILE_DELETE = auto()     # Deleted a file
    FILE_READ = auto()       # Read a file (for context)

    # Command execution
    COMMAND_RUN = auto()     # Ran a shell command

    # Git operations
    GIT_COMMIT = auto()      # Made a git commit
    GIT_PUSH = auto()        # Pushed to remote
    GIT_BRANCH = auto()      # Created/switched branch

    # Web operations
    WEB_FETCH = auto()       # Fetched web content
    WEB_SEARCH = auto()      # Searched the web

    # MCP tool usage
    MCP_TOOL = auto()        # Used an MCP tool

    # Other
    OTHER = auto()           # Other action type


@dataclass
class Action:
    """An action taken by an agent during task execution.

    Actions track what the agent actually did - files edited, commands run,
    commits made, etc. This provides transparency and auditability.

    Example:
        action = Action(
            type=ActionType.FILE_EDIT,
            details={"path": "src/auth.py", "lines_changed": 15},
            before="def authenticate(user):\\n    pass",
            after="def authenticate(user):\\n    if not user:\\n        raise ValueError()",
        )
    """

    type: ActionType
    details: dict[str, Any] = field(default_factory=dict)
    before: str | None = None    # State before (for diffs)
    after: str | None = None     # State after
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    error: str | None = None

    @property
    def path(self) -> Path | None:
        """Get file path if this is a file action."""
        if "path" in self.details:
            return Path(self.details["path"])
        return None

    @property
    def command(self) -> str | None:
        """Get command if this is a command action."""
        return self.details.get("command")

    def to_dict(self) -> dict[str, Any]:
        """Convert action to dictionary representation."""
        return {
            "type": self.type.name,
            "details": self.details,
            "before": self.before[:100] + "..." if self.before and len(self.before) > 100 else self.before,
            "after": self.after[:100] + "..." if self.after and len(self.after) > 100 else self.after,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "error": self.error,
        }


@dataclass
class ResultMetadata:
    """Metadata about the result."""

    agent: str                           # Which agent produced this
    duration_ms: int | None = None       # Execution time
    input_tokens: int | None = None      # Tokens consumed
    output_tokens: int | None = None     # Tokens produced
    cost_usd: float | None = None        # Estimated cost
    model: str | None = None             # Model used (if known)
    raw_output: str | None = None        # Raw CLI output

    @property
    def total_tokens(self) -> int | None:
        """Total tokens used."""
        if self.input_tokens is not None and self.output_tokens is not None:
            return self.input_tokens + self.output_tokens
        return None


@dataclass
class Result:
    """Result of a task execution by an agent.

    Results capture both the output and the actions taken. This allows
    the orchestrator to understand what changed and pass context forward.

    Example:
        result = Result(
            success=True,
            output="Fixed the authentication bug by adding input validation.",
            actions=[
                Action(type=ActionType.FILE_EDIT, details={"path": "src/auth.py"}),
                Action(type=ActionType.COMMAND_RUN, details={"command": "pytest"}),
            ],
            metadata=ResultMetadata(agent="claude", duration_ms=5000),
        )
    """

    success: bool
    output: str
    actions: list[Action] = field(default_factory=list)
    metadata: ResultMetadata = field(default_factory=lambda: ResultMetadata(agent="unknown"))
    session_id: str | None = None        # For continuation
    error: str | None = None             # Error message if failed
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def files_modified(self) -> list[Path]:
        """Get list of files that were modified."""
        paths = []
        for action in self.actions:
            if action.type in (ActionType.FILE_CREATE, ActionType.FILE_EDIT) and action.path:
                paths.append(action.path)
        return paths

    @property
    def commands_run(self) -> list[str]:
        """Get list of commands that were run."""
        return [
            action.command
            for action in self.actions
            if action.type == ActionType.COMMAND_RUN and action.command
        ]

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary representation."""
        return {
            "success": self.success,
            "output": self.output,
            "actions": [a.to_dict() for a in self.actions],
            "metadata": {
                "agent": self.metadata.agent,
                "duration_ms": self.metadata.duration_ms,
                "input_tokens": self.metadata.input_tokens,
                "output_tokens": self.metadata.output_tokens,
                "cost_usd": self.metadata.cost_usd,
                "model": self.metadata.model,
            },
            "session_id": self.session_id,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert result to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def as_context(self) -> dict[str, Any]:
        """Convert result to context for the next task."""
        return {
            "previous_output": self.output,
            "files_modified": [str(p) for p in self.files_modified],
            "commands_run": self.commands_run,
            "success": self.success,
            "session_id": self.session_id,
        }


@dataclass
class OrchestratedResult:
    """Result of orchestrating multiple agents on a task.

    Aggregates results from multiple agents, tracking the overall
    success and individual agent contributions.
    """

    success: bool
    results: list[Result] = field(default_factory=list)
    pattern: str = "unknown"             # Orchestration pattern used
    consensus_score: float | None = None # For consensus pattern
    error: str | None = None

    @property
    def total_duration_ms(self) -> int:
        """Total execution time across all agents."""
        return sum(
            r.metadata.duration_ms or 0
            for r in self.results
        )

    @property
    def total_cost_usd(self) -> float:
        """Total estimated cost across all agents."""
        return sum(
            r.metadata.cost_usd or 0.0
            for r in self.results
        )

    @property
    def all_files_modified(self) -> list[Path]:
        """All files modified across all agents."""
        paths: list[Path] = []
        for result in self.results:
            paths.extend(result.files_modified)
        return list(set(paths))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "success": self.success,
            "pattern": self.pattern,
            "consensus_score": self.consensus_score,
            "results": [r.to_dict() for r in self.results],
            "total_duration_ms": self.total_duration_ms,
            "total_cost_usd": self.total_cost_usd,
            "all_files_modified": [str(p) for p in self.all_files_modified],
            "error": self.error,
        }
