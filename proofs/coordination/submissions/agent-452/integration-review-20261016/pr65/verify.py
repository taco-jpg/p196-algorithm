"""Agent452 independent audit of PR65's explicitly finite/source-only claims."""
from pathlib import Path
from itertools import product
import json, hashlib
expected=[44013800000,44014631044,88028272088,176055554176,847511104847,1595912220595,7546134416546,14002278733003,44036065953044,88072022016088,176133044043176,847473484374847,1595946968749595,7555425665245546,14010851330491103]

def digits(n):
    ds=[]
    while n:
        n,d=divmod(n,10);ds.append(d)
    return ds or [0]

def inspect(n):
    ds=digits(n);L=len(ds)
    q=[ds[i]+ds[-1-i] for i in range(L)]
    carries=[0];out=[]
    for a in q:
        c,d=divmod(a+carries[-1],10)
        carries.append(c);out.append(d)
    if carries[-1]:out.append(carries[-1])
    nxt=0
    for d in reversed(out):nxt=10*nxt+d
    return {'n':n,'width':L,'palindrome':ds==ds[::-1],'q':q,'boundary':q[:3],'middle':q[3:-3],'control':carries[L-3],'next':nxt}

records=[];n=expected[0]
for t,e in enumerate(expected):
    r=inspect(n);r['t']=t
    assert n==e and not r['palindrome'] and r['width']>=6
    records.append(r);n=r['next']
assert [r['control'] for r in records[:7]]==[0,0,0,0,0,0,1]
assert records[7]['middle']==[3,5,9,15,15,9,5,3]
assert [r['control'] for r in records[7:13]]==[0,0,1,0,0,1]

def transition(p,c):
    a,b,d=p
    l0=a%10;l1=(b+a//10)%10;l2=(d+(b+a//10)//10)%10
    h0=(d+c)%10;k1=(d+c)//10;h1=(b+k1)%10;k2=(b+k1)//10;h2=(a+k2)%10;e=(a+k2)//10
    return ((l0+h2,l1+h1,l2+h0) if e==0 else (l0+1,l1+h2,l2+h1)),e

controls=[]
for cs in product((0,1),repeat=7):
    state=(4,4,0)
    for c in cs:state,_=transition(state,c)
    guard=all(cs[i]==v for i,v in [(0,0),(1,0),(3,0),(5,0),(6,1)])
    assert (state==(4,4,0))==guard
    if guard:controls.append(cs)
for r,s in zip(records,records[1:]):
    p,e=transition(tuple(r['boundary']),r['control'])
    assert list(p)==s['boundary']
    assert r['width']+e==s['width']
for first in controls:
    for second in controls:
        state=(4,4,0)
        for c in first+second:state,_=transition(state,c)
        assert state==(4,4,0)
result={'agent':'Agent #452','pr':65,'head':'23e373f784eb8d179d4f6cf07aaaa428ad2a4c52','base':'9de08d78db6526e2ce2dd66cedd5e63f600424bd','status':'INDEPENDENT_FINITE_REPLAY_PASS_SOURCE_AUDIT','kernel_verification_claim':False,'source_obligations':['ActualBoundary.actualControl = carry q (L-3) = 1','SevenStepOrbit.seven_return_iff requires 6<=L, Admissible L q, and initial boundary; retained, not waived','SevenStepOrbit.run_actual applies at any block index under the same width and admissibility conditions'],'records':records,'finite_transducer_words_checked':128,'returning_words':controls,'two_guarded_blocks_checked':16,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
