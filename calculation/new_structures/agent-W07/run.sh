#!/bin/sh
set -eu
D="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$D/reverse_fibre.py"
c++ -O3 -std=c++17 -Wall -Wextra "$D/fibre_20000.cpp" -o /tmp/w07_fibre_20000
/tmp/w07_fibre_20000 300 20000 /tmp/w07_fibre_final.txt
python3 "$D/independent_bigint.py" /tmp/w07_fibre_final.txt
c++ -O3 -std=c++17 -Wall -Wextra "$D/gmp_check.cpp" -lgmpxx -lgmp -o /tmp/w07_gmp_check
/tmp/w07_gmp_check 300 20000
