#!/usr/bin/env python3
"""X01 three-cell neutral six-phase relay, full ordinary big-int replay."""
import sys
sys.set_int_max_str_digits(0)
def step(p):
    c=0;d=[]
    for z in p:
        z+=c;d.append(z%10);c=z//10
    if c:d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))]
def construct(k):
    h=[9]+[14]*k+[5,5,5]+[4]*k+[13]
    low=[max(0,z-9) for z in h]
    hi=[z-u for z,u in zip(h,low)]
    return int(''.join(map(str,(low+hi[::-1])[::-1]))),h+h[::-1]
def runs(p):
    h=p[:len(p)//2];i=0;out=[]
    while i<len(h):
        j=i+1
        while j<len(h) and h[j]==h[i]:j+=1
        if j-i>=3 and h[i] in (14,4):out.append((h[i],i,j-i))
        i=j
    return out
def run(k,T):
    n,p=construct(k);observations={};minodd=10**9
    for t in range(T+1):
        s=str(n)
        actual=[int(s[i])+int(s[-1-i]) for i in range(len(s))]
        assert actual==p,(k,t,'pairword')
        assert s!=s[::-1],(k,t,'palindrome')
        odd=sum(z%2 for z in p)//2
        assert odd>=1,(k,t,'odd witness')
        minodd=min(minodd,odd)
        if t in (0,6,12,60,120,240,480) and t<=T:
            observations[t]=(len(s),runs(p),odd)
        if t==T:break
        p=step(p);n+=int(s[::-1])
    assert [x[2] for x in observations[0][1]]==[k,k]
    assert [x[2] for x in observations[6][1]]==[k,k]
    assert [x[2] for x in observations[12][1]]==[k-5,k-3]
    print('PASS k=%d T=%d minOdd=%d t0=%s t6=%s t12=%s final_digits=%d' %
          (k,T,minodd,observations[0],observations[6],observations[12],len(str(n))))
    if k==200:print('k=200 EXTRA',[(t,observations.get(t)) for t in (60,120,240,480)])
if __name__=='__main__':
    for k in (30,80,200,1000):run(k,min(500,3*k))
