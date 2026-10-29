#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DIR="$(mktemp -d)"
trap 'rm -rf "$DIR"' EXIT
c++ -O3 -std=c++17 "$HERE/verify.cpp" -lgmpxx -lgmp -o "$DIR/x27_verify"
c++ -O3 -std=c++17 "$HERE/longrun.cpp" -o "$DIR/x27_longrun"
"$DIR/x27_verify" 47 20000 > "$DIR/verify.log"
"$DIR/x27_longrun" 47 100000 > "$DIR/longrun.log"
grep -F 'SUMMARY Q=47 T=20000 initialDigits=96 finalDigits=8343 overflow=8247 oddLenStates=10017 evenLenStates=9984 maxFirstOdd=15 noOddGlobal=0 middleOddEvenN=4087 trace=10deca89aba7faa4' "$DIR/verify.log"
grep -F 'SUMMARY T=100000 finalN=41459 overflow=41363 maxOdd=25 noOdd=0 firstNoOdd=-1 out16=18 firstOut16=24456 out32=0 firstOut32=-1 palindrome=-1' "$DIR/longrun.log"
python3 "$HERE/prefix_abstract.py" 4 8
printf 'X27 ALL LOCAL CHECKS PASSED\n'
