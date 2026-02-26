# Installation

This guide covers installing Agent and the AI CLI tools it orchestrates.

## Requirements

- **Python 3.11 or higher**
- **pip** (Python package manager)
- At least one AI CLI tool installed

## Install Agent

### From PyPI (Recommended)

```bash
pip install agent
```

### From Source

```bash
git clone https://github.com/dipankarsarkar/agent.git
cd agent
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

### With Documentation Dependencies

```bash
pip install -e ".[docs]"
```

## Install AI CLI Tools

Agent works with multiple AI coding assistants. Install at least one:

=== "Claude Code"

    Claude Code is Anthropic's official CLI for Claude.

    ```bash
    # Install via npm
    npm install -g @anthropic-ai/claude-code

    # Set your API key
    export ANTHROPIC_API_KEY="your-api-key-here"

    # Verify installation
    claude --version
    ```

    [:octicons-link-external-16: Claude Code Documentation](https://docs.anthropic.com/claude-code)

=== "Codex CLI"

    OpenAI's Codex CLI for code generation and editing.

    ```bash
    # Install via npm
    npm install -g @openai/codex

    # Set your API key
    export OPENAI_API_KEY="your-api-key-here"

    # Verify installation
    codex --version
    ```

    [:octicons-link-external-16: Codex CLI Documentation](https://platform.openai.com/docs/codex)

=== "Gemini CLI"

    Google's Gemini CLI with massive context windows.

    ```bash
    # Install via npm
    npm install -g @google/gemini-cli

    # Set your API key
    export GOOGLE_API_KEY="your-api-key-here"

    # Verify installation
    gemini --version
    ```

    [:octicons-link-external-16: Gemini CLI Documentation](https://github.com/google-gemini/gemini-cli)

=== "Aider"

    Git-integrated AI coding assistant.

    ```bash
    # Install via pip
    pip install aider-chat

    # Set your API key (uses OpenAI or Anthropic)
    export OPENAI_API_KEY="your-api-key-here"

    # Verify installation
    aider --version
    ```

    [:octicons-link-external-16: Aider Documentation](https://aider.chat)

## Verify Installation

After installation, verify everything is working:

```bash
# Check Agent version
agent --version

# List available agents (shows which CLI tools are detected)
agent agents list

# Test a specific agent
agent agents test claude
```

Example output:

```
$ agent agents list
+----------+---------+------------------------------------------+
| Name     | Version | Description                              |
+----------+---------+------------------------------------------+
| claude   | 1.0.0   | Claude Code - complex refactoring        |
| codex    | 1.0.0   | Codex CLI - sandboxed execution          |
+----------+---------+------------------------------------------+
```

## Troubleshooting

### Agent Not Found

If `agent` command is not found:

```bash
# Check if it's in your PATH
which agent

# Or run via Python module
python -m agent --version
```

### CLI Tool Not Detected

If an AI CLI tool isn't showing in `agent agents list`:

1. Verify the tool is installed: `which claude` (or `codex`, `gemini`)
2. Check the tool works standalone: `claude --version`
3. Ensure API keys are set in your environment

### Permission Errors

On Unix systems, you may need to fix permissions:

```bash
# Fix npm global permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

## Next Steps

Once installed, continue to the [Quick Start](quickstart.md) guide to run your first multi-agent workflow.
