#!/bin/sh
# Execute from any working directory, requires Python 3 and C++17; GMP is optional.
set -eu
cd "$(dirname "$0")/../../.."
python3 calculation/new_structures/agent-W30/test_local_rule.py
c++ -std=c++17 -O3 -Wall -Wextra calculation/new_structures/agent-W30/replay.cpp -o /tmp/p196_agent_w30_replay
/tmp/p196_agent_w30_replay 20 150 350 175
/tmp/p196_agent_w30_replay 300 4200 20000 1000
if test "${W30_GMP:-0}" = 1; then
  c++ -std=c++17 -O3 -DW30_GMP calculation/new_structures/agent-W30/replay.cpp -lgmpxx -lgmp -o /tmp/p196_agent_w30_gmp
  /tmp/p196_agent_w30_gmp 20 150 350 175
fi
