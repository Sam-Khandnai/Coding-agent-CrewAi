"""
coding_agent_simple.py — Educational Version

A simple coding agent with CrewAI that can:

1. List project files
2. Read file contents
3. Edit files
4. Run Python code

Usage:

    python coding_agent_simple.py path/to/project
    python coding_agent_simple.py path/to/project "Find and fix the bug"

Environment configuration (.env):

    OPENROUTER_API_KEY=sk-or-...
    OPENROUTER_MODEL=qwen/qwen3-30b-a3b-instruct-2507
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import BaseTool


os.environ["CREWAI_TRACING_ENABLED"] = "false"
# ─────────────────────────────────────────────
# Load environment variables from .env
# ─────────────────────────────────────────────

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

# Project path where the agent will work
WORKING_DIR: Path = Path(".")


# ══════════════════════════════════════════════
# Tool 1 — List Files
# ══════════════════════════════════════════════

class ListFilesTool(BaseTool):

    name: str = "list_project_files"

    description: str = (
        "Lists files and directories inside the project. "
        "To inspect a subdirectory, provide a relative path, "
        "for example 'src'."
    )

    def _run(self, path: str = ".") -> str:

        target = (WORKING_DIR / path).resolve()

        # Prevent access outside the project directory
        if not str(target).startswith(str(WORKING_DIR.resolve())):
            return "Error: Path is outside the project directory."

        if not target.is_dir():
            return f"Error: Directory '{path}' was not found."

        lines = []

        for item in sorted(
            target.iterdir(),
            key=lambda p: (not p.is_dir(), p.name)
        ):

            # Hide unnecessary directories
            if item.name in {
                "__pycache__",
                ".git",
                ".venv",
                "node_modules"
            }:
                continue

            prefix = "[DIR] " if item.is_dir() else "[FILE]"

            lines.append(
                f"{prefix} {item.relative_to(WORKING_DIR)}"
            )

        return "\n".join(lines) if lines else "Directory is empty."


# ══════════════════════════════════════════════
# Tool 2 — Read File
# ══════════════════════════════════════════════

class ReadFileTool(BaseTool):

    name: str = "read_file"

    description: str = (
        "Reads the content of a text file inside the project."
    )

    def _run(self, file_path: str) -> str:

        target = (WORKING_DIR / file_path).resolve()

        if not str(target).startswith(str(WORKING_DIR.resolve())):
            return "Error: Path is outside the project directory."

        if not target.is_file():
            return f"Error: File '{file_path}' was not found."

        try:
            return target.read_text(encoding="utf-8")

        except Exception as e:
            return f"Error while reading file: {e}"


# ══════════════════════════════════════════════
# Tool 3 — Edit File
# ══════════════════════════════════════════════

class EditFileTool(BaseTool):

    name: str = "edit_file"

    description: str = (
        "Finds exact text inside a file and replaces it with new text. "
        "Always read the file before editing it."
    )

    def _run(
        self,
        file_path: str,
        old_text: str,
        new_text: str
    ) -> str:

        target = (WORKING_DIR / file_path).resolve()

        if not str(target).startswith(str(WORKING_DIR.resolve())):
            return "Error: Path is outside the project directory."

        if not target.is_file():
            return f"Error: File '{file_path}' was not found."

        content = target.read_text(encoding="utf-8")

        if old_text not in content:
            return "Error: The specified text was not found in the file."

        if content.count(old_text) > 1:
            return (
                "Error: The specified text appears more than once. "
                "Please provide a more specific text."
            )

        updated = content.replace(old_text, new_text, 1)

        target.write_text(
            updated,
            encoding="utf-8"
        )

        return f"File '{file_path}' was successfully edited."


# ══════════════════════════════════════════════
# Tool 4 — Run Python Code
# ══════════════════════════════════════════════

class RunPythonTool(BaseTool):

    name: str = "run_python"

    description: str = (
        "Runs a Python script inside the project and returns its output."
    )

    def _run(self, script_path: str) -> str:

        target = (WORKING_DIR / script_path).resolve()

        if not str(target).startswith(str(WORKING_DIR.resolve())):
            return "Error: Path is outside the project directory."

        if not target.is_file():
            return f"Error: File '{script_path}' was not found."

        if target.suffix != ".py":
            return "Error: Only .py files can be executed."

        try:

            result = subprocess.run(
                [sys.executable, str(target)],
                cwd=str(WORKING_DIR),
                capture_output=True,
                text=True,
                timeout=30,
            )

            status = (
                "Success"
                if result.returncode == 0
                else "Failed"
            )

            return (
                f"Status: {status}\n"
                f"Output:\n{result.stdout}\n"
                f"Errors:\n{result.stderr}"
            )

        except subprocess.TimeoutExpired:
            return "Error: Execution timed out after 30 seconds."

        except Exception as e:
            return f"Error: {e}"


# ══════════════════════════════════════════════
# Create and Run Agent
# ══════════════════════════════════════════════

def run_agent(request: str) -> str:

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured. "
            "Please add it to the .env file."
        )

    # Connect to the model through OpenRouter
    llm = LLM(
        model=f"openrouter/{OPENROUTER_MODEL}",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.1,
    )

    # Define tools
    tools = [
        ListFilesTool(),
        ReadFileTool(),
        EditFileTool(),
        RunPythonTool(),
    ]

    # Define agent
    agent = Agent(
        role="Senior Software Engineer",

        goal=(
            "Find bugs, edit the necessary files, "
            "and verify the result."
        ),

        backstory=(
            "You are a senior software engineer. "
            "You only work inside the WorkingDir. "
            "Before making any edit, read the file first. "
            "After every change, run the code to verify that it works."
        ),

        llm=llm,
        tools=tools,
        verbose=True,
        allow_delegation=False,
        max_iter=15,
    )

    # Define task
    task = Task(
        description=(
            f"User request:\n{request}\n\n"

            "Required workflow:\n"

            "1. Inspect the project structure using list_project_files\n"
            "2. Read the relevant files using read_file\n"
            "3. Apply the required changes using edit_file\n"
            "4. Verify the result using run_python\n"
            "5. Provide a final report"
        ),

        expected_output=(
            "A report containing: the root cause, "
            "modified files, applied changes, "
            "and final test results."
        ),

        agent=agent,
        tools=tools,
    )

    # Run crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return getattr(result, "raw", str(result))


# ══════════════════════════════════════════════
# Interactive Loop
# ══════════════════════════════════════════════

def interactive_loop() -> None:

    print("=" * 60)
    print("  Coding Agent | CrewAI + OpenRouter")
    print("=" * 60)

    print(f"Project: {WORKING_DIR}")
    print(f"Model:   {OPENROUTER_MODEL}")

    print("Type 'exit' to quit.\n")

    while True:

        try:
            request = input("Request > ").strip()

        except (EOFError, KeyboardInterrupt):

            print("\nGoodbye!")
            return

        if request.lower() in {"exit", "quit"}:
            print("Goodbye!")
            return

        if not request:
            continue

        print("\nWorking...\n")

        try:

            report = run_agent(request)

            print("\n" + "=" * 60)
            print("Final Report")
            print("=" * 60)

            print(report)
            print()

        except Exception as e:
            print(f"\nError: {e}\n")


# ══════════════════════════════════════════════
# Program Entry Point
# ══════════════════════════════════════════════

def main() -> None:

    global WORKING_DIR

    parser = argparse.ArgumentParser(
        description="Educational Coding Agent"
    )

    parser.add_argument(
        "working_dir",
        help="Path to the project directory"
    )

    parser.add_argument(
        "request",
        nargs="?",
        help="User request (optional)"
    )

    args = parser.parse_args()

    # Set project directory
    WORKING_DIR = Path(
        args.working_dir
    ).expanduser().resolve()

    if not WORKING_DIR.is_dir():

        print(
            f"Error: Directory '{WORKING_DIR}' does not exist."
        )

        sys.exit(1)

    if args.request:

        # Direct execution
        print(run_agent(args.request))

    else:

        # Interactive mode
        interactive_loop()


if __name__ == "__main__":
    main()
