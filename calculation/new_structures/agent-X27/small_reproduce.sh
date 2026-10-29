#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
c++ -O3 -std=c++17 "$HERE/verify.cpp" -lgmpxx -lgmp -o "$TMP/verify"
c++ -O3 -std=c++17 "$HERE/longrun.cpp" -o "$TMP/longrun"
c++ -O3 -std=c++17 "$HERE/small_scan.cpp" -o "$TMP/small_scan"
python3 "$HERE/small_scan_independent.py" 5000
"$TMP/small_scan" 5000 32 | tee "$TMP/small_scan.log"
grep -Fx '879 978 ' "$TMP/small_scan.log"
"$TMP/verify" 0 20000 32 879 > "$TMP/verify879.log"
"$TMP/longrun" 0 100000 879 > "$TMP/longrun879.log"
grep -F 'SUMMARY Q=0 T=20000 initialDigits=3 finalDigits=8245 overflow=8242 oddLenStates=9987 evenLenStates=10014 maxFirstOdd=17 noOddGlobal=0 middleOddEvenN=4108 trace=38dd817f4a0c68c3' "$TMP/verify879.log"
grep -F 'SUMMARY T=100000 finalN=41387 overflow=41384 maxOdd=22 noOdd=0 firstNoOdd=-1 out16=25 firstOut16=9237 out32=0 firstOut32=-1 palindrome=-1' "$TMP/longrun879.log"
python3 - <<'PY'
assert 879+978 == 978+879 == 1857
print('STARTER COALESCENCE PASS')
PY
printf 'X27 SMALL-SEED ALL CHECKS PASSED\n'
