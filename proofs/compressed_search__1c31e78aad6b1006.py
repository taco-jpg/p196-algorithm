"""All-period constructive inverse-language search with power-safe quotienting.

Root hits are lifted through every bisimulation quotient to genuine graph
cycles, repeating previously decoded exterior columns whenever required.
Only the final ordinary arithmetic replay can certify a positive exterior.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import product
from collections import Counter
from math import lcm
import json,time,argparse
from search525 import (HERE,initial,preimage,root_cycle,bulk_cycle,step,
                       build_tables,check_exterior)
from bisimulation import quotient

def all_initial():
    f={}
    for q in product(range(19),repeat=3):
        if q==(9,9,9):continue
        r=step(q,0)
        if r==(9,9,9):continue
        v=step(r,1)
        if v!=(9,9,9):f[q]=v
    seen=set();cycles=[]
    for q in sorted(f):
        if q in seen:continue
        path=[];at={};v=q
        while v not in seen and v not in at and v in f:
            at[v]=len(path);path.append(v);v=f[v]
        if v in at:cycles.append(path[at[v]:])
        seen.update(path)
    n=0;edges=[];origin=[];targets=[];keys=set()
    for cyc in cycles:
        B=cyc[0];word,rows=bulk_cycle(B)
        key=min(word[j:]+word[:j]for j in range(len(word)))
        targets.append(dict(bulk=B,pair_period=len(word),word=word,rows=rows,cycle_motifs=cyc))
        if key in keys:continue
        keys.add(key)
        for j,l in enumerate(word):
            edges.append((n+j,n+(j+1)%len(word),l));origin.append(dict(bulk=B,slot=j))
        n+=len(word)
    assert len(cycles)==66 and sum(map(len,cycles))==334
    return dict(vertices=n,edges=edges,origin=origin),targets

def compress(g):
    q=quotient(g['vertices'],g['edges'])
    return dict(vertices=q['vertices'],edges=q['edges']),dict(graph=g,blocks=q['blocks'],rounds=q['rounds'])

def compress_both(g):
    """Alternate exact forward and reversed-graph bisimulation quotients."""
    original=g;operations=[];rounds=0
    while True:
        changed=False
        for reverse in (False,True):
            es=[(v,u,l)for u,v,l in g['edges']]if reverse else g['edges']
            q=quotient(g['vertices'],es)
            after=dict(vertices=q['vertices'],edges=sorted((v,u,l)for u,v,l in q['edges'])if reverse else q['edges'])
            operations.append(dict(graph=g,blocks=q['blocks'],reverse=reverse))
            rounds+=q['rounds'];changed|=after['vertices']<g['vertices'];g=after
        if not changed:break
    return g,dict(graph=original,operations=operations,rounds=rounds)

def lift_cycle(qgraph,cycle,raw,blocks):
    """Lift a positive power, always choosing the quotient phase-zero cut."""
    es=raw['edges'];qes=qgraph['edges'];lookup={}
    for e,(u,v,l)in enumerate(es):lookup.setdefault((u,blocks[v],l),e)
    source=qes[cycle[0]][0]
    u=next(i for i,b in enumerate(blocks)if b==source)
    seen={};history=[];rounds=0
    while u not in seen:
        seen[u]=rounds
        for qe in cycle:
            a,b,l=qes[qe]
            assert blocks[u]==a
            e=lookup[u,b,l];history.append(e);u=es[e][1]
        assert blocks[u]==source
        rounds+=1
    first=seen[u];power=rounds-first
    lifted=history[first*len(cycle):]
    assert len(lifted)==len(cycle)*power
    assert all(es[lifted[j]][1]==es[lifted[(j+1)%len(lifted)]][0]for j in range(len(lifted)))
    return lifted,power

def reconstruct(graphs,stages,cycle,options):
    columns=[];walk=cycle;proof=[]
    for k in range(len(graphs)-1,-1,-1):
        stage=stages[k];raw=stage['graph']
        if 'operations'in stage:
            current=graphs[k]
            for op in reversed(stage['operations']):
                inp=op['graph'];reverse=op['reverse']
                if reverse:
                    qr=dict(vertices=current['vertices'],edges=[(v,u,l)for u,v,l in current['edges']])
                    rr=dict(vertices=inp['vertices'],edges=[(v,u,l)for u,v,l in inp['edges']])
                    lifted,power=lift_cycle(qr,list(reversed(walk)),rr,op['blocks'])
                    walk=list(reversed(lifted))
                else:walk,power=lift_cycle(current,walk,inp,op['blocks'])
                if power>1:columns=[col*power for col in columns]
                proof.append(dict(level=k,reverse=reverse,power=power,pair_period=len(walk)))
                current=inp
        else:
            walk,power=lift_cycle(graphs[k],walk,raw,stage['blocks'])
            if power>1:columns=[col*power for col in columns]
            proof.append(dict(level=k,power=power,pair_period=len(walk)))
        if k==0:
            u=raw['edges'][walk[0]][0];meta=raw['origin'][u]
            B=tuple(meta['bulk'])
            for _ in range(meta['slot']):B=step(step(B,0),1)
            break
        col=[];nextwalk=[]
        for e in walk:
            u,v,l=raw['edges'][e];prior_e,opt=raw['origin'][u]
            nextwalk.append(prior_e);Q,a,b,c,h,R=options[opt];col.extend((Q,R))
        columns.append(col);walk=nextwalk
        n=len(walk)
        assert all(graphs[k-1]['edges'][walk[j]][1]==graphs[k-1]['edges'][walk[(j+1)%n]][0]for j in range(n))
    T=2*len(walk);columns=[[8 if t%2==0 else 17 for t in range(T)]]+columns
    assert all(len(col)==T for col in columns)
    rows=[tuple(col[t]for col in columns)for t in range(T)]
    result=dict(bulk=B,period=T,width=len(columns),rows=rows,lifts=proof,
                common_cap_return=lcm(12,T),finite_integer_family_checked=False)
    result['ordinary_exterior_check']=check_exterior(result)
    return result

def run(mode,layers,cap,both=False):
    start=time.monotonic();fibers,output,_,_=build_tables()
    options=json.loads((HERE.parent/'reverse/local_inverse_tables.json').read_text())['options']
    destination=HERE/(('bidirectional525'if mode=='525'else'all_bulk_bidir')if both else('compressed525'if mode=='525'else'all_bulk'));destination.mkdir(exist_ok=True)
    compressor=compress_both if both else compress
    raw,targets=initial()if mode=='525'else all_initial()
    (destination/'target_cycles.json').write_text(json.dumps(targets,separators=(',',':'))+'\n')
    first,stage=compressor(raw);graphs=[first];stages=[stage];seen={};records=[];status='UNKNOWN depth cap'
    for depth in range(layers+1):
        g=graphs[-1];stage=stages[-1];cycle=root_cycle(g)
        r=dict(depth=depth,vertices=g['vertices'],edges=len(g['edges']),
               before_quotient_vertices=stage['graph']['vertices'],
               before_quotient_edges=len(stage['graph']['edges']),
               refinement_rounds=stage['rounds'],root_cycle_length=None if cycle is None else len(cycle),
               seconds=time.monotonic()-start)
        records.append(r);print(json.dumps(r),flush=True)
        (destination/f'graph_{depth}.json').write_text(json.dumps(dict(graph=g,stage=stage),separators=(',',':'))+'\n')
        if cycle is not None:
            result=reconstruct(graphs,stages,cycle,options)
            (destination/'candidate_exterior.json').write_text(json.dumps(result,indent=2)+'\n')
            status='POSITIVE finite exterior independently replayed; finite integer family not checked';break
        signature=(g['vertices'],tuple(g['edges']))
        if signature in seen:
            status='power-language graph repeat; negative certificate requires independent check'
            print(json.dumps(dict(kind='repeat',first=seen[signature],repeat=depth)),flush=True);break
        seen[signature]=depth
        if depth==layers:break
        raw=preimage(g,fibers,output,cap)
        if raw is None:status='UNKNOWN raw graph size cap';break
        new,newstage=compressor(raw);graphs.append(new);stages.append(newstage)
    result=dict(status=status,mode=mode,records=records,raw_graph_size_cap=cap,
                cyclic_language_semantics='up to positive powers with explicit witness lifting',
                decimal_lychrel_existence_proved=False)
    (destination/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['525','all'],default='525');p.add_argument('--layers',type=int,default=16);p.add_argument('--cap',type=int,default=2000000);p.add_argument('--both',action='store_true');a=p.parse_args();run(a.mode,a.layers,a.cap,a.both)
