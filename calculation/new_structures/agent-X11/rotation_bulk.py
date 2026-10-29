#!/usr/bin/env python3
"""Exact golden-ratio irrational cut checker for two-sided base-10 carries.
Only a bulk identity is checked, NOT a finite-centre Lychrel certificate."""
from functools import cmp_to_key

class Q5:
    __slots__=('u','v','d')
    def __init__(self,u=0,v=0,d=1):
        self.u,self.v,self.d=u,v,d
    def __add__(self,x):
        if isinstance(x,int):x=Q5(x)
        return Q5(self.u*x.d+x.u*self.d,self.v*x.d+x.v*self.d,self.d*x.d)
    def __neg__(self):return Q5(-self.u,-self.v,self.d)
    def __sub__(self,x):return self+-x
    def __truediv__(self,k):return Q5(self.u,self.v,self.d*k)
    def sign(self):
        u,v=self.u,self.v
        if not v:return (u>0)-(u<0)
        if not u:return (v>0)-(v<0)
        if (u>0)==(v>0):return 1 if u>0 else -1
        a=u*u-5*v*v
        assert a!=0
        return ((a>0)-(a<0)) * (1 if u>0 else -1)
    def floor(self):
        # Float only seeds the search; every adjustment compares exact surds.
        m=int((self.u+self.v*5**.5)/self.d)
        while (self-Q5(m)).sign()<0:m-=1
        while (self-Q5(m+1)).sign()>=0:m+=1
        return m
    def frac(self):return self-Q5(self.floor())
    def __lt__(self,o):return (self-o).sign()<0
    def __eq__(self,o):return (self-o).sign()==0

alpha=Q5(-1,1,2)
def z(k):return Q5(-k,k,2).frac()
def cut_sort(k):return sorted(set(k),key=cmp_to_key(lambda a,b:(z(a)-z(b)).sign()))

class Rotation:
    def __init__(self,coeff):
        self.cuts=dict(coeff)
        assert 0 in self.cuts
        self.ord=cut_sort(self.cuts)
        self.end=[z(k) for k in self.ord]
        assert self.ord[0]==0
    def at(self,theta):
        theta=theta.frac()
        lo,hi=0,len(self.end)
        while lo+1<hi:
            m=(lo+hi)//2
            if not (theta<self.end[m]):lo=m
            else:hi=m
        return self.cuts[self.ord[lo]]
    def get(self,j,x):return self.at(x+Q5(-j,j,2))
    def step(self,g,r=24):
        # Finite exact circle arrangement, including each discontinuity.
        cuts=cut_sort(k-s for k in self.ord for s in range(-r-2,r+3))
        def local(x):
            def reset(i,sgn):
                for j in range(1,r+1):
                    p=self.get(i+sgn*j,x)
                    if p!=9:return int(p>=10)
                raise ValueError('neutral carry run exceeds checked radius')
            return ((self.get(0,x)+reset(0,-1))%10+
                    (self.get(-g,x)+reset(-g,+1))%10)
        vals={}
        for t,k in enumerate(cuts):
            e1=z(k);e2=z(cuts[(t+1)%len(cuts)])
            if t==len(cuts)-1:e2=e2+1
            vals[k]=local((e1+e2)/2)
            assert local(e1)==vals[k], ('right-continuity',k,g)
        changes={0:vals[0]}
        for i in range(1,len(cuts)):
            if vals[cuts[i]]!=vals[cuts[i-1]]:changes[cuts[i]]=vals[cuts[i]]
        if vals[cuts[-1]]!=vals[0]:changes[0]=vals[0]
        return Rotation(changes)

def digits_seed(n,theta=Q5(0)):
    w=[(theta+Q5(-(i+1),i+1,2)).floor()-
       (theta+Q5(-i,i,2)).floor() for i in range(n)]
    assert all(v in (0,1) for v in w)
    return [7+v for v in w]+[9]*n

def ordinary_step(d):
    out=[];carry=0
    for a,b in zip(d,d[::-1]):
        v=a+b+carry;out.append(v%10);carry=v//10
    if carry:out.append(carry)
    assert out[-1]!=0
    return out,carry

def main():
    import argparse,json
    p=argparse.ArgumentParser()
    p.add_argument('--width',type=int,default=1500)
    p.add_argument('--steps',type=int,default=88)
    p.add_argument('--phase-num',type=int,default=0)
    p.add_argument('--phase-den',type=int,default=1)
    p.add_argument('--negative-control',action='store_true')
    a=p.parse_args()
    theta=Q5(a.phase_num,0,a.phase_den)
    f=Rotation({0:16,-1:17}); d=digits_seed(a.width,theta)
    records=[]
    for t in range(a.steps+1):
        pairs=[d[i]+d[-i-1] for i in range(len(d))]
        half=len(d)//2
        checks=sum(f.get(i,theta)==pairs[i] for i in range(100,half-100))
        assert checks==max(0,half-200), ('bulk mismatch',t)
        records.append((t,len(d),len(f.ord),checks,d==d[::-1]))
        if t==a.steps:break
        d,g=ordinary_step(d);f=f.step(g)
    if a.negative_control:
        changed=pairs[:]
        changed[140]=(changed[140]+1)%19
        assert changed[140]!=f.get(140,theta)
        print('NEGATIVE CONTROL PASS')
    print(json.dumps({'phase':[a.phase_num,a.phase_den],'steps':a.steps,
        'matched_coefficients':sum(r[3] for r in records),
        'max_cuts':max(r[2] for r in records),'final_cuts':records[-1][2],
        'first_palindrome':next((r[0] for r in records if r[4]),None),
        'overflow_count':records[-1][1]-records[0][1]}))
if __name__=='__main__':main()
