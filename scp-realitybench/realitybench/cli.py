"""Canonical CLI entrypoint.

Implementation intentionally not faked. Commands remain unavailable until their RB contracts
are implemented; this module fails closed instead of returning mock PASS.
"""
from __future__ import annotations

import argparse

COMMANDS = ("validate", "run", "replay", "score", "verify-result", "build-suite", "commit-suite")


def main() -> int:
    parser = argparse.ArgumentParser(prog="rb")
    parser.add_argument("command", choices=COMMANDS)
    args, _ = parser.parse_known_args()
    parser.error(f"RB command '{args.command}' is defined by contract but not yet implemented; refusing mock success")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
