"""OpenAI Codex CLI agent implementation."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from datetime import datetime
from typing import TYPE_CHECKING

from agent.core.agent import Agent, AgentCapabilities
from agent.core.result import Action, ActionType, Result, ResultMetadata
from agent.core.task import Task, TaskType
from agent.utils.process import run_command, stream_command, is_available

if TYPE_CHECKING:
    pass


class CodexAgent(Agent):
    """Agent that wraps the OpenAI Codex CLI (codex command).

    Codex CLI is OpenAI's coding agent that runs in your terminal:
    - Non-interactive mode with `codex exec`
    - JSON output with --json flag
    - Sandbox execution for safety
    - MCP support for tool integration

    Strengths:
    - Broad knowledge across languages and frameworks
    - Sandboxed execution for safe testing
    - Full-stack development tasks
    - Context switching between projects
    """

    def __init__(self, command: str = "codex") -> None:
        self._command = command
        self._version_cache: str | None = None

    @property
    def name(self) -> str:
        return "codex"

    @property
    def version(self) -> str:
        if self._version_cache is None:
            self._version_cache = self._get_version()
        return self._version_cache

    @property
    def description(self) -> str:
        return "OpenAI Codex - Broad knowledge, sandboxed execution, full-stack development"

    def _get_version(self) -> str:
        """Get Codex CLI version."""
        import asyncio
        try:
            result = asyncio.get_event_loop().run_until_complete(
                run_command([self._command, "--version"], timeout=10)
            )
            if result.success:
                return result.stdout.strip()
        except Exception:
            pass
        return "unknown"

    def capabilities(self) -> AgentCapabilities:
        return (
            AgentCapabilities.EXECUTE |
            AgentCapabilities.STREAM |
            AgentCapabilities.FILE_EDIT |
            AgentCapabilities.FILE_CREATE |
            AgentCapabilities.COMMAND_RUN |
            AgentCapabilities.MCP |
            AgentCapabilities.JSON_OUTPUT |
            AgentCapabilities.SANDBOX
        )

    def can_handle(self, task: Task) -> float:
        """Codex excels at broad coding tasks and testing."""
        scores = {
            TaskType.CODE_CREATE: 0.90,
            TaskType.CODE_EDIT: 0.85,
            TaskType.TEST_WRITE: 0.90,
            TaskType.TEST_RUN: 0.95,
            TaskType.BUG_FIX: 0.85,
            TaskType.REFACTOR: 0.75,
            TaskType.ANALYZE: 0.75,
            TaskType.REVIEW: 0.70,
            TaskType.DOCUMENT: 0.70,
            TaskType.RESEARCH: 0.65,
            TaskType.GENERAL: 0.75,
        }
        return scores.get(task.task_type, 0.7)

    async def validate(self) -> bool:
        """Check if Codex CLI is available."""
        return is_available(self._command)

    async def execute(self, task: Task) -> Result:
        """Execute a task using Codex CLI."""
        start_time = datetime.now()

        cmd = self._build_command(task)

        try:
            result = await run_command(
                cmd,
                timeout=task.constraints.timeout,
                cwd=str(task.constraints.working_directory) if task.constraints.working_directory else None,
            )

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            return self._parse_result(result.stdout, result.stderr, result.success, duration_ms)

        except Exception as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            return Result(
                success=False,
                output="",
                error=str(e),
                metadata=ResultMetadata(agent=self.name, duration_ms=duration_ms),
            )

    async def stream(self, task: Task) -> AsyncIterator[str]:
        """Stream response from Codex CLI."""
        cmd = self._build_command(task, stream=True)

        async for chunk in stream_command(
            cmd,
            cwd=str(task.constraints.working_directory) if task.constraints.working_directory else None,
        ):
            yield chunk

    def _build_command(self, task: Task, stream: bool = False) -> list[str]:
        """Build the Codex CLI command."""
        # Use `codex exec` for non-interactive mode
        cmd = [self._command, "exec", task.prompt]

        # Add JSON output for parsing (unless streaming)
        if not stream:
            cmd.append("--json")

        # Add sandbox mode based on constraints
        if task.constraints.auto_approve:
            cmd.extend(["--sandbox", "workspace-write"])
        else:
            cmd.extend(["--sandbox", "read-only"])

        # Session continuation
        if "session_id" in task.context and task.context["session_id"]:
            cmd.extend(["resume", task.context["session_id"]])

        return cmd

    def _parse_result(
        self,
        stdout: str,
        stderr: str,
        success: bool,
        duration_ms: int,
    ) -> Result:
        """Parse Codex CLI output into Result."""
        actions: list[Action] = []

        # Codex outputs newline-delimited JSON events
        output_text = ""
        session_id = None

        for line in stdout.strip().split("\n"):
            if not line:
                continue
            try:
                event = json.loads(line)
                event_type = event.get("type", "")

                # Extract assistant message content
                if event_type == "assistant_message":
                    content = event.get("content", "")
                    if isinstance(content, str):
                        output_text += content
                    elif isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                output_text += item.get("text", "")

                # Extract session ID
                if "session_id" in event:
                    session_id = event["session_id"]

                # Extract tool calls
                if event_type == "tool_call":
                    action_type = self._tool_to_action_type(event.get("name", ""))
                    actions.append(Action(
                        type=action_type,
                        details={
                            "tool": event.get("name"),
                            "input": event.get("input", {}),
                        },
                    ))

            except json.JSONDecodeError:
                # Not JSON, append as text
                output_text += line + "\n"

        return Result(
            success=success,
            output=output_text.strip() or stdout,
            actions=actions,
            session_id=session_id,
            error=stderr if not success else None,
            metadata=ResultMetadata(
                agent=self.name,
                duration_ms=duration_ms,
                raw_output=stdout,
            ),
        )

    def _tool_to_action_type(self, tool_name: str) -> ActionType:
        """Map Codex tool names to action types."""
        mapping = {
            "read_file": ActionType.FILE_READ,
            "write_file": ActionType.FILE_CREATE,
            "edit_file": ActionType.FILE_EDIT,
            "shell": ActionType.COMMAND_RUN,
            "run_command": ActionType.COMMAND_RUN,
        }
        return mapping.get(tool_name, ActionType.OTHER)
