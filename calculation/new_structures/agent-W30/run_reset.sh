#!/bin/sh
set -eu
BASE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
sh "$BASE/run_sync.sh"
CXX=${CXX:-g++}
"$CXX" -std=c++17 -O3 -Wall -Wextra "$BASE/adaptive_windows.cpp" -o /tmp/w30_window_probe
/tmp/w30_window_probe 85000
