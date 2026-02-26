"""Agent - Multi-Agent CLI Orchestrator.

Orchestrate AI coding agents (Claude, Codex, Gemini, Aider, Continue)
to collaborate on complex development tasks.
"""

__version__ = "0.1.0"

from agent.core.agent import Agent, AgentCapabilities
from agent.core.task import Task, TaskType, TaskConstraints
from agent.core.result import Result, Action, ActionType

__all__ = [
    "Agent",
    "AgentCapabilities",
    "Task",
    "TaskType",
    "TaskConstraints",
    "Result",
    "Action",
    "ActionType",
]
