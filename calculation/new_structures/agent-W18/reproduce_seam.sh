#!/usr/bin/env bash
set -euo pipefail
D=calculation/new_structures/agent-W18
X="$(mktemp -d)";trap 'rm -rf "$X"' EXIT
c++ -O3 -std=c++17 "$D/seam_wave.cpp" -o "$X/wave"
c++ -O3 -std=c++17 "$D/seam_clock.cpp" -o "$X/clock"
c++ -O3 -std=c++17 "$D/postcollision_bigint.cpp" -o "$X/big"
"$X/wave" 4138 25000 > "$X/wave.log"
"$X/clock" 19990 300 > "$X/clock.log"
"$X/big" 4138 25000 > "$X/big.log"
grep -q 'PASS Q=4138 T=25000 first_non99=20006,20010 all_nonpal=1' "$X/wave.log"
grep -q 't=25000 lengths=18644,18646,18648 ab=7395/3853+2/3855/7396 bc=7390/3866+2/3868/7390' "$X/wave.log"
grep -q 'Q=4140 first_non99=20014 delay=4' "$X/clock.log"
grep -q 'Q=4177 first_non99=20192 delay=4' "$X/clock.log"
grep -q 'PASS Q=4138 T=25000 final_digits=18644 final_hash=704483961' "$X/big.log"
echo "PASS W18: 25k direct-digit 3-seed seam, 40-size clock, independent radix1e9"
