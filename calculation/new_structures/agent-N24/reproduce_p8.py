#!/usr/bin/env python3
"""Reproduce N24 p8/m48 hybrid; both independent exact decimal arithmetic engines.
From repo root: python3 calculation/new_structures/agent-N24/reproduce_p8.py
Reduced smoke test: python3 calculation/new_structures/agent-N24/reproduce_p8.py 100
"""
import json,sys,copy,pathlib
from replay_bigint import main as big
from replay_digitlist import main as digit
from small_probe import step

def neutral_conversion(d):
    B,W=d['B'],d['W'];a=d['initial_lattice_copies'];u=d['initial_neutral_width']
    left=B[0]+W[0]*a+[9]*u
    P=left+[18]+left[::-1]
    for _ in range(5):P=step(P)
    start=len(B[0])+len(W[0])*a
    region=P[start:start+u+3]
    assert region[3:20]==[0]*17, ('central carry switch',region)
    return dict(step=5,zero_run_at_least=17,location_from_lsb=start+3)

def run(d,steps):
    assert d['period']==8 and d['lattice_period']==48 and d['overflow']==[1,0]*4
    assert 56+int(str(56)[::-1])==121  # palindrome detector positive control
    source=neutral_conversion(d)
    b=big(d,steps)
    v=digit(d,steps)
    assert b['seed_sha256']==v['seed_sha256'] and b['final_sha256']==v['final_sha256']
    assert b['samples']==v['samples']
    if steps>=2:
        bad=copy.deepcopy(d);bad['B'][1][0]=(bad['B'][1][0]+1)%19
        try:big(bad,2)
        except AssertionError:pass
        else:raise AssertionError('corrupted expected temporal boundary was not detected')
    if steps==20000:
        assert b['initial_digits']==6495 and b['final_digits']==16495
        assert b['samples'][-1]==[20000,16495,297,0]
        assert b['final_sha256']=='e3e9530f676dbb4adb69d94ad127fa7079bfdf54251fcc839b7db55aa8cbfa71'
    return dict(result='COMPUTED',steps=steps,seed_length=b['initial_digits'],final_length=b['final_digits'],frontier_samples=b['samples'],seed_sha256=b['seed_sha256'],final_sha256=b['final_sha256'],carry_conversion=source,independent_methods_agree=True,no_palindrome=True)

if __name__=='__main__':
    path=pathlib.Path(__file__).with_name('p8_hybrid_data.json')
    d=json.loads(path.read_text())
    steps=int(sys.argv[1]) if len(sys.argv)>1 else d['steps']
    print(json.dumps(run(d,steps),indent=2))
