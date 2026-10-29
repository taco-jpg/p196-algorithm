#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
D="$(mktemp -d)"
trap 'rm -rf "$D"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra orbit.cpp -o "$D/orbit"
c++ -std=c++17 -O3 -Wall -Wextra compare.cpp -o "$D/compare"
cd "$D"
./orbit 5200 20000 100 0 > orbit_summary.txt
sha256sum -c <(printf '1ac3fab0b58380650216be6422de62394fa7d0f55b37885420f2b19b7a612905  seed.txt\n')
grep -q 'first_gamma_error=-1 first_prefix8_error=-1 first_palindrome=-1 first_odd_pair_loss=NO final_digits=20400' orbit_summary.txt
./compare 5200 20000 100 > front_summary.txt
python3 "$OLDPWD/front_check.py" front_dense.tsv
python3 "$OLDPWD/check_bigint.py" seed.txt 0 10000 2000
python3 "$OLDPWD/check_bigint.py" seed.txt 10000 18000 2000
python3 "$OLDPWD/check_bigint.py" seed.txt 18000 20000 1000
sha256sum -c <(printf 'b2bd57e0b8c53f4353b77ee44ad3f0047975d7a7695c016a5f227e163878395d  checkpoint_20000.txt\n')
# Two controls: spatial front from a shorter initial seed, and distinct asymmetric input lifts.
./orbit 1000 5000 100 0 > control_short.txt
grep -q 'first_prefix8_error=4020 first_palindrome=-1' control_short.txt
./orbit 5200 2000 100 1 > control_asymmetric_lift.txt
grep -q 'first_gamma_error=-1 first_prefix8_error=-1 first_palindrome=-1' control_asymmetric_lift.txt
echo 'AGENT_N13_FULL_REPLAY_AND_FRONT_PASS'
