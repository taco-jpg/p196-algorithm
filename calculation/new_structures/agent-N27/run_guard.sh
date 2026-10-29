#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -std=c++17 -O3 -Wall -Wextra -Wno-unused-function -Wno-unused-variable -Wno-return-type guard_replay.cpp -o /tmp/n27_guard_replay
/tmp/n27_guard_replay 40 94
/tmp/n27_guard_replay 80 185
/tmp/n27_guard_replay 200 476
/tmp/n27_guard_replay 500 1184
/tmp/n27_guard_replay 3000 7254
python3 guard_generic.py
