#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 three_step_eraser.py > /tmp/w13_three_step_check.json
g++ -std=c++17 -O3 replay20k.cpp -lgmpxx -lgmp -o /tmp/w13_replay
/tmp/w13_replay 300 25 20000
python3 - <<'PY'
import json
with open('/tmp/w13_three_step_check.json') as f: d=json.load(f)
assert d['q65_M3_exhaustive']==729
assert d['odd_exterior_witnesses_t0_t3']==[0,1,0,4]
print('W13_LOCAL_CERTIFICATE_PASS')
PY
