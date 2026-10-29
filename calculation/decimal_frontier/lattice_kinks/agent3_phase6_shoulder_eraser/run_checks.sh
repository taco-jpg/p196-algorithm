#!/bin/sh
set -eu
D=calculation/decimal_frontier/lattice_kinks/agent3_phase6_shoulder_eraser
CXX=${CXX:-g++}
"$CXX" -O3 -std=c++17 -Wall -Wextra "$D/primary.cpp" -o /tmp/agent3_phase6_shoulder_eraser
/tmp/agent3_phase6_shoulder_eraser "$D/controls.txt"
python3 "$D/independent_check.py"
