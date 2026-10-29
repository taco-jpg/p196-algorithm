#!/bin/sh
set -eu
cd "$(dirname "$0")"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
g++ -O3 -std=c++17 -Wall -Wextra shield_profile.cpp -o "$tmp/profile"
g++ -O3 -std=c++17 -Wall -Wextra shield_verify.cpp -o "$tmp/verify"
"$tmp/profile" > "$tmp/crossings.csv"
python3 - "$tmp/crossings.csv" <<'PY'
import json,sys
expected=json.load(open('shield_data.json'))
rows=[[int(x) for x in l.strip().split(',')] for l in open(sys.argv[1])]
assert [r[0] for r in rows]==[r['h'] for r in expected['rows']]
assert [r[1:] for r in rows]==[r['first'] for r in expected['rows']]
print('PROFILE_TABLE_PASS',len(rows),'dyadic levels',len(rows)*5,'crossing times')
PY
"$tmp/verify"
python3 shield_independent.py 4 5 6 7 8 9 10
printf 'AGENT_N15_DYADIC_SHIELD_ALL_LOCAL_CHECKS_PASSED\n'
