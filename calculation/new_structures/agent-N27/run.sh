#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -O3 -std=c++17 -Wall -Wextra replay.cpp -o /tmp/n27_replay
/tmp/n27_replay 3000 12000 20000 0
/tmp/n27_replay 40 1000 333 1
/tmp/n27_replay 40 1000 272 0
python3 bigint_check.py 100 3000 12000 0
python3 bigint_check.py 30 40 1000 1
