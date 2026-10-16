"""Exact local domain-wall evolution, not a finite integer construction.

Each state is two nonneutral periodic tails and an explicitly finite patch.
Carries in the tails are computed exactly.  A return is an identity of
bi-infinite folded rows; it still requires finite exterior and center glue.
"""
from dataclasses import dataclass
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research'))
from resume_renewal_bulk import transform
from astra_substitution_twobulk import pool


def cyclic(q):
    n=len(q);assert any(x!=9 for x in q)
    a=[0]*n;b=[0]*n;c=0
    for _ in range(2):
        for i in range(n):a[i]=c;c=(q[i]+c)//10
    c=0
    for _ in range(2):
        for i in reversed(range(n)):c=(q[i]+c)//10;b[i]=c
    assert all(a[(i+1)%n]==(q[i]+a[i])//10 for i in range(n))
    assert all(b[i]==(q[i]+b[(i+1)%n])//10 for i in range(n))
    return tuple(a),tuple(b)


@dataclass(frozen=True)
class Domain:
    left:tuple
    right:tuple
    start:int
    patch:tuple

    @property
    def end(self):return self.start+len(self.patch)

    def at(self,i):
        if i<self.start:return self.left[i%len(self.left)]
        if i>=self.end:return self.right[i%len(self.right)]
        return self.patch[i-self.start]

    def trim(self):
        a=0;b=len(self.patch)
        while a<b and self.patch[a]==self.left[(self.start+a)%len(self.left)]:a+=1
        while b>a and self.patch[b-1]==self.right[(self.start+b-1)%len(self.right)]:b-=1
        return Domain(self.left,self.right,self.start+a,self.patch[a:b])

    def step(self,h):
        assert h in (0,1)
        # A nonneutral tail resets either carry within one motif.  One
        # additional column covers the overflow comparison shift.
        x=self.start-len(self.left)-1;y=self.end+len(self.right)+1
        aa,_=cyclic(self.left);_,bb=cyclic(self.right)
        c=aa[x%len(self.left)];lo=[]
        for i in range(x,y):v=self.at(i)+c;lo.append(v%10);c=v//10
        c=bb[y%len(self.right)];hi=[]
        for i in reversed(range(x,y)):v=self.at(i)+c;hi.append(v%10);c=v//10
        hi.reverse()
        ll=transform(self.left,h);rr=transform(self.right,h)
        assert ll is not None and rr is not None
        out=tuple(lo[i-x]+hi[i-h-x] for i in range(x+h,y))
        return Domain(ll,rr,x+h,out).trim()

    def shifted(self,d):
        l=tuple(self.left[(i-d)%len(self.left)] for i in range(len(self.left)))
        r=tuple(self.right[(i-d)%len(self.right)] for i in range(len(self.right)))
        return Domain(l,r,self.start+d,self.patch)

    def same(self,other):
        if self.left!=other.left or self.right!=other.right:return False
        return all(self.at(i)==other.at(i) for i in range(min(self.start,other.start),max(self.end,other.end)))

    def serial(self):return dict(left=self.left,right=self.right,start=self.start,patch=self.patch)


def verify(B,C,patch,shift,period=24):
    q=Domain(tuple(B),tuple(C),0,tuple(patch));start=q;trace=[q.serial()]
    for t in range(period):q=q.step(t%2);trace.append(q.serial())
    assert q.same(start.shifted(shift))
    return dict(left=B,right=C,patch=patch,shift=shift,period=period,clock=[t%2 for t in range(period)],trace=trace,
                scope='exact bi-infinite folded-row identity; finite boundaries not supplied')


if __name__=='__main__':
    bs=pool(24)
    here=Path(__file__).resolve().parent
    (here/'motifs.txt').write_text(str(len(bs))+'\n'+'\n'.join(' '.join(map(str,b)) for b in bs)+'\n')
    print(json.dumps(dict(nonconstant_motifs=len(bs))))
