"""Unbounded-word nonemptiness + exact least-closure counterexamples.

The 46 transducer states bound the length of a shortest accepted word, not
the length of a reverse-and-add orbit or the words the language certifies.
Learned clauses forbid tile sets whose least closed language is unsafe.
"""
from collections import deque
import json, time, z3, argparse
from tile_closure import closure_tiles
from persist_spacetime_weighted import FS, FE, TERMS, NW


def nonempty():
    s = z3.Solver()
    a = [z3.Bool(f'a{i}') for i in range(NW)]
    w = [z3.Bool(f'w{i}') for i in range(len(FS))]
    rank = [z3.BitVec(f'r{i}',6) for i in range(len(FS))]
    s.add(w[0], w[1], rank[0] == 0, rank[1] == 0)
    inc = [[] for _ in FS]
    for k,(u,q,o,v) in enumerate(FE):
        inc[v].append(z3.And(w[u],a[k],z3.ULT(rank[u],rank[v])))
    for i in range(2,len(FS)):
        s.add(z3.Implies(w[i],z3.Or(inc[i])))
    s.add(z3.Or([z3.And(w[x],a[k]) for (x,c),(extra,oc,k) in TERMS.items()]))
    return s,a


def accepted_path(allowed):
    outgoing = [[] for _ in FS]
    for k,(u,q,o,v) in enumerate(FE):
        if k in allowed:
            outgoing[u].append((v,k))
    terms = {}
    for (u,c),(x,oc,k) in TERMS.items():
        if k in allowed:
            terms[u] = (k,c)
    paths = {0:[],1:[]}
    todo = deque(paths)
    while todo:
        u = todo.popleft()
        if u in terms:
            k,c = terms[u]
            p = paths[u]+[k]
            return p, ([FE[k][1] for k in paths[u]],c)
        for v,k in outgoing[u]:
            if v not in paths:
                paths[v] = paths[u]+[k]
                todo.append(v)
    raise AssertionError('ranked model has no accepted path')


def run(seconds=600):
    s,a = nonempty()
    start=time.monotonic();count=0;clauses=[];seen=set()
    while time.monotonic()-start < seconds:
        s.set(timeout=max(1,int(1000*(seconds-(time.monotonic()-start)))))
        status=s.check()
        if status!=z3.sat:
            return dict(status=str(status),seconds=time.monotonic()-start,clauses=clauses,
                        reason=s.reason_unknown() if status==z3.unknown else None)
        model=s.model()
        allowed={k for k,x in enumerate(a) if z3.is_true(model.eval(x,model_completion=True))}
        path,word=accepted_path(allowed)
        good,fixed,sizes=closure_tiles(path)
        if good:
            return dict(status='candidate',word=word,allowed_tiles=sorted(fixed),seed_tiles=path,
                        closure_sizes=sizes,seconds=time.monotonic()-start,learned=len(clauses))
        # Greedy deletion is sufficient: every retained clause is validated by
        # a fresh exact graph closure, whether or not it is a minimum core.
        core=sorted(set(path))
        for k in list(core):
            small=[j for j in core if j!=k]
            if not closure_tiles(small)[0]:
                core=small
        assert core
        key=tuple(core)
        assert key not in seen
        seen.add(key);clauses.append(core)
        s.add(z3.Or([z3.Not(a[k]) for k in core]))
        count+=1
        if count%100==0:
            print(json.dumps(dict(learned=count,last_core=len(core),last_word=word,
                                  seconds=time.monotonic()-start)),flush=True)
    return dict(status='unknown',reason='wall-clock budget',seconds=time.monotonic()-start,clauses=clauses)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=600);args=p.parse_args()
    out=run(args.seconds)
    from pathlib import Path
    path=Path(__file__).with_name('grammar_cegis_result.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='clauses'},indent=2),flush=True)
