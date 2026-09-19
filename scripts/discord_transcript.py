#!/usr/bin/env python3
"""Forward xangi-stackchan's structured stderr log to a Discord channel.

This helper is opt-in. It sends nothing unless XANGI_DISCORD_CHANNEL_ID is set.
"""

import json
import os
import subprocess
import sys


CHANNEL_ID = os.environ.get("XANGI_DISCORD_CHANNEL_ID", "").strip()
COMMAND = os.environ.get("XANGI_DISCORD_COMMAND", "xangi-cmd")


def send(message: str) -> None:
    if not CHANNEL_ID or not message:
        return
    try:
        subprocess.run(
            [COMMAND, "discord_send", "--channel", CHANNEL_ID, "--message", message],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:
        print(f"discord transcript error: {exc}", file=sys.stderr, flush=True)


def transcript_line(payload: dict) -> str:
    if text := str(payload.get("voice_input", "")).strip():
        return f"IN: {text}"
    if payload.get("type") == "turn.complete":
        if text := str(payload.get("text", "")).strip():
            return f"Stackchan: {text}"
    return ""


if not CHANNEL_ID:
    print("XANGI_DISCORD_CHANNEL_ID is required; transcript forwarding disabled.", file=sys.stderr)
    raise SystemExit(2)

for raw_line in sys.stdin:
    # Keep the bridge's normal structured logs visible in the terminal.
    print(raw_line, end="", file=sys.stderr, flush=True)
    try:
        payload = json.loads(raw_line)
    except json.JSONDecodeError:
        continue
    if isinstance(payload, dict):
        send(transcript_line(payload))
