#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 semica.py
c++ -O3 -std=c++17 particle.cpp -o /tmp/n17_particle
c++ -O3 -std=c++17 independent_gmp.cpp -lgmp -o /tmp/n17_gmp
/tmp/n17_particle 500 1000 >/tmp/n17_control.csv
/tmp/n17_particle 8000 20000 >/tmp/n17_particle.csv
/tmp/n17_gmp 8000 20000 /tmp/n17_gmp.csv
diff -u <(tail -n +2 /tmp/n17_particle.csv) <(tail -n +2 /tmp/n17_gmp.csv)
echo "PASS: exact exterior, digit-list and independent GMP agree at all milestones."
