#!/usr/bin/env python3
"""Two-column lookahead, solving simultaneous time-closed pairs (19² states).
Search tool, NOT a complete proof of existence of a central seam.
"""
from carryset_transfer import read,contracts,horizon
from collections import defaultdict
import sys
def extend_two(g,rows,cap=8):
    p=len(g);A,L=contracts(g,rows)
    assert all(A)
    edges=[]
    for t in range(p):
        e=[[] for _ in range(361)]
        for z in range(19):
            for w in range(19):
                for v in (0,1):
                    cz=(w+v)//10
                    u=(z+cz)//10
                    if u not in A[t]:continue
                    l=(z+L[t])//10
                    hz=(rows[t][-1]+u)%10 if g[t]=='1' else (z+cz)%10
                    hw=(z+cz)%10 if g[t]=='1' else (w+v)%10
                    zn=(z+L[t])%10+hz
                    wn=(w+l)%10+hw
                    e[19*z+w].append((19*zn+wn,v))
        edges.append(e)
    out=[]
    for start in range(361):
        table=[{start:None}]
        for t in range(p):
            next_table={}
            for state in table[-1]:
                for nxt,upper in edges[t][state]:
                    if nxt not in next_table:next_table[nxt]=(state,upper)
            table.append(next_table)
            if not next_table:break
        if len(table)!=p+1 or start not in table[-1]:continue
        state=start;path=[];upper=[]
        for t in range(p,0,-1):
            pred,v=table[t][state]
            path.append(state);upper.append(v);state=pred
        assert state==start
        path.reverse();upper.reverse()
        ext=[old+[q//19,q%19] for old,q in zip(rows,path)]
        assert all(contracts(g,ext)[0])
        out.append((ext,upper,horizon(g,ext)))
        if len(out)>=cap:break
    return out
if __name__=='__main__':
    g,rows=read()
    # Diagnostic on rooted K10 prefix. The archived K12 witness is one positive
    # two-column extension reached after choosing a favourable K10 branch.
    opts=extend_two(g,[r[:10] for r in rows],cap=8)
    print('K10 -> K12 two-column extensions:',len(opts))
    print('horizons:',[v[-1] for v in opts])
    assert opts
