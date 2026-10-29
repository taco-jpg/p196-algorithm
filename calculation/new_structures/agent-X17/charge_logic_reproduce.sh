#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
"${CXX:-g++}" -std=c++17 -O3 -Wall -Wextra -Werror "$here/charge_logic.cpp" -o "$tmp/charge_logic"
for n in 2001 6001 10001 20001; do "$tmp/charge_logic" "$n" "$tmp/charge_logic_$n.csv"; done
python3 "$here/charge_logic.py" 2001 "$tmp/python_2001.csv"
python3 - "$here/charge_logic_2001.csv" "$tmp/charge_logic_2001.csv" "$tmp/python_2001.csv" <<'PY'
import csv,sys
lists=[]
for f in sys.argv[1:]:
 with open(f,newline='') as g: lists.append(list(csv.reader(g)))
assert lists[0]==lists[1]==lists[2]
print('PASS: 256 Python bigint / C++ digit / stored gate truth-table rows identical')
PY
python3 "$here/charge_logic_bdd.py" "$tmp" "$tmp/charge_logic_bdd.json"
python3 - "$here/charge_logic_bdd.json" "$tmp/charge_logic_bdd.json" <<'PY'
import json,sys
assert json.load(open(sys.argv[1]))==json.load(open(sys.argv[2]))
print('PASS: 12-node minimized exact BDD matches recorded source-controlled JSON')
PY
if [ "${DEEP:-0}" = 1 ]; then
  python3 "$here/charge_logic.py" 6001 "$tmp/python_6001.csv"
  python3 - "$tmp/charge_logic_6001.csv" "$tmp/python_6001.csv" <<'PY'
import csv,sys
with open(sys.argv[1],newline='') as a,open(sys.argv[2],newline='') as b:
 assert list(csv.reader(a))==list(csv.reader(b))
print('PASS: extra 6001-digit independent Python bigint truth table')
PY
fi
