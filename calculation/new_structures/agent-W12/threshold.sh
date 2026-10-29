#!/bin/sh
# Independent exact q=3042 all-length certificate and q=3041 near-miss.
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bin=/tmp/w12_threshold_$$
pass=/tmp/w12_threshold_pass_$$.log
fail=/tmp/w12_threshold_fail_$$.log
trap 'rm -f "$bin" "$pass" "$fail"' EXIT HUP INT TERM
c++ -O3 -std=c++17 "$here/check.cpp" -o "$bin"
"$bin" 3042 20000 > "$pass"
grep -F 'PASS ALL_Q_GE_3042 steps=20000 gamma0=11697 gamma1=8303 max_outer_equal_prefix=16 periods=1:19954,4:47, pairperiods=1:19955,4:46,' "$pass"
grep -F 't=20000 digits=20475 period=1 pairperiod=1 mismatch=6 inserted=0000 fnv64=335bb10132092c44' "$pass"
if "$bin" 3041 20000 > "$fail" 2>&1; then
  echo 'ERROR: q=3041 unexpectedly passed the 128-digit central-window criterion' >&2; exit 1
fi
grep -F 'PERIOD_FAIL t=19998' "$fail"
echo 'SHARPENING_PASS: q>=3042 certified; q=3041 misses only the chosen 128-digit core criterion.'
