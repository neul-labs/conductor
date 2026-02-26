"""Claude CLI agent implementation."""

from __future__ import annotations

import json
import re
from collections.abc import AsyncIterator
from datetime import datetime
from typing import TYPE_CHECKING

from agent.core.agent import Agent, AgentCapabilities
from agent.core.result import Action, ActionType, Result, ResultMetadata
from agent.core.task import Task, TaskType
from agent.utils.process import run_command, stream_command, is_available

if TYPE_CHECKING:
    pass


class ClaudeAgent(Agent):
    """Agent that wraps the Claude CLI (claude command).

    Claude Code is Anthropic's CLI for Claude, supporting:
    - Headless mode with -p flag
    - JSON output with --output-format json
    - Tool allowlisting with --allowedTools
    - Session continuation with --continue/--resume
    - Streaming responses

    Environment: ANTHROPIC_API_KEY

    Strengths:
    - Complex refactoring and multi-file changes
    - Architectural work and code analysis
    - Quality synthesis and review
    """

    def __init__(self, command: str = "claude") -> None:
        self._command = command
        self._version_cache: str | None = None

    @property
    def name(self) -> str:
        return "claude"

    @property
    def version(self) -> str:
        if self._version_cache is None:
            self._version_cache = self._get_version()
        return self._version_cache

    @property
    def description(self) -> str:
        return "Claude Code - Complex refactoring, multi-file changes, architectural work"

    def _get_version(self) -> str:
        """Get Claude CLI version."""
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
            AgentCapabilities.GIT_COMMIT |
            AgentCapabilities.MCP |
            AgentCapabilities.CONTINUE_SESSION |
            AgentCapabilities.JSON_OUTPUT |
            AgentCapabilities.WEB_ACCESS
        )

    def can_handle(self, task: Task) -> float:
        """Claude excels at complex refactoring and architectural work."""
        scores = {
            TaskType.REFACTOR: 0.95,
            TaskType.ANALYZE: 0.90,
            TaskType.REVIEW: 0.85,
            TaskType.CODE_EDIT: 0.85,
            TaskType.CODE_CREATE: 0.85,
            TaskType.BUG_FIX: 0.80,
            TaskType.DOCUMENT: 0.80,
            TaskType.TEST_WRITE: 0.75,
            TaskType.RESEARCH: 0.70,
            TaskType.GENERAL: 0.75,
        }
        return scores.get(task.task_type, 0.7)

    async def validate(self) -> bool:
        """Check if Claude CLI is available."""
        return is_available(self._command)

    async def execute(self, task: Task) -> Result:
        """Execute a task using Claude CLI."""
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
        """Stream response from Claude CLI."""
        cmd = self._build_command(task, stream=True)

        async for chunk in stream_command(
            cmd,
            cwd=str(task.constraints.working_directory) if task.constraints.working_directory else None,
        ):
            yield chunk

    def _build_command(self, task: Task, stream: bool = False) -> list[str]:
        """Build the Claude CLI command."""
        cmd = [self._command, "-p", task.prompt]

        # Add JSON output for parsing (unless streaming)
        if not stream:
            cmd.extend(["--output-format", "json"])

        # Add allowed tools
        if task.constraints.allowed_tools:
            for tool in task.constraints.allowed_tools:
                cmd.extend(["--allowedTools", tool])

        # Add context from previous tasks
        if "session_id" in task.context and task.context["session_id"]:
            cmd.extend(["--resume", task.context["session_id"]])
        elif task.context.get("continue_session"):
            cmd.append("--continue")

        return cmd

    def _parse_result(
        self,
        stdout: str,
        stderr: str,
        success: bool,
        duration_ms: int,
    ) -> Result:
        """Parse Claude CLI output into Result."""
        actions: list[Action] = []

        # Try to parse JSON output
        try:
            data = json.loads(stdout)
            output = data.get("result", stdout)
            session_id = data.get("session_id")

            # Extract token usage
            input_tokens = data.get("input_tokens")
            output_tokens = data.get("output_tokens")
            cost_usd = data.get("cost_usd")

            # Parse tool calls as actions
            for tc in data.get("tool_calls", []):
                action_type = self._tool_to_action_type(tc.get("name", ""))
                actions.append(Action(
                    type=action_type,
                    details={
                        "tool": tc.get("name"),
                        "input": tc.get("input", {}),
                    },
                    success=tc.get("output") is not None,
                ))

            return Result(
                success=success,
                output=output,
                actions=actions,
                session_id=session_id,
                metadata=ResultMetadata(
                    agent=self.name,
                    duration_ms=duration_ms,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=cost_usd,
                    raw_output=stdout,
                ),
            )
        except json.JSONDecodeError:
            # Plain text output
            return Result(
                success=success,
                output=stdout,
                actions=self._infer_actions_from_text(stdout),
                error=stderr if not success else None,
                metadata=ResultMetadata(
                    agent=self.name,
                    duration_ms=duration_ms,
                    raw_output=stdout,
                ),
            )

    def _tool_to_action_type(self, tool_name: str) -> ActionType:
        """Map Claude tool names to action types."""
        mapping = {
            "Read": ActionType.FILE_READ,
            "Write": ActionType.FILE_CREATE,
            "Edit": ActionType.FILE_EDIT,
            "Bash": ActionType.COMMAND_RUN,
            "WebFetch": ActionType.WEB_FETCH,
            "WebSearch": ActionType.WEB_SEARCH,
        }
        return mapping.get(tool_name, ActionType.OTHER)

    def _infer_actions_from_text(self, text: str) -> list[Action]:
        """Infer actions from plain text output."""
        actions: list[Action] = []

        # Look for file edit patterns
        file_patterns = [
            r"(?:edited|modified|updated|changed)\s+['\"]?([^\s'\"]+)['\"]?",
            r"(?:created|wrote)\s+['\"]?([^\s'\"]+)['\"]?",
        ]
        for pattern in file_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                actions.append(Action(
                    type=ActionType.FILE_EDIT,
                    details={"path": match.group(1)},
                ))

        # Look for command patterns
        cmd_patterns = [
            r"(?:ran|executed|running)\s+[`'\"]([^`'\"]+)[`'\"]",
        ]
        for pattern in cmd_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                actions.append(Action(
                    type=ActionType.COMMAND_RUN,
                    details={"command": match.group(1)},
                ))

        return actions
