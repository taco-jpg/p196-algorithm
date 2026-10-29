#!/bin/sh
set -eu
D="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python3 "$D/two_step_bigint.py"
c++ -std=c++17 -O3 -Wall -Wextra "$D/two_step_eraser.cpp" -o /tmp/w07_two_step_eraser
/tmp/w07_two_step_eraser
c++ -std=c++17 -O3 -Wall -Wextra "$D/gmp_check.cpp" -lgmpxx -lgmp -o /tmp/w07_gmp_check
/tmp/w07_gmp_check 300 20000 4
