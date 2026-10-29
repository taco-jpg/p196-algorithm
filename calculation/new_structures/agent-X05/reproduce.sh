#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 controls.py
FULL=$(mktemp)
trap 'rm -f "$FULL"' EXIT
python3 affine_rle.py --min 10000 --steps 2000 --checks 0 --period 0 --save "$FULL"
python3 - "$FULL" <<'PY'
import json,hashlib,sys
full=json.load(open(sys.argv[1])); want=json.load(open('expected.json'))
for key in ['label','scope','MIN_A','MIN_B','certified_steps','final_terms','final_length','not_infinite']:
 assert full[key]==want[key],(key,full[key],want[key])
for expected in want['rows']:
 observed=full['rows'][expected['t']]
 assert observed==expected,(expected['t'],observed,expected)
print('AFFINE_ORTHANT_ALL_LENGTH_2000_PASS')
PY
python3 independent.py --a 10000 --b 10017 --steps 1200
