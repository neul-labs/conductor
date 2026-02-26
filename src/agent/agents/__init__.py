"""Agent implementations for various AI CLI tools."""

from agent.agents.claude import ClaudeAgent
from agent.agents.codex import CodexAgent

__all__ = [
    "ClaudeAgent",
    "CodexAgent",
]


def get_default_agents() -> list:
    """Get the default set of agents."""
    return [
        ClaudeAgent(),
        CodexAgent(),
    ]
