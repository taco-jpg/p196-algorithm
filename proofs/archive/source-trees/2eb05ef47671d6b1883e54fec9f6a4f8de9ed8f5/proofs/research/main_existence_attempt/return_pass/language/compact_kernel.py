"""Memory-conscious continuation of the exact horizon-four kernel search.

Product states and class edges are packed into integers. BFS parents and
reverse-edge incidence use flat integer arrays. The prior 500k-cap record is
left untouched. A time/state cap always produces UNKNOWN.
"""
from array import array
import argparse
import hashlib
import json
import time

from residual_kernel import HERE, CENTERS, START_FST, fst_edge, fst_term, realize


def carry_graph():
    keys = list(START_FST)
    ids = {x:i for i,x in enumerate(keys)}
    edges,terms = [],[]
    for st in keys:
        row=[]
        for q in range(19):
            for ns,out in fst_edge(st,q):
                if ns not in ids:
                    ids[ns]=len(keys)
                    keys.append(ns)
                row.append((q,out,ids[ns]))
        edges.append(row)
        ts=[]
        for cidx,c in enumerate(CENTERS):
            term=fst_term(st,c)
            if term is not None:
                extra,oc=term
                ts.append((cidx,extra,0 if oc is None else oc//2+1))
        terms.append(ts)
    return edges,terms


def run(depth,cap,seconds,prefix=''):
    start=time.monotonic()
    deadline=start+seconds
    machine=json.loads((HERE/('observation_%sdepth%d.json'%(prefix,depth))).read_text())
    d,f=machine['delta'],machine['finish']
    n=len(d)
    width=11*n
    fedges,fterms=carry_graph()
    nf=len(fedges)
    assert nf==46
    # Packed product state: ((input DFA state)*n+output DFA state)*nf+FST.
    states=[0,1]
    ids={0:0,1:1}
    parents=array('I',[0xffffffff,0xffffffff])
    letters=array('B',[0,0])
    edges={}
    reps=array('i',[-1])*width
    unknown=None
    for index,code in enumerate(states):
        if index%1000==0 and time.monotonic()>deadline:
            unknown='UNKNOWN_time_cap'
            break
        pair,x=divmod(code,nf)
        si,so=divmod(pair,n)
        for cidx,extra,ocidx in fterms[x]:
            target=so if extra is None else d[so][extra]
            a,b=11*si+cidx,11*target+ocidx
            key=a*width+b
            witness=11*index+cidx
            if key not in edges:
                edges[key]=witness
            if reps[a]<0:
                reps[a]=witness
        for q,out,y in fedges[x]:
            nxt=(d[si][q]*n+d[so][out])*nf+y
            if nxt not in ids:
                if len(states)>=cap:
                    unknown='UNKNOWN_state_cap'
                    break
                ids[nxt]=len(states)
                states.append(nxt)
                parents.append(index)
                letters.append(q)
        if unknown:
            break
        if index and index%100000==0:
            print(json.dumps(dict(progress_product_states=len(states),processed=index,
                                  class_edges=len(edges),seconds=time.monotonic()-start)),flush=True)
    result=dict(depth=depth,dfa_states=n,product_states=len(states),class_edges=len(edges),
                state_cap=cap,seconds_cap=seconds,seconds=time.monotonic()-start)
    if prefix:
        result['observer_refinement']=prefix.rstrip('_')
    dest=HERE/('kernel_%sdepth%d_extended.json'%(prefix,depth))
    if unknown:
        result['status']=unknown
        dest.write_text(json.dumps(result,indent=2)+'\n')
        return result

    del ids,states
    heads=array('i',[-1])*width
    sources=array('I')
    links=array('i')
    witnesses=array('I')
    for key,w in edges.items():
        a,b=divmod(key,width)
        assert reps[a]>=0 and reps[b]>=0
        sources.append(a)
        links.append(heads[b])
        witnesses.append(w)
        heads[b]=len(sources)-1
    del edges
    ranks=array('i',[-1])*width
    targets=array('i',[-1])*width
    chosen=array('i',[-1])*width
    order=array('I')
    for a,w in enumerate(reps):
        if w>=0 and f[a//11][a%11]&1:
            ranks[a]=0
            chosen[a]=w
            order.append(a)
    bad_count=len(order)
    for b in order:
        e=heads[b]
        while e>=0:
            a=sources[e]
            if ranks[a]<0:
                ranks[a]=ranks[b]+1
                chosen[a]=witnesses[e]
                targets[a]=b
                order.append(a)
            e=links[e]
    del heads,sources,links,witnesses
    live=[a for a,w in enumerate(reps) if w>=0 and ranks[a]<0]
    result.update(status='POSITIVE_CANDIDATE' if live else 'EMPTY_KERNEL',
                  classes=len(order)+len(live),initial_bad_classes=bad_count,
                  elimination_depth=max(ranks),live_class_count=len(live),
                  seconds=time.monotonic()-start)

    def word(w):
        index,cidx=divmod(w,11)
        ps=[]
        while parents[index]!=0xffffffff:
            ps.append(letters[index])
            index=parents[index]
        ps.reverse()
        return ps,CENTERS[cidx]

    if live:
        p,c=word(reps[live[0]])
        num=realize(p,c)
        result.update(seed=[p,c],representative=str(num),
                      proposed_lychrel_witness=str(num+int(str(num)[::-1])))
    # Streaming keeps the 828k-class proof from becoming 828k Python dicts.
    with dest.open('w') as fp:
        fp.write(json.dumps(result)[:-1])
        fp.write(',"live_classes":')
        json.dump(live,fp,separators=(',',':'))
        fp.write(',"eliminated":[')
        for pos,a in enumerate(order):
            if pos:
                fp.write(',')
            p,c=word(chosen[a])
            json.dump(dict(source=a,target=None if targets[a]<0 else targets[a],
                           rank=ranks[a],word=[p,c]),fp,separators=(',',':'))
        fp.write(']}\n')
    result['certificate_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
    result['seconds']=time.monotonic()-start
    (HERE/('kernel_%sdepth%d_extended_summary.json'%(prefix,depth))).write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--depth',type=int,default=4)
    p.add_argument('--cap',type=int,default=3000000)
    p.add_argument('--seconds',type=float,default=300)
    p.add_argument('--image1',action='store_true')
    args=p.parse_args()
    print(json.dumps(run(args.depth,args.cap,args.seconds,'image1_' if args.image1 else '')),flush=True)
