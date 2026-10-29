#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -std=c++17 -O3 front_scan.cpp -o /tmp/w03_front_scan
/tmp/w03_front_scan 15 450 80 >/tmp/w03_front_scan.csv
python3 independent.py /tmp/w03_front_scan.csv repair_events.csv
grep '^52,' /tmp/w03_front_scan.csv
