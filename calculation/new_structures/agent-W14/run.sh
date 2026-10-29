#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
g++ -O3 -std=c++17 gauge_replay.cpp -lgmp -o /tmp/w14_gauge_replay
python3 independent_check.py
/tmp/w14_gauge_replay rows.txt 300 20000
/tmp/w14_gauge_replay rows.txt 301 20000
