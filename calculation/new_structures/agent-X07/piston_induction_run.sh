#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 piston_induction_check.py
# The previous finite-control witness can be replayed independently as:
# c++ -std=c++17 -O3 piston_probe.cpp -lgmpxx -lgmp -o /tmp/piston_probe
# /tmp/piston_probe 60000 -2907
