#!/usr/bin/env python3
"""Base-10 signed two-band necessary quotient:
1<=|M|<=4, A=E one digit each, B=D one digit each at every phase.
All periods, all decimal digits, eight +/-1/0 signed moves,
both relative orders. Old x/u run digits ignored: carry image invariant.
Requires center4_lift.py and base10_restricted.py from parent PRs.
"""
from itertools import product
from array import array
from time import monotonic
from center4_lift import center_moves,components
from base10_restricted import P,image,TRACES,multiorder

def census():
    started=monotonic()
    states=[(M,c) for m in (1,2,3,4)
            for M in product(range(10),repeat=m) for c in (0,1)]
    centergraph={s:set() for s in states};centerops={}
    for s in states:
      ops=center_moves(*s);centerops[s]=ops
      for M2,*_ in ops:
        for bit in (0,1):centergraph[s].add((M2,bit))
    mixed=[scc for scc in components(centergraph)
           if len({len(x[0])%2 for x in scc})>1]
    if len(mixed)!=1 or len(mixed[0])!=244:
        raise RuntimeError('necessary center mixed-parity SCC changed')
    centers=sorted(mixed[0]);center_ids={s:i for i,s in enumerate(centers)}

    exterior={0:[],1:[]}
    for a in range(1,10):
      for e in range(10):
        c1=(a+e)//10
        for b in range(10):
          for d in range(10):
            c2=(b+d+c1)//10
            exterior[c2].append(((a,),(b,),(d,),(e,)))
    if len(exterior[0])!=4500 or len(exterior[1])!=4500:
        raise RuntimeError('exterior carry count changed')
    exterior_ids={bit:{q:i for i,q in enumerate(exterior[bit])}
                  for bit in (0,1)}

    options=[]
    for M,c2 in centers:
      rows=[]
      for M2,a,d,f,U,V,R in centerops[(M,c2)]:
        for trace,dg,dh in TRACES[f]:
          if trace[3][2]!=a or trace[4][2]!=d:continue
          # Exactly one digit in each side fixed block, before and after.
          if trace[1][2]+trace[2][2]!=0:continue
          if trace[5][2]+trace[6][2]!=0:continue
          rows.append((M2,trace,f))
      options.append(rows)

    n=244*4500
    print('PREFLIGHT centers',244,'outer_quadruples_each_carry',4500,
          'vertices',n,'admissible_center_traces',sum(map(len,options)),
          'seconds',round(monotonic()-started,2),flush=True)

    def successors(node):
      k,i=divmod(node,4500)
      M,c2=centers[k];A,B,D,E=exterior[c2][i]
      O,R,f=image(10,P(A,B,M,D,E,0,9,0,9))
      if R[0]+R[3]!=9 or R[1]+R[2]!=9:return ()
      result=[]
      for Mtarget,trace,fneed in options[k]:
        if f!=fneed:continue
        for Z in multiorder(O,R,trace):
          A2,B2,M2,D2,E2=Z
          if M2!=Mtarget or not (len(A2)==len(B2)==len(D2)==len(E2)==1):
            continue
          if A2[0]==0:continue
          c1next=(E2[0]+A2[0])//10
          c2next=(D2[0]+B2[0]+c1next)//10
          k2=center_ids.get((M2,c2next))
          if k2 is None:continue
          j2=exterior_ids[c2next].get((A2,B2,D2,E2))
          if j2 is None:raise RuntimeError('target missing from exact carry partition')
          result.append(k2*4500+j2)
      return result

    indeg=array('I',[0])*n
    active=arcs=0
    for k in range(n):
      row=successors(k)
      active+=bool(row);arcs+=len(row)
      for j in row:
        if indeg[j]==0xffffffff:raise OverflowError('indegree overflow')
        indeg[j]+=1
      if k and k%200000==0:
        print('INDEG',k,'arcs',arcs,'seconds',
              round(monotonic()-started,2),flush=True)
    print('PASS1 vertices',n,'active',active,'arcs',arcs,flush=True)

    todo=array('I',(i for i,d in enumerate(indeg) if d==0))
    head=0
    while head<len(todo):
      src=todo[head];head+=1
      for j in successors(src):
        if indeg[j]==0:raise RuntimeError('inconsistent indegree accounting')
        indeg[j]-=1
        if indeg[j]==0:todo.append(j)
      if head%200000==0:
        print('PEEL',head,'seconds',round(monotonic()-started,2),flush=True)
    remaining=n-head
    print('FINAL vertices',n,'active',active,'arcs',arcs,
          'peeled',head,'residual',remaining,
          'seconds',round(monotonic()-started,2),flush=True)
    if (n,active,arcs,head,remaining)!=(1098000,131070,207360,1098000,0):
      raise RuntimeError('incomplete/different census: no negative accepted')
    print('COMPUTED_BOUNDED_NEGATIVE: M<=4 A1 B1 ALL_PERIODS')
    print('NOT_DECIMAL_LYCHREL_THEOREM')

if __name__=='__main__':census()
