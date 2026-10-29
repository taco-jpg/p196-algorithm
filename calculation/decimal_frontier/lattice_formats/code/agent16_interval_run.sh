#!/usr/bin/env bash
# All complete controls for exact backward interval-preimage theorem.
set -euo pipefail
D=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
OUT=${1:-$(mktemp -d)}
mkdir -p "$OUT"
ulimit -v 8000000
PYTHONPATH="$D" python3 "$D/agent16_interval_independent.py" | tee "$OUT/independent.txt"
PYTHONPATH="$D" python3 "$D/agent16_interval_preimage.py" --min-r 4 --max-r 200 > "$OUT/diagonal_pilot.txt"
PYTHONPATH="$D" python3 "$D/agent16_interval_preimage.py" --min-r 500 --max-r 500 >> "$OUT/diagonal_pilot.txt"
PYTHONPATH="$D" python3 "$D/agent16_interval_preimage.py" --min-r 1000 --max-r 1000 >> "$OUT/diagonal_pilot.txt"
tail -n 8 "$OUT/diagonal_pilot.txt"
c++ -std=c++17 -O3 "$D/agent16_interval_controls.cpp" -o "$OUT/graph"
nice -n 15 "$OUT/graph" 9 1100011000 > "$OUT/control_b9.txt"
nice -n 15 "$OUT/graph" 13 1010010000 > "$OUT/control_b13.txt"
python3 - "$OUT" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);a=(p/'control_b9.txt').read_text().splitlines();b=(p/'control_b13.txt').read_text().splitlines()
assert a[0]=='G base=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7 maxdepth=146 generated=1005301'
assert a.count('SCC depth=61 size=4')==2
assert b[0]=='G base=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5 maxdepth=197 generated=254201'
assert 'SCC depth=55 size=1' in b and 'SCC depth=75 size=1' in b
print(a[0]);print(b[0]);print('ALL CHECKS PASSED (exact interval-preimage algorithm and positive controls)')
PY
