#!/usr/bin/env python3
"""Grade an instructor-controlled Linux lab from machine state, not student claims."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import uuid

BACKUP = Path("/home/learner/legacy-backups/app.conf.bak")
REFLECTION = Path("/home/learner/reflection.txt")
REPORT_DIR = Path("/var/lib/cloudx-ctf/reports")

def can_read_as(username, path):
    try:
        result = subprocess.run(
            ["runuser", "-u", username, "--", "test", "-r", str(path)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=5, check=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False

def assess(backup=BACKUP, reflection=REFLECTION, owner="learner", outsider="observer"):
    if not backup.is_file():
        raise RuntimeError("Challenge backup is missing; reinitialize the exercise")
    mode = stat.S_IMODE(backup.stat().st_mode)
    secure_mode = (mode & 0o077) == 0
    outsider_blocked = not can_read_as(outsider, backup)
    owner_can_read = can_read_as(owner, backup)
    reflection_ok = reflection.is_file() and len(
        reflection.read_text(encoding="utf-8", errors="replace").strip()
    ) >= 40
    checks = [
        ("Restrict the backup to its owner", 35, secure_mode),
        ("Verify a different unprivileged user is denied", 30, outsider_blocked),
        ("Verify the legitimate owner retains access", 20, owner_can_read),
        ("Submit a reflection of at least 40 characters", 15, reflection_ok),
    ]
    score = sum(points for _, points, passed in checks if passed)
    next_steps = [
        description for description, _, passed in checks if not passed
    ]
    return {
        "attempt_id": str(uuid.uuid4()),
        "challenge_id": "linux-file-permissions-01",
        "challenge_version": "0.1",
        "assessment_version": "0.1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "score": score,
        "max_score": 100,
        "complete": score == 100,
        "rubric": [
            {"criterion": description, "possible": points,
             "earned": points if passed else 0, "passed": passed}
            for description, points, passed in checks
        ],
        "feedback": ("All automated checks passed; instructor should review the explanation."
                     if not next_steps else "Next: " + "; ".join(next_steps) + "."),
        "notes": [
            "This grades observable Linux state, not understanding or command intent.",
            "Reflection length is checked, not its correctness; instructor review is required.",
            "No shell history or secrets are sent to any external API.",
        ],
        "observed_file_mode": oct(mode),
    }

def main():
    parser = argparse.ArgumentParser(description="Grade a Cloudx-CTF Linux permissions exercise")
    parser.add_argument("--output-dir", type=Path, default=REPORT_DIR)
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error("Run as an instructor with sudo so independent user checks are reliable")
    try:
        report = assess()
        args.output_dir.mkdir(parents=True, exist_ok=True)
        path = args.output_dir / "latest-report.json"
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        os.chmod(path, 0o600)
        print(json.dumps(report, indent=2))
        print("\nSaved report:", path)
        return 0
    except (OSError, RuntimeError) as exc:
        print("Assessment error:", exc, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
