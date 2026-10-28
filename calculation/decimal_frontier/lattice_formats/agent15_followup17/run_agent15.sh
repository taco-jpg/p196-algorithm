#!/bin/sh
# From the directory containing these files, on a machine with 8 GB+ RAM:
# sh run_agent15.sh; all exact control runs and 17 per-stream checks are performed.
set -eu
cd "$(dirname "$0")"
c++ -O3 -std=c++17 agent15_compact.cpp -o agent15_compact
c++ -O3 -std=c++17 agent15_mirror.cpp -o agent15_mirror
c++ -O3 -std=c++17 agent15_independent_mirror.cpp -o agent15_independent_mirror
nice -n 10 python3 -u agent15_verify.py
