#!/bin/sh
# Run from repository root. Optional first argument is finite time horizon.
set -eu
T=${1:-20000}
cd calculation/new_structures/agent-W16
g++ -std=c++17 -O3 skew_contract.cpp -o /tmp/w16_contract
g++ -std=c++17 -O3 independent_gmp.cpp -lgmpxx -lgmp -o /tmp/w16_gmp
/tmp/w16_contract 440 530 "$T"
/tmp/w16_gmp 440 530 "$T"
# A distinct, independently pumped pair of counts.
/tmp/w16_contract 443 537 "$T"
