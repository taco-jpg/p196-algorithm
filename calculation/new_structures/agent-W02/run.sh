#!/bin/sh
set -eu
here=calculation/new_structures/agent-W02
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cxx=g++
"$cxx" -O3 -std=c++17 "$here/front_trace.cpp" -o "$tmp/front_trace"
"$cxx" -O3 -std=c++17 "$here/independent_decimal.cpp" -o "$tmp/independent_decimal"
"$cxx" -O3 -std=c++17 "$here/local_clock.cpp" -o "$tmp/local_clock"
"$cxx" -O3 -std=c++17 "$here/independent_collision.cpp" -o "$tmp/independent_collision"
"$tmp/front_trace" 5000 > "$tmp/front.tsv" 2> "$tmp/front.log"
grep -F 'FRONT_LOCK A_right_last_failure=336 B_right_last_failure=154 A_second_site_last_failure=4592 B_second_site_last_failure=4644 checks=4925 matches=4606,4792' "$tmp/front.log"
[ "$(sha256sum "$tmp/front.tsv" | cut -d' ' -f1)" = 79691eb68dd08543c3627b68e5b46bde3de5b7aa86fb7ee9419b3e14e23e0ab8 ]
"$tmp/independent_decimal" "$tmp/front.tsv" 5000
"$tmp/local_clock" 3100 $(seq 180 9 1620) > "$tmp/clock.tsv"
[ "$(sha256sum "$tmp/clock.tsv" | cut -d' ' -f1)" = d349e2c7df422e114574a1fda56b2f5c94c9ba134622efe8d516e32f403f27f4 ]
python3 - "$tmp/clock.tsv" <<'PY'
import sys
r={int(v[0]):(int(v[1]),int(v[2])) for line in open(sys.argv[1]) if (v:=line.split())}
assert len(r)==161 and min(r)==180 and max(r)==1620
assert all(r[g+378][0]-r[g][0]==608 for g in range(189,550,9))
assert r[558][0]-r[180][0]==605
assert r[936][0]-r[558][0]==607
print('COLLISION_CLOCK_PASS 41 affine cases, two exact boundary countercontrols')
PY
"$tmp/independent_collision"
cp "$tmp/front.tsv" "$tmp/corrupted.tsv"
sed -i '2s/ 1 / 2 /' "$tmp/corrupted.tsv"
if "$tmp/independent_decimal" "$tmp/corrupted.tsv" 1 >/dev/null 2>&1; then echo 'NEGATIVE_CONTROL_FAILED' >&2; exit 1; fi
echo 'CORRUPTION_REJECTED; ALL W02 CHECKS PASSED'
