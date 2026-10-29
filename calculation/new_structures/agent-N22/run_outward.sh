#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
CXX="${CXX:-g++}"
"$CXX" -O3 -std=c++17 -Wall -Wextra -Werror "$here/outward_digits.cpp" -o "$tmp/digits"
"$CXX" -O3 -std=c++17 -Wall -Wextra -Werror "$here/outward_gmp.cpp" -lgmpxx -lgmp -o "$tmp/gmp"
"$CXX" -O3 -std=c++17 -Wall -Wextra -Werror "$here/front_probe.cpp" -o "$tmp/pairwords"
"$tmp/digits" "$here/rows.csv" "$here/B.csv" "$here/tail80.csv" 20000 "$tmp/observed" 100
"$tmp/gmp" "$here/rows.csv" "$here/B.csv" "$here/tail80.csv" 20000 100 "$tmp/observed_checkpoints.txt" | tail -n 2
tail80="$(head -n1 "$here/tail80.csv")"
"$tmp/pairwords" "$here/rows.csv" "$here/B.csv" "$tail80" 0 100 1000 > "$tmp/probe.log" 2> "$tmp/probe.err"
python3 - "$tmp/observed_stats.csv" "$tmp/probe.log" <<'PY'
import sys,re,csv
with open(sys.argv[1]) as f:
    data={int(d['t']):int(d['matched_band']) for d in csv.DictReader(f)}
front={}
for line in open(sys.argv[2]):
    match=re.match(r't=(\d+) front=(-?\d+)',line)
    if match: front[int(match.group(1))]=int(match.group(2))
shared=sorted(data.keys()&front.keys())
assert len(shared)>=40
assert all(data[t]==4800+front[t] for t in shared)
assert all(front[t]>=2 for t in range(8,129,8))
assert (front[128],front[176],front[184],front[256],front[1000])==(7,0,-1,-9,-119)
print('INDEPENDENT PAIRWORD CONTROL: ',len(shared),'exact frontier checkpoints, front +7 at t128, first negative at t184, t1000=-119')
PY
"$tmp/digits" "$here/rows.csv" "$here/B.csv" "$here/tail80.csv" 50000 "$tmp/diagnostic" 100 --until-break 2> "$tmp/break.log"
grep -q '^B_BREAK phase=6 t=33166 index=10$' "$tmp/break.log"
echo 'CONTROL: rooted rec2 exterior fails exactly at t=33166, index=10 (no infinite claim)'
cp "$here/rows.csv" "$tmp/corrupted.csv"
sed -i '1s/^4,/5,/' "$tmp/corrupted.csv"
if "$tmp/digits" "$tmp/corrupted.csv" "$here/B.csv" "$here/tail80.csv" 20000 "$tmp/corrupted" 100 > "$tmp/negative.log" 2>&1; then
   echo 'FAIL: corrupted rec2 lattice was accepted' >&2; exit 1
fi
echo 'NEGATIVE CONTROL: corrupted rec2 row rejected'
python3 - <<'PY'
n=89
for t in range(24):
    assert str(n)!=str(n)[::-1]
    n+=int(str(n)[::-1])
assert str(n)==str(n)[::-1] and n==8813200023188
print('POSITIVE CONTROL: base-10 seed 89 reaches palindrome at t=24')
PY
echo 'ALL OUTWARD-DRIFT REPLAY CHECKS PASSED'
