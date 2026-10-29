#!/bin/sh
set -eu
BASE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CXX=${CXX:-g++}
"$CXX" -std=c++17 -O3 "$BASE/extract_gamma.cpp" -o /tmp/w30_extract_gamma
/tmp/w30_extract_gamma 60000 >/tmp/w30_gamma60000.txt
python3 "$BASE/sync_physical.py" /tmp/w30_gamma60000.txt
python3 "$BASE/reset_checker.py"
