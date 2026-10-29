"""Delete the configured local SQLite checkpoint file after explicit confirmation."""

import argparse
from pathlib import Path

from _bootstrap import ROOT  # noqa: F401

from src.config import PROJECT_ROOT, get_settings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yes", action="store_true", help="confirm deletion without prompting")
    args = parser.parse_args()
    configured = get_settings().checkpoint_db_path
    if not configured:
        print("CHECKPOINT_DB_PATH is not configured; nothing to delete.")
        return
    target = Path(configured)
    if not target.is_absolute():
        target = (PROJECT_ROOT / target).resolve()
    safe_root = (PROJECT_ROOT / "data" / "checkpoints").resolve()
    if safe_root not in target.parents:
        raise SystemExit(f"Refusing to delete outside {safe_root}: {target}")
    if not target.exists():
        print(f"Checkpoint file does not exist: {target}")
        return
    if not args.yes:
        answer = input(f"Delete {target}? Type DELETE to confirm: ")
        if answer != "DELETE":
            print("Cancelled.")
            return
    target.unlink()
    print(f"Deleted local checkpoint file: {target}")


if __name__ == "__main__":
    main()

