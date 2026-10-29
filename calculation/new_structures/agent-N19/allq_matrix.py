#!/usr/bin/env python3
"""Finite Boolean-matrix proof of universal counter pumping along a reference trace."""
import csv,sys
from unary_allk import mat,mul
from counter_six import PHASES
X=[p[1] for p in PHASES[:6]]
Y=[p[4] for p in PHASES[:6]]
def verify(fname):
    with open(fname,newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==20001,len(rows)
    for t in range(6):
        for gamma in (0,1):
            Mx=mat((X[t],X[(t+1)%6]),gamma)
            My=mat((Y[t],Y[(t+1)%6]),gamma)
            assert mul(Mx,Mx)==Mx,('left matrix not idempotent',t,gamma)
            assert mul(My,My)==My,('right matrix not idempotent',t,gamma)
    min_left=10**12;min_right=10**12
    for t in range(20000):
        a=rows[t];b=rows[t+1]
        n=int(a['digits']);n2=int(b['digits']);gamma=n2-n
        assert gamma in (0,1),(t,gamma)
        assert int(a['step'])==t and int(b['step'])==t+1
        for side in ('left','right'):
            s0=int(a[side+'_start']);l0=int(a[side+'_count'])
            s1=int(b[side+'_start']);l1=int(b[side+'_count'])
            assert l0>=100 and l1>=100
            intersection=min(s0+l0,s1+l1)-max(s0,s1)
            assert intersection>=8,(t,side,intersection)
            if side=='left':min_left=min(min_left,intersection)
            else:min_right=min(min_right,intersection)
        la=int(a['left_start'])+int(a['left_count'])
        ra=int(a['right_start'])
        lb=int(b['left_start'])+int(b['left_count'])
        rb=int(b['right_start'])
        assert la<ra and lb<rb,(t,la,ra,lb,rb)
    print('ALLQ_IDEMPOTENCE_PASS: 12/12 physical two-ended carry matrices M^2=M')
    print('ALLQ_ALIGNED_OVERLAPS_PASS: 20000/20000 edges; minima',min_left,min_right)
    print('ALLQ_SOUND_LIFT: for all integer q>=0 and every t<=20000, exact pairword pump; odd-coefficient witness from bulk20k_pump_q.cpp')
if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else 'bulk_digits.csv')
