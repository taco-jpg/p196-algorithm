#!/usr/bin/env python3
"""X07 exact repunit quotient dynamics and independent decimal controls.

For h>=digitlen(q), q>0, q mod9=2, define N=(10**h-1)*q.
Put m=digitlen(q), A=10**m-q, and rm(A)=reverse of m-digit padded A.
Then rev_decimal(N)=(10**h-1)*(1+rm(A)) exactly, so
      q_next=q+1+rm(A).
The state remains protected iff q_next < 10**h.
"""
import collections
import json
import sys
from pathlib import Path

sys.set_int_max_str_digits(200000)


def quotient_step(q):
    assert q > 0 and q % 9 == 2
    m = len(str(q))
    a = 10**m-q
    assert a > 0
    reflected = int(str(a).zfill(m)[::-1])
    return q+1+reflected


def protected(h,q):
    return h >= 1 and 0 < q < 10**h and q % 9 == 2


def check_direct(h,q):
    assert protected(h,q)
    M = 10**h-1
    n = M*q
    s = str(n)
    assert s != s[::-1], (h,q,'palindrome')
    m = len(str(q))
    a = 10**m-q
    # Independent fixed-width digit decomposition, including L=0.
    low = [int(z) for z in str(a).zfill(m)[::-1]]
    digits = low+[9]*(h-m)+[9-z for z in low]
    assert int(''.join(str(x) for x in digits[::-1]))==n
    qn = quotient_step(q)
    assert n+int(s[::-1])==M*qn, (h,q,'reversal identity failed')
    assert qn%9==2 and qn>q
    if qn<10**h:
        assert str(M*qn)!=str(M*qn)[::-1]
    return qn


def exhaustive_small():
    values={}
    for h in range(1,7):
        tested=closed=0
        for q in range(2,10**h,9):
            qn=check_direct(h,q)
            tested+=1
            closed += qn<10**h
        values[str(h)]={'tested':tested,'next_protected':closed}
    return values


def check_shared_quotient():
    # Explicit independent integer construction for n=20,50,100.
    observations=[]
    for n in (20,50,100):
        N=10**n-2908
        for t in range(2):
            N+=int(str(N)[::-1])
        h=n-4
        M=10**h-1
        q,r=divmod(N,M)
        assert (q,r)==(31988,0), (n,q,r)
        t=2
        while protected(h,q):
            assert N==M*q
            sn=str(N)
            assert sn!=sn[::-1]
            qn=quotient_step(q)
            N+=int(sn[::-1])
            assert N==M*qn, (n,t,'independent big-integer disagreement')
            q=qn
            t+=1
        observations.append({'n':n,'h':h,'first_unprotected_step':t,'terminal_q_digits':len(str(q)),'reached_q':str(q)[:30]})
    assert observations[1]['first_unprotected_step']==106
    assert observations[2]['first_unprotected_step']==236
    return observations


def check_regeneration(event_file):
    events=json.load(open(event_file))['events']
    assert len(events)==136
    counts=collections.Counter()
    before_after=collections.Counter()
    controls=[]
    for e in events:
        m=e['m']
        low=[int(z) for z in f"{e['A']:0{m}d}"[::-1]]
        ds=low+[9-z for z in low]
        N=int(''.join(map(str,ds[::-1])))
        T=e['entries'][0]['t']
        for t in range(T):
            s=str(N)
            assert s!=s[::-1],(e['A'],m,t)
            N+=int(s[::-1])
        L=e['entries'][0]['L']
        new_m=(len(str(N))-L)//2
        h=new_m+L
        assert h==8, (e,new_m,h)
        M=10**h-1
        q,r=divmod(N,M)
        assert r==0 and q%9==2 and protected(h,q), (m,e['A'],T,N)
        check_direct(h,q)
        counts[(m,L)]+=1
        before_after[(m,h)]+=1
        if e['A'] in (521,3491) and (m,e['A']) in ((4,521),(6,3491)):
            controls.append({'initial_A':e['A'],'initial_h':m,'recovery_step':T,'recovered_h':h,'q':q,'N':str(N)})
    assert counts=={(4,1):26,(6,1):73,(6,2):37},counts
    assert before_after=={(4,8):26,(6,8):110},before_after
    return {'counts':{f'{m}_to_h8_L{l}':v for (m,l),v in sorted(counts.items())},'controls':controls}


def main():
    root=Path(__file__).resolve().parent
    small=exhaustive_small()
    shared=check_shared_quotient()
    repairs=check_regeneration(root/'renewal_events.json')
    data={'label':'COMPUTED','small_exhaustive':small,'shared_quotient':shared,'repair_funnel':repairs}
    output=root/'quotient_measurements.json'
    output.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
