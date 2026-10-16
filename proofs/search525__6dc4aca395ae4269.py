"""Constructive all-period inverse-language search for the525 periodic tails.

The exact temporal bulk period is discovered, not prescribed. Every trim
vertex retains its raw (input edge, inverse option) provenance so a root
cycle can be lifted to actual finite exterior rows.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import permutations
from collections import deque,Counter
from math import lcm
import json,time,argparse,hashlib

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'reverse'))
from check_reverse_certificate import build_tables,encode_letter,decode_letter
from sofic_reverse import scc_trim

def carry(q,i,d):
    j=(i+d)%len(q)
    while q[j]==9:j=(j+d)%len(q)
    return int(q[j]>=10)

def step(q,h):
    p=len(q)
    return tuple((q[i]+carry(q,i,-1))%10+
                 (q[(i-h)%p]+carry(q,(i-h)%p,1))%10 for i in range(p))

def bulk_cycle(B):
    q=B;seen={};words=[];rows=[]
    while q not in seen:
        seen[q]=len(words);r=step(q,0)
        words.append(encode_letter(carry(q,0,-1),carry(r,0,-1),
                     (q[0]+carry(q,0,1))//10,
                     r[-1]-10*((r[-1]+carry(r,-1,1))//10)))
        rows.extend((q,r));q=step(r,1)
    assert q==B and seen[q]==0
    return tuple(words),rows

def initial():
    n=0;edges=[];records=[];keys=set();provenance=[]
    for B in sorted(set(permutations((5,2,5)))|set(permutations((13,16,13)))):
        w,rows=bulk_cycle(B)
        key=min(w[r:]+w[:r]for r in range(len(w)))
        records.append(dict(bulk=B,pair_period=len(w),word=w,rows=rows))
        if key in keys:continue
        keys.add(key)
        for j,label in enumerate(w):
            edges.append((n+j,n+(j+1)%len(w),label))
            provenance.append(dict(bulk=B,slot=j))
        n+=len(w)
    return dict(vertices=n,edges=edges,origin=provenance),records

def trim_with_origin(n,edges,origin):
    # SCC extraction is independently replayable. Preserve exact raw vertex
    # identities by tagging labels with their original endpoints temporarily.
    adj=[[]for _ in range(n)];rev=[[]for _ in range(n)]
    for u,v,l in edges:adj[u].append(v);rev[v].append(u)
    seen=bytearray(n);order=[]
    for root in range(n):
        if seen[root]:continue
        seen[root]=1;stack=[(root,0)]
        while stack:
            u,i=stack[-1]
            if i==len(adj[u]):order.append(u);stack.pop();continue
            v=adj[u][i];stack[-1]=(u,i+1)
            if not seen[v]:seen[v]=1;stack.append((v,0))
    comp=[-1]*n;sizes=[]
    for root in reversed(order):
        if comp[root]>=0:continue
        k=len(sizes);size=0;stack=[root];comp[root]=k
        while stack:
            u=stack.pop();size+=1
            for v in rev[u]:
                if comp[v]<0:comp[v]=k;stack.append(v)
        sizes.append(size)
    es=[(u,v,l)for u,v,l in edges if comp[u]==comp[v] and (sizes[comp[u]]>1 or u==v)]
    kept=sorted({u for u,v,l in es}|{v for u,v,l in es});ids={u:i for i,u in enumerate(kept)}
    return dict(vertices=len(kept),edges=[(ids[u],ids[v],l)for u,v,l in es],
                origin=[origin[u]for u in kept])

def preimage(g,fibers,output,cap):
    n=g['vertices'];es=g['edges'];outgoing=[[]for _ in range(n)]
    for i,(u,v,l)in enumerate(es):outgoing[u].append(i)
    origin=[(i,x)for i,(u,v,l)in enumerate(es)for x in fibers[l]]
    if len(origin)>cap:return None
    ids={x:i for i,x in enumerate(origin)};raw=[]
    for u,(e,x)in enumerate(origin):
        for f in outgoing[es[e][1]]:
            for y in fibers[es[f][2]]:
                label=output[x][y]
                if label>=0:raw.append((u,ids[f,y],label))
                if len(raw)>cap:return None
    return trim_with_origin(len(origin),raw,origin)

def root_cycle(g):
    n=g['vertices'];es=g['edges'];root=encode_letter(0,1,1,7)
    out=[[]for _ in range(n)];indeg=[0]*n
    for i,(u,v,l)in enumerate(es):
        if l==root:out[u].append(i);indeg[v]+=1
    todo=deque(i for i,d in enumerate(indeg)if d==0);alive=bytearray([1])*n
    while todo:
        u=todo.popleft();alive[u]=0
        for e in out[u]:
            v=es[e][1];indeg[v]-=1
            if indeg[v]==0:todo.append(v)
    if not any(alive):return None
    # Walk backwards through the remaining finite graph; every live vertex
    # has a live predecessor. Repeated vertex gives an actual oriented cycle.
    incoming=[[]for _ in range(n)]
    for u in range(n):
        if alive[u]:
            for e in out[u]:
                v=es[e][1]
                if alive[v]:incoming[v].append(e)
    v=next(i for i,a in enumerate(alive)if a);seen={};back=[]
    while v not in seen:
        seen[v]=len(back);e=incoming[v][0];back.append(e);v=es[e][0]
    cycle=list(reversed(back[seen[v]:]))
    assert all(es[cycle[j]][1]==es[cycle[(j+1)%len(cycle)]][0]for j in range(len(cycle)))
    return cycle

def decode_cycle(graphs,cycle,options):
    depth=len(graphs)-1;n=len(cycle);columns=[];walk=cycle
    for k in range(depth,0,-1):
        g=graphs[k];nextwalk=[];col=[]
        for e in walk:
            u,v,l=g['edges'][e];prior_e,opt=g['origin'][u]
            nextwalk.append(prior_e);Q,a,b,c,h,R=options[opt];col.extend((Q,R))
        assert all(graphs[k-1]['edges'][nextwalk[j]][1]==graphs[k-1]['edges'][nextwalk[(j+1)%n]][0]for j in range(n))
        columns.append(col);walk=nextwalk
    start_e=walk[0];start_vertex=graphs[0]['edges'][start_e][0]
    meta=graphs[0]['origin'][start_vertex];B=tuple(meta['bulk']);slot=meta['slot']
    for _ in range(slot):B=step(step(B,0),1)
    # Select the exact bulk at the root-cycle's initial temporal phase.
    cols=[[8 if t%2==0 else 17 for t in range(2*n)]]+columns
    rows=[tuple(col[t]for col in cols)for t in range(2*n)]
    return dict(bulk=B,period=2*n,width=len(cols),rows=rows,
                root_cycle=cycle,inverse_depth=depth)

def digits(q,c):
    ds=[]
    for x in q:c,d=divmod(x+c,10);ds.append(d)
    return ds,c

def check_exterior(result):
    rows=result['rows'];q=tuple(result['bulk']);initial=q
    for t,row in enumerate(rows):
        assert row[0]==(8 if t%2==0 else 17)
        assert all(0<=x<=18 for x in row)
        low,lc=digits(row,0)
        high_rev,hc=digits(row[::-1],(q[0]+carry(q,0,1))//10);high=high_rev[::-1]
        assert lc==carry(q,0,-1) and hc==t%2
        nxt=tuple(low[i]+(1 if t%2 and i==0 else high[i-t%2])for i in range(len(row)))
        assert nxt==rows[(t+1)%len(rows)]
        nq=step(q,t%2)
        if t%2:assert nq[0]==(q[0]+carry(q,0,-1))%10+high[-1]
        q=nq
    assert q==initial
    return True

def run(layers,cap):
    start=time.monotonic();fibers,output,_,_=build_tables()
    local=json.loads((HERE.parent/'reverse/local_inverse_tables.json').read_text());options=local['options']
    assert local['fibers']==[list(x)for x in fibers] and local['output']==output
    first,targets=initial();graphs=[first];seen={};records=[];status='UNKNOWN depth cap'
    (HERE/'target_cycles.json').write_text(json.dumps(targets,indent=2)+'\n')
    for depth in range(layers+1):
        g=graphs[-1];cycle=root_cycle(g)
        record=dict(depth=depth,vertices=g['vertices'],edges=len(g['edges']),root_cycle_length=None if cycle is None else len(cycle),seconds=time.monotonic()-start)
        records.append(record);print(json.dumps(record),flush=True)
        (HERE/f'graph_{depth}.json').write_text(json.dumps(g,separators=(',',':'))+'\n')
        if cycle is not None:
            result=decode_cycle(graphs,cycle,options);result['independent_exterior_check']=check_exterior(result)
            result['common_cap_return']=lcm(12,result['period'])
            result['finite_integer_family_checked']=False
            (HERE/'candidate_exterior.json').write_text(json.dumps(result,indent=2)+'\n')
            status='POSITIVE finite exterior; finite family still to check';break
        signature=(g['vertices'],tuple(g['edges']))
        if signature in seen:
            status='exact repeated graph; all-period negative closure requires independent certificate'
            print(json.dumps(dict(kind='graph_repeat',first=seen[signature],repeat=depth)),flush=True);break
        seen[signature]=depth
        if depth==layers:break
        nxt=preimage(g,fibers,output,cap)
        if nxt is None:status='UNKNOWN raw graph size cap';break
        graphs.append(nxt)
    summary=dict(status=status,records=records,graph_size_cap=cap,
                 decimal_lychrel_existence_proved=False)
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--layers',type=int,default=20);p.add_argument('--cap',type=int,default=2000000);a=p.parse_args();run(a.layers,a.cap)
