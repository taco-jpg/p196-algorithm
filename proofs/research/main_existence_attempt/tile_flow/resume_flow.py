"""Resume exact carry-tile invariant synthesis using rank-free path flow.

Selected tiles encode a finite accepting path, possibly with disconnected
cycles. Initial states have no incoming edges. Noninitial states have at most
one selected incoming edge and at most one selected outgoing edge/terminal;
incoming exists iff outgoing/terminal exists. Exactly one initial departure
and one terminal are selected. The initial walk cannot enter a cycle: its
first repeated vertex would have two selected incoming edges. Thus a finite
accepting path exists. Conversely every nonempty allowed-tile language has
a simple accepting path and therefore satisfies this selection encoding.

Learned clauses constrain path-tile subsets, not the final allowed language.
Every clause is justified by exact all-length least closure becoming unsafe.
"""
from collections import deque
from pathlib import Path
import argparse, hashlib, json, sys, time
import z3

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'main_existence_attempt' / 'invariant'))
from tile_closure import closure_tiles
from grammar_cegis import accepted_path
from persist_spacetime_weighted import FS, FE, TS, TERMS, NW, history_path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, obj):
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(obj, indent=2)+'\n')
    temp.replace(path)


def replay_prior(path):
    start=time.monotonic()
    prior=json.loads(path.read_text())
    clauses=prior['clauses'];seen=set();max_rounds=0;max_tiles=0
    for i,core in enumerate(clauses):
        assert core and len(core)==len(set(core))
        assert all(isinstance(k,int) and 0<=k<NW for k in core)
        key=tuple(sorted(core));assert key not in seen;seen.add(key)
        good,allowed,sizes=closure_tiles(core)
        max_rounds=max(max_rounds,len(sizes)-1);max_tiles=max(max_tiles,len(allowed))
        if good:
            audit=dict(status='replay_failure',index=i,core=core,source=str(path),source_sha256=digest(path))
            save_json(HERE/'prior_replay.json',audit)
            raise AssertionError(audit)
        if (i+1)%8000==0:
            print(json.dumps(dict(stage='prior_replay',checked=i+1,seconds=time.monotonic()-start)),flush=True)
    audit=dict(status='all_unsafe_clauses_replayed',clauses=len(clauses),seconds=time.monotonic()-start,
               max_closure_rounds=max_rounds,max_closure_tiles=max_tiles,source=str(path),
               source_sha256=digest(path),closure_source_sha256=digest(ROOT/'main_existence_attempt/invariant/tile_closure.py'))
    save_json(HERE/'prior_replay.json',audit)
    print(json.dumps(audit),flush=True)
    return [list(c) for c in clauses],seen,audit


def flow_solver():
    solver=z3.SolverFor('QF_FD')
    selected=[z3.Bool(f'tile_{k}') for k in range(NW)]
    incoming=[[] for _ in FS];outgoing=[[] for _ in FS]
    for k,(u,q,o,v) in enumerate(FE):
        assert v not in (0,1)
        incoming[v].append(selected[k]);outgoing[u].append(selected[k])
    terminals=[]
    for (u,c),(extra,oc,k) in TERMS.items():
        outgoing[u].append(selected[k]);terminals.append(selected[k])
    solver.add(z3.PbEq([(a,1) for a in outgoing[0]+outgoing[1]],1))
    solver.add(z3.PbEq([(a,1) for a in terminals],1))
    for v in range(2,len(FS)):
        if len(incoming[v])>1:solver.add(z3.AtMost(*incoming[v],1))
        if len(outgoing[v])>1:solver.add(z3.AtMost(*outgoing[v],1))
        solver.add(z3.Or(incoming[v])==z3.Or(outgoing[v]))
    return solver,selected


def numeric_seed(word):
    p,c=word
    ds=[max(q-9,0) for q in p]+([] if c is None else [c//2])+[min(q,9) for q in p[::-1]]
    assert ds and ds[-1]>0 and all(0<=d<=9 for d in ds)
    n=sum(d*10**i for i,d in enumerate(ds))
    expected=list(p)+([] if c is None else [c])+list(p[::-1])
    assert [ds[i]+ds[-1-i] for i in range(len(ds))]==expected
    n1=n+int(str(n)[::-1]);n2=n1+int(str(n1)[::-1])
    return dict(realization=str(n),first_step=str(n1),lychrel_candidate=str(n2),
                candidate_nonpalindromic=(str(n2)!=str(n2)[::-1]),witness_shift=2)


def run(prior_path,seconds):
    clauses,seen,audit=replay_prior(prior_path)
    old_count=len(clauses)
    solver,selected=flow_solver()
    for core in clauses:
        solver.add(z3.Or([z3.Not(selected[k]) for k in core]))
    print(json.dumps(dict(stage='flow_ready',states=len(FS),tiles=NW,loaded_clauses=old_count)),flush=True)
    start=time.monotonic();last_save=start;new_count=0;oracle_calls=0;longest_path=0
    def state(status,**extra):
        return dict(status=status,encoding='rank_free_boolean_path_flow',solver='Z3 QF_FD',
                    prior_clauses=old_count,new_clauses=new_count,total_clauses=len(clauses),
                    seconds=time.monotonic()-start,oracle_calls=oracle_calls,
                    longest_witness_edges=longest_path,clauses=clauses,**extra)
    while time.monotonic()-start<seconds:
        solver.set(timeout=max(1,int(1000*(seconds-(time.monotonic()-start)))))
        status=solver.check()
        if status!=z3.sat:
            return state(str(status),reason=solver.reason_unknown() if status==z3.unknown else None)
        model=solver.model()
        choices={k for k,a in enumerate(selected) if z3.is_true(model.eval(a,model_completion=True))}
        path,word=accepted_path(choices)
        assert len(path)==len(set(path))
        assert path==history_path((tuple(word[0]),word[1]))
        longest_path=max(longest_path,len(path)-1)
        good,fixed,sizes=closure_tiles(path);oracle_calls+=1
        if good:
            seed=numeric_seed(word)
            assert seed['candidate_nonpalindromic']
            return state('candidate',word=word,seed_tiles=path,allowed_tiles=sorted(fixed),
                         closure_sizes=sizes,numeric_seed=seed)
        core=sorted(set(path))
        for k in list(core):
            small=[j for j in core if j!=k]
            bad=not closure_tiles(small)[0];oracle_calls+=1
            if bad:core=small
        assert core
        key=tuple(core);assert key not in seen
        seen.add(key);clauses.append(core);new_count+=1
        solver.add(z3.Or([z3.Not(selected[k]) for k in core]))
        if new_count%1000==0:
            print(json.dumps(dict(stage='flow_search',new_clauses=new_count,total_clauses=len(clauses),
                                  seconds=time.monotonic()-start,last_core_size=len(core),longest_witness_edges=longest_path)),flush=True)
        if time.monotonic()-last_save>=30:
            save_json(HERE/'flow_checkpoint.json',state('running'))
            last_save=time.monotonic()
    return state('unknown',reason='wall-clock budget')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=600)
    p.add_argument('--prior',type=Path,default=ROOT/'main_existence_attempt/invariant/grammar_cegis_result.json')
    args=p.parse_args()
    out=run(args.prior,args.seconds)
    save_json(HERE/'flow_result.json',out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('clauses','allowed_tiles')},indent=2),flush=True)
