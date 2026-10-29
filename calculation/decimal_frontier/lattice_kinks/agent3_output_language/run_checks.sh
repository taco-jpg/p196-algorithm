#!/bin/sh
set -eu
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT HUP INT TERM
c++ -O3 -std=c++17 -Wall -Wextra -pedantic "$D/primary.cpp" -o "$T/primary"
"$T/primary" "$T/witness.txt"
printf '%s  %s\n' ac5a2193fbcbcd5ef03cef2cd9a57185f5f570dd96b5bd55566559c801f457a8 "$T/witness.txt" | sha256sum -c -
cmp "$T/witness.txt" "$D/witness.txt"
python3 "$D/independent_check.py"
echo 'STANDALONE REPRODUCTION PASS (not repository tools/verify.py)'
