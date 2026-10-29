#!/usr/bin/env bash
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
C="${CXX:-g++}"
"$C" -std=c++17 -O2 -Wall -Wextra "$D/repair72_pump.cpp" -o "${TMPDIR:-/tmp}/n22_repair72_pump"
for d in -5 4; do
    for qk in '5 34' '5 35' '6 34' '8 40' '16 80'; do
        # intentional splitting of the two integers in qk
        read -r q k <<< "$qk"
        "${TMPDIR:-/tmp}/n22_repair72_pump" "$D/rows.csv" "$D/B.csv" "$q" "$k" "$d"
    done
done
python3 "$D/repair72_bigint.py"