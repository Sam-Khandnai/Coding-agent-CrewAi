# ══════════════════════════════════════════════
# Program Entry Point
# ══════════════════════════════════════════════

import argparse
from pathlib import Path
import sys

from coding_agent.Agent_Task import run_agent
from coding_agent.Interactive_Loop import interactive_loop


def main() -> None:

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

    working_dir = Path(
        args.working_dir
    ).expanduser().resolve()

    if not working_dir.is_dir():
        print(
            f"Error: Directory '{working_dir}' does not exist."
        )
        sys.exit(1)

    print(f"Working directory: {working_dir}")

    if args.request:
        print(
            run_agent(
                args.request,
                working_dir,
            )
        )
    else:
        interactive_loop(working_dir)


if __name__ == "__main__":
    main()