#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -O3 -std=c++17 census.cpp -o census
python3 phase8_pumping.py
python3 independent.py
: >odd_counts.txt
for ((start=0;start<2476099;start+=200000));do
 end=$((start+200000));if ((end>2476099));then end=2476099;fi
 ./census ODD "$end" -1 "$start" >> odd_counts.txt
done
python3 aggregate.py odd_counts.txt
