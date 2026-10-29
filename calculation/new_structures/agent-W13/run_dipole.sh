#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 charge_dipole.py > /tmp/w13_charge_dipole_observations.json
g++ -O3 -std=c++17 replay20k_dipole.cpp -lgmpxx -lgmp -o /tmp/w13_dipole_gmp
/tmp/w13_dipole_gmp 6000 20 20000
g++ -O3 -std=c++17 replay_string100k.cpp -o /tmp/w13_dipole_strings
/tmp/w13_dipole_strings 80 100000 32
python3 - <<'PY'
import json
p=json.load(open('/tmp/w13_charge_dipole_observations.json'))
assert p['separations_checked'][-1]==12003
assert p['max_corridor_len']==12006
assert p['compact_160digit_pair']['pair_merge_t']==5
assert p['compact_160digit_pair']['integer_merge_t']==6
assert len(p['compact_baseline_seed'])==160
print('W13_CHARGE_DIPOLE_LOCAL_PASS')
PY
