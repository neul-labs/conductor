"""Sequential (pipeline) orchestration pattern.

In sequential orchestration, tasks are executed one after another,
with each task building on the results of the previous one.

Example:
    Research → Implement → Test → Document
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.core.result import OrchestratedResult, Result
from agent.core.task import Task

if TYPE_CHECKING:
    from agent.core.agent import Agent


class SequentialPattern:
    """Sequential orchestration pattern.

    Executes a series of tasks in order, passing context from
    one task to the next. The router selects the best agent
    for each task.

    Example:
        pattern = SequentialPattern(agents=[claude, codex])
        result = await pattern.execute([
            Task(prompt="Research authentication patterns"),
            Task(prompt="Implement the auth module"),
            Task(prompt="Write tests for auth"),
        ])
    """

    def __init__(
        self,
        agents: list[Agent],
        *,
        stop_on_failure: bool = True,
    ) -> None:
        """Initialize the sequential pattern.

        Args:
            agents: List of agents to choose from
            stop_on_failure: Whether to stop the pipeline if a task fails
        """
        self.agents = agents
        self.stop_on_failure = stop_on_failure

    async def execute(self, tasks: list[Task]) -> OrchestratedResult:
        """Execute tasks sequentially.

        Args:
            tasks: List of tasks to execute in order

        Returns:
            OrchestratedResult with all task results
        """
        results: list[Result] = []
        accumulated_context: dict = {}

        for task in tasks:
            # Add context from previous tasks
            task_with_context = task.with_context(**accumulated_context)

            # Select the best agent for this task
            agent = self._select_agent(task_with_context)

            if agent is None:
                results.append(Result(
                    success=False,
                    output="",
                    error="No available agent for task",
                    metadata={"agent": "none"},  # type: ignore
                ))
                if self.stop_on_failure:
                    break
                continue

            # Execute the task
            result = await agent.execute(task_with_context)
            results.append(result)

            # Accumulate context for next task
            accumulated_context.update(result.as_context())
            accumulated_context["previous_agent"] = agent.name

            # Stop on failure if configured
            if not result.success and self.stop_on_failure:
                break

        return OrchestratedResult(
            success=all(r.success for r in results),
            results=results,
            pattern="sequential",
        )

    def _select_agent(self, task: Task) -> Agent | None:
        """Select the best agent for a task.

        Args:
            task: The task to find an agent for

        Returns:
            The best available agent, or None if none available
        """
        if not self.agents:
            return None

        # Score each agent and pick the highest
        scored_agents = [
            (agent, agent.can_handle(task))
            for agent in self.agents
        ]

        # Sort by score descending
        scored_agents.sort(key=lambda x: x[1], reverse=True)

        # Return the best agent (if any have positive score)
        best_agent, best_score = scored_agents[0]
        if best_score > 0:
            return best_agent

        return None


class ParallelPattern:
    """Parallel orchestration pattern.

    Executes a single task across multiple agents simultaneously,
    then aggregates the results.

    Example:
        pattern = ParallelPattern(agents=[claude, codex, gemini])
        result = await pattern.execute(
            Task(prompt="Review this code for issues"),
            agents=["claude", "codex"]  # Optionally specify which agents
        )
    """

    def __init__(
        self,
        agents: list[Agent],
    ) -> None:
        """Initialize the parallel pattern.

        Args:
            agents: List of agents to use
        """
        self.agents = agents

    async def execute(
        self,
        task: Task,
        agent_names: list[str] | None = None,
    ) -> OrchestratedResult:
        """Execute a task across multiple agents in parallel.

        Args:
            task: The task to execute
            agent_names: Optional list of specific agent names to use

        Returns:
            OrchestratedResult with all agent results
        """
        import anyio

        # Filter agents if specific names provided
        if agent_names:
            agents_to_use = [a for a in self.agents if a.name in agent_names]
        else:
            agents_to_use = self.agents

        if not agents_to_use:
            return OrchestratedResult(
                success=False,
                results=[],
                pattern="parallel",
                error="No agents available",
            )

        results: list[Result] = []

        async def run_agent(agent: Agent) -> Result:
            return await agent.execute(task)

        # Run all agents in parallel
        async with anyio.create_task_group() as tg:
            result_list: list[Result] = []

            async def run_and_collect(agent: Agent) -> None:
                result = await run_agent(agent)
                result_list.append(result)

            for agent in agents_to_use:
                tg.start_soon(run_and_collect, agent)

            # Wait for all to complete
            results = result_list

        return OrchestratedResult(
            success=any(r.success for r in results),
            results=results,
            pattern="parallel",
        )
