#!/usr/bin/env bash
# Self-contained positive pumping tests and a deliberately failing shorter-root control.
set -euo pipefail
cd "$(dirname "$0")"
c++ -O3 -std=c++17 pump_universe.cpp -o /tmp/n17_pump_universe
c++ -O3 -std=c++17 pump_gmp.cpp -lgmp -o /tmp/n17_pump_gmp
c++ -O3 -std=c++17 pump_long.cpp -o /tmp/n17_pump_long
c++ -O3 -std=c++17 pump_long_gmp.cpp -lgmp -o /tmp/n17_pump_long_gmp
c++ -O3 -std=c++17 pump_random.cpp -o /tmp/n17_pump_random
c++ -O3 -std=c++17 pump_exact_control.cpp -o /tmp/n17_pump_control
/tmp/n17_pump_universe 500 1500 20 | tee /tmp/n17u.txt
/tmp/n17_pump_gmp 500 1500 20 | tee /tmp/n17g.txt
for m in 40 60 80; do /tmp/n17_pump_universe 500 1500 "$m"; done
/tmp/n17_pump_universe 1000 2500 20
/tmp/n17_pump_long 8000 20000 20 | tee /tmp/n17l.txt
/tmp/n17_pump_long_gmp 8000 20000 20 | tee /tmp/n17lg.txt
/tmp/n17_pump_random
/tmp/n17_pump_control 250 1200 20
python3 - <<'PY'
from pathlib import Path
u=Path('/tmp/n17u.txt').read_text()
g=Path('/tmp/n17g.txt').read_text()
l=Path('/tmp/n17l.txt').read_text()
lg=Path('/tmp/n17lg.txt').read_text()
for s in (u,g):
 for marker in ('variants=361','paired_steps=541861','checked_cells=372461750','firstfail=-1','bad_gamma=-1','bad_pal=-1'):
  assert marker in s,(marker,s)
for s in (l,lg):
 for marker in ('all_cells=210008000','firstfail=-1','badgamma=-1','palindrome=-1','finalLen=26000'):
  assert marker in s,(marker,s)
print('PASS: independent folded-pairword pumping evidence, 361-case basin and full 20k replay.')
PY
