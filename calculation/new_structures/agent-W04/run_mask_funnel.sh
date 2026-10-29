#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 mask_funnel.py
g++ -O3 -std=c++17 -Wall -Wextra mask_funnel_20k.cpp -o /tmp/agent_w04_mask_funnel_20k
/tmp/agent_w04_mask_funnel_20k 15000 16000 20000 > /tmp/agent_w04_mask_funnel_20k.log
python3 - <<'PY'
import json,re
r=json.load(open('mask_checkpoints.json'))
s=open('/tmp/agent_w04_mask_funnel_20k.log').read()
a=re.search(r'FOUR_MASKS_ALL_DISTINCT_AT_T0_AND_T1_COMMON_EXACT_INTEGER_AT_T2 digits=(\d+) fnv=([0-9a-f]+)',s)
assert a and int(a[1])==r['common_t2']['digits'] and a[2]==r['common_t2']['fnv_hex']
checks=re.findall(r'MASKED_CHECKPOINT t=(\d+) digits=(\d+) fnv=([0-9a-f]+)',s)
assert len(checks)==len(r['checkpoints'])
for t,d,h in checks:
    assert int(d)==r['checkpoints'][t]['digits'] and h==r['checkpoints'][t]['fnv_hex']
assert s.count('MASKED_ORDINARY_DECIMAL_20000_PASS')==1
bad=json.loads(json.dumps(r));bad['checkpoints']['20000']['fnv_hex']='0'*16
try:
    assert checks[-1][2]==bad['checkpoints']['20000']['fnv_hex']
except AssertionError:
    print('CORRUPTED_FINGERPRINT_REJECTED')
else: raise AssertionError('bad control incorrectly accepted')
print(s,end='')
print('AGENT_W04_MASK_FUNNEL_ALL_CHECKS_PASSED')
PY
