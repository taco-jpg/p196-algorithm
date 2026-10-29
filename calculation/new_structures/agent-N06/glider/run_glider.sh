#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -std=c++17 -O3 -Wall -Wextra ../buffered_prefix.cpp -o /tmp/n06_glider_seed
c++ -std=c++17 -O3 -Wall -Wextra gmp_glider.cpp -lgmpxx -lgmp -o /tmp/n06_glider_gmp
c++ -std=c++17 -O3 -Wall -Wextra ../frontier.cpp -o /tmp/n06_glider_vector
/tmp/n06_glider_seed seed 225 > /tmp/n06_glider_seed225.txt
/tmp/n06_glider_gmp < /tmp/n06_glider_seed225.txt | tee /tmp/n06_glider_output.txt
grep -q 'GLIDER checked=17723 front_fail=0 motif_fail=0 min_motif_match=161 first_break_t=19723 front_before=57 front_after=37 matched=0' /tmp/n06_glider_output.txt
/tmp/n06_glider_vector 225 20000 | tail -n 1 | grep -q 'SHIFT88 minus20 mismatches=0 checked=18901'
echo N06_GLIDER_161_CHECKS_PASSED