#!/bin/sh
# Directional mirror guard: 26,710 exact decimal additions and first off-clock edge.
set -eu
cd "$(dirname "$0")/../../.."
python3 calculation/new_structures/agent-W30/test_mirror_lock.py
c++ -std=c++17 -O3 -Wall -Wextra -DW30_ASYM_GUARD calculation/new_structures/agent-W30/replay.cpp -o /tmp/p196_w30_mirror
/tmp/p196_w30_mirror 300 4200 26710 2000
if test "${W30_TEST_BREAK:-0}" = 1; then
  if /tmp/p196_w30_mirror 300 4200 26711 26710 > /tmp/p196_w30_first_break.log 2>&1; then
     echo "ERROR: the deliberately overextended alternating overflow expectation should fail"
     exit 1
  fi
  grep -q 'FAILED: overflow schedule t=26710 expected=1 observed=0' /tmp/p196_w30_first_break.log
  echo "PASS first schedule-break negative control at edge t=26710"
fi
