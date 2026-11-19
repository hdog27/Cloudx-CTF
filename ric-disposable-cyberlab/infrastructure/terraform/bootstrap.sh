#!/bin/bash
set -euo pipefail

# Safe, local-only learning scenario: no deliberately vulnerable network daemon.
id learner >/dev/null 2>&1 || useradd --create-home --shell /bin/bash learner

install -d -o root -g root -m 0755 /opt/cloudx-ctf
install -d -o root -g root -m 0755 /opt/cloudx-ctf/legacy-backups

cat > /opt/cloudx-ctf/START-HERE.txt <<'EOF'
Cloudx-CTF / Phase 1 — Linux file permissions

Scenario: A fictional application stored a sensitive value in a backup file.
Objective:
  1. Switch to the unprivileged learner account: sudo -iu learner
  2. Find the legacy backup under /opt/cloudx-ctf
  3. Explain why the file is readable by an unprivileged user
  4. As an administrator, apply a safer permission and verify that
     the learner can no longer read it.

Useful commands: find, ls -l, stat, cat, chmod, sudo -iu learner
Record the commands and evidence you used. This is an instructor demo,
not a secure or graded challenge. The example flag is public in GitHub.
EOF

cat > /opt/cloudx-ctf/legacy-backups/app.conf.bak <<'EOF'
# FAKE TRAINING DATA — NEVER STORE REAL SECRETS HERE
APP_NAME=Cloudx-Demo
DEMO_FLAG=CLOUDX{VERIFY_BACKUP_FILE_PERMISSIONS}
EOF

chmod 0644 /opt/cloudx-ctf/START-HERE.txt
chmod 0644 /opt/cloudx-ctf/legacy-backups/app.conf.bak
logger -t cloudx-ctf "Phase 1 permissions lab initialized"
