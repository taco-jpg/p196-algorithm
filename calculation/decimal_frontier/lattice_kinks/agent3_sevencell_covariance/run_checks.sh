#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
c++ -O3 -std=c++17 "$HERE/primary.cpp" -o "$TMP/primary"
c++ -O3 -std=c++17 "$HERE/independent_check.cpp" -o "$TMP/independent"
"$TMP/primary" 2 0 "$TMP/source.bin"
"$TMP/primary" 0 1563 "$TMP/g0.bin"
"$TMP/primary" 1 0 "$TMP/g1.bin"
(
 cd "$TMP"
 printf '%s\n' \
 'a2d878e8247679cb7e0b70bb2cdd2171678e17c3b193f09fc35a31de1c32d143  source.bin' \
 '49e548146c864a8e9788cfdf988a8c28ed466a843c4cf804ce617ecc120432dd  g0.bin' \
 '785922edd7c7d0fb54f42e6461d95cab51d8ce1a800e191358a0d443dbd7a9bd  g1.bin' \
 | sha256sum -c -
)
"$TMP/independent" "$TMP/source.bin" "$TMP/g0.bin" "$TMP/g1.bin" "$HERE"
echo 'ALL SEVEN-CELL LOCAL CHECKS PASSED (not repository verify.py)'
