#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -std=c++17 -O3 -march=native -mavx2 -fopenmp bitparallel_census.cpp -o /tmp/ac27_cone
/tmp/ac27_cone --selftest
/tmp/ac27_cone > census_reproduced.txt
python3 control.py
echo "AC27_FULL_CENSUS_REPRODUCED"
