"""All-temporal-period preimages for the genuinely new28-phase bulk cycle.

Adapted from the sibling reverse/sofic_reverse.py cyclic-language method.
The alphabet now retains all seven phases of N,N,N,N,O,O,O separately.
No temporal period is fixed in this search. A size cap remains UNKNOWN.
"""
from pathlib import Path
from collections import Counter
import json,time,argparse
from columns import initial as root_state,bulk_state
HERE=Path(__file__).resolve().parent
CLOCK=(0,0,0,0,1,1,1)
OUTER=(1,2,4,9,18,9,10)


def encode(t,a,v):
    assert 0<=t<7 and a in (0,1)
    assert (-1<=v<=9)if CLOCK[t]else(v in (0,1))
    return 22*t+11*a+v+CLOCK[t]


def decode(l):
    t=l//22;a=(l%22)//11;v=l%11-CLOCK[t]
    assert encode(t,a,v)==l
    return t,a,v


def state_word(state):
    a,b,z=state;word=[];j=k=0
    for t,x in enumerate(a):
        if CLOCK[t%7]:word.append(encode(t%7,x,z[k]));k+=1
        else:word.append(encode(t%7,x,b[j]));j+=1
    return tuple(word)


def options(label):
    t,alpha,other=decode(label);out=[]
    for q in range(19):
        for a in (0,1):
            if (q+a)//10!=alpha:continue
            low=(q+a)%10
            if CLOCK[t]:
                for incoming in (0,1):
                    e=(q+incoming)//10
                    if q-10*e==other:
                        opt=(t,q,a,e,low)
                        if opt not in out:out.append(opt)
            else:
                c=(q+other)//10
                out.append((t,q,a,c,low+(q+other)%10))
    return tuple(out)


def output(x,y):
    t,q,a,c,value=x
    if y[0]!=(t+1)%7:return -1
    if CLOCK[t]:
        z=y[1]-value-c
        if -1<=z<=9 and 0<=z+c<=9:return encode(t,a,z)
    elif y[1]==value:return encode(t,a,c)
    return -1


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
    good=[(u,v,l)for u,v,l in edges if comp[u]==comp[v]and(sizes[comp[u]]>1 or u==v)]
    kept=sorted({u for u,v,l in good}|{v for u,v,l in good});rename={u:i for i,u in enumerate(kept)}
    return len(kept),[(rename[u],rename[v],l)for u,v,l in good],kept


def inverse(n,edges,cap):
    outgoing=[[]for _ in range(n)]
    for i,(u,v,l)in enumerate(edges):outgoing[u].append(i)
    fibers={l:options(l)for u,v,l in edges}
    vertices=[(i,x)for i,(u,v,l)in enumerate(edges)for x in fibers[l]]
    if len(vertices)>cap:return None
    ids={v:i for i,v in enumerate(vertices)};raw=[]
    for u,(e,x)in enumerate(vertices):
        for f in outgoing[edges[e][1]]:
            for y in fibers[edges[f][2]]:
                l=output(x,y)
                if l>=0:raw.append((u,ids[f,y],l))
                if len(raw)>cap:return None
    count,es,kept=scc_trim(len(vertices),raw)
    return count,es,[vertices[i]for i in kept],dict(raw_vertices=len(vertices),raw_edges=len(raw))


def initial(new_only=True,all_recurrent=False,macro_periods=None):
    if all_recurrent:
        catalog=json.loads((HERE/'bulk7_complete_recurrent.json').read_text())
        words=set()
        for cycle in catalog['cycles']:
            if macro_periods is not None and len(cycle)not in macro_periods:continue
            for B in cycle:
                w=state_word(bulk_state(B,CLOCK*len(cycle)))
                period=next(p for p in range(7,len(w)+1,7)if len(w)%p==0 and all(w[i]==w[i%p]for i in range(len(w))))
                w=w[:period]
                words.add(min(w[k:]+w[:k]for k in range(0,period,7)))
        n=0;edges=[]
        for w in sorted(words):
            for j,l in enumerate(w):edges.append((n+j,n+(j+1)%len(w),l))
            n+=len(w)
        return n,edges,sorted(words)
    data=json.loads((HERE/'clock28_0_bulk.json').read_text());motifs=data['motifs']
    if new_only:
        old=json.loads((HERE/'clock14_bulk.json').read_text())[0]['returning_period3']
        motifs=[B for B in motifs if B not in old]
    words=set()
    for B in motifs:
        w=state_word(bulk_state(B,CLOCK*4))
        w=min(w[7*k:]+w[:7*k]for k in range(4))
        period=next(p for p in (7,14,28)if all(w[i]==w[i%p]for i in range(28)))
        words.add(w[:period])
    n=0;edges=[]
    for w in sorted(words):
        for j,l in enumerate(w):edges.append((n+j,n+(j+1)%len(w),l))
        n+=len(w)
    return n,edges,sorted(words)


def run(layers=12,cap=1000000,new_only=True,all_recurrent=False,macro_periods=None):
    began=time.monotonic();n,es,words=initial(new_only,all_recurrent,macro_periods)
    rw=state_word(root_state(OUTER,CLOCK));allowed=set(rw)
    graphs=[];records=[];status='UNKNOWN';recurrence=None
    prefix='sofic7_full'if all_recurrent else('sofic28_new'if new_only else'sofic28_all')
    if macro_periods is not None:prefix='sofic7_periods_'+'_'.join(map(str,macro_periods))
    for d in range(layers+1):
        root=bool(scc_trim(n,[e for e in es if e[2]in allowed])[0])
        r=dict(depth=d,vertices=n,edges=len(es),root_cycle=root,seconds=time.monotonic()-began)
        records.append(r);print(json.dumps(r),flush=True)
        (HERE/f'{prefix}_depth{d}.json').write_text(json.dumps(dict(vertices=n,edges=es),separators=(',',':'))+'\n')
        if root:status='ROOT_CYCLE_RECONSTRUCTION_REQUIRED';break
        same=next((i for i,g in enumerate(graphs)if g==(n,es)),None)
        if same is not None:
            status='EXACT_GRAPH_RECURRENCE_ROOT_ABSENT';recurrence=dict(first=same,repeat=d);break
        graphs.append((n,es))
        if d==layers:break
        nxt=inverse(n,es,cap)
        if nxt is None:status='UNKNOWN_GRAPH_CAP';break
        n,es,provenance,rawinfo=nxt
        (HERE/f'{prefix}_map{d+1}.json').write_text(json.dumps(dict(vertices=provenance,**rawinfo),separators=(',',':'))+'\n')
    result=dict(status=status,clock=CLOCK,outer=OUTER,new_tails_only=new_only and not all_recurrent,
                reason='layer limit'if status=='UNKNOWN'else('graph cap'if status=='UNKNOWN_GRAPH_CAP'else None),
                all_recurrent_non_neutral_period3=all_recurrent and macro_periods is None,
                uses_complete_recurrent_catalog=all_recurrent,
                macro_periods=macro_periods,
                seed_cycles=len(words),seed_words=words,root_word=rw,records=records,
                recurrence=recurrence,cap=cap,arbitrary_temporal_multiples=True,
                independent_certificate_replay_pending=True,
                finite_exterior_supplied=False,decimal_existence_proved=False)
    (HERE/f'{prefix}_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in('records','seed_words')}),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--layers',type=int,default=12)
    p.add_argument('--cap',type=int,default=1000000);p.add_argument('--all-tails',action='store_true')
    p.add_argument('--all-recurrent',action='store_true')
    p.add_argument('--macro-periods')
    a=p.parse_args();run(a.layers,a.cap,not a.all_tails,a.all_recurrent,
                         None if a.macro_periods is None else list(map(int,a.macro_periods.split(','))))
