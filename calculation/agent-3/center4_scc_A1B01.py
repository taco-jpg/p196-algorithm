#!/usr/bin/env python3
"""All-period decimal signed two-band necessary quotient:
|A|=|E|=1, 1<=|M|<=4, matched |B|=|D| in {0,1}
and side widths MAY SWITCH between phases. Exact five-block carries,
all eight -1/0/+1 signed moves and all shared-block local orderings.
Requires center4_lift.py and base10_restricted.py in parent draft PRs.
"""
from itertools import product
from array import array
from time import monotonic
from center4_lift import center_moves,components
from base10_restricted import P,image,TRACES,multiorder

def census():
    t=monotonic()
    phases=[(M,c) for m in (1,2,3,4)
            for M in product(range(10),repeat=m) for c in (0,1)]
    proj={q:set() for q in phases};center_ops={}
    for q in phases:
      options=center_moves(*q);center_ops[q]=options
      for M2,*_ in options:
        for c in (0,1):proj[q].add((M2,c))
    comps=components(proj)
    mixed=[c for c in comps if len({len(p[0])%2 for p in c})>1]
    if len(mixed)!=1 or len(mixed[0])!=244:
        raise RuntimeError('necessary 244-center baseline changed')
    centers=sorted(mixed[0]);center_ids={p:i for i,p in enumerate(centers)}

    outer={0:[],1:[]}
    for a in range(1,10):
      for e in range(10):
        c1=(a+e)//10
        outer[c1].append(((a,),(),(),(e,)))
        for b in range(10):
          for d in range(10):
            c2=(b+d+c1)//10
            outer[c2].append(((a,),(b,),(d,),(e,)))
    if len(outer[0])!=4545 or len(outer[1])!=4545:
        raise RuntimeError('correlated carry classes must each be 4545')
    outer_ids={c:{p:i for i,p in enumerate(outer[c])} for c in (0,1)}

    candidates=[]
    for M,c2 in centers:
      choices=[]
      for Mtarget,a,d,f,U,V,R in center_ops[(M,c2)]:
        for trace,dg,dh in TRACES[f]:
          if trace[3][2]==a and trace[4][2]==d:
            choices.append((Mtarget,trace,f))
      candidates.append(choices)

    n=244*4545
    print('PREFLIGHT centers',244,'outer_quadruples_per_carry',4545,
          'vertices',n,'candidate_center_traces',sum(map(len,candidates)),
          'seconds',round(monotonic()-t,2),flush=True)

    def successors(node):
      k,j=divmod(node,4545)
      M,c2=centers[k];A,B,D,E=outer[c2][j]
      O,R,f=image(10,P(A,B,M,D,E,0,9,0,9))
      # Both neutral output pairs must be complementary.
      if R[0]+R[3]!=9 or R[1]+R[2]!=9:return ()
      result=[]
      for Mtarget,trace,fneed in candidates[k]:
        if f!=fneed:continue
        for Z in multiorder(O,R,trace):
          A2,B2,M2,D2,E2=Z
          if M2!=Mtarget or len(A2)!=1 or len(E2)!=1:continue
          if A2[0]==0 or len(B2)!=len(D2) or len(B2)>1:continue
          c1next=(A2[0]+E2[0])//10
          c2next=c1next if not B2 else (B2[0]+D2[0]+c1next)//10
          next_center=center_ids.get((M2,c2next))
          if next_center is None:continue
          pair=outer_ids[c2next].get((A2,B2,D2,E2))
          if pair is None:raise RuntimeError('missing actual target carry tuple')
          result.append(next_center*4545+pair)
      return result

    degree=array('I',[0])*n
    arcs=active=0
    for i in range(n):
      destinations=successors(i)
      active+=bool(destinations);arcs+=len(destinations)
      for j in destinations:
        if degree[j]==0xffffffff:raise OverflowError('indegree')
        degree[j]+=1
      if i and i%200000==0:
        print('INDEG',i,'arcs',arcs,'elapsed',
              round(monotonic()-t,2),flush=True)
    print('PASS1 vertices',n,'active',active,'arcs',arcs,flush=True)

    fifo=array('I',(i for i,v in enumerate(degree) if v==0))
    head=0
    while head<len(fifo):
      i=fifo[head];head+=1
      for j in successors(i):
        if degree[j]==0:raise RuntimeError('Kahn degree mismatch')
        degree[j]-=1
        if degree[j]==0:fifo.append(j)
      if head%200000==0:
        print('PEEL',head,'elapsed',round(monotonic()-t,2),flush=True)

    residual=n-head
    print('FINAL vertices',n,'active',active,'arcs',arcs,'peeled',head,
          'residual',residual,'seconds',round(monotonic()-t,2),flush=True)
    if (n,active,arcs,head,residual)!=(1108980,133701,278139,1108980,0):
        raise RuntimeError('census incomplete/changed; no negative accepted')
    print('BOUNDED_NEGATIVE: ALL_PERIODS A1 B_WIDTH_0_OR_1_SWITCHING M<=4')
    print('NOT_GENERAL_DECIMAL_LYCHREL_THEOREM')

if __name__=='__main__':census()
