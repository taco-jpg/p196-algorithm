#!/usr/bin/env bash
# Complete uncapped finite controls (primary DFS, separate brute force, b9/b13).
set -euo pipefail
D=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
OUT=${1:-$(mktemp -d)}
mkdir -p "$OUT"
ulimit -v 4000000
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
c++ -O3 -std=c++17 "$D/agent16_interior_exact.cpp" -o "$OUT/a16_interior"
nice -n 15 "$OUT/a16_interior" 4 12 | tee "$OUT/interior_primary.txt"
python3 "$D/agent16_interior_independent.py" --max-r 7 | tee "$OUT/interior_independent.txt"
c++ -O3 -std=c++17 "$D/agent16_root_graph.cpp" -o "$OUT/a16_root"
for pair in '9 1100011000' '13 1010010000'; do
    read -r b g <<< "$pair"
    nice -n 15 "$OUT/a16_root" "$b" "$g" > "$OUT/control_b${b}.txt"
done
python3 - "$OUT" <<'PY'
import sys
from pathlib import Path
out=Path(sys.argv[1]);rows={b:(out/f'control_b{b}.txt').read_text().splitlines() for b in (9,13)}
for b in (9,13): print(rows[b][0]);print(*rows[b][1:],sep='\n')
assert rows[9][0].startswith('G base=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7')
assert rows[9].count('SCC depth=61 size=4')==2
assert rows[13][0].startswith('G base=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5')
assert 'SCC depth=55 size=1' in rows[13] and 'SCC depth=75 size=1' in rows[13]
print('ALL AGENT-16 INTERIOR NO-EDGE CONTROLS PASSED')
PY
