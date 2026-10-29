#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 transducer.py
python3 dfa_checker.py
g++ -O3 -std=c++17 -Wall -Wextra replay.cpp -lgmpxx -lgmp -o /tmp/p196_agent_N09_replay
/tmp/p196_agent_N09_replay 196 20000 2000 > /tmp/p196_agent_N09_replay_196_20000.txt
diff -u replay_196_20000.txt /tmp/p196_agent_N09_replay_196_20000.txt
echo 'AGENT_N09_ALL_CHECKS_PASSED'
