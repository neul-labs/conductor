"""Main CLI entry point for agent."""

from __future__ import annotations

import asyncio
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from agent import __version__

app = typer.Typer(
    name="agent",
    help="Multi-Agent CLI Orchestrator - Coordinate AI coding agents for complex tasks.",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"[bold blue]agent[/bold blue] v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """Agent - Multi-Agent CLI Orchestrator.

    Orchestrate AI coding agents (Claude, Codex, Gemini, Aider, Continue)
    to collaborate on complex development tasks.
    """
    pass


@app.command("run")
def run_command(
    prompt: Annotated[str, typer.Argument(help="The task prompt to execute")],
    agent: Annotated[
        Optional[str],
        typer.Option(
            "--agent", "-a",
            help="Specific agent to use (claude, codex, gemini, aider, continue).",
        ),
    ] = None,
    output_format: Annotated[
        str,
        typer.Option(
            "--output-format", "-o",
            help="Output format: text, json.",
        ),
    ] = "text",
    stream: Annotated[
        bool,
        typer.Option(
            "--stream/--no-stream",
            help="Stream the response.",
        ),
    ] = True,
    timeout: Annotated[
        float,
        typer.Option(
            "--timeout", "-t",
            help="Execution timeout in seconds.",
        ),
    ] = 300.0,
) -> None:
    """Execute a task with a single agent.

    Examples:

        # Use default agent (best match)
        agent run "Fix the bug in auth.py"

        # Use specific agent
        agent run --agent codex "Write tests for the API"

        # Get JSON output
        agent run -o json "Explain this code"
    """
    from agent.agents import get_default_agents
    from agent.core.task import Task, TaskConstraints
    from agent.orchestration.supervisor import Supervisor

    # Create supervisor with default agents
    agents = get_default_agents()
    supervisor = Supervisor(agents)

    # Create task
    task = Task(
        prompt=prompt,
        constraints=TaskConstraints(
            timeout=timeout,
            stream=stream,
        ),
    )

    # Run the task
    async def _run() -> None:
        if stream and not agent:
            # Stream output for default agent selection
            selected = supervisor._select_best_agent(task)
            if selected and selected.supports(
                __import__("agent.core.agent", fromlist=["AgentCapabilities"]).AgentCapabilities.STREAM
            ):
                console.print(f"[dim]Using agent: {selected.name}[/dim]\n")
                async for chunk in selected.stream(task):
                    console.print(chunk, end="")
                console.print()
                return

        result = await supervisor.run_single(task, agent_name=agent)

        if output_format == "json":
            console.print(result.to_json())
        else:
            if result.success:
                console.print(result.output)
            else:
                console.print(f"[red]Error:[/red] {result.error}")

            if result.actions:
                console.print(f"\n[dim]Actions taken: {len(result.actions)}[/dim]")
                for action in result.actions:
                    console.print(f"  [dim]- {action.type.name}: {action.details}[/dim]")

    asyncio.run(_run())


@app.command("orchestrate")
def orchestrate_command(
    prompts: Annotated[
        list[str],
        typer.Argument(help="Task prompts to orchestrate"),
    ],
    pattern: Annotated[
        str,
        typer.Option(
            "--pattern", "-p",
            help="Orchestration pattern: sequential, parallel, consensus.",
        ),
    ] = "sequential",
    agents: Annotated[
        Optional[str],
        typer.Option(
            "--agents", "-a",
            help="Comma-separated list of agents to use.",
        ),
    ] = None,
    threshold: Annotated[
        float,
        typer.Option(
            "--threshold",
            help="Consensus threshold (0.0-1.0) for consensus pattern.",
        ),
    ] = 0.75,
    output_format: Annotated[
        str,
        typer.Option(
            "--output-format", "-o",
            help="Output format: text, json.",
        ),
    ] = "text",
) -> None:
    """Orchestrate multiple agents on a task or pipeline.

    Examples:

        # Sequential pipeline
        agent orchestrate "Research auth patterns" "Implement auth" "Write tests"

        # Parallel review
        agent orchestrate --pattern parallel "Review src/auth.py for issues"

        # Consensus validation
        agent orchestrate --pattern consensus --threshold 0.8 "Is this migration safe?"
    """
    from agent.agents import get_default_agents
    from agent.core.task import Task
    from agent.orchestration.supervisor import Supervisor, OrchestrationPattern

    # Create supervisor
    all_agents = get_default_agents()
    supervisor = Supervisor(all_agents)

    # Parse pattern
    pattern_map = {
        "sequential": OrchestrationPattern.SEQUENTIAL,
        "parallel": OrchestrationPattern.PARALLEL,
        "consensus": OrchestrationPattern.CONSENSUS,
        "handoff": OrchestrationPattern.HANDOFF,
    }
    orch_pattern = pattern_map.get(pattern.lower())
    if not orch_pattern:
        console.print(f"[red]Unknown pattern:[/red] {pattern}")
        console.print(f"Available: {', '.join(pattern_map.keys())}")
        raise typer.Exit(1)

    # Parse agent names
    agent_names = agents.split(",") if agents else None

    # Create tasks
    tasks = [Task(prompt=p) for p in prompts]

    async def _run() -> None:
        console.print(f"[bold]Orchestrating {len(tasks)} task(s) using [blue]{pattern}[/blue] pattern[/bold]\n")

        result = await supervisor.orchestrate(
            tasks=tasks,
            pattern=orch_pattern,
            agents=agent_names,
            consensus_threshold=threshold,
        )

        if output_format == "json":
            import json
            console.print(json.dumps(result.to_dict(), indent=2))
            return

        # Print results
        for i, r in enumerate(result.results):
            console.print(f"\n[bold]Task {i + 1}[/bold] ([dim]{r.metadata.agent}[/dim]):")
            if r.success:
                # Truncate long output
                output = r.output
                if len(output) > 500:
                    output = output[:500] + "..."
                console.print(output)
            else:
                console.print(f"[red]Error:[/red] {r.error}")

        # Summary
        console.print("\n" + "=" * 50)
        if result.success:
            console.print("[green]Orchestration completed successfully[/green]")
        else:
            console.print(f"[red]Orchestration failed:[/red] {result.error}")

        if result.consensus_score is not None:
            console.print(f"Consensus score: {result.consensus_score:.2%}")

        console.print(f"Total duration: {result.total_duration_ms}ms")
        if result.total_cost_usd > 0:
            console.print(f"Estimated cost: ${result.total_cost_usd:.4f}")

    asyncio.run(_run())


# Agents subcommand
agents_app = typer.Typer(
    name="agents",
    help="Manage and inspect available agents.",
)
app.add_typer(agents_app, name="agents")


@agents_app.command("list")
def agents_list(
    json_output: Annotated[
        bool,
        typer.Option("--json", "-j", help="Output as JSON."),
    ] = False,
) -> None:
    """List available agents."""
    from agent.agents import get_default_agents

    agents = get_default_agents()

    if json_output:
        import json
        data = [
            {
                "name": a.name,
                "version": a.version,
                "description": a.description,
                "capabilities": str(a.capabilities()),
            }
            for a in agents
        ]
        console.print(json.dumps(data, indent=2))
        return

    table = Table(title="Available Agents")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Description")

    for a in agents:
        table.add_row(a.name, a.version, a.description)

    console.print(table)


@agents_app.command("test")
def agents_test(
    name: Annotated[str, typer.Argument(help="Agent name to test")],
) -> None:
    """Test an agent with a simple prompt."""
    from agent.agents import get_default_agents
    from agent.core.task import Task

    agents = get_default_agents()
    agent = next((a for a in agents if a.name == name), None)

    if not agent:
        console.print(f"[red]Agent not found:[/red] {name}")
        console.print(f"Available: {', '.join(a.name for a in agents)}")
        raise typer.Exit(1)

    async def _test() -> None:
        console.print(f"[bold]Testing {name} agent...[/bold]\n")

        # Check availability
        available = await agent.validate()
        if not available:
            console.print(f"[red]Agent {name} is not available[/red]")
            console.print("Make sure the CLI tool is installed and configured.")
            raise typer.Exit(1)

        console.print(f"[green]Agent available[/green]: {agent.version}\n")

        # Run a simple test
        task = Task(prompt="Say 'Hello from agent test!' and nothing else.")
        console.print("[dim]Running test prompt...[/dim]\n")

        result = await agent.execute(task)

        if result.success:
            console.print(f"[green]Success![/green]")
            console.print(f"Response: {result.output[:200]}")
        else:
            console.print(f"[red]Failed:[/red] {result.error}")

    asyncio.run(_test())


@agents_app.command("capabilities")
def agents_capabilities() -> None:
    """Show capabilities of all agents."""
    from agent.agents import get_default_agents

    agents = get_default_agents()

    table = Table(title="Agent Capabilities")
    table.add_column("Agent", style="cyan")
    table.add_column("Capabilities")

    for a in agents:
        caps = str(a.capabilities()).replace("AgentCapabilities.", "")
        table.add_row(a.name, caps)

    console.print(table)


if __name__ == "__main__":
    app()
