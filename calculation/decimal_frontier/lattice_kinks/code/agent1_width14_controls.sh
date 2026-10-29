#!/usr/bin/env bash
# Complete reproducibility suite for agent-1 rec0 width14 result.
# Execute from any directory in a complete repository checkout.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$HERE/../../../.." && pwd)
CASEFILE="$HERE/../data/agent1_width14_cases.json"
BIN=$(mktemp -d)
trap 'rm -rf "$BIN"' EXIT

# Ensure the independently transcribed Z3 lattice is bytewise equivalent to
# the current repository's SCC-0 columns; no silent input drift is accepted.
PYTHONPATH="$HERE" python3 - "$ROOT/calculation/decimal_frontier/lattice_formats/p8_scc.txt" <<'PYCODE'
import sys
from lib7 import parse_scc
from agent1_width14_z3 import Wcols, gam, nB, m
rec=parse_scc(sys.argv[1])[0]
assert (rec['p'],len(rec['path']),len(rec['cyc']),rec['g'])==(8,39,20,'10101010')
assert rec['cyc']==Wcols and nB==39 and m==20 and gam==[1,0,1,0,1,0,1,0]
print('PASS independently encoded lattice equals repository rec0 SCC-0')
PYCODE

# Independent exact phase2 branch partition and two arithmetic/bigint positives.
bash "$HERE/agent1_width14_phase2_prefix_controls.sh"

# Mandatory independent exterior reference controls, each before the K1 run.
c++ -std=c++17 -O3 "$ROOT/calculation/decimal_frontier/lattice_formats/code/bauto3.cpp" -o "$BIN/bauto3"
"$BIN/bauto3" 9 10 10 -g 1100011000 -cap 3000000 -maxscc 8 > "$BIN/base9.log"
"$BIN/bauto3" 13 10 10 -g 1010010000 -cap 3000000 -maxscc 8 > "$BIN/base13.log"
grep -Eq '^SCC .*cyclen=4 depth=61 ' "$BIN/base9.log"
grep -Eq '^SCC .*depth=55 ' "$BIN/base13.log"
grep -Eq '^SCC .*depth=75 ' "$BIN/base13.log"
printf 'PASS position-automaton controls: b9 m=4 depth61; b13 depth55,depth75\n'

# Optional independent QF_BV encoding: four width14/H10 SAT controls, each
# replayed with ordinary decimal big integers. This encoding shares only the
# recorded lattice input with the one-hot solver and is not used for UNSAT.
if python3 -c 'import ctypes; ctypes.CDLL("libz3.so.4")' >/dev/null 2>&1; then
  for o in 0 1 2 3; do
    K1_WORK_DIR="$BIN" python3 "$HERE/agent1_width14_bv.py" 14 "$o" 10 > "$BIN/bv_o${o}.log"
    grep -q 'result 1 ' "$BIN/bv_o${o}.log"
    python3 "$HERE/agent1_independent_replay.py" 14 "$o" 10 "$BIN/agent1_bv_w14_o${o}_h10.smt2.witness.json"
  done
  printf 'PASS independent QF_BV H10 positive controls for all four width14 classes\n'
fi

# Primary cross-platform solver is canonical sat_kink.py + python-sat/CaDiCaL.
if python3 -c 'from pysat.solvers import Cadical153' >/dev/null 2>&1; then
  python3 "$HERE/agent1_width14_reproduce.py" --all --cases "$CASEFILE"
else
  # Second independent CNF implementation uses only Python stdlib and
  # system libz3.so.4 (Linux). One solver process per case, no state cap.
  export K1_WORK_DIR="$BIN"
  for entry in '0 32 33' '1 34 35' '2 28 30' '3 38 39'; do
    read -r o satH unsatH <<< "$entry"
    python3 "$HERE/agent1_width14_z3.py" 8 "$o" "$satH" --witness > "$BIN/w8_sat.log"
    grep -q 'result 1 ' "$BIN/w8_sat.log"
    python3 "$HERE/agent1_independent_replay.py" 8 "$o" "$satH" "$BIN/agent1_w8_o${o}_h${satH}.smt2.witness.json"
    python3 "$HERE/agent1_width14_z3.py" 8 "$o" "$unsatH" > "$BIN/w8_unsat.log"
    grep -q 'result -1 ' "$BIN/w8_unsat.log"
  done
  printf 'PASS all width8 boundary controls\n'
  python3 "$HERE/agent1_width14_z3.py" 14 3 30 --seq --witness > "$BIN/w14_positive.log"
  grep -q 'result 1 ' "$BIN/w14_positive.log"
  python3 "$HERE/agent1_independent_replay.py" 14 3 30 "$BIN/agent1_w14_o3_h30.smt2.witness.json"
  # Mutation control: a corrupted frozen exterior digit MUST be rejected.
  python3 - "$BIN/agent1_w14_o3_h30.smt2.witness.json" "$BIN/tampered.json" <<'PY_MALFORMED'
import json,sys
j=json.load(open(sys.argv[1]));j['initial_layer'][0]=(j['initial_layer'][0]+1)%19
with open(sys.argv[2],'w') as f:json.dump(j,f)
PY_MALFORMED
  if python3 "$HERE/agent1_independent_replay.py" 14 3 30 "$BIN/tampered.json" > "$BIN/tampered.log" 2>&1; then
    echo 'ERROR: independent bigint checker accepted a corrupted frozen digit' >&2
    exit 1
  fi
  printf 'PASS width14 finite positive control and corrupted-witness rejection\n'
  mapfile -t targets < <(python3 - "$CASEFILE" <<'PY'
import json,sys
j=json.load(open(sys.argv[1]))
assert j['status']=='COMPUTED' and j['base']==10 and j['free_half_width']==14
bounds=j['confirmed_unsat_by_phase']
assert set(bounds)=={'0','1','2','3'}
for o in range(4):print(o,bounds[str(o)])
PY
)
  for entry in "${targets[@]}"; do
    read -r o H <<< "$entry"
    # Phase 3 was searched with compact sequential one-hot CNF;
    # other phases used canonical pairwise at-most-one clauses.
    z3_extra=()
    if [[ "$o" == '3' ]]; then z3_extra=(--seq); fi
    python3 "$HERE/agent1_width14_z3.py" 14 "$o" "$H" "${z3_extra[@]}" > "$BIN/w14_o${o}.log"
    grep -q 'result -1 ' "$BIN/w14_o${o}.log"
    printf 'PASS width14 class=%s H=%s UNSAT\n' "$o" "$H"
  done
fi
printf 'PASS all controls and all four exact width14 UNSAT cases\n'
