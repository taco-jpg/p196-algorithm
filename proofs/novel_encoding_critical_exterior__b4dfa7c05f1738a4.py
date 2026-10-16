"""Exact temporal-rotation quotient of maximal-speed neutral exterior graph.

All segments have length two. The outer mirrored-sum clock is8 ->17 ->8.
At a segment start immediately after overflow the first digit is1, so the
last digit must be7. Restrict only the initial spatial edge to right digit7.
Cyclic permutation of identical time segments is a graph automorphism and
preserves the neutral accepting predicate; quotienting it is exact.
"""
from continuation_theory_multigrowth import transitions,neutral
from collections import deque
import time,json,argparse

def canonical(s):
    n=len(s[0])
    return min(tuple(v[k:]+v[:k] for v in s) for k in range(n))

def search(segments,seconds=40,maxstates=100000,quotient=True):
    ts=time.monotonic();deadline=ts+seconds;periods=[2]*segments
    start=((1,)*segments,(2,)*segments,(0,)*segments)
    roots=[]
    norm=canonical if quotient else lambda s:s
    for ns,dp in transitions(10,periods,start,deadline):
        if dp[1]==7:roots.append(norm(ns))
    queue=deque(set(roots));depth={s:1 for s in queue};edges=0;accept=[];complete=True
    layers={1:len(queue)}
    try:
        while queue:
            if time.monotonic()>deadline or len(depth)>=maxstates:
                complete=False;break
            s=queue.popleft()
            for ns,dp in transitions(10,periods,s,deadline):
                ns=norm(ns);edges+=1
                if neutral(10,periods,ns):
                    accept.append({'state':ns,'depth':depth[s]+1})
                if ns not in depth:
                    d=depth[s]+1;depth[ns]=d;layers[d]=layers.get(d,0)+1;queue.append(ns)
    except TimeoutError:complete=False
    return {'period':2*segments,'growth':segments,'critical_outer_clock':[8,17],
            'temporal_rotation_quotient':quotient,'complete':complete,
            'states':len(depth),'edges':edges,'remaining_queue':len(queue),
            'layers':layers,'accepted':accept,'seconds':time.monotonic()-ts}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--segments',type=int,default=6)
    ap.add_argument('--seconds',type=float,default=40);ap.add_argument('--states',type=int,default=100000);ap.add_argument('--no-quotient',action='store_true')
    a=ap.parse_args();result=search(a.segments,a.seconds,a.states,not a.no_quotient)
    print(json.dumps(result),flush=True)
    open(f'novel_encoding_critical_p{2*a.segments}'+('_unquotiented' if a.no_quotient else '')+'.json','w').write(json.dumps(result,indent=2))
