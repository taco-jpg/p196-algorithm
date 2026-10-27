#!/usr/bin/env python3
"""Base-10 center-only OVERAPPROXIMATION for signed two-neutral-band edge format.

Scope: 1<=|M|<=3, incoming inner carry free (0/1), outgoing inner carry
must be its complement; center-adjacent signed moves each in {-1,0,+1},
exactly once each, either local order; next incoming carry free. All outer
blocks, their widths and moves are deliberately forgotten.
No Lean theorem. A mixed-parity cyclic SCC would be inconclusive, not a cert.
"""
from itertools import product

def val(ds):
    n=0
    for d in ds:n=10*n+d
    return n

def step(M,c2):
    n=val(M)+val(M[::-1])+c2
    m=len(M);c3=n//10**m
    if c3!=1-c2:return []
    R=tuple(n//10**(m-1-i)%10 for i in range(m))
    U=9*(1-c3);V=9*(1-c2)
    out=[]
    for a,d in product((-1,0,1),repeat=2):
      for order in ((('left',a),('right',d)),(('right',d),('left',a))):
        z=list(R);valid=True
        for side,shift in order:
            digit=U if side=='left' else V
            if shift==1:
                if not z or (z[0] if side=='left' else z[-1])!=digit:
                    valid=False;break
                if side=='left':z.pop(0)
                else:z.pop()
            elif shift==-1:
                if side=='left':z.insert(0,digit)
                else:z.append(digit)
        if valid and len(z) in (1,2,3):
            item=(tuple(z),a,d,U,V,R)
            if item not in out:out.append(item)
    return out

def sccs(adj):
    nodes=list(adj)
    seen=set();order=[]
    for v in nodes:
      if v in seen:continue
      seen.add(v);stack=[(v,iter(adj[v]))]
      while stack:
        try:w=next(stack[-1][1])
        except StopIteration:
          order.append(stack.pop()[0]);continue
        if w not in seen:
          seen.add(w);stack.append((w,iter(adj[w])))
    rev={x:set() for x in nodes}
    for v,out in adj.items():
      for w in out:rev[w].add(v)
    seen.clear();answer=[]
    for v in reversed(order):
      if v in seen:continue
      comp=set();stack=[v];seen.add(v)
      while stack:
        w=stack.pop();comp.add(w)
        for z in rev[w]:
          if z not in seen:seen.add(z);stack.append(z)
      answer.append(comp)
    return answer

def census():
    states=[(M,c) for m in (1,2,3) for M in product(range(10),repeat=m) for c in (0,1)]
    adj={p:set() for p in states}
    raw_edges=0;tested=0
    for p in states:
      for M2,a,d,U,V,R in step(*p):
        raw_edges+=1
        for h in (3,8):
          src=(U,)*h+R+(V,)*h
          dst=(U,)*(h+a)+M2+(V,)*(h+d)
          if src!=dst:raise AssertionError(('word identity',p,M2,a,d))
          tested+=1
        # Deliberately allow either next incoming carry, an overapproximation.
        for cnext in (0,1):adj[p].add((M2,cnext))
    comps=sccs(adj)
    cyclic=[co for co in comps if len(co)>1 or any(x in adj[x] for x in co)]
    mixed=[co for co in cyclic if len({len(x[0])%2 for x in co})>1]
    E=sum(len(v) for v in adj.values())
    print('states',len(states),'allowed_sources',sum(bool(adj[x]) for x in states),
          'raw_center_moves',raw_edges,'arcs',E,'SCCs',len(comps),
          'cyclic_SCCs',len(cyclic),'cyclic_sizes',sorted(len(co) for co in cyclic),
          'mixed_parity_cyclic_SCCs',len(mixed),'center_word_tests',tested)
    if (len(states),sum(bool(adj[x]) for x in states),raw_edges,E,
        len(comps),sorted(len(co) for co in cyclic),len(mixed),tested) != (2220,1100,1992,3984,2057,[10,38,118],1,3984):
        raise AssertionError('census changed')
    cycle=[
       ((1,0),1), ((9,1,2),0), ((1,3,1),1), ((2,6,3),1),
       ((6,2,6),0), ((2,5,2),1), ((5,0,5),0)]
    shifts=[]
    for p,q in zip(cycle,cycle[1:]+cycle[:1]):
        witnesses=[(a,d,U,V,R) for M2,a,d,U,V,R in step(*p) if M2==q[0]]
        if not witnesses or q not in adj[p]:
            raise AssertionError(('projected edge missing',p,q))
        shifts.append(witnesses[0][:2])
    if sum(len(p[0])%2 != len(q[0])%2 for p,q in zip(cycle,cycle[1:]+cycle[:1]))!=2:
        raise AssertionError('expected two parity flips')
    print('projection_only_seven_edge_cycle',cycle,'center_boundary_moves',shifts)
    print('MIXED PARITY CYCLIC SCC PRESENT; THIS IS NOT A FULL CERTIFICATE')

if __name__=='__main__':census()
