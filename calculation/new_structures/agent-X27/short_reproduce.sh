#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
c++ -O3 -std=c++17 "$HERE/verify.cpp" -lgmpxx -lgmp -o "$TMP/verify"
c++ -O3 -std=c++17 "$HERE/longrun.cpp" -o "$TMP/longrun"
python3 "$HERE/coalescence.py"
"$TMP/verify" 3 20000 32 > "$TMP/short-verify.log"
"$TMP/longrun" 3 100000 > "$TMP/short-longrun.log"
grep -F 'SUMMARY Q=3 T=20000 initialDigits=8 finalDigits=8272 overflow=8264 oddLenStates=10038 evenLenStates=9963 maxFirstOdd=20 noOddGlobal=0 middleOddEvenN=4158 trace=16db298943fc4b8e' "$TMP/short-verify.log"
grep -F 'SUMMARY T=100000 finalN=41354 overflow=41346 maxOdd=20 noOdd=0 firstNoOdd=-1 out16=17 firstOut16=1731 out32=0 firstOut32=-1 palindrome=-1' "$TMP/short-longrun.log"
printf 'X27 SHORT SEED ALL CHECKS PASSED\n'
