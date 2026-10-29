#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -O3 -std=c++17 -fopenmp exhaustive.cpp -o /tmp/w10_exhaustive
OMP_NUM_THREADS=5 /tmp/w10_exhaustive
python3 bulk_absorption.py
python3 replay_samples.py
