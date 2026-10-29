#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 four_step_precursor.py > /tmp/w13_phase1_controls.json
g++ -O3 -std=c++17 replay20k_phase1.cpp -lgmpxx -lgmp -o /tmp/w13_phase1_replay
/tmp/w13_phase1_replay 300 25 20000
python3 - <<'PY'
import json
j=json.load(open('/tmp/w13_phase1_controls.json'))
assert j['q65_M3_combinations']==27
assert j['independent_python_int_controls']==36
assert j['odd_exterior_witnesses_t0_to_t4']==[1,0,4,0,7]
print('W13_PHASE1_LOCAL_PASS')
PY
