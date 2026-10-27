#!/usr/bin/env python3
"""Base10 signed two-band bounded negative via sound one-million-state quotient.

DEPENDENCIES: exact Agent3 base10_restricted.py in parent PR #359 and
center4_lift.py in parent PR #396. This file lives in stacked review.
Scope: all periods, |M|<=4, |A|=|E|<=2, B=D=empty,
eight independent signed moves in {-1,0,1}, both local orders.
Ignore old input run digits in the quotient: they never enter the fixed
carry image, so this only adds possible transitions, never loses one.
"""
from itertools import product
from collections import Counter
from array import array
from time import monotonic
from center4_lift import center_moves,components
from base10_restricted import P,image,TRACES,multiorder

def main():
    t0=monotonic()
    S=[(M,c) for m in (1,2,3,4)
       for M in product(range(10),repeat=m) for c in (0,1)]
    adj={s:set() for s in S};center_opts={}
    for s in S:
        options=center_moves(*s);center_opts[s]=options
        for M2,*_ in options:
            for nxt in (0,1):adj[s].add((M2,nxt))
    comp=components(adj)
    mixed=[q for q in comp if len({len(s[0])%2 for s in q})>1]
    if len(mixed)!=1 or len(mixed[0])!=244:
        raise RuntimeError('center component baseline changed')
    centers=sorted(mixed[0]);center_id={s:i for i,s in enumerate(centers)}
    aeopts={};aeindex={}
    for c in (0,1):
        entries=[]
        for width in (1,2):
          for a in range(10**(width-1),10**width):
            A=(a,) if width==1 else (a//10,a%10)
            rev=a if width==1 else (a%10)*10+a//10
            for e in range(10**width):
              if (e+rev>=10**width)!=bool(c):continue
              E=(e,) if width==1 else (e//10,e%10)
              entries.append((A,E))
        aeopts[c]=entries
        aeindex[c]={p:i for i,p in enumerate(entries)}
    if len(aeopts[0])!=4545 or len(aeopts[1])!=4545:
        raise RuntimeError('carry-partition count changed')
    n=244*4545
    # A/E carry with empty B/D is exact: c2=carry(E+reverse(A)).
    # Preselect only center move traces with empty destination B,D.
    candidates=[]
    for M,c2 in centers:
      rows=[]
      for M2,a,d,f,U,V,R in center_opts[(M,c2)]:
        for trace,dg,dh in TRACES[f]:
          if trace[3][2]!=a or trace[4][2]!=d:continue
          if trace[1][2]+trace[2][2]!=0:continue
          if trace[5][2]+trace[6][2]!=0:continue
          rows.append((M2,trace,dg,dh,f))
      candidates.append(rows)
    print('PREFLIGHT','centers',len(centers),
          'A_E_carry_pairs_per_center',4545,
          'quotient_vertices',n,'admissible_center_traces',
          sum(map(len,candidates)),flush=True)

    def successors(i):
        center_index,ae_index=divmod(i,4545)
        M,c2=centers[center_index]
        A,E=aeopts[c2][ae_index]
        # Old source x,u in {0,9} are not used by image(),
        # so any representative complementary pair suffices.
        O,R,f=image(10,P(A,(),M,(),E,0,9,0,9))
        out=[]
        for Mnext,trace,dg,dh,required_f in candidates[center_index]:
            if f!=required_f:continue
            for Z in multiorder(O,R,trace):
                A2,B2,M2,D2,E2=Z
                if B2 or D2 or M2!=Mnext or not A2 or A2[0]==0:continue
                if len(A2)!=len(E2) or not (1<=len(A2)<=2):continue
                width=len(A2)
                e_num=sum(E2[t]*10**(width-t-1) for t in range(width))
                a_rev=sum(A2[width-1-t]*10**(width-t-1)
                          for t in range(width))
                next_c2=int(e_num+a_rev>=10**width)
                next_center=center_id.get((M2,next_c2))
                if next_center is None:continue
                next_ae=aeindex[next_c2].get((A2,E2))
                if next_ae is None:
                    raise RuntimeError('in-domain target omitted')
                out.append(next_center*4545+next_ae)
        return out

    indegree=array('I',[0])*n;arcs=active=0
    for i in range(n):
        dests=successors(i)
        active+=bool(dests);arcs+=len(dests)
        for j in dests:
            if indegree[j]==0xffffffff:
                raise OverflowError('indegree overflow')
            indegree[j]+=1
        if i and i%200000==0:
            print('INDEG','visited',i,'arcs',arcs,
                  'seconds',round(monotonic()-t0,2),flush=True)
    print('FIRST_PASS','vertices',n,'arcs',arcs,'active',active,flush=True)

    # Generate exact same edges again on demand, avoiding gigabytes of
    # Python adjacency objects; duplicate edges are tracked in both passes.
    fifo=array('I',(i for i,d in enumerate(indegree) if d==0))
    read=0
    while read<len(fifo):
        src=fifo[read];read+=1
        for dst in successors(src):
            if indegree[dst]==0:
                raise RuntimeError('Kahn degree accounting failure')
            indegree[dst]-=1
            if indegree[dst]==0:fifo.append(dst)
        if read%200000==0:
            print('PEEL','removed',read,
                  'seconds',round(monotonic()-t0,2),flush=True)
    residual=n-read
    print('COMPLETE','quotient_vertices',n,'active_sources',active,
          'arcs',arcs,'peeled',read,'residual',residual,
          'seconds',round(monotonic()-t0,2),flush=True)
    if (n,active,arcs,read,residual)!=(1108980,282216,1034280,1108980,0):
        raise RuntimeError('unexpected census (not an accepted negative)')
    print('BOUNDED_NEGATIVE: ALL_PERIODS M<=4 A<=2 B=D=EMPTY')
    print('NOT_A_GENERAL_DECIMAL_LYCHREL_THEOREM')

if __name__=='__main__':main()
