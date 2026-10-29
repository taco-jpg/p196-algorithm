#!/usr/bin/env python3
"""Exact integer length-budget checks for a two-pumped-band glider cycle.
Run from repository root: python3 calculation/new_structures/agent-N05/balanced_glider_periods.py
Budgets are necessary arithmetic only; they do NOT assert glider existence.
"""
from math import gcd

def minimal_horizon(name,period,m,gam,left_gain,right_gain):
    assert len(gam)==period and set(gam)<={'0','1'}
    assert left_gain>=0 and right_gain>=0
    ones=gam.count('1')
    assert ones>0
    target=2*m*(left_gain+right_gain)
    assert target>0 and target%ones==0
    laps=target//ones
    T=period*laps
    assert sum(int(gam[t%period]) for t in range(T))==target
    # All fixed finite blocks return at T. Each band occurs in each mirror half.
    for a in (2,3,13):
        for b in (2,9,17):
            before=2*(34+m*a+5+m*b+11)+2
            after=2*(34+m*(a+left_gain)+5+m*(b+right_gain)+11)+2
            assert after-before==target
    return dict(name=name,m=m,gam=gam,period=period,first_horizon=T,
                orbit_gain=target,left_band_gain=m*left_gain,
                right_band_gain=m*right_gain)

S=[('p12/m9','100010001000',9),('p8/m20','10101010',20),('p8/m48','10101010',48)]
if __name__=='__main__':
    for name,gam,m in S:
        stationary=minimal_horizon(name,len(gam),m,gam,1,0)
        moving=minimal_horizon(name,len(gam),m,gam,1,1)
        assert moving['first_horizon']==2*stationary['first_horizon']
        print(name,'one-band pumping',stationary['first_horizon'],
              'balanced glider pumping',moving['first_horizon'],
              'length-gain',moving['orbit_gain'])
    print('LENGTH_BUDGET_PASS')
