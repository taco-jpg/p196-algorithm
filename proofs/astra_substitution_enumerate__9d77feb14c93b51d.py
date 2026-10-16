"""Complete finite enumeration of local two-bulk pump components.

All transitions are ordinary integer column arithmetic. Scope is one fixed
24-step alternating overflow clock and the specified finite component width.
Local loops do not assert existence without compatible gluing.
"""
from itertools import product
import argparse,json,time
from pathlib import Path
from astra_substitution_gluing import trace
from astra_substitution_twobulk import pool

def outer_three_filter():
    # Every edge admits an arbitrary carry from the omitted interior. Hence
    # this graph overapproximates every genuine alternating exterior prefix.
    states=[(a,b,c) for a in (8,17) for b in range(19) for c in range(19)]
    graph={}
    for q in states:
        h=int(q[0]==17);targets=set()
        lo,_=digits(q,0)
        for incoming in (0,1):
            hi,out=digits(q[::-1],incoming);hi=hi[::-1]
            if out!=h:continue
            nxt=tuple(lo[i]+(1 if h and i==0 else hi[i-h]) for i in range(3))
            if nxt[0]==(8 if h else 17):targets.add(nxt)
        graph[q]=targets
    eligible=[]
    for q in states:
        reach={q}
        for _ in range(24):reach={v for u in reach for v in graph[u]}
        if q in reach:eligible.append(q)
    data={'state_count':len(states),'edge_count':sum(map(len,graph.values())),'period':24,'return_states':eligible,'initial_nonoverflow_prefixes':[q for q in eligible if q[0]==8],
          'graph':[{'q':q,'targets':sorted(graph[q])} for q in states],
          'scope':'Complete722-state arbitrary-interior-carry overapproximation; every genuine24-step alternating exterior loop projects to a length24 closed walk.'}
    return data

def digits(word,carry):
    out=[]
    for q in word:out.append((q+carry)%10);carry=(q+carry)//10
    return out,carry

def transition(kind,w,bt,t,ct=None):
    h=t%2;b=bt[t];bn=bt[(t+1)%24];n=len(w)
    if kind=='exterior':
        if w[0]!=(8 if h==0 else 17):return None
        lo,lc=digits(w,0);hi,rc=digits(w[::-1],b['R'][0]);hi=hi[::-1]
        if lc!=b['A'][0] or rc!=h:return None
        out=tuple(lo[i]+(1 if h and i==0 else hi[i-h]) for i in range(n))
        if h and b['lo'][0]+hi[-1]!=bn['q'][0]:return None
        return out
    if kind=='center':
        g=t//2;ng=(t+1)//2;d=g//2;shift=ng//2-d;newn=n+(ng%2)-(g%2)
        lo,lc=digits(w,b['A'][d%3]);hi=lo[::-1]
        if lc!=b['R'][d%3]:return None
        def outside(i,which):
            if i<0:return b[which][(d+i)%3]
            return b['hi' if which=='lo' else 'lo'][(d-1-(i-n))%3]
        def target(i):return bn['q'][(d+shift+i)%3] if i<0 else bn['q'][(d+shift-1-(i-newn))%3]
    else:
        c=ct[t];cn=ct[(t+1)%24];d=t//8;shift=(t+1)//8-d;newn=n
        lo,lc=digits(w,b['A'][d%3]);hi,rc=digits(w[::-1],c['R'][d%3]);hi=hi[::-1]
        if lc!=c['A'][d%3] or rc!=b['R'][d%3]:return None
        def outside(i,which):return b[which][(d+i)%3] if i<0 else c[which][(d+i-n)%3]
        def target(i):return bn['q'][(d+shift+i)%3] if i<0 else cn['q'][(d+shift+i-newn)%3]
    def dig(i,which):return (lo if which=='lo' else hi)[i] if 0<=i<n else outside(i,which)
    out=tuple(dig(shift+i,'lo')+dig(shift+i-h,'hi') for i in range(newn))
    if any(dig(shift+i,'lo')+dig(shift+i-h,'hi')!=target(i) for i in (-1,newn)):return None
    if kind=='center':
        if out!=out[::-1]:return None
        if len(out)%2 and out[len(out)//2]%2:return None
    return out

def enumerate_component(kind,B,width,C=None,maxsamples=3,prefixes=None):
    start=time.monotonic();bt=trace(B);ct=trace(C) if C is not None else None
    if kind=='center':
        assert width%2==0
        seeds=(x+x[::-1] for x in product(range(19),repeat=width//2))
    elif kind=='exterior':
        seeds=((8,)+x for x in product(range(19),repeat=width-1)) if prefixes is None else (p+x for p in prefixes for x in product(range(19),repeat=width-3))
    else:seeds=product(range(19),repeat=width)
    count=0;loops=0;hist=[0]*25;samples=[]
    for initial in seeds:
        count+=1;w=initial
        for t in range(24):
            w=transition(kind,w,bt,t,ct)
            if w is None:hist[t]+=1;break
        else:
            hist[24]+=1
            if w==initial:
                loops+=1
                if len(samples)<maxsamples:samples.append(initial)
    return dict(kind=kind,B=B,C=C,width=width,states=count,return_loops=loops,exit_histogram=hist,samples=samples,seconds=time.monotonic()-start,status='COMPLETE_FINITE_LOCAL_ENUMERATION')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['exterior','center'],default='center');p.add_argument('--width',type=int,default=6);p.add_argument('--limit',type=int,default=198);p.add_argument('--include-uniform',action='store_true');p.add_argument('--prefix-filter',action='store_true');p.add_argument('--out',default='astra_substitution_center_enumeration.json');a=p.parse_args()
    motifs=pool(24)[:a.limit]
    if a.include_uniform:motifs +=[(v,v,v) for v in range(0,19,2)]
    rows=[];prefixes=None
    if a.prefix_filter:
        assert a.kind=='exterior' and a.width>=3
        data=outer_three_filter();Path('astra_substitution_outer_three_graph.json').write_text(json.dumps(data,indent=2)+'\n')
        prefixes=data['initial_nonoverflow_prefixes']
        print(json.dumps({'prefix_filter':prefixes,'states':data['state_count'],'edges':data['edge_count']}),flush=True)
    for B in motifs:
        r=enumerate_component(a.kind,B,a.width,prefixes=prefixes);rows.append(r)
        if len(rows)%10==0 or r['return_loops']:
            Path(a.out).write_text(json.dumps(rows,indent=2)+'\n')
            print(json.dumps({'processed':len(rows),'motif':B,'loops':r['return_loops'],'seconds':r['seconds']}),flush=True)
    Path(a.out).write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps({'motifs':len(rows),'states':sum(r['states'] for r in rows),'loops':sum(r['return_loops'] for r in rows),'positive_components':sum(bool(r['return_loops']) for r in rows)}),flush=True)
