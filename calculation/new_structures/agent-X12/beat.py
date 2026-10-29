#!/usr/bin/env python3
"""X12 COMPUTED, finite two-clock decimal centre-insertion transport.
No infinite-orbit claim. Reproduce: python3 beat.py
"""
import json, sys
sys.set_int_max_str_digits(0)
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]

def seed(q,r):
    u=[1]*40;u[13],u[20],u[30]=7,7,6
    c=[8,0,0]+u+[1]*r+[16]+[1]*r+u[::-1]+[0,0,8]
    a=B+W*q
    return a+c+a[::-1]

def normstep(p):
    ds=[];carry=0
    for v in p:
        s=v+carry;ds.append(s%10);carry=s//10
    if carry:ds.append(carry)
    return [ds[i]+ds[-1-i] for i in range(len(ds))],carry

def splice(p,z):
    if len(z)!=len(p)+2:return None
    h=len(p)//2; i=0
    while i<h and p[i]==z[i]:i+=1
    for k in range(min(i,h),-1,-1):
        if p[:k]!=z[:k]:continue
        s=z[k]
        if z[k+1:len(z)-k-1]==p[k:len(p)-k] and z[len(z)-k-1]==s and (k==0 or z[-k:]==p[-k:]):
            return k,s
    return None

def integer(p):
    ds=[0]*len(p)
    for i in range((len(p)+1)//2):
        j=len(p)-1-i;v=p[i]
        if i==j:
            assert v%2==0;ds[i]=v//2
        else: ds[i]=min(9,v);ds[j]=v-ds[i]
    assert ds[-1]!=0
    return int(''.join(map(str,ds[::-1])))

def pairs(x):
    s=str(x)
    return [int(a)+int(b) for a,b in zip(s[::-1],s)]

def replay(q,r,steps,integers=False):
    p,z=seed(q,r),seed(q,r+1)
    if integers:x,y=integer(p),integer(z)
    states=[]; gamma=[];bad=None
    for t in range(steps+1):
        entry=splice(p,z)
        if entry is None:
            bad=t;break
        k,s=entry;states.append((k,k-len(p)//2,s))
        if t>=1: assert s==[2,4,8,16,14,10][(t-1)%6]
        if integers:
            assert pairs(x)==p and pairs(y)==z,('bigint mismatch',q,r,t)
            assert str(x)!=str(x)[::-1] and str(y)!=str(y)[::-1]
        if t==steps:break
        p,g=normstep(p);z,h=normstep(z)
        assert g==h;gamma.append(g)
        if integers:x+=int(str(x)[::-1]);y+=int(str(y)[::-1])
    def first_break(delta,coordinate,distance):
        return next((i for i in range(len(states)-delta) if states[i+delta][coordinate]-states[i][coordinate]!=distance),None)
    return dict(q=q,r=r,checked=len(states)-1,first_splice_failure=bad,
      first_overflow_clock_failure=next((i for i,v in enumerate(gamma) if v!=int(i%2==0)),None),
      first_12step_relative_drift_failure=first_break(12,1,-5),
      first_264step_absolute_drift_failure=first_break(264,0,-44),
      integer_states_checked=2*len(states) if integers else 0,
      t0_cut=states[0],last_cut=states[-1])

def main():
    life=[]
    for r in range(1,101):
        actual=replay(1,r,6*((r-1)//5)+25)
        expected=6*((r-1)//5)+[13,15,16,16,17][(r-1)%5]
        assert actual['first_splice_failure']==expected,(r,actual,expected)
        life.append(expected)
    # Independent whole-integer decimal arithmetic, not normstep, advances x/y.
    stable=replay(7,850,1000,True)
    adaptive=replay(1,850,1000,True)
    assert stable['first_splice_failure'] is None and stable['first_overflow_clock_failure'] is None
    assert stable['first_12step_relative_drift_failure'] is None and stable['first_264step_absolute_drift_failure'] is None
    assert adaptive['first_splice_failure'] is None
    assert (adaptive['first_overflow_clock_failure'],adaptive['first_12step_relative_drift_failure'])==(622,613)
    print(json.dumps(dict(label='COMPUTED',finite_lifetimes_r1_to_r100=life,
              first100_lifetimes_formula='L(5k+s)=6k+(13,15,16,16,17)[s-1], 1<=s<=5',
              stable=stable,adaptive=adaptive,not_claimed='infinite decimal Lychrel or a closed macrocertificate'),indent=2))
if __name__=='__main__':main()
