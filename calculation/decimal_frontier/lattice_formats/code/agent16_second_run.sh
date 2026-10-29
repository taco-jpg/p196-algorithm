#!/usr/bin/env bash
# Complete independent matrix/trajectory controls and mandatory b9/b13 checks.
set -euo pipefail
D=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
OUT=${1:-$(mktemp -d)}
mkdir -p "$OUT"
ulimit -v 8000000
PYTHONPATH="$D" python3 "$D/agent16_second_independent.py" > "$OUT/second_independent.txt"
tail -n 4 "$OUT/second_independent.txt"
c++ -std=c++17 -O3 "$D/agent16_root_graph.cpp" -o "$OUT/agent16_graph"
for pair in '4 101100' '9 1100011000' '13 1010010000'; do
  read -r b g <<< "$pair"
  nice -n 15 "$OUT/agent16_graph" "$b" "$g" > "$OUT/control_b${b}.txt"
done
python3 - "$OUT" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);data={b:(p/f'control_b{b}.txt').read_text().splitlines() for b in (4,9,13)}
for b in (4,9,13):print(data[b][0])
assert data[4][0].startswith('G base=4 g=101100 states=957 edges=1012 nontrivial_sccs=4')
assert data[9][0].startswith('G base=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7')
assert data[9].count('SCC depth=61 size=4')==2
assert data[13][0].startswith('G base=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5')
assert 'SCC depth=55 size=1' in data[13]
assert 'SCC depth=75 size=1' in data[13]
print('ALL F2 ALL-K SECOND-COLUMN CONTROLS PASSED')
PY
