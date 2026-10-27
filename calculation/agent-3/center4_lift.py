#!/usr/bin/env python3
"""Base10 signed two-band center<=4 minimal projection loop and scoped lift.
Imports Agent3's exact full-block helpers in base10_restricted.py (PR #359).
The projected loop is NOT a decimal certificate.
"""
from itertools import product
from collections import Counter,deque
from time import monotonic
from base10_restricted import P,image,TRACES,multiorder

C=[((0,1,0),1),((9,0,2,1),0),((0,2,3,0),1),((0,5,5,1),1),
   ((2,1,0,2),1),((4,1,1,5),1),((9,2,3),0),((2,5,2),1),((5,0,5),0)]

def center_moves(M,c2):
    m=len(M)
    v=rev=0
    for z in M:v=10*v+z
    for z in M[::-1]:rev=10*rev+z
    n=v+rev+c2;c3=n//10**m
    if c3!=1-c2:return ()
    R=tuple((n//10**(m-i-1))%10 for i in range(m))
    U,V=9*(1-c3),9*(1-c2)
    ret=[]
    for a,d in product((-1,0,1),repeat=2):
      f=d-a
      if f not in (0,1):continue
      for order in (((U,'left',a),(V,'right',d)),
                    ((V,'right',d),(U,'left',a))):
        Z=list(R);valid=True
        for char,side,shift in order:
          if shift>0:
            if not Z or (Z[0] if side=='left' else Z[-1])!=char:
              valid=False;break
            if side=='left':Z.pop(0)
            else:Z.pop()
          elif shift<0:
            if side=='left':Z.insert(0,char)
            else:Z.append(char)
        if valid and 1<=len(Z)<=4:
          item=(tuple(Z),a,d,f,U,V,R)
          if item not in ret:ret.append(item)
    return ret

def components(adj):
    used=set();order=[]
    for start in adj:
      if start in used:continue
      used.add(start);stack=[(start,iter(adj[start]))]
      while stack:
        try:q=next(stack[-1][1])
        except StopIteration:
          order.append(stack.pop()[0]);continue
        if q not in used:used.add(q);stack.append((q,iter(adj[q])))
    inv={p:set() for p in adj}
    for p,row in adj.items():
      for q in row:inv[q].add(p)
    used.clear();result=[]
    for start in reversed(order):
      if start in used:continue
      used.add(start);stack=[start];comp=set()
      while stack:
        p=stack.pop();comp.add(p)
        for q in inv[p]:
          if q not in used:used.add(q);stack.append(q)
      result.append(comp)
    return result

def projection():
    ss=[(M,c) for m in (1,2,3,4)
        for M in product(range(10),repeat=m) for c in (0,1)]
    edges={s:{} for s in ss}
    for p in ss:
      for M2,a,d,f,U,V,R in center_moves(*p):
        for nxt in (0,1):edges[p].setdefault((M2,nxt),(a,d,f,U,V,R))
    comps=components(edges)
    cyc=[S for S in comps if len(S)>1 or any(x in edges[x] for x in S)]
    mixed=[S for S in cyc if len({len(x[0])%2 for x in S})>1]
    assert len(mixed)==1 and len(mixed[0])==244
    assert (len(ss),sum(map(len,edges.values())),len(comps),
            sorted(map(len,cyc)))==(22220,28400,21949,[10,20,244])
    W=mixed[0];best=None
    for p in W:
      for q in edges[p]:
        if q not in W or len(p[0])%2==len(q[0])%2:continue
        pred={q:None};todo=deque([q])
        while todo:
          v=todo.popleft()
          if v==p:break
          for w in edges[v]:
            if w in W and w not in pred:pred[w]=v;todo.append(w)
        if p in pred:
          trail=[];cur=p
          while cur!=q:trail.append(cur);cur=pred[cur]
          path=[p,q]+list(reversed(trail[:-1]))+[p]
          if best is None or len(path)<len(best):best=path
    assert best is not None and len(best)-1==9
    assert all(q in edges[p] for p,q in zip(C,C[1:]+C[:1]))
    assert sum(edges[p][q][2] for p,q in zip(C,C[1:]+C[:1]))==2
    for p,q in zip(C,C[1:]+C[:1]):
      a,d,f,U,V,R=edges[p][q]
      M2=q[0]
      for h in (3,8):
        assert (U,)*h+R+(V,)*h==(U,)*(h+a)+M2+(V,)*(h+d)
    print('projection_states',len(ss),'arcs',sum(map(len,edges.values())),
          'SCCs',len(comps),'cyclic_SCC_sizes',sorted(map(len,cyc)),
          'mixed_parity_SCC_size',len(W),'shortest_mixed_parity_cycle',len(best)-1)
    print('explicit_9_edge_loop_with_f2',C)
    print('center_boundary_moves',
          [(edges[p][q][0],edges[p][q][1],edges[p][q][2])
           for p,q in zip(C,C[1:]+C[:1])])

def bounded_full_lift():
    t=monotonic();states=[]
    for phase,(M,c2) in enumerate(C):
      for aa in range(1,100):
        a=1 if aa<10 else 2
        A=(aa,) if a==1 else (aa//10,aa%10)
        for ee in range(10**a):
          E=(ee,) if a==1 else (ee//10,ee%10)
          arev=aa if a==1 else (aa%10)*10+aa//10
          if (ee+arev>=10**a)!=bool(c2):continue
          for x,u in product((0,9),repeat=2):
            states.append((phase,P(A,(),M,(),E,x,9-x,u,9-u)))
    index={p:i for i,p in enumerate(states)}
    graph=[[] for _ in states];active=0;stage_counts=Counter()
    for k,(j,p) in enumerate(states):
      O,R,f=image(10,p)
      if R[0]+R[3]!=9 or R[1]+R[2]!=9:continue
      if f!=(len(C[(j+1)%9][0])-len(C[j][0]))%2:continue
      active+=1
      for trace,dg,dh in TRACES[f]:
        for Z in multiorder(O,R,trace):
          if not (len(Z[0])==len(Z[4]) and 1<=len(Z[0])<=2):continue
          if Z[1] or Z[3] or Z[2]!=C[(j+1)%9][0] or Z[0][0]==0:continue
          q=P(*Z,R[0],R[3],R[1],R[2])
          nxt=index.get(((j+1)%9,q))
          if nxt is not None:graph[k].append(nxt);stage_counts[j]+=1
    indegree=[0]*len(states)
    for row in graph:
      for q in row:indegree[q]+=1
    todo=deque(i for i,degree in enumerate(indegree) if degree==0)
    peeled=0
    while todo:
      k=todo.popleft();peeled+=1
      for q in graph[k]:
        indegree[q]-=1
        if indegree[q]==0:todo.append(q)
    counts=(len(states),active,sum(map(len,graph)),peeled)
    assert counts==(163620,78372,111492,163620),counts
    print('exact_bounded_full_graph','phases',len(C),'states',counts[0],
          'active_sources',counts[1],'arcs',counts[2],
          'peeled',counts[3],'residual',counts[0]-counts[3],
          'by_phase_arcs',sorted(stage_counts.items()),
          'elapsed_seconds',round(monotonic()-t,2))
    print('NO_CLOSED_LIFT_FOR_THIS_9_CYCLE_WITH_A_WIDTH_1_OR_2_AND_B_D_EMPTY')

if __name__=='__main__':
    projection()
    bounded_full_lift()
