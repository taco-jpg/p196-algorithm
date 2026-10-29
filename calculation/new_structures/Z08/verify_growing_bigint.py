#!/usr/bin/env python3
"""Independent Python-bigint audit of the exact growing-seam local window.

For each algebraically admissible period-3 R bulk cycle and q=20,40,80,160,
compare the 120-step fixed-collar recurrence against actual decimal N+reverse(N).
This is a local verifier, not an all-time certificate.
"""
from itertools import product
import json, sys
from pathlib import Path
sys.set_int_max_str_digits(0)
GAMMA = [1,0,0,0,1,0,0,0,1,0,0,0]
B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [
[5,18,4,8,1,15,4,0,5], [10,14,13,12,9,7,10,4,5],
[1,10,8,5,9,16,0,9,11], [4,0,17,11,9,12,2,9,2],
[8,1,15,4,0,5,5,18,4], [12,9,7,10,4,5,10,14,13],
[5,9,16,0,9,11,1,10,8], [11,9,12,2,9,2,4,0,17],
[4,0,5,5,18,4,8,1,15], [10,4,5,10,14,13,12,9,7],
[0,9,11,1,10,8,5,9,16], [2,9,2,4,0,17,11,9,12]]
LW, RR = 108, 171
US = [(6,12,9),(9,18,0)]

def mod(x,m): return x % m
def alt(w): return sum((1 if i%2==0 else -1)*x for i,x in enumerate(w))
def bulk_step(w,gamma):
    n=len(w)
    a=None
    for s in (0,1):
        c=s;v=[s]
        for x in w: c=(x+c)//10;v.append(c)
        if c==s: a=v;break
    if a is None: raise AssertionError('no cyclic low carry')
    b=None
    for s in (0,1):
        v=[0]*(n+1);v[n]=s
        for i in range(n-1,-1,-1):v[i]=(w[i]+v[i+1])//10
        if v[0]==s: b=v;break
    if b is None: raise AssertionError('no cyclic high carry')
    return [(w[i]+a[i])%10 + ((w[(i-1)%n]+b[i])%10 if gamma else (w[i]+b[i+1])%10) for i in range(n)]
def low_cyclic(w):
    for s in (0,1):
        c=s
        for x in w:c=(x+c)//10
        if c==s:return s
    raise AssertionError('no low carry fixed point')
def local_step(h,gamma,lowcarry,highstate,leftprev):
    n=len(h);low=[0]*n;high=[0]*n;c=lowcarry
    for i,x in enumerate(h):
        z=x+c;low[i]=z%10;c=z//10
    st=highstate
    if not gamma:
        for i in range(n-1,-1,-1):
            high[i]=st
            if h[i]!=9:st=int(h[i]>=10)
    else:
        for i in range(n-1,-1,-1):
            if h[i]!=9:st=int(h[i]>=10)
            high[i]=st
    if not gamma:return [low[i]+(h[i]+high[i])%10 for i in range(n)]
    return [low[0]+(leftprev+high[0])%10]+[low[i]+(h[i-1]+high[i])%10 for i in range(1,n)]
def realize(p):
    assert p==p[::-1] and all(0<=x<=18 for x in p)
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))
def pairword(n):
    d=list(map(int,str(n)[::-1]))
    return [d[i]+d[-1-i] for i in range(len(d))]
def template(q,m,k,J,R,U,C):
    h=B+W[0]*q+list(J)+list(R)*m+list(U)*k
    return h+list(C)+h[::-1]
def r_candidates(U):
    out=[]
    for R in product(range(19),repeat=3):
        if sum(R)%9 or alt(R)%11 != alt(U)%11 or R==U or R==(9,9,9):continue
        x=list(R);hit999=(x==[9,9,9])
        for t in range(120):
            x=bulk_step(x,GAMMA[t%12])
            hit999 |= x==[9,9,9]
        if tuple(x)==R and not hit999:out.append(R)
    return out
def j_first(U):
    residue=(6*alt(U))%11 # solve 2*A(J0)=A(U) mod 11
    for code in range(19**5):
        z=code;j=[]
        for _ in range(5):j.append(z%19);z//=19
        if (2*alt(j))%11==alt(U)%11:return tuple(j)
    raise AssertionError('no J gate word')
def local_init(J,R):
    return W[0]* (LW//9)+list(J)+list(R)*(RR//3)
def main():
    assert len(B)==34 and LW%9==0 and RR%3==0
    wt=[list(W[0])]
    for t in range(120):
        wt.append(bulk_step(wt[-1],GAMMA[t%12]))
        assert wt[-1]==W[(t+1)%12],('W phase mismatch',t+1,wt[-1],W[(t+1)%12])
    assert wt[120]==W[0]
    total=0;full_returns=0;local_phase_checks=0;clock_failures=0;max_mismatch=None
    all_rows=[]
    for U in US:
        J=j_first(U)
        C=(0,8,0) if U==(6,12,9) else (1,0,1)
        assert len(C)%2==1 and C[1]%2==0 and alt(C)%11==alt(U)%11
        Rs=r_candidates(U)
        assert len(Rs)==(6 if U==(6,12,9) else 10),(U,len(Rs),Rs)
        print('U',U,'J0',J,'C',C,'R_candidates',Rs)
        for R in Rs:
            rt=[list(R)]
            for t in range(120):rt.append(bulk_step(rt[-1],GAMMA[t%12]))
            assert rt[120]==list(R)
            assert all(x!=[9,9,9] for x in rt[:-1])
            assert all(not any(x[i]==9 and x[(i+1)%3]==9 for i in range(3)) for x in rt[:-1])
            for q in (20,40,80,160):
                m,k=120,100
                p=template(q,m,k,J,R,U,C)
                n=realize(p)
                h=local_init(J,R)
                off=len(B)+9*q-LW
                local_phase_checks+=1
                assert pairword(n)[off:off+len(h)]==h,('initial window',U,R,q)
                exact_clock=True
                for t in range(120):
                    n2=n+int(str(n)[::-1])
                    gamma=len(str(n2))-len(str(n))
                    if gamma!=GAMMA[t%12]:
                        exact_clock=False;clock_failures+=1
                        raise AssertionError(('physical overflow clock mismatch',U,R,q,t,gamma,GAMMA[t%12]))
                    low=low_cyclic(wt[t])
                    high=next((int(x>=10) for x in rt[t] if x!=9),None)
                    assert high is not None
                    h=local_step(h,GAMMA[t%12],low,high,wt[t][8])
                    n=n2
                    actual=pairword(n)
                    got=actual[off:off+len(h)]
                    if got!=h:
                        ix=next(i for i,(a,b) in enumerate(zip(got,h)) if a!=b)
                        raise AssertionError(('local-vs-bigint mismatch',U,R,q,t,ix,got[ix],h[ix],off))
                local_phase_checks+=120
                want=template(q,m+1,k+4,J,R,U,C)
                ret=(pairword(n)==want)
                full_returns+=int(ret);total+=1
                mismatch=next((i for i,(a,b) in enumerate(zip(pairword(n),want)) if a!=b),min(len(pairword(n)),len(want)) if len(pairword(n))!=len(want) else None)
                all_rows.append({'U':U,'R':R,'q':q,'m':m,'k':k,'J0':J,'C':C,'clock':'PASS','local_window':'PASS all t=0..120','full_120_return':ret,'first_full_mismatch':mismatch,'digits':len(str(n))})
        print('U_CONTROL_PASS',U,'R_count',len(Rs),'q_values',4)
    print('SUMMARY',json.dumps({'independent_bigint_cases':total,'local_window_phase_checks':local_phase_checks,'clock_failures':clock_failures,'full_120_returns':full_returns,'scope':'controls only; exhaustive J0 census is in grow_packet_scan.cpp'},separators=(',',':')))
    with Path(__file__).with_name('bigint_controls.json').open('w') as f:json.dump(all_rows,f,indent=2)
if __name__=='__main__':main()
