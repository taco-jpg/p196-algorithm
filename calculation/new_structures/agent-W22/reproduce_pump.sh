#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
g++ -std=c++17 -O3 "$ROOT/hinge_pump.cpp" -o "$TMP/pump"
g++ -std=c++17 -O3 "$ROOT/hinge_fast.cpp" -o "$TMP/digit"
(cd "$TMP" && ./pump 20000 > pump.log &&
 ./digit 14000 8001 16000 20000 > k1.log &&
 ./digit 14000 8037 16000 20000 > k37.log &&
 tail -1 pump.log && grep '^PASS ' k1.log && grep '^PASS ' k37.log)
