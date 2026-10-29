#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -std=c++17 -O3 cap_scan.cpp -o /tmp/w03_cap_scan
/tmp/w03_cap_scan all >/tmp/w03_cap_scan.csv
python3 independent_caps.py /tmp/w03_cap_scan.csv
c++ -std=c++17 -O3 independent20k.cpp -o /tmp/w03_digits_20k
/tmp/w03_digits_20k 200 88 26 20000 | grep 'PASS 20000 steps, len=8638 gamma=8234 hash=232300713'
python3 replay20k.py 200 88 26 20000
