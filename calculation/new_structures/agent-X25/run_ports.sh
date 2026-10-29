#!/bin/sh
set -eu
cd "$(dirname "$0")"
temp=$(mktemp -d)
trap 'rm -rf "$temp"' EXIT HUP INT TERM
g++ -O3 -std=c++17 carry_ports.cpp -o "$temp/ports"
"$temp/ports" 600 2500 5000 > "$temp/ports.txt"
diff -u carry_ports_expected.txt "$temp/ports.txt"
"$temp/ports" 350 1500 3000 | grep -F 'pin_runs_stable A=3,1,0,3, D=3,1,0,3,'
g++ -O3 -std=c++17 carry_ports_gmp.cpp -lgmpxx -lgmp -o "$temp/gmp"
"$temp/gmp" 140 960 1792 | tee "$temp/gmp.txt"
grep -F 'A actual-number carry-port recurrence good=721/1001 lastfailure=421 stable_from=422' "$temp/gmp.txt"
grep -F 'D actual-number carry-port recurrence good=648/1001 lastfailure=496 stable_from=497' "$temp/gmp.txt"
grep -F 'GMP_DECIMAL_DIGIT_CARRY_PASS three seeds, 1793 time states each' "$temp/gmp.txt"
echo CARRY_PORTS_PASS
