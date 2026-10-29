#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
cxx="$(command -v g++)"
exe="$(mktemp /tmp/x10_overlap_XXXXXX)"
trap 'rm -f "$exe"' EXIT
"$cxx" -std=c++17 -O3 -Wall -Wextra overlap_capacity.cpp -o "$exe"
"$exe" | tee /tmp/agent_X10_overlap_check.txt
cmp /tmp/agent_X10_overlap_check.txt overlap_capacity_check.txt
python3 overlap_bigint.py
printf 'ALL X10 OVERLAP CHECKS PASSED\n'
