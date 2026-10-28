#!/usr/bin/env python3
"""Independent all-carry-class g01 search (no one-carry invariant assumption).
For closure x0=b*(a+h0+e)-(l0+l1+c0+Y), enumerate a,e,c0
and validate full unshortened equations. All states are exact integer tuples.
"""
from collections import deque
import sys

def exact_edges(b, state, first=False):
    L,H,Y=state
    l0,l1=L&1,(L>>1)&1
    h0,h1=H&1,(H>>1)&1
    for a in range(2):
      for e in range(2):
       for c0 in range(2):
        x0=b*(a+h0+e)-(l0+l1+c0+Y)
        if x0 < int(first) or x0>2*b-2: continue
        if (x0+l0)//b!=a or (x0+c0)//b!=h0: continue
        x1=(x0+l0)%b + (x0+c0)%b
        if x1<0 or x1>2*b-2 or (x1+l1)//b!=e or (x1+l1)%b+Y!=x0: continue
        for c1 in (0,1):
          if (x1+c1)//b != h1: continue
          yield (a+2*e, c0+2*c1, (x1+c1)%b)

def accepting(b,s):
    L,H,Y=s
    return (L&1)+(H&1)==1 and ((L>>1)&1)+((H>>1)&1)==1 and Y==(b-1)*((L>>1)&1)

def bfs(b):
    root=(0,2,1);seen={root}; q=deque([(root,0)]); accepted=[]; maxdepth=0
    while q:
      s,d=q.popleft();maxdepth=max(maxdepth,d)
      for n in exact_edges(b,s,first=(s==root and d==0)):
        if n in seen:continue
        seen.add(n); q.append((n,d+1))
        if accepting(b,n):accepted.append((n,d+1))
    return len(seen),accepted,maxdepth
if __name__=='__main__':
 for n in map(int,sys.argv[1:]):
    b=2**n
    result=bfs(b)
    print(f'exponent={n},base={b},states={result[0]},accepts={result[1]},maxdepth={result[2]}',flush=True)
