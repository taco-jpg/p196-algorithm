#!/usr/bin/env python3
"""Independent ordinary-base-ten test of every localized p39/K12 transition."""
from pathlib import Path
def load():
    d=dict(s.split('=',1) for s in Path(__file__).with_name('p39_k12.txt').read_text().strip().splitlines())
    return d['gamma'],[list(map(int,r.split(','))) for r in d['rows'].split(';')]
def digits(n):
    d=[]
    while n:
        n,v=divmod(n,10)
        d.append(v)
    return d or [0]
def valid_caps(g,rows):
    ans=[];p=len(g);k=len(rows[0])
    for t,outer in enumerate(rows):
        allowed=[]
        for c in (0,1):
            # Force the top carry independently on this ONE step only.
            coefficients=outer+[18*c]+outer[::-1]
            number=sum(v*10**i for i,v in enumerate(coefficients))
            d=digits(number)
            nxt=[d[j]+d[len(d)-1-j] for j in range(len(d))]
            if len(d)==len(coefficients)+int(g[t]) and nxt[:k]==rows[(t+1)%p]:
                allowed.append(c)
        ans.append(allowed)
    return ans
if __name__=='__main__':
    g,rows=load()
    assert len(g)==39==len(rows) and all(len(x)==12 and x[0]>0 for x in rows)
    assert all(g!=g[:d]*(39//d) for d in range(1,39) if 39%d==0)
    a=valid_caps(g,rows)
    assert all(a),[t for t,v in enumerate(a) if not v]
    assert sum(len(v)==2 for v in a)==14
    corrupted=[x[:] for x in rows]
    corrupted[0][0]=0
    assert not all(valid_caps(g,corrupted))
    print('PASS 39/39 independent decimal integer transitions, width 12')
    print('PASS 14 phases with two legal top carries; corrupted root rejected')
    print('NOTE caps are independent each step: not a global decimal orbit')
