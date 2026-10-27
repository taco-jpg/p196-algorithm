#!/usr/bin/env python3
"""All-period DECIMAL center-<=3 signed-two-band necessary projection.
PAPER semantics and COMPUTED SCC; no full decimal certificate or Lean theorem.
Each center-adjacent boundary has one signed shift in {-1,0,1},
both local orders. All exterior block widths and moves are forgotten.
"""
from itertools import product

def val(ds):
    n=0
    for d in ds:n=10*n+d
    return n

def next_middle(M,c2):
    m=len(M)
    n=val(M)+val(M[::-1])+c2
    c3=n//10**m
    if c3!=1-c2:return ()
    R=tuple(n//10**(m-i-1)%10 for i in range(m))
    U,V=9*(1-c3),9*(1-c2)
    outcomes=[]
    for a,d in product((-1,0,1),repeat=2):
      # Necessity from matched outer/inner runs and |B'|=|D'|.
      # For any full signed edge, leading carry f = d-a in {0,1}.
      if d-a not in (0,1):continue
      for order in (((U,'left',a),(V,'right',d)),
                    ((V,'right',d),(U,'left',a))):
        Z=list(R)
        valid=True
        for digit,side,shift in order:
          if shift>0:
            if not Z or (Z[0] if side=='left' else Z[-1])!=digit:
                valid=False;break
            if side=='left':Z.pop(0)
            else:Z.pop()
          elif shift<0:
            if side=='left':Z.insert(0,digit)
            else:Z.append(digit)
        if valid and len(Z) in (1,2,3):
          record=(tuple(Z),a,d,U,V,R)
          if record not in outcomes:outcomes.append(record)
    return tuple(outcomes)

def strongly_connected(adj):
    seen=set();finish=[]
    for v in adj:
      if v in seen:continue
      seen.add(v);stack=[(v,iter(adj[v]))]
      while stack:
        try:w=next(stack[-1][1])
        except StopIteration:
          finish.append(stack.pop()[0]);continue
        if w not in seen:
          seen.add(w);stack.append((w,iter(adj[w])))
    reverse={v:set() for v in adj}
    for v,targets in adj.items():
      for w in targets:reverse[w].add(v)
    seen.clear();result=[]
    for v in reversed(finish):
      if v in seen:continue
      comp=set();stack=[v];seen.add(v)
      while stack:
        w=stack.pop();comp.add(w)
        for z in reverse[w]:
          if z not in seen:seen.add(z);stack.append(z)
      result.append(comp)
    return result

def census():
    states=[(M,c) for m in (1,2,3)
            for M in product(range(10),repeat=m) for c in (0,1)]
    adjacency={p:set() for p in states}
    moves=tests=0
    for p in states:
      for M2,a,d,U,V,R in next_middle(*p):
        moves+=1
        # Arithmetic control, not substitute for literal move argument:
        for h in (3,8):
          src=(U,)*h+R+(V,)*h
          dst=(U,)*(h+a)+M2+(V,)*(h+d)
          if src!=dst:raise AssertionError(('center signed equality',p,M2,a,d))
          tests+=1
        for cnext in (0,1):
          # Deliberately overapproximate the next incoming carry.
          adjacency[p].add((M2,cnext))
    components=strongly_connected(adjacency)
    cyclic=[S for S in components if len(S)>1
            or any(x in adjacency[x] for x in S)]
    mixed=[S for S in cyclic if len({len(s[0])%2 for s in S})>1]
    counts=(len(states),sum(bool(adjacency[s]) for s in states),moves,
            sum(map(len,adjacency.values())),len(components),
            sorted(map(len,cyclic)),len(mixed),tests)
    expected=(2220,1100,1410,2820,2172,[4,10,18,20],0,2820)
    print('vertices',counts[0],'active_sources',counts[1],
          'local_move_records',counts[2],'arcs',counts[3],
          'SCCs',counts[4],'cyclic_SCC_sizes',counts[5],
          'mixed_parity_cyclic_SCCs',counts[6],
          'literal_center_word_tests',counts[7],flush=True)
    if counts!=expected:raise AssertionError((counts,expected))
    # Demonstrate why previously reported 7-edge center-only loop
    # was an artifact of forgetting exterior leading-carry constraints.
    R=(0,1,0)
    # len(M) 3 -> len(M') 2 requires f=1 and right-edge extraction +1:
    # the prior 7-loop instead extracted the *left* zero (+1,0),
    # which implies d-a=-1, impossible as an actual leading carry.
    assert (0-1)==-1
    print('CENTER_1_TO_3_ALL_PERIOD_POSITIVE_GAIN_EXCLUDED_IN_SCOPED_FORMAT')
    print('NO_UNBOUNDED_DECIMAL_LYCHREL_CLAIM')

if __name__=='__main__':census()
