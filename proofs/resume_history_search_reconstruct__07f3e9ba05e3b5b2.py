"""Recover the current decimal pair-sum word from a bounded carry history.

An exact implementation of a polynomial identity, not a Lychrel witness.
Each row contains the outgoing carries in least-significant-first order.
"""
from dataclasses import dataclass
from collections import deque
import json,random

@dataclass(frozen=True)
class CarryRow:
    carry: tuple[int,...]
    @property
    def width(self):return len(self.carry)
    @property
    def overflow(self):return self.carry[-1]

def current_q_from_history(rows,modulus=32):
    assert rows and all(row.width>0 and set(row.carry)<={0,1}for row in rows)
    assert sum(not row.overflow for row in rows)>=modulus.bit_length()-1
    assert modulus>18 and modulus&(modulus-1)==0
    r=[0]*rows[0].width
    for row in rows:
        L=row.width;h=row.overflow;assert len(r)==L
        # A_h r, where A_0=2 and A_1=1+x.
        if h:
            a=r+[0]
            for i,x in enumerate(r):a[i+1]+=x
        else:a=[2*x for x in r]
        M=L+h;f=[0]*M
        # A=(x-10)C. Its coefficient of x^L is the overflow h.
        for i,c in enumerate(row.carry):
            f[i]-=10*c
            if i+1<M:f[i+1]+=c
            else:assert c==0
        # F_h(C)=A+reverse_M(A).
        r=[(a[i]+f[i]+f[M-1-i])%modulus for i in range(M)]
    if any(x>18 for x in r):raise ValueError('History violates a necessary decimal coefficient condition')
    return tuple(r)

def integer_step(n):
    """Independently derive a carry row by ordinary decimal addition."""
    ds=[int(x)for x in str(n)[::-1]];carry=0;cs=[]
    for a,b in zip(ds,ds[::-1]):
        carry=(a+b+carry)//10;cs.append(carry)
    return n+int(str(n)[::-1]),CarryRow(tuple(cs))

def q_of_integer(n):
    ds=tuple(map(int,str(n)[::-1]));return tuple(a+b for a,b in zip(ds,ds[::-1]))

def verify():
    rng=random.Random(1961205)
    seeds=list(range(1,301))+[rng.randrange(10**rng.randrange(1,40))for _ in range(100)]
    checks=0
    for seed in seeds:
        n=seed;history=deque(maxlen=12)
        for t in range(24):
            n,row=integer_step(n);history.append(row)
            if sum(not r.overflow for r in history)>=5:
                assert current_q_from_history(list(history))==q_of_integer(n),(seed,t)
                checks+=1
    n=196;history=deque(maxlen=12);example=None
    for t in range(1000):
        n,row=integer_step(n);history.append(row)
        if len(history)==12:
            assert sum(not r.overflow for r in history)>=5
            reconstructed=current_q_from_history(list(history));assert reconstructed==q_of_integer(n)
            checks+=1
            if t==11:example={'seed':196,'steps':12,'integer':n,'current_pair_sums':reconstructed,'nonoverflow_steps':sum(not r.overflow for r in history),'history':[r.carry for r in history]}
    return {'status':'passed','seeded_random_generator':1961205,'comparisons':checks,'consecutive_windows_for_196':989,'example':example,'existence_proof':False}

if __name__=='__main__':
    out=verify();print(json.dumps(out,indent=2));open('resume_history_search_reconstruct_results.json','w').write(json.dumps(out,indent=2))
