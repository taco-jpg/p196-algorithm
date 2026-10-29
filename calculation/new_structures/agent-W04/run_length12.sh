#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 length12_pdr.py > /tmp/agent_w04_length12_pdr.log
g++ -O3 -std=c++17 length12_20k.cpp -o /tmp/agent_w04_length12_digits
g++ -O3 -std=c++17 length12_limbs.cpp -o /tmp/agent_w04_length12_limbs
/tmp/agent_w04_length12_digits 15000 16000 20000 100 > /tmp/agent_w04_length12_digits.log
/tmp/agent_w04_length12_digits 15000 15000 20000 100 > /tmp/agent_w04_length12_diagonal.log
/tmp/agent_w04_length12_limbs 15000 16000 20000 100 > /tmp/agent_w04_length12_limbs.log
python3 - <<'PY'
import json,re
raw=json.load(open('length12_checkpoints.json'))
d=open('/tmp/agent_w04_length12_digits.log').read()
l=open('/tmp/agent_w04_length12_limbs.log').read()
p=open('/tmp/agent_w04_length12_pdr.log').read()
baseline=open('/tmp/agent_w04_length12_diagonal.log').read()
pattern=r'CHECKPOINT (\d+) digits=(\d+) A=(\d+) B=(\d+) digest=([0-9a-f]+) numeric_fnv=([0-9a-f]+)'
check=lambda txt:[dict(t=int(t),digits=int(n),A=int(a),B=int(b),trace=h,fnv=v) for t,n,a,b,h,v in re.findall(pattern,txt)]
assert check(d)==raw['checkpoints']==check(l)
assert 'FINITE_CERTIFICATE_AND_MUTATION_REJECTION_PASS' in p
assert p.count('EDGE ') == 12
assert 'ALL_PUMP_PROOFS_PASS' in p
assert 'IND_INT_REPLAY_PASS:' in p
assert 'COMPUTED 20000 shape-and-nonpalindrome states=20001' in d
row=raw['diagonal_reference']
assert f"minOverlapA={row['minOverlapA']}" in baseline
assert f"minOverlapB={row['minOverlapB']}" in baseline
assert f"minOdd={row['minOdd']}" in baseline
assert f"final_digits={row['final_digits']}" in baseline
assert f"digest={row['final_trace']}" in baseline
assert f"numeric_fnv={row['final_numeric_fnv']}" in baseline
assert 'LIMB_20000_PASS states=20001' in l
assert f"minA={raw['expected_min_run_A']}" in l and f"minB={raw['expected_min_run_B']}" in l
wrong=json.loads(json.dumps(raw));wrong['checkpoints'][-1]['fnv']='0'*16
try:assert check(d)==wrong['checkpoints']
except AssertionError:print('CORRUPTED_REBOUND_FINGERPRINT_REJECTED')
else:raise AssertionError('mutation not rejected')
print('\n'.join([x for x in p.splitlines() if 'PASS' in x or 'THEOREM' in x]))
print(l,end='')
print('AGENT_W04_LENGTH12_ALL_CHECKS_PASSED')
PY
