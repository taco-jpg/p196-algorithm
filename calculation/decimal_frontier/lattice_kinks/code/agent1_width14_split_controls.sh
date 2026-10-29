#!/usr/bin/env bash
# Exact phase-3 split verification, OPTIONAL until every branch returns UNSAT.
# Executed from a complete repository checkout containing the matching code/
# and data/ files. Does not claim other widths or phases.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$HERE/../../../.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
export K1_WORK_DIR="$TMP"

# Independently ensure the C++ arithmetic checker has the EXACT current rec0
# 8x20 pair rows / steady carry schedule, not an accidental copied lattice.
PYTHONPATH="$HERE" python3 - "$ROOT/calculation/decimal_frontier/lattice_formats/p8_scc.txt" "$HERE/agent1_width14_latdata.h" <<'PY'
import re,sys
from lib7 import parse_scc,Lattice
p=sys.argv[1];h=open(sys.argv[2]).read();lat=Lattice(parse_scc(p)[0])
for name,exp in [('LAT_W',lat.Wt)]:
 s=re.search(name+r'\[8\]\[20\]\s*=\s*\{(.*?)\};',h,re.S).group(1)
 actual=[[int(x) for x in grp.split(',') if x.strip()] for grp in re.findall(r'\{([^{}]*)\}',s)]
 assert actual==exp,(name,actual,exp)
# Carries reproduce the exact stable external carry bits after 30 cycles.
cups=[]
for t in range(8):
 word=lat.Bt[t]+lat.Wt[t]*40
 carry=0;in_c=[]
 for d in word:
  in_c.append(carry);carry=int(d+carry>=10)
 cups.append([in_c[lat.nB+lat.m*30+j] for j in range(lat.m)])
s=re.search(r'LAT_CUP\[8\]\[20\]\s*=\s*\{(.*?)\};',h,re.S).group(1)
actual=[[int(x) for x in grp.split(',') if x.strip()] for grp in re.findall(r'\{([^{}]*)\}',s)]
assert cups==actual
print('PASS C++ row/carry data matches independent rec0 reconstruction')
PY

c++ -O3 -std=c++17 "$HERE/agent1_width14_dfs.cpp" -o "$TMP/checker"
# Mandatory SAT positive controls for EACH difficult digit: fixing the first
# free coefficient must not silently add a contradiction. Check ordinary
# 403-digit integer reverse-and-add, complete exterior and no palindrome.
for d in 1 5 10 14; do
  python3 "$HERE/agent1_width14_split.py" 14 3 10 --seq "--first=$d" --witness > "$TMP/positive${d}.log"
  grep -q 'result 1 wall' "$TMP/positive${d}.log"
  python3 "$HERE/agent1_independent_replay.py" 14 3 10 \
    "$TMP/agent1_w14_o3_h10_first${d}.smt2.witness.json" > "$TMP/replay${d}.log"
  grep -q '^PASS width=14 o=3 H=10' "$TMP/replay${d}.log"
  cells=$(python3 -c 'import json,sys; print(",".join(map(str,json.load(open(sys.argv[1]))["initial_layer"][6:])))' \
    "$TMP/agent1_w14_o3_h10_first${d}.smt2.witness.json")
  "$TMP/checker" 3 10 "$d" --check "$cells" > "$TMP/cppcheck${d}.log"
  grep -q 'life=10 ' "$TMP/cppcheck${d}.log"
  echo "PASS phase3/H10 first=$d SAT + independent C++ window and decimal bigint replay"
done
if [[ "${1:-}" == '--positive-only' ]]; then
  echo 'PASS all split-solver positive controls; H80 remains UNDECIDED'
  exit 0
fi
# Exact complete negative slices for all 15 easy first-free coefficients.
for d in 0 2 3 4 6 7 8 9 11 12 13 15 16 17 18; do
  "$TMP/checker" 3 80 "$d" 80 > "$TMP/dfs${d}.log"
  grep -q '^DONE_SLICE phase=3 H=80 ' "$TMP/dfs${d}.log"
  if grep -q '^SAT ' "$TMP/dfs${d}.log"; then exit 1; fi
  echo "PASS phase3/H80 first=$d exhaustive C++ DFS"
done
if [[ "${1:-}" == '--easy-only' ]]; then
  echo 'PASS all 15 complete C++ H80 negative slices; four hard H80 digits UNDECIDED'
  exit 0
fi
# Remaining hard first digits: exact sequential one-hot Boolean CNF through Z3.
for d in 1 5 10 14; do
  python3 "$HERE/agent1_width14_split.py" 14 3 80 --seq "--first=$d" > "$TMP/sat${d}.log"
  grep -q 'result -1 wall' "$TMP/sat${d}.log"
  echo "PASS phase3/H80 first=$d exhaustive split CNF"
done
echo 'PASS complete independent phase-3 H80 exclusion (no width14 all-phase assertion)'
