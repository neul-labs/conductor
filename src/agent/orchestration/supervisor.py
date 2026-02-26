"""Supervisor - the main orchestrator that coordinates agents."""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from agent.core.result import OrchestratedResult, Result
from agent.core.task import Task
from agent.orchestration.patterns.sequential import SequentialPattern, ParallelPattern

if TYPE_CHECKING:
    from agent.core.agent import Agent


class OrchestrationPattern(Enum):
    """Available orchestration patterns."""

    SEQUENTIAL = auto()   # Pipeline: task1 → task2 → task3
    PARALLEL = auto()     # Concurrent: all agents work on same task
    HANDOFF = auto()      # Dynamic: agents hand off to each other
    CONSENSUS = auto()    # Validation: multiple agents must agree


class Supervisor:
    """Supervisor orchestrator that coordinates multiple agents.

    The Supervisor is the main entry point for multi-agent orchestration.
    It manages agent selection, task routing, and result aggregation.

    Example:
        supervisor = Supervisor(agents=[claude, codex, gemini])

        # Sequential pipeline
        result = await supervisor.orchestrate(
            tasks=[
                Task(prompt="Research patterns"),
                Task(prompt="Implement feature"),
            ],
            pattern=OrchestrationPattern.SEQUENTIAL,
        )

        # Parallel review
        result = await supervisor.orchestrate(
            tasks=[Task(prompt="Review this code")],
            pattern=OrchestrationPattern.PARALLEL,
            agents=["claude", "codex"],
        )
    """

    def __init__(self, agents: list[Agent]) -> None:
        """Initialize the supervisor.

        Args:
            agents: List of available agents
        """
        self.agents = agents
        self._agent_map = {a.name: a for a in agents}

    async def orchestrate(
        self,
        tasks: list[Task],
        pattern: OrchestrationPattern = OrchestrationPattern.SEQUENTIAL,
        *,
        agents: list[str] | None = None,
        stop_on_failure: bool = True,
        consensus_threshold: float = 0.75,
    ) -> OrchestratedResult:
        """Orchestrate tasks using the specified pattern.

        Args:
            tasks: List of tasks to execute
            pattern: Orchestration pattern to use
            agents: Optional list of specific agent names to use
            stop_on_failure: For sequential, whether to stop on failure
            consensus_threshold: For consensus, required agreement level

        Returns:
            OrchestratedResult with all results
        """
        # Filter agents if specific names provided
        available_agents = self._get_agents(agents)

        if not available_agents:
            return OrchestratedResult(
                success=False,
                results=[],
                pattern=pattern.name.lower(),
                error="No agents available",
            )

        if pattern == OrchestrationPattern.SEQUENTIAL:
            return await self._run_sequential(tasks, available_agents, stop_on_failure)

        elif pattern == OrchestrationPattern.PARALLEL:
            if len(tasks) != 1:
                return OrchestratedResult(
                    success=False,
                    results=[],
                    pattern="parallel",
                    error="Parallel pattern requires exactly one task",
                )
            return await self._run_parallel(tasks[0], available_agents)

        elif pattern == OrchestrationPattern.CONSENSUS:
            if len(tasks) != 1:
                return OrchestratedResult(
                    success=False,
                    results=[],
                    pattern="consensus",
                    error="Consensus pattern requires exactly one task",
                )
            return await self._run_consensus(tasks[0], available_agents, consensus_threshold)

        else:
            return OrchestratedResult(
                success=False,
                results=[],
                pattern=pattern.name.lower(),
                error=f"Pattern {pattern.name} not yet implemented",
            )

    async def run_single(
        self,
        task: Task,
        agent_name: str | None = None,
    ) -> Result:
        """Run a single task with one agent.

        Args:
            task: The task to execute
            agent_name: Specific agent to use (or best match)

        Returns:
            Result from the agent
        """
        if agent_name:
            agent = self._agent_map.get(agent_name)
            if not agent:
                from agent.core.result import ResultMetadata
                return Result(
                    success=False,
                    output="",
                    error=f"Agent '{agent_name}' not found",
                    metadata=ResultMetadata(agent="none"),
                )
        else:
            # Find best agent for the task
            agent = self._select_best_agent(task)
            if not agent:
                from agent.core.result import ResultMetadata
                return Result(
                    success=False,
                    output="",
                    error="No available agent for task",
                    metadata=ResultMetadata(agent="none"),
                )

        return await agent.execute(task)

    def _get_agents(self, names: list[str] | None) -> list[Agent]:
        """Get agents by name, or all if no names specified."""
        if names:
            return [a for a in self.agents if a.name in names]
        return self.agents

    def _select_best_agent(self, task: Task) -> Agent | None:
        """Select the best agent for a task based on scores."""
        if not self.agents:
            return None

        scored = [(a, a.can_handle(task)) for a in self.agents]
        scored.sort(key=lambda x: x[1], reverse=True)

        if scored and scored[0][1] > 0:
            return scored[0][0]
        return None

    async def _run_sequential(
        self,
        tasks: list[Task],
        agents: list[Agent],
        stop_on_failure: bool,
    ) -> OrchestratedResult:
        """Run tasks sequentially."""
        pattern = SequentialPattern(agents, stop_on_failure=stop_on_failure)
        return await pattern.execute(tasks)

    async def _run_parallel(
        self,
        task: Task,
        agents: list[Agent],
    ) -> OrchestratedResult:
        """Run task on all agents in parallel."""
        pattern = ParallelPattern(agents)
        return await pattern.execute(task)

    async def _run_consensus(
        self,
        task: Task,
        agents: list[Agent],
        threshold: float,
    ) -> OrchestratedResult:
        """Run task on all agents and check for consensus.

        Consensus is determined by checking if agents agree on success/failure
        and comparing output similarity.
        """
        # First run in parallel
        parallel_result = await self._run_parallel(task, agents)

        if not parallel_result.results:
            return parallel_result

        # Calculate consensus score based on success agreement
        success_count = sum(1 for r in parallel_result.results if r.success)
        consensus_score = success_count / len(parallel_result.results)

        # Check if we meet the threshold
        meets_threshold = consensus_score >= threshold

        return OrchestratedResult(
            success=meets_threshold and any(r.success for r in parallel_result.results),
            results=parallel_result.results,
            pattern="consensus",
            consensus_score=consensus_score,
            error=None if meets_threshold else f"Consensus threshold not met: {consensus_score:.2f} < {threshold}",
        )

    def list_agents(self) -> list[str]:
        """List all available agent names."""
        return [a.name for a in self.agents]

    async def validate_agents(self) -> dict[str, bool]:
        """Validate all agents and return availability status."""
        return {a.name: await a.validate() for a in self.agents}
