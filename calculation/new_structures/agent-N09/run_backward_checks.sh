#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 learn_regular.py > /tmp/p196_agent_N09_backward_counts.txt
diff -u backward_counts.txt /tmp/p196_agent_N09_backward_counts.txt
echo 'AGENT_N09_BACKWARD_CHECKS_PASSED'
