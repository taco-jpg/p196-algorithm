#!/usr/bin/env bash
set -u
cd /workspace/p196-agent1-session-20261016/handoff-boundary/attempt-001
export LEAN_PATH=/workspace/p196-agent1-research-20261016/proofs/contributions/agent-1/groupIII-20261016/review/clean-001/source
sha256sum Boundary.lean > source.sha256
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --version > lean-version.txt
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -o Boundary.olean Boundary.lean > Boundary.log 2>&1
result=$?
printf '%s\n' "$result" > exit-code.txt
sha256sum Boundary.lean Boundary.log command.sh > evidence.sha256
cat Boundary.log
exit "$result"
