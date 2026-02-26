"""Process management utilities for running CLI commands."""

from __future__ import annotations

import asyncio
import shutil
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any


@dataclass
class CommandResult:
    """Result of running a command."""

    stdout: str
    stderr: str
    returncode: int
    command: list[str]

    @property
    def success(self) -> bool:
        """Whether the command succeeded."""
        return self.returncode == 0


async def run_command(
    cmd: list[str],
    *,
    timeout: float | None = None,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    input_data: str | None = None,
) -> CommandResult:
    """Run a command and return the result.

    Args:
        cmd: Command and arguments as a list
        timeout: Maximum execution time in seconds
        cwd: Working directory
        env: Environment variables (merged with current env)
        input_data: Data to send to stdin

    Returns:
        CommandResult with stdout, stderr, and return code

    Raises:
        asyncio.TimeoutError: If the command times out
    """
    import os

    # Merge environment
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE if input_data else None,
        cwd=cwd,
        env=full_env,
    )

    try:
        stdout_bytes, stderr_bytes = await asyncio.wait_for(
            process.communicate(input=input_data.encode() if input_data else None),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        raise

    return CommandResult(
        stdout=stdout_bytes.decode("utf-8", errors="replace"),
        stderr=stderr_bytes.decode("utf-8", errors="replace"),
        returncode=process.returncode or 0,
        command=cmd,
    )


async def stream_command(
    cmd: list[str],
    *,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
) -> AsyncIterator[str]:
    """Stream output from a command line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory
        env: Environment variables

    Yields:
        Lines of output as they arrive
    """
    import os

    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=cwd,
        env=full_env,
    )

    if process.stdout:
        async for line in process.stdout:
            yield line.decode("utf-8", errors="replace")

    await process.wait()


def which(command: str) -> str | None:
    """Find the path to a command.

    Args:
        command: Command name to find

    Returns:
        Full path to the command, or None if not found
    """
    return shutil.which(command)


def is_available(command: str) -> bool:
    """Check if a command is available.

    Args:
        command: Command name to check

    Returns:
        True if the command is available
    """
    return which(command) is not None
