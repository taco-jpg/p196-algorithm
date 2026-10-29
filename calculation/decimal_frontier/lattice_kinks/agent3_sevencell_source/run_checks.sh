#!/bin/sh
set -eu
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT HUP INT TERM
c++ -O3 -std=c++17 "$D/seven_rank.cpp" -o "$T/primary"
c++ -O3 -std=c++17 "$D/independent.cpp" -o "$T/independent"
"$T/primary" "$T/witness.bin"
printf '%s  %s\n' 'a2d878e8247679cb7e0b70bb2cdd2171678e17c3b193f09fc35a31de1c32d143' "$T/witness.bin" | sha256sum -c -
"$T/independent" "$T/witness.bin" "$D"
printf 'ALL SEVEN-CELL STANDALONE CHECKS PASSED\n'
