"""Agent452 independent decimal-vector replay; no imported PR implementation."""
import json, pathlib, time, hashlib
from fractions import Fraction
P=pathlib.Path(__file__).parent

def digits(n):
    out=[]
    while n:
        n,d=divmod(n,10); out.append(d)
    return out or [0]

def add_reversed(ds):
    result=[]; carry=0
    for i,a in enumerate(ds):
        carry,d=divmod(a+ds[-1-i]+carry,10)
        result.append(d)
    if carry: result.append(carry)
    return result

def is_pal(ds):
    return all(ds[i]==ds[-1-i] for i in range(len(ds)//2))

def first(seed,cap):
    ds=digits(seed)
    for t in range(cap+1):
        if is_pal(ds): return t
        if t<cap: ds=add_reversed(ds)
    return None

def value(ds):
    result=0
    for d in reversed(ds): result=10*result+d
    return result

def it(k,c,t):
    ds=digits(10**k-c)
    for _ in range(t): ds=add_reversed(ds)
    return value(ds)

def fit(c,t,k1,k2):
    y1,y2=it(k1,c,t),it(k2,c,t)
    a=Fraction(y2-y1,10**k2-10**k1)
    return a,y1-a*10**k1

def first_failure(c,ks,k1,k2,cap=80):
    for t in range(cap+1):
        a,b=fit(c,t,k1,k2)
        mismatches=[k for k in ks if it(k,c,t)!=a*10**k+b]
        if mismatches: return {'t':t,'failing_ks':mismatches}
    return None

start=time.monotonic()
result={'implementation':'Independent least-significant-first decimal vectors with explicit carry; no PR imports','probe':{k:first(10**k-26,5000) for k in range(4,13)}}
assert all(v is None for v in result['probe'].values())
(P/'independent.json').write_text(json.dumps(result,indent=2))
print('probe',result['probe'],flush=True)
s=[c for c in range(1,5000) if all(first(10**k-c,1000) is None for k in range(4,9))]
assert s==[26,1402,4112,4832]
result['survivors']=s
result['extended']={c:[first(10**k-c,3000) for k in range(4,13)] for c in s}
for c,vs in result['extended'].items():
    assert vs==([None]*5+[73]+[None]*3 if c==4112 else [None]*9)
print('survivors',s,'extended',result['extended'],flush=True)
result['affine_original_sample']={c:first_failure(c,[10,11,12,15,20,25],20,21) for c in (26,1402,4832)}
result['affine_wider_sample']={c:first_failure(c,[20,21,22,25,30,35],30,31) for c in (26,1402,4832)}
result['c26_t15_fit']=[str(x) for x in fit(26,15,20,21)]
a,b=fit(26,15,20,21)
result['c26_t15_mismatch_delta']={k:str(it(k,26,15)-(a*10**k+b)) for k in [4,10,11,12,15,20,21,25,30,40,100]}
result['duration_seconds']=time.monotonic()-start
result['checker_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
(P/'independent.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
