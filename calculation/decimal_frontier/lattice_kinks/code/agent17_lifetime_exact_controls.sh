#!/bin/sh
# From calculation/decimal_frontier/lattice_kinks/code. Requires python-sat with CaDiCaL.
set -eu
cd "$(dirname "$0")"
python3 agent17_lifetime_exact.py --selftest
out=$(mktemp)
trap 'rm -f "$out"' EXIT HUP INT TERM
# Hstart=40 is ALREADY UNSAT in this exact lattice, so the legacy lifet.py
# incorrectly prints 39 (its unproved assumption is that Hstart is SAT).
python3 agent17_lifetime_exact.py ../data/lat_p12m9.txt 8 0 40 --max-horizon 64 > "$out"
cat "$out"
grep -Fx 'EXACT: max SAT horizon=33; first UNSAT horizon=34' "$out"
printf '%s\n' 'PASS: published p12/m9 width8 o0 control, including UNSAT initial horizon'
