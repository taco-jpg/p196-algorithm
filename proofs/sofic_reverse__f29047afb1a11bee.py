"""Exact cyclic regular-language preimages, allowing every temporal period.

An edge-labeled graph accepts labels of finite closed walks. Preimage uses
vertices=(old graph edge, local inverse option), so no temporal correlations
are discarded. SCC trimming preserves all and only labels of closed walks.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,time,argparse
from check_reverse_certificate import build_tables,target,canonical,unpack,encode_letter

HERE=Path(__file__).resolve().parent

def scc_trim(n,edges):
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
    good=[(u,v,l)for u,v,l in edges if comp[u]==comp[v] and (sizes[comp[u]]>1 or u==v)]
    kept=sorted({u for u,v,l in good}|{v for u,v,l in good})
    rename={u:i for i,u in enumerate(kept)}
    return len(kept),[(rename[u],rename[v],l)for u,v,l in good],Counter(sizes[comp[u]]for u in kept)

def preimage(n,edges,fibers,output,cap):
    outgoing=[[]for _ in range(n)]
    for i,(u,v,l)in enumerate(edges):outgoing[u].append(i)
    options=[];index={}
    for i,(u,v,l)in enumerate(edges):
        for x in fibers[l]:index[i,x]=len(options);options.append((i,x))
    if len(options)>cap:return None
    result=[]
    for u,(e,x)in enumerate(options):
        _,v,_=edges[e]
        for f in outgoing[v]:
            for y in fibers[edges[f][2]]:
                l=output[x][y]
                if l>=0:result.append((u,index[f,y],l))
                if len(result)>cap:return None
    return scc_trim(len(options),result)

def contains_uniform(n,edges,label):
    return bool(scc_trim(n,[e for e in edges if e[2]==label])[0])

def initial():
    words={canonical(target(B))for B in [(9,3,6),(9,6,3)]}
    edges=[];n=0
    for packed in sorted(words):
        w=unpack(*packed)
        period=next(p for p in (1,2,3,4,6,12)if all(w[i]==w[i%p]for i in range(12)))
        for j,l in enumerate(w[:period]):edges.append((n+j,n+(j+1)%period,l))
        n+=period
    return n,edges

def run(layers,cap):
    begin=time.monotonic();fibers,output,_,_=build_tables();n,edges=initial()
    records=[]
    for k in range(layers+1):
        rootlabel=encode_letter(0,1,1,7)
        record=dict(depth=k,vertices=n,edges=len(edges),
                    root_uniform_cycle=contains_uniform(n,edges,rootlabel),
                    letters=len({l for u,v,l in edges}),
                    seconds=time.monotonic()-begin)
        records.append(record);print(json.dumps(record),flush=True)
        if k<=8:
            (HERE/f'sofic_depth_{k}.json').write_text(json.dumps(dict(vertices=n,edges=edges),separators=(',',':'))+'\n')
        if k==layers:break
        result=preimage(n,edges,fibers,output,cap)
        if result is None:
            print(json.dumps(dict(status='UNKNOWN graph size cap',cap=cap)),flush=True)
            break
        n,edges,component_sizes=result
        print(json.dumps(dict(kind='component_sizes',depth=k+1,vertex_weighted_histogram=component_sizes)),flush=True)
    (HERE/'sofic_summary.json').write_text(json.dumps(dict(records=records,
        arbitrary_width_status='UNKNOWN',decimal_lychrel_existence_proved=False),indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--layers',type=int,default=8);p.add_argument('--cap',type=int,default=2000000);a=p.parse_args();run(a.layers,a.cap)
