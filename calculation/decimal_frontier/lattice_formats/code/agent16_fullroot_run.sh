#!/usr/bin/env bash
# Reproduce the exact all-base 101100 rooted graph theorem and positive controls.
set -euo pipefail
D=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
OUT=${1:-$(mktemp -d)}
mkdir -p "$OUT"
ulimit -v 8000000
c++ -std=c++17 -O3 "$D/agent16_root_graph.cpp" -o "$OUT/agent16_graph"
python3 "$D/agent16_root_independent.py" --binary "$OUT/agent16_graph" \
  --witness "$D/agent16_b4_loops.json" > "$OUT/independent.txt"
grep '^PASS' "$OUT/independent.txt"
for pair in '9 1100011000' '13 1010010000'; do
  read -r b g <<< "$pair"
  nice -n 15 "$OUT/agent16_graph" "$b" "$g" > "$OUT/control_b${b}.txt"
done
python3 - "$OUT" <<'PY'
from pathlib import Path
import sys
out=Path(sys.argv[1]);data={}
for b in (9,13):
    lines=(out/f'control_b{b}.txt').read_text().splitlines()
    data[b]=lines
    print(lines[0]); print(*lines[1:],sep='\n')
assert data[9][0]=='G base=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7 maxdepth=146 generated=1005301'
assert data[13][0]=='G base=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5 maxdepth=197 generated=254201'
assert data[9].count('SCC depth=61 size=4')==2
assert 'SCC depth=55 size=1' in data[13]
assert 'SCC depth=75 size=1' in data[13]
print('ALL GRAPH/CONTROL CHECKS PASSED')
PY
