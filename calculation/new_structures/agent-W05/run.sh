#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 allq_renewal.py
c++ -std=c++17 -O3 replay.cpp -lgmpxx -lgmp -o /tmp/w05_replay_$$
trap 'rm -f /tmp/w05_replay_$$' EXIT
for q in 1 2 7 47; do /tmp/w05_replay_$$ "$q" 264; done
/tmp/w05_replay_$$ 230 20000
