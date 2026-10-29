#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 paired_transducer.py
python3 regular_cert.py
python3 replay_bigint.py 20000
g++ -O3 -std=c++17 -Wall -Wextra decimal_replay.cpp -o /tmp/agent_n08_decimal_replay
/tmp/agent_n08_decimal_replay 196 20000
