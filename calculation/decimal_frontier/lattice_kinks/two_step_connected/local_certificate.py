#!/usr/bin/env python3
"""Finite carry-cone PAPER PROOF checker for all-spatial-length 3-site
connected TWO-STEP erasure motifs of the p12/m9 decimal lattice.

The exact local 1D two-sided transducers are implemented from the column
normalization equations, not from a real-N simulation. Translation by 9
preserves the local input/carries. The proof in the result report supplies
the carry-reset lemma and safe-margin bound.
"""
from pathlib import Path
import json,sys

def load(path):
    z=list(map(int,Path(path).read_text().split()))
    assert z[:4]==[12,34,9,10]
    g=z[4:16]
    w=[z[16+9*t:16+9*t+9] for t in range(12)]
    cups=[z[124+9*t:124+9*t+9] for t in range(12)]
    assert len(z)==640
    return g,w,cups

def cell(w,t,i):return w[t][(i-34)%9]

def upper_boundary(w,t,end):
    # The incoming upper-mirror carry D[end] is determined by the bulk
    # columns end+1..end+10; test BOTH possible remote centre carries.
    def test(u):
        for i in range(end+10,end,-1):
            u=(cell(w,t,i)+u)//10
        return u
    a,b=test(0),test(1)
    assert a==b,('remote centre carry did not reset',t,end)
    return a

def finite_step(w,cups,t,start,end,p,g):
    up={};down={}
    carry=cups[t][(start-34)%9]
    for i in range(start,end+1):
        total=p[i]+carry
        up[i]=total%10
        carry=total//10
    descending=upper_boundary(w,t,end)
    for i in range(end,start-1,-1):
        total=p[i]+descending
        down[i]=total%10
        descending=total//10
    if g==0:
        return {i:up[i]+down[i] for i in range(start,end+1)}
    return {i:up[i]+down[i-1] for i in range(start+1,end+1)}

def check(data,motifs):
    g,w,cups=load(data)
    assert g==[1,0,0,0]*3
    cases=json.loads(Path(motifs).read_text())
    assert len(cases)==15 and {x['phase'] for x in cases}=={3,7,11}
    for phase in (3,7,11):
        assert g[phase]==0 and g[(phase+1)%12]==1
        assert all(not (w[phase][i]==9 and w[phase][(i+1)%9]==9) for i in range(9))
        assert 9 not in w[(phase+1)%12]
    for row in cases:
        t,r,values=row['phase'],row['residue'],row['replace']
        assert len(values)==3 and all(0<=a<=18 for a in values)
        for shift in (0,9,18,45,90):
            j=52+r+shift
            start,end=j-12,j+15
            assert start>=34
            p={i:cell(w,t,i) for i in range(start,end+1)}
            changed=p.copy()
            for k,v in enumerate(values):
                assert p[j+k]!=v
                changed[j+k]=v
            q=finite_step(w,cups,t,start,end,p,0)
            qq=finite_step(w,cups,t,start,end,changed,0)
            defect=[i for i in q if q[i]!=qq[i]]
            assert defect,('first step should differ',t,r)
            # The lowest nonzero coefficient of the first successor-pairword
            # difference is not divisible by 10. Thus its weighted integer
            # value cannot vanish, and the second-step INTEGERS differ.
            first=min(defect)
            assert (qq[first]-q[first])%10 != 0,(t,r,qq[first]-q[first])
            assert min(defect)>start+4 and max(defect)<end-4,('first cone not contained',t,r)
            for i in range(start+2,end-2):
                assert q[i]==cell(w,(t+1)%12,i),('wrong reference next row',t,r,i)
            second=finite_step(w,cups,(t+1)%12,start,end,q,1)
            second_changed=finite_step(w,cups,(t+1)%12,start,end,qq,1)
            assert second==second_changed,('two-step defect survives',t,r)
    print('FINITE_CARRY_CONE_ALL_15_MOTIFS_PASS')
    print('CARRY_RESET_AND_PERIOD9_TRANSLATION_PASS')

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    check(sys.argv[1] if len(sys.argv)>1 else str(root/'lattice_input.txt'),
          sys.argv[2] if len(sys.argv)>2 else str(root/'motifs.json'))
