#!/usr/bin/env python3
"""X01 near-neutral decimal two-band relay; exact pairword plus independent bigint."""
import sys
sys.set_int_max_str_digits(0)
def step(p):
    c=0;d=[]
    for z in p:
        z+=c;d.append(z%10);c=z//10
    if c:d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))]
def seed(k):
    h=[9]+[14]*k+[5,5]+[4]*k+[13]
    low=[max(0,z-9) for z in h]
    high=[z-u for z,u in zip(h,low)]
    n=int(''.join(map(str,(low+high[::-1])[::-1])))
    return n,h+h[::-1]
def widths(p):
    h=p[:len(p)//2];out=[];i=0
    while i<len(h):
        j=i+1
        while j<len(h) and h[j]==h[i]:j+=1
        if j-i>5 and h[i] in (14,4):out.append((h[i],i,j-i))
        i=j
    return out
def run(k,T):
    n,p=seed(k);minodd=1000000;data={}
    for t in range(T+1):
        s=str(n)
        actual=[int(s[i])+int(s[-1-i]) for i in range(len(s))]
        assert actual==p,(k,t,'pairword failure')
        assert s!=s[::-1],(k,t,'palindrome')
        odds=sum(z&1 for z in p)//2
        assert odds>0,(k,t,'lost odd guard')
        minodd=min(minodd,odds)
        if t in (0,6,12):data[t]=(len(s),widths(p),odds)
        if t==T:break
        p=step(p);n+=int(s[::-1])
    assert [a[2] for a in data[0][1]]==[k,k]
    assert [a[2] for a in data[6][1]]==[k-1,k]
    assert [a[2] for a in data[12][1]]==[k-6,k-3]
    print('PASS k=%d T=%d min_odd_pairs=%d t0=%s t6=%s t12=%s' %
          (k,T,minodd,data[0],data[6],data[12]))
if __name__=='__main__':
    for k in (30,80,200,1000):run(k,min(500,3*k))
