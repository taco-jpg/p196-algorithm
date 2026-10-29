#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 two_counter_pdr.py
g++ -std=c++17 -O3 -Wall -Wextra independent_20k.cpp -o /tmp/w04_digits
g++ -std=c++17 -O3 -Wall -Wextra independent_gmp.cpp -lgmpxx -lgmp -o /tmp/w04_gmp
/tmp/w04_digits 15000 15000 20000 100 > /tmp/w04_reference.log
/tmp/w04_digits 15000 16000 20000 100 > /tmp/w04_digits.log
/tmp/w04_gmp 15000 16000 20000 100 > /tmp/w04_gmp.log
python3 compare_checkpoints.py /tmp/w04_digits.log /tmp/w04_gmp.log
if /tmp/w04_digits 15000 16000 10 16001 > /tmp/w04_bad.log 2>&1; then
  echo 'FAIL: impossible bulk-width negative control was accepted' >&2;exit 1
else
  grep 'BAND_SHAPE_FAIL' /tmp/w04_bad.log
fi
tail -1 /tmp/w04_reference.log
tail -1 /tmp/w04_digits.log
tail -1 /tmp/w04_gmp.log
echo AGENT_W04_ALL_CHECKS_PASSED