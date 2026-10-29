#!/usr/bin/env bash
# Independent exact arithmetic controls for the two phase-2/H76 branches.
# Does not assert the hard branches UNSAT; this is NOT a complete width14 result.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$HERE/../../../.." && pwd)
DATA="$HERE/../data"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
c++ -O3 -std=c++17 "$HERE/agent1_width14_dfs.cpp" -o "$TMP/dfs"
# Check all 19 possible first free pair coefficients: every excluded digit
# fails by the exact overapproximating arithmetic prefix propagation.
for d in $(seq 0 18); do
  if [[ "$d" == 9 || "$d" == 18 ]]; then
    "$TMP/dfs" 2 76 "$d" --prefix > "$TMP/prefix_$d.log"
    grep -q "^PREFIX phase=2 H=76 first=$d may_survive=1$" "$TMP/prefix_$d.log"
  else
    if "$TMP/dfs" 2 76 "$d" --prefix > "$TMP/prefix_$d.log"; then
      echo "Unexpected phase2 prefix survivor: $d" >&2
      exit 1
    else
      rc=$?
      [[ "$rc" == 5 ]] || exit "$rc"
    fi
    grep -q "^PREFIX phase=2 H=76 first=$d may_survive=0$" "$TMP/prefix_$d.log"
  fi
done
printf 'PASS phase2 H76: 17/19 first-digit branches excluded by independent exact prefix arithmetic\n'
# Each remaining first-digit branch is feasible at a short finite horizon.
# Witnesses are from independent QF_BV and one-hot Z3 encodings, respectively.
for d in 9 18; do
  file="$DATA/agent1_width14_o2_first${d}_h10.json"
  python3 "$HERE/agent1_independent_replay.py" 14 2 10 "$file" > "$TMP/replay_$d.log"
  grep -q '^PASS width=14 o=2 H=10' "$TMP/replay_$d.log"
  cells=$(python3 -c 'import json,sys;print(",".join(map(str,json.load(open(sys.argv[1]))["initial_layer"][6:])))' "$file")
  "$TMP/dfs" 2 10 "$d" --check "$cells" > "$TMP/cpp_$d.log"
  grep -q '^CHECK phase=2 H=10 ' "$TMP/cpp_$d.log"
  grep -q 'life=10 ' "$TMP/cpp_$d.log"
  printf 'PASS phase2 H10 first=%s: decimal big-int replay and C++ arithmetic check\n' "$d"
done
printf 'PASS phase2 branch partition and independent positive controls (H76 hard branches remain UNDECIDED)\n'
