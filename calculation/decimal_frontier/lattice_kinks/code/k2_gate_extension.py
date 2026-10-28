#!/usr/bin/env python3
"""Exact 36-state complete finite-support one-step pairword-collision census on p12/m9 bulk.
Runs with no optional dependencies. All pairs of coefficients are palindromic.
"""
from collections import deque
from pathlib import Path
import sys

def load(path):
    q=iter(map(int,Path(path).read_text().split()))
    p,nB,m,b=[next(q) for _ in range(4)]
    gam=[next(q) for _ in range(p)]
    W=[[next(q) for _ in range(m)] for _ in range(p)]
    cup=[[next(q) for _ in range(m)] for _ in range(p)]
    B=[[next(q) for _ in range(nB)] for _ in range(p)]
    assert (p,nB,m,b)==(12,34,9,10)
    return gam,W,cup,B

def word(t,n,W,B):
    h=(n+1)//2
    u=B[t]+[W[t][(i-34)%9] for i in range(34,h)]
    if n&1 and u[-1]&1:u[-1]+=1 if u[-1]<18 else -1
    return u+u[:n//2][::-1]

def norm(P):
    O=[]; C=[0]
    for x in P:
        z=x+C[-1];O.append(z%10);C.append(z//10)
    return O,C

def rows(t,W,B,n=400):
    P=word(t,n,W,B);O,C=norm(P)
    assert C[-1]==0, ('gamma != 0',t)
    entries=[]
    for r in range(9):
        i=34+18+r;ii=n-1-i
        entries.append((P[i],O[i]+O[ii],C[i],C[ii+1],C[i+1],C[ii]))
    return entries

def steps(tab,r,a,b,first=False):
    q,s,_,_,_,_=tab[r]
    for new in range(19):
        if first and new==q:continue
        for u in (0,1):
            if (new+u)//10 != b:continue
            if (new+a)%10+(new+u)%10 != s:continue
            yield (r+1)%9,(new+a)//10,u,new

def shortest(tab,r,stats=None):
    _,_,a,b,_,_=tab[r]
    todo=deque()
    for rr,aa,bb,v in steps(tab,r,a,b,True):todo.append(((rr,aa,bb),[v]))
    seen=set()
    while todo:
        state,path=todo.popleft()
        rr,aa,bb=state
        if (aa,bb)==(tab[rr][2],tab[rr][3]):
            if stats is not None:stats["visited"]=len(seen)
            return path
        if state in seen:continue
        seen.add(state)
        for nr,na,nb,value in steps(tab,rr,aa,bb):todo.append(((nr,na,nb),path+[value]))
    if stats is not None:stats["visited"]=len(seen)
    return None

def pairs(P):
    O,C=norm(P)
    return tuple(O[i]+O[len(O)-1-i] for i in range(len(O))),C[-1]

def seed(P):
    n=len(P);d=[0]*n
    for i in range(n//2):
        q=P[i]; hi=max(0,q-9)
        if i==0:hi=max(1,hi)
        lo=q-hi
        assert 0<=lo<=9 and 0<=hi<=9
        d[i]=lo;d[n-1-i]=hi
    if n%2:assert P[n//2]%2==0;d[n//2]=P[n//2]//2
    assert d[-1]>0
    return d

def ordinary(P):
    d=seed(P);n=len(d);out=[];carry=0
    for i in range(n):
        z=d[i]+d[n-1-i]+carry;out.append(z%10);carry=z//10
    if carry:out.append(carry)
    return tuple(out[i]+out[-1-i] for i in range(len(out)))

def bigint_pairs(P):
    d=seed(P)
    n=int(''.join(str(x) for x in reversed(d)))
    val=n+int(str(n)[::-1])
    s=str(val)
    return tuple(int(s[i])+int(s[-1-i]) for i in range(len(s)))

def run(path):
    gam,W,cup,B=load(path)
    solved={}
    for t,g in enumerate(gam):
        if g:continue
        tab=rows(t,W,B)
        # Check lattice periodicity of the full pairword and both normalizing carry directions.
        for n in (400,401,418,419,490,491):
            P=word(t,n,W,B); O,C=norm(P)
            assert C[-1]==0
            for r in range(9):
                for k in (0,1,2):
                    i=34+18+r+9*k;ii=n-1-i
                    assert (P[i],O[i]+O[ii],C[i],C[ii+1],C[i+1],C[ii])==tab[r]
        hits=[];counts=[]
        for r in range(9):
            stats={}
            path=shortest(tab,r,stats)
            counts.append(stats["visited"])
            if path is None:continue
            hits.append((r,path))
            assert len(path)<=36 # 9 periodic residues * four carry states
            for n in (200,201,210,211,400,401,418,419,700,701,1800,1801):
                original=word(t,n,W,B); expect=ordinary(original)
                for k in range(0, min(8, max(0,(n//2-13-len(path)-(34+18+r))//9+1))):
                    j=34+18+r+9*k
                    assert j+len(path)<n//2-12
                    changed=original[:]
                    for u,new in enumerate(path):
                        i=j+u;changed[i]=changed[n-1-i]=new
                    assert changed!=original
                    assert pairs(changed)==pairs(original),('pair mismatch',t,n,r,k)
                    assert ordinary(changed)==expect,('ordinary mismatch',t,n,r,k)
                    if n in (200,400,701,1800) and k==0:
                        assert bigint_pairs(original)==bigint_pairs(changed)==expect
        solved[t]=hits
        print('PHASE',t,'HITS',[(r,len(v),v) for r,v in hits],'CLOSED_STATES',counts,flush=True)
    assert list(solved)==[1,2,3,5,6,7,9,10,11]
    assert {t for t,h in solved.items() if h}=={1,2,5,6,9,10}
    assert {t for t,h in solved.items() if not h}=={3,7,11}
    assert all(len(h)==1 and len(h[0][1])==7 for h in solved.values() if h)
    print('COMPLETE finite-state search: nine gamma0 phases x nine residue starts, <=36 carry states; positive witnesses ordinary integer replay PASS')

if __name__=='__main__':
    run(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).resolve().parents[1]/'data'/'lat_p12m9.txt'))
