#!/bin/sh
set -eu
here=calculation/new_structures/agent-W02
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
g++ -O3 -std=c++17 "$here/front_trace_40k.cpp" -o "$tmp/front"
g++ -O3 -std=c++17 "$here/independent_decimal_40k.cpp" -o "$tmp/check"
"$tmp/front" 40000 > "$tmp/trace.tsv" 2> "$tmp/front.log"
grep -F 'FRONT_LOCK A_right_last_failure=336 B_right_last_failure=154 A_second_site_last_failure=37804 B_second_site_last_failure=39604 checks=39925 matches=39606,39792' "$tmp/front.log"
[ "$(sha256sum "$tmp/trace.tsv" | cut -d' ' -f1)" = 3942215a5ebadbbc45f1712aa263ef7f24f84411330cd343d8b613ceb25ee3e7 ]
"$tmp/check" "$tmp/trace.tsv" 40000
python3 "$here/pulse_check_40k.py" "$tmp/trace.tsv"
cp "$tmp/trace.tsv" "$tmp/bad.tsv"
sed -i '2s/ 16 / 17 /' "$tmp/bad.tsv"
if "$tmp/check" "$tmp/bad.tsv" 1 > /dev/null 2>&1; then echo CORRUPTION_UNDETECTED >&2;exit 1;fi
echo 'W02_40K_ALL_CHECKS_PASSED'
