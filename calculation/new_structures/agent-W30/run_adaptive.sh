#!/bin/sh
set -eu
BASE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CXX=${CXX:-g++}
"$CXX" -std=c++17 -O3 -Wall -Wextra "$BASE/adaptive_replay.cpp" -o /tmp/w30_adaptive_replay
python3 "$BASE/test_adaptive_graph.py"
/tmp/w30_adaptive_replay 50473 1000 5000
