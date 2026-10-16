"""Constructive all-period forward/reverse boundary-language joins.

Forward columns use exact local carry arithmetic and SCC trimming.
Bidirectional bisimulation quotients preserve cyclic words up to powers;
all quotient and column origins are retained for explicit witness lifting.
Every positive join must pass the separate ordinary exterior checker.
Size caps yield UNKNOWN, never an arbitrary-width exclusion.
"""
from pathlib import Path
from itertools import product
from collections import defaultdict,Counter,deque
from math import lcm
import sys,json,time,argparse
sys.dont_write_bytecode=True

HERE=Path(__file__).resolve().parent
REV=HERE.parent/'reverse525'
sys.path[:0]=[str(REV),str(HERE.parent/'reverse')]
from search525 import trim_with_origin,check_exterior,step
from compressed_search import compress_both,lift_cycle
from check_reverse_certificate import decode_letter,encode_letter

def forward_tables():
    options=[];fibers=[[]for _ in range(88)]
    for letter in range(88):
        a,b,c,z=decode_letter(letter)
        for Q,d,e in product(range(19),(0,1),(0,1)):
            highcarry,hi=divmod(Q+d,10)
            if highcarry!=c:continue
            ap,lo=divmod(Q+a,10)
            R=lo+hi
            if R<9 and e or R>9 and not e:continue
            if not 0<=z+e<=9:continue
            bp,olow=divmod(R+b,10)
            Qnext=olow+z+e
            if not 0<=Qnext<=18:continue
            new=encode_letter(ap,bp,d,R-10*e)
            fibers[letter].append(len(options))
            options.append((Q,d,e,R,Qnext,new))
    return options,fibers

def image(graph,options,fibers,cap):
    n=graph['vertices'];es=graph['edges'];outgoing=[[]for _ in range(n)]
    for i,(u,v,l)in enumerate(es):outgoing[u].append(i)
    origin=[(i,x)for i,(u,v,l)in enumerate(es)for x in fibers[l]]
    if len(origin)>cap:return None,dict(cap_kind='raw vertices',raw_vertices=len(origin))
    ids={x:i for i,x in enumerate(origin)}
    by_q=defaultdict(list)
    for e,x in origin:by_q[e,options[x][0]].append(x)
    edges=[]
    for u,(e,x)in enumerate(origin):
        Q,d,h,R,Qnext,new=options[x]
        for f in outgoing[es[e][1]]:
            for y in by_q[f,Qnext]:
                edges.append((u,ids[f,y],new))
                if len(edges)>cap:return None,dict(cap_kind='raw edges',raw_vertices=len(origin),raw_edges=len(edges))
    trimmed=trim_with_origin(len(origin),edges,origin)
    return trimmed,dict(raw_vertices=len(origin),raw_edges=len(edges))

def any_cycle(n,edges):
    """Return edge indices of a directed cycle, or None after exact deletion."""
    out=[[]for _ in range(n)];ind=[0]*n
    for e,(u,v,_)in enumerate(edges):out[u].append(e);ind[v]+=1
    queue=deque(u for u in range(n)if not ind[u]);alive=bytearray([1])*n
    while queue:
        u=queue.popleft();alive[u]=0
        for e in out[u]:
            v=edges[e][1];ind[v]-=1
            if not ind[v]:queue.append(v)
    if not any(alive):return None
    incoming=[[]for _ in range(n)]
    for e,(u,v,l)in enumerate(edges):
        if alive[u]and alive[v]:incoming[v].append(e)
    v=next(u for u in range(n)if alive[u]);seen={};back=[]
    while v not in seen:
        seen[v]=len(back);e=incoming[v][0];back.append(e);v=edges[e][0]
    cycle=list(reversed(back[seen[v]:]))
    assert all(edges[cycle[j]][1]==edges[cycle[(j+1)%len(cycle)]][0]for j in range(len(cycle)))
    return cycle

def intersection(left,right,cap):
    L=defaultdict(list);R=defaultdict(list)
    for e,(u,v,l)in enumerate(left['edges']):L[l].append(e)
    for e,(u,v,l)in enumerate(right['edges']):R[l].append(e)
    count=sum(len(es)*len(R[l])for l,es in L.items())
    if count>cap:return None,dict(status='UNKNOWN product edge cap',raw_product_edges=count)
    ids={};nodes=[];edges=[];provenance=[]
    def vertex(pair):
        if pair not in ids:ids[pair]=len(nodes);nodes.append(pair)
        return ids[pair]
    for l,les in L.items():
        for e in les:
            u,v,_=left['edges'][e]
            for f in R[l]:
                x,y,_=right['edges'][f]
                edges.append((vertex((u,x)),vertex((v,y)),l));provenance.append((e,f))
    cycle=any_cycle(len(nodes),edges)
    stats=dict(status='EMPTY exact cyclic intersection'if cycle is None else'CYCLIC INTERSECTION',
               product_vertices=len(nodes),product_edges=len(edges),cycle_length=None if cycle is None else len(cycle))
    if cycle is None:return None,stats
    return dict(left=[provenance[e][0]for e in cycle],right=[provenance[e][1]for e in cycle],
                labels=[edges[e][2]for e in cycle]),stats

def uncompress(graph,stage,walk):
    power_total=1;proof=[];current=graph
    for op in reversed(stage['operations']):
        inp=op['graph'];reverse=op['reverse']
        if reverse:
            qr=dict(vertices=current['vertices'],edges=[(v,u,l)for u,v,l in current['edges']])
            rr=dict(vertices=inp['vertices'],edges=[(v,u,l)for u,v,l in inp['edges']])
            lifted,power=lift_cycle(qr,list(reversed(walk)),rr,op['blocks'])
            walk=list(reversed(lifted))
        else:walk,power=lift_cycle(current,walk,inp,op['blocks'])
        power_total*=power;proof.append(dict(reverse=reverse,power=power,pair_period=len(walk)))
        current=inp
    assert current==stage['graph']
    return walk,power_total,proof

def decode_forward(history,cycle,options):
    walk=cycle;columns=[];proof=[];original_length=len(cycle)
    for k in range(len(history)-1,0,-1):
        rec=history[k];walk,power,logs=uncompress(rec['graph'],rec['stage'],walk)
        columns=[col*power for col in columns];proof.append(dict(depth=k,quotients=logs))
        raw=rec['stage']['graph'];col=[];prior=[]
        for edge in walk:
            u,v,l=raw['edges'][edge];e,opt=raw['origin'][u]
            Q,d,h,R,Qnext,new=options[opt]
            assert l==new
            col.extend((Q,R));prior.append(e)
        columns.append(col);walk=prior
        prev=history[k-1]['graph']['edges']
        assert all(prev[walk[j]][1]==prev[walk[(j+1)%len(walk)]][0]for j in range(len(walk)))
    assert all(history[0]['graph']['edges'][e][2]==41 for e in walk)
    columns.reverse();T=2*len(walk)
    columns=[[8 if t%2==0 else 17 for t in range(T)]]+columns
    return columns,len(walk)//original_length,proof

def decode_reverse(history,cycle,options):
    walk=cycle;columns=[];proof=[];original_length=len(cycle)
    for k in range(len(history)-1,-1,-1):
        rec=history[k];walk,power,logs=uncompress(rec['graph'],rec['stage'],walk)
        columns=[col*power for col in columns];proof.append(dict(depth=k,quotients=logs))
        raw=rec['stage']['graph']
        if k==0:
            source=raw['edges'][walk[0]][0];meta=raw['origin'][source]
            B=tuple(meta['bulk'])
            for _ in range(meta['slot']):B=step(step(B,0),1)
            return columns,B,len(walk)//original_length,proof
        col=[];prior=[]
        for edge in walk:
            u,v,l=raw['edges'][edge];e,opt=raw['origin'][u]
            Q,a,b,c,h,R=options[opt]
            col.extend((Q,R));prior.append(e)
        columns.append(col);walk=prior
        prev=history[k-1]['graph']['edges']
        assert all(prev[walk[j]][1]==prev[walk[(j+1)%len(walk)]][0]for j in range(len(walk)))

def reconstruct(forward,reverse,hit,fopts,ropts):
    fc,fp,flogs=decode_forward(forward,hit['left'],fopts)
    rc,B,rp,rlogs=decode_reverse(reverse,hit['right'],ropts)
    power=lcm(fp,rp);fc=[col*(power//fp)for col in fc];rc=[col*(power//rp)for col in rc]
    cols=fc+rc;T=2*len(hit['labels'])*power
    assert all(len(col)==T for col in cols)
    rows=[tuple(col[t]for col in cols)for t in range(T)]
    result=dict(bulk=B,period=T,width=len(cols),rows=rows,
                forward_depth=len(forward)-1,reverse_depth=len(reverse)-1,
                join_pair_period=len(hit['labels']),forward_lift_power=fp,reverse_lift_power=rp,
                joined_lift_power=power,forward_lifts=flogs,reverse_lifts=rlogs,
                finite_integer_family_checked=False)
    result['ordinary_exterior_check']=check_exterior(result)
    return result

def load_reverse(mode):
    directory=REV/('bidirectional525'if mode=='525'else'all_bulk_bidir')
    paths=sorted(directory.glob('graph_*.json'),key=lambda p:int(p.stem.split('_')[-1]))
    return [json.loads(p.read_text())for p in paths],directory

def run(layers,cap,product_cap,modes):
    start=time.monotonic();fopts,fibers=forward_tables()
    ropts=json.loads((HERE.parent/'reverse/local_inverse_tables.json').read_text())['options']
    (HERE/'forward_local_options.json').write_text(json.dumps(dict(options=fopts,fibers=fibers),separators=(',',':'))+'\n')
    reverse={mode:load_reverse(mode)for mode in modes}
    history=[dict(graph=dict(vertices=1,edges=[(0,0,41)]))]
    records=[];joins=[];seen={};status='UNKNOWN forward depth cap'
    for depth in range(layers+1):
        rec=history[-1];g=rec['graph']
        record=dict(depth=depth,vertices=g['vertices'],edges=len(g['edges']),seconds=time.monotonic()-start)
        records.append(record);print(json.dumps(dict(kind='forward',**record)),flush=True)
        (HERE/f'graph_{depth}.json').write_text(json.dumps(rec,separators=(',',':'))+'\n')
        for mode,(rh,directory)in reverse.items():
            for r in range(len(rh)-1,-1,-1):
                hit,stats=intersection(g,rh[r]['graph'],product_cap)
                row=dict(forward_depth=depth,reverse_mode=mode,reverse_depth=r,**stats)
                joins.append(row);print(json.dumps(dict(kind='join',**row)),flush=True)
                if hit is not None:
                    result=reconstruct(history,rh[:r+1],hit,fopts,ropts)
                    (HERE/'candidate_exterior.json').write_text(json.dumps(result,indent=2)+'\n')
                    status='POSITIVE finite exterior ordinary carry replay passed; no finite family yet'
                    report=dict(status=status,records=records,joins=joins,seconds=time.monotonic()-start,
                                finite_lychrel_witness=False)
                    (HERE/'summary.json').write_text(json.dumps(report,indent=2)+'\n');return report
        signature=(g['vertices'],tuple(map(tuple,g['edges'])))
        if signature in seen:
            status='forward power-language repeated; full negative conclusion requires independent closure audit'
            break
        seen[signature]=depth
        if depth==layers:break
        raw,stats=image(g,fopts,fibers,cap)
        print(json.dumps(dict(kind='forward_image',depth=depth+1,**stats)),flush=True)
        if raw is None:status='UNKNOWN forward raw graph size cap';break
        compressed,stage=compress_both(raw)
        history.append(dict(graph=compressed,stage=stage))
    report=dict(status=status,records=records,joins=joins,seconds=time.monotonic()-start,
                raw_graph_cap=cap,product_edge_cap=product_cap,
                cyclic_language_semantics='up to positive powers, with complete reconstruction provenance',
                finite_lychrel_witness=False)
    (HERE/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ('records','joins')}),flush=True)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--layers',type=int,default=24)
    p.add_argument('--cap',type=int,default=2000000);p.add_argument('--product-cap',type=int,default=2000000)
    p.add_argument('--modes',nargs='+',choices=['525','all'],default=['525','all'])
    a=p.parse_args();run(a.layers,a.cap,a.product_cap,a.modes)
