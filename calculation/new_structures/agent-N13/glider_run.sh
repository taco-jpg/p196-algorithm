#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
D="$(mktemp -d)"
trap 'rm -rf "$D"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra glider.cpp -o "$D/glider"
"$D/glider" 5200 20000 100 1000 | tee "$D/cxx.out"
grep -Fx 'half=5200 steps=20000 patch=100 begin=1000 digit_checks=13300700 first_bad=-1 wrong_offset19_failures=18137 r75_failures=1000,1001,' "$D/cxx.out"
python3 glider_independent.py
printf 'AGENT_N13_SHEARED_DIGIT_GLIDER_PASS\n'
