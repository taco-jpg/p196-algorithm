#!/bin/sh
set -eu
DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
python3 "$DIR/ca_bounded.py"
python3 - "$DIR" <<'PY'
import json,sys
sys.path.insert(0,sys.argv[1]);import ca_bounded as c
actual=json.load(open(sys.argv[1]+'/ca_bounded_data.json'))
n,sets=c.certify_bulk(); w=c.certify_ends()
assert actual['universal_TM_factors']==n
assert actual['gamma']==list(c.GAMMA)
assert actual['bulk_allowed_values']==sets
assert actual['decimal_nonpal_witnesses_1_to_15']==[list(x) for x in w]
assert actual['time_steps']==15
print('TRACKED_BOUND_RUN_EVIDENCE_PASS')
PY
TMP=$(mktemp "${TMPDIR:-/tmp}/agentN15-bounded.XXXXXXXX")
trap 'rm -f "$TMP"' EXIT HUP INT TERM
${CXX:-c++} -O2 -std=c++17 "$DIR/ca_bounded_independent.cpp" -o "$TMP"
"$TMP"
printf '%s\n' 'AGENT_N15_15_STEP_ALL_LEVEL_COMPLETE_PASS'
