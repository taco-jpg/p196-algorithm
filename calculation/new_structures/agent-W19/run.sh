#!/bin/sh
set -eu
repo=calculation/new_structures/agent-W19
phase=calculation/new_structures/agent-N26/p8_rec0_rows.txt
bin=$(mktemp -d)
trap 'rm -rf "$bin"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra -Werror "$repo/search_centre.cpp" -o "$bin/search"
g++ -O3 -std=c++17 -Wall -Wextra -Werror "$repo/erasure.cpp" -o "$bin/erase"
g++ -O3 -std=c++17 -Wall -Wextra -Werror "$repo/replay_gmp.cpp" -lgmpxx -lgmp -o "$bin/gmp"
"$bin/search"
"$bin/erase" 12 0 1
"$bin/erase" 12 300 1
"$bin/erase" 10 2 2
"$bin/erase" 10 3 4
python3 "$repo/independent_mixed.py"
python3 "$repo/make_seed.py" --out "$bin/seed"
"$bin/erase" --long 12 300 1 20000 "$phase"
"$bin/gmp" "$phase" "$bin/seed_zero.txt" "$bin/seed_ones.txt" 20000
printf '%s\n' 'W19_ALL_CONTROLS_PASS'
