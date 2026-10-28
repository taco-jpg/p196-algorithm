#!/usr/bin/env python3
"""Independent check of the position-automaton MODEL: brute-force the Lean-mirror B-map F on all trimmed lists of length <= L in base b,
find periodic orbits (cycles of F that stay in the box), and verify that bx accepts each cycle's (g,e) stream (bx must be complete)."""
import sys, itertools, subprocess, re, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from verify_ext import Bstep
HERE=os.path.dirname(os.path.abspath(__file__)); BX=os.path.join(os.path.dirname(HERE),'bin','bx')
b=int(sys.argv[1]); L=int(sys.argv[2]); pmax=int(sys.argv[3]) if len(sys.argv)>3 else 12
def lists():
    for n in range(0,L+1):
        for B in itertools.product(range(2*b-1),repeat=n):
            if n and B[0]==0: continue
            if n and B[-1]==b-1: continue       # trimmed
            yield B
F={}; info={}
for B in lists():
    nb,e1,gm,u=Bstep(b,list(B))
    info[B]=(e1,gm)
    F[B]=tuple(nb) if len(nb)<=L else None
# cycles in functional graph on box
seen={}; cycles=[]
for B in F:
    path=[]; x=B
    while x is not None and x not in seen and x in F:
        seen[x]=len(path)*0+1; path.append(x); x=F[x]
    # detect cycle among path
    if x is not None and x in F and x in path:
        i=path.index(x); cyc=path[i:]
        cycles.append(cyc)
    for y in path: seen[y]=2
# cycles may be reported once per entry; dedupe by min rotation
uniq={}
for cyc in cycles:
    k=min(range(len(cyc)),key=lambda i:cyc[i:]+cyc[:i]) if False else None
    key=frozenset(cyc); uniq[key]=cyc
print(f'base {b}, width<={L}: {len(F)} lists, {len(uniq)} periodic orbits inside the box')
bad=0
for key,cyc in uniq.items():
    g=''.join(str(info[B][1]) for B in cyc); e=''.join(str(info[B][0]) for B in cyc)
    p=len(cyc)
    if p>pmax: continue
    out=subprocess.run([BX,str(b),'-g',g,'-cap','5000000'],capture_output=True,text=True).stdout
    es=set(re.findall(r' e=([01]+)@',out))
    ok= e in es
    print(' orbit p=%d g=%s e=%s widths=%s -> bx %s'%(p,g,e,sorted(set(len(B) for B in cyc)),'OK' if ok else 'MISSING!'))
    if not ok: bad+=1
print('missing:',bad)
