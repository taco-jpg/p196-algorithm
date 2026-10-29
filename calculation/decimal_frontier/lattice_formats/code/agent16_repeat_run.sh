#!/usr/bin/env bash
# All-parameter PAPER theorem: finite transfer and independent constructions.
set -euo pipefail
D=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
OUT=${1:-$(mktemp -d)}
mkdir -p "$OUT"
ulimit -v 8000000
python3 "$D/repeat101100.py" --max-base 100 --max-k 8 > "$OUT/repeat_transfer.txt"
python3 "$D/repeat101100_construct.py" > "$OUT/repeat_construct.txt"
tail -n 2 "$OUT/repeat_transfer.txt"
tail -n 3 "$OUT/repeat_construct.txt"
c++ -std=c++17 -O3 "$D/agent16_root_graph.cpp" -o "$OUT/agent16_graph"
for pair in '9 1100011000' '13 1010010000'; do
  read -r b g <<< "$pair"
  nice -n 15 "$OUT/agent16_graph" "$b" "$g" > "$OUT/control_b${b}.txt"
done
python3 - "$OUT" <<'PY'
from pathlib import Path
import sys
out=Path(sys.argv[1])
s9=(out/'control_b9.txt').read_text()
s13=(out/'control_b13.txt').read_text()
assert s9.startswith('G base=9 g=1100011000 states=956310 edges=1005301 nontrivial_sccs=7')
assert s9.count('SCC depth=61 size=4')==2
assert s13.startswith('G base=13 g=1010010000 states=250302 edges=254201 nontrivial_sccs=5')
assert 'SCC depth=55 size=1' in s13 and 'SCC depth=75 size=1' in s13
print('ALL REPEAT/CONTROL CHECKS PASSED')
PY
