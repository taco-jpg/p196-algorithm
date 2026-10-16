"""Exact univariate affine run-family certificates for reverse-and-add.

A run length is a*k+b for all integers k>=0. Searches propose identities;
certify verifies the entire parameter family using exact affine inequalities.
No finite sample is treated as an all-time proof.
"""
from dataclasses import dataclass
from itertools import groupby
import argparse,json,random,time

@dataclass(frozen=True)
class A:
    a:int
    b:int
    def __add__(self,o):
        if isinstance(o,int):o=A(0,o)
        return A(self.a+o.a,self.b+o.b)
    def __sub__(self,o):
        if isinstance(o,int):o=A(0,o)
        return A(self.a-o.a,self.b-o.b)
    def at(self,k):return self.a*k+self.b
    def shift(self,k):return A(self.a,self.at(k))
    def positive(self):return self.a>=0 and self.b>=1
    def zero(self):return self.a==self.b==0

class BranchChange(Exception):pass

def norm(runs):
    out=[]
    for q,n in runs:
        if n.zero():continue
        if not n.positive():raise BranchChange(('nonpositive',n))
        if out and out[-1][0]==q:out[-1]=(q,out[-1][1]+n)
        else:out.append((q,n))
    return tuple(out)

def min_affine(x,y):
    d=x-y
    if d.a>=0 and d.b>=0:return y
    if d.a<=0 and d.b<=0:return x
    raise BranchChange(('crossing',x,y))

def add_reversed(runs):
    left=list(runs);right=list(reversed(runs));i=j=0;out=[]
    while i<len(left) and j<len(right):
        x,n=left[i];y,m=right[j];k=min_affine(n,m)
        out.append((x+y,k));n=n-k;m=m-k
        if n.zero():i+=1
        elif not n.positive():raise BranchChange(('residual',n))
        else:left[i]=(x,n)
        if m.zero():j+=1
        elif not m.positive():raise BranchChange(('residual',m))
        else:right[j]=(y,m)
    assert i==len(left) and j==len(right)
    return norm(out)

def digits(runs,base=10):
    out=[];c=0
    for q,n in runs:
        s=q+c;first=s%base;cc=s//base
        if cc==c:out.append((first,n))
        else:
            out.append((first,A(0,1)))
            out.append(((q+cc)%base,n-1))
        c=cc
    if c:out.append((c,A(0,1)))
    return norm(out)

def step(runs,base=10):
    d=digits(runs,base);return add_reversed(d)

def no_palindromic_member(runs):
    if tuple(q for q,n in runs)!=tuple(q for q,n in reversed(runs)):return True
    diffs=[n-m for (q,n),(r,m) in zip(runs,reversed(runs))]
    if any(d.a==0 and d.b!=0 for d in diffs):return True
    d=next((d for d in diffs if d.a),None)
    if d is None:return False
    if (-d.b)%d.a:return True
    k=(-d.b)//d.a
    return k<0 or any(e.at(k)!=0 for e in diffs)

def encode(q):return tuple((x,A(0,len(list(g)))) for x,g in groupby(q))
def expand(runs,k=0):return tuple(x for x,n in runs for _ in range(n.at(k)))
def from_number(n,base):
    ds=[]
    while n:ds.append(n%base);n//=base
    return encode(tuple(x+y for x,y in zip(ds,reversed(ds))))
def q_valid(runs,base):
    if not runs or runs[0][0]==0:return False
    if any(not 0<=q<=2*base-2 for q,n in runs):return False
    if runs!=tuple(reversed(runs)):return False
    # For odd q width, the central sum must be even. An odd central symbol
    # is legal only when its central run is even for every parameter.
    q,n=runs[len(runs)//2]
    return q%2==0 or (n.a%2==0 and n.b%2==0)

def representative(q,base):
    assert tuple(q)==tuple(reversed(q));ds=[0]*len(q)
    for i in range(len(q)//2):
        hi=min(base-1,q[i]);ds[i]=q[i]-hi;ds[-1-i]=hi
    if len(q)%2:assert q[len(q)//2]%2==0;ds[len(q)//2]=q[len(q)//2]//2
    assert ds[-1]
    return sum(d*base**i for i,d in enumerate(ds))

def certify(start,delta,period,base=10):
    if not any(delta) or min(delta)<0:return None
    for shift in (0,1,2,4,8,16,32,64,128,256,1024):
        family=tuple((q,A(d,n.b+d*shift)) for (q,n),d in zip(start,delta))
        if not q_valid(family,base):return None
        w=family;trace=[]
        try:
            for t in range(period):
                out=digits(w,base)
                if not no_palindromic_member(out):return None
                trace.append({'q':[(q,n.a,n.b) for q,n in w], 'digits':[(q,n.a,n.b) for q,n in out]})
                w=add_reversed(out)
        except BranchChange:continue
        goal=tuple((q,n.shift(1)) for q,n in family)
        if w==goal:
            raw=representative(expand(family),base)
            rev=0;remaining=raw
            while remaining:
                rev=base*rev+remaining%base;remaining//=base
            # The first carried output is certified nonpalindromic. The
            # arbitrary digit split realizing Q_0 might itself be a palindrome.
            return {'status':'AFFINE_IDENTITY_VERIFIED','base':base,'period':period,'parameter_shift':shift,'family':[(q,n.a,n.b) for q,n in family], 'pair_sum_representative':str(raw), 'seed':str(raw+rev), 'seed_offset':1, 'trace':trace, 'proof_scope':'exact integer-affine branch checks for every parameter k>=0; not a Lean proof'}
    return None

def search_orbit(initial,base=10,steps=240,cap=100):
    w=initial;seen={};best=0
    for t in range(steps):
        if len(w)>cap:return None,'run_cap',t
        key=tuple(x for x,n in w);lengths=tuple(n.b for x,n in w)
        for u,old in seen.get(key,[]):
            delta=tuple(x-y for x,y in zip(lengths,old))
            if delta and min(delta)>=0 and max(delta)>0:
                result=certify(tuple((q,A(0,n)) for q,n in zip(key,old)),delta,t-u,base)
                if result:return result,'certificate',t
        seen.setdefault(key,[]).append((t,lengths))
        ds=digits(w,base)
        if not no_palindromic_member(ds):return None,'palindrome',t+1
        w=add_reversed(ds)
    return None,'step_cap',steps

def controls():
    for base in (2,3,10,11):
        for n in range(1,3000):
            q=from_number(n,base);ds=digits(q,base)
            digs=[];m=n
            while m:digs.append(m%base);m//=base
            rev=sum(x*base**i for i,x in enumerate(reversed(digs)))
            actual=n+rev
            assert sum(x*base**i for i,x in enumerate(expand(ds)))==actual
            assert no_palindromic_member(ds)==(expand(ds)!=expand(ds)[::-1])
            assert step(q,base)==from_number(actual,base)
    binary,why,t=search_orbit(from_number(22,2),2)
    assert binary is not None,(why,t)
    # Reject families with an isolated palindromic parameter, not only
    # identically palindromic families.
    assert not no_palindromic_member(((1,A(1,1)),(0,A(0,1)),(1,A(0,4))))
    assert no_palindromic_member(((1,A(2,1)),(0,A(0,1)),(1,A(0,4))))
    return binary

def search(count=10000,seconds=120,seed=196):
    rng=random.Random(seed);start=time.monotonic();stats={};best=[]
    for i in range(count):
        # Several independent long runs, with short interfaces. Full q is
        # symmetric; odd-center parity is respected by construction.
        p=[]
        for j in range(rng.randrange(1,6)):
            x=rng.randrange(1 if not p else 0,19)
            n=rng.choice([1,2,3,4,8,16,32,64])
            p.extend([x]*n)
        middle=[] if rng.randrange(2)==0 else [2*rng.randrange(10)]
        w=encode(tuple(p+middle+p[::-1]))
        result,why,t=search_orbit(w)
        stats[why]=stats.get(why,0)+1
        if len(best)<12 or t>best[-1][0]:best=sorted(best+[(t,[(q,n.b) for q,n in w],why)],reverse=True)[:12]
        if result:
            json.dump(result,open('exist_affine_runs_certificate.json','w'),indent=2)
            return dict(attempts=i+1,status='CANDIDATE_REQUIRING_INDEPENDENT_AUDIT',certificate=result)
        if (i+1)%500==0:print(json.dumps({'attempts':i+1,'seconds':time.monotonic()-start,'stats':stats}),flush=True)
        if time.monotonic()-start>=seconds:break
    return dict(attempts=i+1,seconds=time.monotonic()-start,stats=stats,best=best,decimal_existence_proved=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=120);p.add_argument('--count',type=int,default=10000);args=p.parse_args()
    control=controls();json.dump(control,open('exist_affine_runs_binary_control.json','w'),indent=2)
    print('Exact arithmetic controls passed; binary infinite family rediscovered.',flush=True)
    result=search(args.count,args.seconds);json.dump(result,open('exist_affine_runs_results.json','w'),indent=2);print(json.dumps(result),flush=True)
