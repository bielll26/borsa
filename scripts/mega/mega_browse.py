#!/usr/bin/env python3
"""
MEGA CMD Wrapper - Browse, search, and download files from MEGA cloud storage.

Usage:
    python scripts/mega/mega_browse.py --action list --path /
    python scripts/mega/mega_browse.py --action find --path / --pattern "*.mp4"
    python scripts/mega/mega_browse.py --action download --path /remote/file.mp4 --output output/mega-downloads/
    python scripts/mega/mega_browse.py --action info
"""

import subprocess
import sys
import os
import argparse
import json
from pathlib import Path


def run_mega_cmd(command: list[str]) -> tuple[bool, str]:
    """Run a MEGA CMD command and return (success, output)."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip() or result.stdout.strip()
    except FileNotFoundError:
        return False, "MEGA CMD not found. Install from https://mega.io/cmd"
    except subprocess.TimeoutExpired:
        return False, "Command timed out after 60 seconds"


def check_install() -> bool:
    """Check if MEGA CMD is installed."""
    ok, output = run_mega_cmd(["mega-version"])
    if ok:
        print(f"[OK] MEGA CMD: {output.splitlines()[0]}")
        return True
    else:
        print(f"[X] {output}")
        print("\nInstall MEGA CMD from: https://mega.io/cmd")
        return False


def check_login() -> bool:
    """Check if user is logged in."""
    ok, output = run_mega_cmd(["mega-whoami"])
    if ok:
        print(f"[OK] Logged in as: {output}")
        return True
    else:
        print("[X] Not logged in to MEGA")
        print("Run: mega-login your@email.com")
        return False


def list_files(path: str = "/", detailed: bool = False) -> bool:
    """List files at the given MEGA path."""
    cmd = ["mega-ls"]
    if detailed:
        cmd.append("-l")
    cmd.append(path)

    ok, output = run_mega_cmd(cmd)
    if ok:
        print(f"\nFiles in {path}:")
        print("-" * 40)
        print(output if output else "(empty)")
        return True
    else:
        print(f"[X] Failed to list {path}: {output}")
        return False


def find_files(path: str = "/", pattern: str = "*") -> bool:
    """Search for files matching a pattern."""
    ok, output = run_mega_cmd(["mega-find", path, "--pattern", pattern])
    if ok:
        print(f"\nSearch results for '{pattern}' in {path}:")
        print("-" * 40)
        lines = output.splitlines() if output else []
        print(f"Found {len(lines)} file(s)")
        for line in lines:
            print(f"  {line}")
        return True
    else:
        print(f"[X] Search failed: {output}")
        return False


def download_file(remote_path: str, local_path: str = "output/mega-downloads/") -> bool:
    """Download a file from MEGA."""
    os.makedirs(local_path, exist_ok=True)
    print(f"Downloading {remote_path} -> {local_path}")
    ok, output = run_mega_cmd(["mega-get", remote_path, local_path])
    if ok:
        print(f"[OK] Downloaded to {local_path}")
        return True
    else:
        print(f"[X] Download failed: {output}")
        return False


def show_info() -> bool:
    """Show account and storage info."""
    print("\n--- MEGA Account Info ---")
    check_login()
    print()
    ok, output = run_mega_cmd(["mega-du", "/"])
    if ok:
        print(f"Storage usage:\n{output}")
    return ok


def main():
    parser = argparse.ArgumentParser(description="MEGA CMD file browser")
    parser.add_argument("--action", choices=["list", "find", "download", "info", "check"],
                        default="check", help="Action to perform")
    parser.add_argument("--path", default="/", help="MEGA path (default: /)")
    parser.add_argument("--pattern", default="*", help="Search pattern for find")
    parser.add_argument("--output", default="output/mega-downloads/", help="Local download path")
    parser.add_argument("--detailed", action="store_true", help="Show detailed listing")

    args = parser.parse_args()

    if not check_install():
        sys.exit(1)

    if args.action == "check":
        check_login()
    elif args.action == "list":
        if not check_login():
            sys.exit(1)
        list_files(args.path, args.detailed)
    elif args.action == "find":
        if not check_login():
            sys.exit(1)
        find_files(args.path, args.pattern)
    elif args.action == "download":
        if not check_login():
            sys.exit(1)
        download_file(args.path, args.output)
    elif args.action == "info":
        show_info()


if __name__ == "__main__":
    main()
