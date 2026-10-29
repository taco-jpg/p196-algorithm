#!/bin/sh
set -eu
D="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
c++ -std=c++17 -O3 -Wall -Wextra "$D/multigate.cpp" -o /tmp/w07_multigate
/tmp/w07_multigate
python3 "$D/multigate_bigint.py"
c++ -std=c++17 -O3 -Wall -Wextra "$D/gmp_multigate.cpp" -lgmpxx -lgmp -o /tmp/w07_gmp_multigate
/tmp/w07_gmp_multigate 300 20000
