# ══════════════════════════════════════════════
# Interactive Loop
# ══════════════════════════════════════════════
from coding_agent.configs import OPENROUTER_MODEL, MIN_REQUEST_LENGTH
from coding_agent.Agent_Task import run_agent
from pathlib import Path

MIN_REQUEST_LENGTH 

def interactive_loop(working_dir: Path) -> None:

    print("=" * 60)
    print("  Coding Agent | CrewAI + OpenRouter")
    print("=" * 60)

    print(f"Project: {working_dir}")
    print(f"Model:   {OPENROUTER_MODEL}")

    print("Type 'exit' to quit.\n")

    while True:

        try:
            request = input("You > ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if request.lower() in {"exit", "quit"}:
            print("Goodbye!")
            return

        if not request:
            continue

        if len(request) < MIN_REQUEST_LENGTH:
            print(f"Please enter a task with at least {MIN_REQUEST_LENGTH} characters.\n")
            continue

        print("\nWorking...\n")

        try:
            report = run_agent(
                request,
                working_dir,
            )

            print("\n" + "=" * 60)
            print("Final Report")
            print("=" * 60)

            print(report)
            print()

        except Exception as e:
            print(f"\nError: {e}\n")