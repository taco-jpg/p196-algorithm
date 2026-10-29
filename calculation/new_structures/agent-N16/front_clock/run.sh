#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 check_twist.py
g++ -O3 -std=c++17 front_clock.cpp -lgmp -o /tmp/p196_n16_frontclock
/tmp/p196_n16_frontclock rows.txt 5 300
/tmp/p196_n16_frontclock rows.txt 100 2000
/tmp/p196_n16_frontclock rows.txt 300 20000
/tmp/p196_n16_frontclock rows.txt 301 20000
echo N16_FRONT_CLOCK_ALL_PASS
