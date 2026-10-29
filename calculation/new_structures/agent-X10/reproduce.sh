#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 four_sheet.py --steps 264 --middle 37 --output /tmp/agent-X10-four_sheet_data.json
g++ -std=c++17 -O3 -Wall -Wextra four_sheet_fast.cpp -o /tmp/agent-X10-four_sheet_fast
/tmp/agent-X10-four_sheet_fast 20000 > /tmp/agent-X10-fast_20k.csv
g++ -std=c++17 -O3 -Wall -Wextra decimal_replay.cpp -o /tmp/agent-X10-decimal_replay
/tmp/agent-X10-decimal_replay 20000 11985 11985 > /tmp/agent-X10-replay_20k.txt
if /tmp/agent-X10-decimal_replay 1000 200 200 continued > /tmp/agent-X10-collision.txt; then
  echo 'ERROR: small-gap collision guard negative control unexpectedly passed' >&2
  exit 1
fi
grep -q 'first_mismatch=329' /tmp/agent-X10-collision.txt
grep -q 'matched=20001 nonpal=20001 guard_exit=-1 first_mismatch=-1 final_bound=11984' /tmp/agent-X10-replay_20k.txt
echo 'ALL AGENT-X10 CHECKS PASSED'
