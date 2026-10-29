#!/usr/bin/env python3
"""Exact all-length scalar-nine centre-renewal certificate checker (stdlib only).
Run from any cwd: python3 calculation/new_structures/Agent6NineRailCentreRenewal/reproduce.py
"""
import json
from pathlib import Path

CORES = {
    'even8a': [18,8,3,1,1,3,8,18],
    'even8b': [0,10,15,17,17,15,10,0],
    'odd9a': [3,15,2,2,0,2,2,15,3],
    'odd9b': [15,3,16,16,18,16,16,3,15],
    'even6a': [10,14,1,1,14,10],
    'even6b': [8,4,17,17,4,8],
    'odd7a': [9,8,7,18,7,8,9],
    'odd7b': [9,10,11,0,11,10,9],
}

def edge(C, gamma):
    """Exact two-ended carry map with 9-rail complementary carries."""
    assert C and C == C[::-1] and all(0 <= x <= 18 for x in C)
    choices=[]
    for a in (0,1):
        carry=a
        digits=[]
        for x in C:
            v=x+carry
            digits.append(v%10)
            carry=v//10
        b=carry
        if a+b != 1:
            continue
        if gamma == 0:
            D=[digits[i]+digits[-1-i] for i in range(len(C))]
        else:
            endpoint=digits[0]+9*a
            D=[endpoint]+[digits[i]+digits[len(C)-i] for i in range(1,len(C))]+[endpoint]
        assert D == D[::-1] and all(0 <= x <= 18 for x in D)
        assert len(D)%2 == 0 or D[len(D)//2]%2 == 0
        choices.append((a,b,D))
    return choices

def certificate(name, core):
    H=48 if len(core) in (6,7) else 24
    C=core[:]
    rows=[]
    for t in range(H):
        gamma=int(t%4==0)
        opts=edge(C,gamma)
        assert len(opts)==1, (name,t,C,opts)
        a,b,D=opts[0]
        rows.append({'phase':t,'gamma':gamma,'lower_carry':a,'upper_carry':b,
                     'centre':C,'next_centre':D})
        C=D
    delta=H//8
    assert C == [9]*delta+core+[9]*delta, (name,C)
    return {'name':name,'period':H,'gain_per_side':delta,'core':core,'rows':rows}

def check_padding():
    # A finite control for the separate algebraic identity
    # edge(9^j C 9^j,g) = 9^j edge(C,g) 9^j.
    tested=0
    for core in CORES.values():
        C=core[:]
        for t in range(48):
            gamma=int(t%4==0)
            opts=edge(C,gamma)
            assert len(opts)==1
            a,b,D=opts[0]
            for j in range(7):
                padded=edge([9]*j+C+[9]*j,gamma)
                assert padded==[(a,b,[9]*j+D+[9]*j)]
                tested+=1
            C=D
    return tested

def main():
    generated=[certificate(name,core) for name,core in CORES.items()]
    data=json.loads(Path(__file__).with_name('cert.json').read_text())
    assert data['schema']=='Agent6NineRailCentreRenewal-v1'
    assert len(data['certificates'])==len(generated)
    for c,d in zip(data['certificates'],generated):
        assert c=={'name':d['name'],'period':d['period'],
                   'gain_per_side':d['gain_per_side'],'core':d['core'],
                   'ports':''.join(str(row['lower_carry']) for row in d['rows'])}, c['name']
    n=check_padding()
    print('ALL CHECKS PASSED: 8 all-length conditional centre renewals,',
          sum(c['period'] for c in generated),'exact phase rows,',n,
          'padding-commutation controls')

if __name__=='__main__':main()
