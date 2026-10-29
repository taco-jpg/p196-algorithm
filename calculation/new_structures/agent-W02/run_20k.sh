#!/bin/sh
set -eu
here=calculation/new_structures/agent-W02
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -O3 -std=c++17 "$here/front_trace_20k.cpp" -o "$tmp/front"
g++ -O3 -std=c++17 "$here/independent_decimal_20k.cpp" -o "$tmp/check"
"$tmp/front" 20000 > "$tmp/trace.tsv" 2> "$tmp/front.log"
grep -F 'FRONT_LOCK A_right_last_failure=336 B_right_last_failure=154 A_second_site_last_failure=14624 B_second_site_last_failure=18932 checks=19925 matches=19606,19792' "$tmp/front.log"
[ "$(sha256sum "$tmp/trace.tsv" | cut -d' ' -f1)" = 2b196574f6302f3263febb8629ae926d3d6861531539f86d1dfa76070e755fba ]
"$tmp/check" "$tmp/trace.tsv" 20000
python3 "$here/pulse_check.py" "$tmp/trace.tsv"
cp "$tmp/trace.tsv" "$tmp/bad.tsv"
sed -i '2s/ 16 / 17 /' "$tmp/bad.tsv"
if "$tmp/check" "$tmp/bad.tsv" 1 >/dev/null 2>&1; then echo CORRUPTION_NOT_DETECTED >&2; exit 1; fi
echo 'W02_20K_ALL_CHECKS_PASSED'
