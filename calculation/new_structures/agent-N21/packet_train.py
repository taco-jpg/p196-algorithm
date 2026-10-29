#!/usr/bin/env python3
"""N21: exact pair-coefficient transduced train, base 10.
Constructive finite-time observation, NOT a decimal certificate.
Coordinates are least-significant-first; packet anchors are congruent modulo 9.
"""
import json
BASE = 10
N = 5000
ANCHORS = (300, 804, 1308, 1812)
B2 = (2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11)
W2 = (1,10,8,5,9,16,0,9,11)
KINK = (6,1,0,1,11,14,10,6,11,16,1)
CHECK_TIMES = (0,72,144,216,288,360,432,504,576,648,720,792,818,819,820)
def background(n=N):
    assert n % 2 == 0
    h=n//2
    q=list(B2)+[W2[(i-len(B2))%9] for i in range(len(B2),h)]
    return q+q[::-1]
def insert(p,anchors):
    q=p.copy()
    for at in anchors:
        assert at>=34 and at+len(KINK)<len(q)//2
        for off,v in enumerate(KINK):
            q[at+off]=q[len(q)-1-at-off]=v
    return q
def pair_step(p):
    digits=[];carry=0
    for x in p:
        z=x+carry
        digits.append(z%10);carry=z//10
    if carry:digits.append(carry)
    n=len(digits)
    return [digits[i]+digits[n-1-i] for i in range(n)]
def support(a,b):
    d=[i for i in range(len(a)//2) if a[i]!=b[i]]
    return [d[0],d[-1],len(d)] if d else []
def run():
    p=background()
    states=[p]+[insert(p,(a,)) for a in ANCHORS]+[insert(p,ANCHORS)]
    records=[];first_failure=None
    prefix=(0,0,0,1,1,1,1,2,2,2,2,3)
    for t in range(821):
        bg=states[0]
        bad=[i for i in range(len(bg)//2) if bg[i]+sum(s[i]-bg[i] for s in states[1:-1])!=states[-1][i]]
        if bad and first_failure is None:first_failure=t
        assert len(bg)==N+3*(t//12)+prefix[t%12],('length',t)
        profiles=[]
        for j,s in enumerate(states[1:-1]):
            profiles.append([(i-ANCHORS[j],s[i]-bg[i]) for i in range(len(bg)//2) if s[i]!=bg[i]])
        assert all(profile==profiles[0] for profile in profiles[1:]),('packet translation',t)
        if t in CHECK_TIMES:
            r={'step':t,'digits':len(bg),'support':[support(bg,s) for s in states[1:-1]],'nonlinear_lower_positions':bad}
            records.append(r);print(json.dumps(r,separators=(',',':')))
        assert all(len(s)==len(bg) for s in states)
        assert all(s==s[::-1] for s in states)
        assert all(0<=v<=18 for s in states for v in s)
        if t<820:states=[pair_step(s) for s in states]
    assert first_failure==820,first_failure
    assert records[-2]['nonlinear_lower_positions']==[]
    assert records[-1]['nonlinear_lower_positions']==[648,649,650,1152,1153,1154,1656,1657,1658]
    assert records[-1]['digits']==5205
    print('PAIR_TRAIN_PASS first nonlinear interaction at step 820, no earlier failure')
    return records
if __name__=='__main__':run()
