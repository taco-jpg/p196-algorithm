#!/usr/bin/env bash
set -u
cd /workspace/p196-agent1-session-20261016/catalog-order-author/attempt-001
export LEAN_PATH=/workspace/p196-agent1-outer-20261016/proofs/contributions/agent-1/periodic-outer-catalog-20261016/choices-author/attempt-002:/workspace/p196-agent1-session-20261016/periodic-phase-parent-clean-001/agent1-periodic-phase-catalog/source
sha256sum Agent1PeriodicCatalogOrder.lean > source.sha256
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --version > lean-version.txt
ulimit -v 1800000
/usr/bin/time -v /workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent1PeriodicCatalogOrder.olean Agent1PeriodicCatalogOrder.lean > compile.log 2> resource.log
result=$?
printf '%s\n' "$result" > exit-code.txt
sha256sum Agent1PeriodicCatalogOrder.lean compile.log resource.log command.sh > evidence.sha256
cat compile.log resource.log
exit "$result"
