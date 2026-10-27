#!/usr/bin/env python3
"""Bounded signed two-band graph; no unbounded decimal claim."""
from itertools import product
from collections import defaultdict, deque
from argparse import ArgumentParser
import time

P=lambda A,B,M,D,E,x,y,u,v:(A,B,M,D,E,x,y,u,v)

def number(seq,b):
    z=0
    for d in seq:z=z*b+d
    return z

def blocksum(a,c,carry,b):
    if len(a)!=len(c) or carry not in (0,1):
        raise ValueError("invalid fixed addition")
    width=len(a)
    n=number(a,b)+number(c,b)+carry
    if n>=2*b**width:raise ValueError("carry too large")
    return tuple((n//b**(width-1-i))%b for i in range(width)), n//b**width

def image(b,p):
    A,B,M,D,E,x,y,u,v=p
    r0,c1=blocksum(E,A[::-1],0,b)
    r1,c2=blocksum(D,B[::-1],c1,b)
    r2,c3=blocksum(M,M[::-1],c2,b)
    r3,c4=blocksum(B,D[::-1],c3,b)
    r4,c5=blocksum(A,E[::-1],c4,b)
    t=b-1
    return ((1,)*c5+r4,r3,r2,r1,r0),(t*(1-c4),t*(1-c3),t*(1-c2),t*(1-c1)),c5

def one_boundary(block,run,side,d):
    z=list(block)
    if d>0:
        if len(z)<d:return None
        if side=='L':
            if z[-d:]!=[run]*d:return None
            del z[-d:]
        else:
            if z[:d]!=[run]*d:return None
            del z[:d]
    elif d<0:
        if side=='L':z.extend([run]*(-d))
        else:z=[run]*(-d)+z
    return tuple(z)

def multiorder(blocks,runs,trace):
    # Complete for arbitrary ordering of exactly these eight boundary moves.
    # Movements on distinct fixed blocks commute; the three internal
    # blocks each have just two possible relative orders.
    jobs=[[] for _ in range(5)]
    for i,side,d in trace:jobs[i+(side=='R')].append((runs[i],side,d))
    variants=[]
    for block,acts in zip(blocks,jobs):
        cases=[]
        for seq in (acts,acts[::-1]):
            z=tuple(block)
            for r,side,d in seq:
                z=one_boundary(z,r,side,d) if z is not None else None
            if z is not None and z not in cases:cases.append(z)
        if not cases:return ()
        variants.append(cases)
    return product(*variants)

def move(blocks,runs,trace):
    z=[list(b) for b in blocks]
    off=[0]*4
    for i,side,d in trace:
        j=i+(side=='R')
        if d>0:
            if len(z[j])<d:return None
            if side=='L':
                if z[j][-d:]!=[runs[i]]*d:return None
                del z[j][-d:]
            else:
                if z[j][:d]!=[runs[i]]*d:return None
                del z[j][:d]
        elif d<0:
            if side=='L':z[j].extend([runs[i]]*(-d))
            else:z[j]=[runs[i]]*(-d)+z[j]
        off[i]+=d
    return tuple(map(tuple,z)),tuple(off)

def valid_boundary_traces(ov):
    # Equality of A/E and B/D sizes plus equality of both run shifts:
    # l0=r3+ov, l3=r0+ov, l1=r2+ov, r1=l2-ov.
    for r3,r0,r2,l2 in product((-1,0,1),repeat=4):
        l0=r3+ov;l3=r0+ov;l1=r2+ov;r1=l2-ov
        if min(l0,l3,l1,r1)<-1 or max(l0,l3,l1,r1)>1:continue
        yield ((0,'L',l0),(0,'R',r0),(1,'L',l1),(1,'R',r1),
               (2,'L',l2),(2,'R',r2),(3,'L',l3),(3,'R',r3)),l0+r0,l1+r1

TRACES={ov:tuple(valid_boundary_traces(ov)) for ov in (0,1)}
if tuple(map(len,(TRACES[0],TRACES[1])))!=(81,16):
    raise AssertionError("invalid trace enumeration")

def allstates(b,alphabet,runs,maxa,maxd,maxm):
    for a in range(1,maxa+1):
      for A in product(alphabet,repeat=a):
       if A[0]==0:continue
       for E in product(alphabet,repeat=a):
        for d in range(maxd+1):
         for B in product(alphabet,repeat=d):
          for D in product(alphabet,repeat=d):
           for m in range(maxm+1):
            for M in product(alphabet,repeat=m):
             for x,u in product(runs,repeat=2):
              yield P(A,B,M,D,E,x,b-1-x,u,b-1-u)

def search(b,alphabet,runs,maxa,maxd,maxm):
    t0=time.monotonic()
    states=list(allstates(b,alphabet,runs,maxa,maxd,maxm))
    idx={p:i for i,p in enumerate(states)}
    edges=[[] for _ in states];active=0;overflows=0
    for i,p in enumerate(states):
      blocks,r,ov=image(b,p)
      if r[0]+r[3]!=b-1 or r[1]+r[2]!=b-1:continue
      active+=1;overflows+=ov
      for trace,dg,dh in TRACES[ov]:
        for z in multiorder(blocks,r,trace):
          if not z[0] or z[0][0]==0:continue
          if len(z[0])!=len(z[4]) or len(z[1])!=len(z[3]):continue
          q=P(*z,r[0],r[3],r[1],r[2])
          j=idx.get(q)
          if j is not None:edges[i].append((j,dg,dh,ov))
    indeg=[0]*len(states);nedge=0
    for row in edges:
      nedge+=len(row)
      for j,_,_,_ in row:indeg[j]+=1
    todo=deque(i for i,d in enumerate(indeg) if d==0)
    removed=0
    while todo:
      i=todo.popleft();removed+=1
      for j,_,_,_ in edges[i]:
        indeg[j]-=1
        if indeg[j]==0:todo.append(j)
    residual=[i for i,d in enumerate(indeg) if d>0]
    print("base",b,"alphabet",''.join(map(str,alphabet)),"runs",''.join(map(str,runs)),
          "maxa",maxa,"maxd",maxd,"maxm",maxm,
          "states",len(states),"active",active,"leading_overflow_sources",overflows,
          "edges",nedge,"peeled",removed,"residual",len(residual),
          "seconds",round(time.monotonic()-t0,3),flush=True)
    return states,edges,residual

def unit_tests():
    from random import Random
    rng=Random(0xB196)
    for b in (2,3,10,11,17,26):
      for _ in range(3000):
       a=rng.randrange(1,4);d=rng.randrange(0,4);m=rng.randrange(0,4)
       rnd=lambda n:tuple(rng.randrange(b) for _ in range(n))
       A=(rng.randrange(1,b),)+rnd(a-1);B=rnd(d);M=rnd(m);D=rnd(d);E=rnd(a)
       x=rng.randrange(b);u=rng.randrange(b)
       p=P(A,B,M,D,E,x,b-1-x,u,b-1-u)
       g=rng.randrange(0,9);h=rng.randrange(0,9)
       w=A+(x,)*g+B+(u,)*h+M+(b-1-u,)*h+D+(b-1-x,)*g+E
       z,r,_=image(b,p)
       rw=z[0]+(r[0],)*g+z[1]+(r[1],)*h+z[2]+(r[2],)*h+z[3]+(r[3],)*g+z[4]
       if number(w,b)+number(w[::-1],b)!=number(rw,b):
           raise AssertionError("reverse-add crosscheck")
    print("bigint_formula_controls 18000 PASS",flush=True)
    # Positive control from existing Agent 3 draft #320, independently replayed.
    phases=(
      P((1,0),(1,1),(1,1,0,1),(0,0),(0,0),1,0,1,0),
      P((1,1),(0,0),(1,0,0,0),(1,1),(0,1),0,1,0,1),
      P((1,0),(1,1),(1,0,1),(0,0),(0,0),1,0,1,0),
      P((1,1),(0,0),(0,1,0),(1,1),(0,1),0,1,0,1))
    traces=((),((0,'L',1),(0,'R',-1),(1,'L',1),(2,'L',1)),(),
            ((0,'L',1),(0,'R',-1),(1,'L',1),(1,'R',-1)))
    gains=[]
    for i,p in enumerate(phases):
       z,r,_=image(2,p)
       got=move(z,r,traces[i])
       if got is None:raise AssertionError("positive trace")
       blocks,off=got
       q=phases[(i+1)%4]
       if blocks!=(q[0],q[1],q[2],q[3],q[4]):raise AssertionError("blocks")
       if r!=(q[5],q[7],q[8],q[6]):raise AssertionError("runs")
       if off[0]!=off[3] or off[1]!=off[2]:raise AssertionError("gains")
       gains.append((off[0],off[1]))
    if gains!=[(0,0),(0,1),(0,0),(0,0)]:raise AssertionError("positive gains")
    def fullword(p,g,h):
       A,B,M,D,E,x,y,u,v=p
       return A+(x,)*g+B+(u,)*h+M+(v,)*h+D+(y,)*g+E
    g=h=2;n=number(fullword(phases[0],g,h),2)
    for i in range(4000):
       w=fullword(phases[i%4],g,h)
       if n!=number(w,2) or w==w[::-1]:raise AssertionError("positive orbit")
       n+=int(bin(n)[2:][::-1],2)
       dg,dh=gains[i%4];g+=dg;h+=dh
    print("base2_4phase_4000step_positive_control PASS",flush=True)

if __name__=="__main__":
    ap=ArgumentParser()
    ap.add_argument("--base",type=int,default=10)
    ap.add_argument("--alphabet",default="0123456789")
    ap.add_argument("--runs",default="09")
    ap.add_argument("--max-a",type=int,default=1)
    ap.add_argument("--max-d",type=int,default=1)
    ap.add_argument("--max-m",type=int,default=2)
    ap.add_argument("--test",action="store_true")
    o=ap.parse_args()
    if o.test:unit_tests()
    search(o.base,tuple(int(c) for c in o.alphabet),
           tuple(int(c) for c in o.runs),o.max_a,o.max_d,o.max_m)
