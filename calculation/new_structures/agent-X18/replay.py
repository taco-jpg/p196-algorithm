#!/usr/bin/env python3
"""Independent conventional bigint replay; source lattice rows are shared with N18."""
import json
from pathlib import Path
from hashlib import sha256
base=Path(__file__).parent
raw=[[int(x) for x in line.split()]
     for line in (base.parent/'agent-N18'/'lattice.txt').read_text().splitlines()]
assert len(raw)==47 and all(len(x)==8 for x in raw[:39])
assert all(len(x)==20 for x in raw[39:])
B=[line[0] for line in raw[:39]]
W=raw[39]
U=json.loads((base/'candidate.json').read_text())['U']

def seed(q):
    C=[8,0,0]+U+[16]+U[::-1]+[0,0,8]
    L=B+W*q
    P=L+C+L[::-1]
    digits=[0]*len(P)
    for j,p in enumerate(P[:len(P)//2]):
        digits[j]=min(p,9)
        digits[-j-1]=p-digits[j]
    digits[len(P)//2]=P[len(P)//2]//2
    assert digits[-1]!=0 and all(0<=d<=9 for d in digits)
    return int(''.join(map(str,digits[::-1]))),P

def pairdigits(n):
    ds=list(map(int,str(n)[::-1]))
    return [ds[j]+ds[-j-1] for j in range(len(ds))]

def run(q,steps=352):
    n,P=seed(q)
    assert pairdigits(n)==P
    history={}
    h=sha256()
    for t in range(steps+1):
        ds=str(n)
        assert ds!=ds[::-1],('palindrome',q,t)
        Q=pairdigits(n)
        assert Q==P,('arithmetic mismatch',q,t)
        assert Q[:39]==[r[t%8] for r in raw[:39]],('exterior mismatch',q,t)
        assert len(Q)%2==0 or Q[len(Q)//2]%2==0
        h.update(bytes(Q[:39]))
        h.update(len(Q).to_bytes(8,'little'))
        if t and t%88==0:
            k=39+(q-1)*20
            assert Q[:k]==B+W*(q-1)
            R=Q[k:-k]
            p=0
            while p<20 and R[p]==W[p]:p+=1
            history[t]={'prefix':p,'matches':sum(x==y for x,y in zip(R[:20],W)),
                        'centre_length_before_trim':len(R),'head':R[:20]}
        if t==steps:break
        # Independent Python native bigint arithmetic
        n+=int(str(n)[::-1])
        # Separate exact base-ten coefficient-word implementation
        c=0;d=[]
        for x in P:
            v=x+c;d.append(v%10);c=v//10
        if c:d.append(1)
        assert c==(t%2==0),('gamma',q,t,c)
        P=[d[j]+d[-j-1] for j in range(len(d))]
    assert [history[t]['prefix'] for t in (88,176,264,352)]==[20,20,20,2]
    assert [history[t]['matches'] for t in (88,176,264,352)]==[20,20,20,5]
    return {'q':q,'steps':steps,'seed_digits':len(str(seed(q)[0])),
            'final_digits':len(str(n)),'trace_sha256':h.hexdigest(),
            'renewals':history}

if __name__=='__main__':
    result=[run(q) for q in (1,2,3,4)]
    for x in result:
        print('PASS',x['q'],x['steps'],x['seed_digits'],'to',x['final_digits'],
              [(x['renewals'][t]['prefix'],x['renewals'][t]['matches'])
               for t in (88,176,264,352)],x['trace_sha256'])
