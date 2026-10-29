#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -O3 -std=c++17 -Wall -Wextra pump_pairs.cpp -o /tmp/n06_pump_vector
c++ -O3 -std=c++17 -Wall -Wextra gmp_pump.cpp -lgmpxx -lgmp -o /tmp/n06_pump_gmp
c++ -O3 -std=c++17 -Wall -Wextra ../buffered_prefix.cpp -o /tmp/n06_pump_seed
for L in 1 2 10 100 224; do
 T=$((110 + 88*L))
 /tmp/n06_pump_vector "$L" "$T" | tail -n 1
 { /tmp/n06_pump_seed seed "$L"; /tmp/n06_pump_seed seed "$((L+1))"; } | /tmp/n06_pump_gmp "$L" "$T" | tail -n 1
done
{ /tmp/n06_pump_seed seed 2; /tmp/n06_pump_seed seed 3; } | /tmp/n06_pump_gmp 2 5 mutate | tail -n 1 | grep -q 'firstCore=0 firstFront=0'
echo N06_PUMP_ALL_CHECKS_PASSED