#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -std=c++17 -O3 -Wall -Wextra buffered_prefix.cpp -o /tmp/n06_buffered
c++ -std=c++17 -O3 -Wall -Wextra independent_gmp.cpp -lgmpxx -lgmp -o /tmp/n06_gmp
c++ -std=c++17 -O3 -Wall -Wextra frontier.cpp -o /tmp/n06_frontier
for L in 0 1 2 3 5 10 20 50 100 224 225 226; do
 T=$((228 + 88*L))
 /tmp/n06_buffered scan "$L" "$T"
done
/tmp/n06_buffered scan 225 20000 | tee /tmp/n06_digit_result.txt
/tmp/n06_buffered seed 225 > /tmp/n06_seed.txt
sha256sum /tmp/n06_seed.txt
/tmp/n06_gmp 20000 < /tmp/n06_seed.txt | tee /tmp/n06_gmp_result.txt
grep -q 'first8_failure=-1 palindrome=-1 gamma_failure=-1 modulo1000000007=630236571 fnv64=15053747816378579192' /tmp/n06_digit_result.txt
grep -q 'first8_failure=-1 palindrome=-1 gamma_failure=-1 modulo1000000007=630236571 fnv64=15053747816378579192' /tmp/n06_gmp_result.txt
/tmp/n06_frontier 225 20000 | tail -n 5 | tee /tmp/n06_frontier_result.txt
grep -q 'SHIFT88 minus20 mismatches=0 checked=18901' /tmp/n06_frontier_result.txt
echo N06_ALL_CHECKS_PASSED