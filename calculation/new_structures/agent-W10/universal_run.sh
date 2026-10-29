#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 symbolic_33.py
g++ -O3 -std=c++17 -Wall -Wextra zero_insertion.cpp -o /tmp/w10_zero_insert
/tmp/w10_zero_insert 20000 > /tmp/w10_zero_checkpoints.tsv
diff -u zero_checkpoints.tsv /tmp/w10_zero_checkpoints.tsv
bash ../agent-W10/run.sh
echo 'ALL UNIVERSAL W10 CHECKS PASSED'
