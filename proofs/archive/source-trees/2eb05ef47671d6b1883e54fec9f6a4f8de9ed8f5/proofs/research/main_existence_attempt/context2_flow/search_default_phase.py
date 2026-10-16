"""Rank-free context-two CEGIS with checked finite unsafe derivations.

Flow variables select a simple accepted seed path, plus harmless disconnected
cycles. This restriction is complete for nonempty closed context-two languages.
"""
from pathlib import Path
import importlib.util, sys, json, time, signal, argparse, hashlib
from collections import defaultdict
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'context2_cegis'/'search.py'
spec=importlib.util.spec_from_file_location('context2_checked',OLD)
B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
z3=B.z3


def nonempty_flow():
    solver=z3.SolverFor('QF_FD');solver.set(random_seed=196)
    a=[z3.Bool('a'+str(i)) for i in range(len(B.FEATURES))]
    incoming=[[] for _ in B.NODES];outgoing=[[] for _ in B.NODES];terminal=[]
    uses=defaultdict(int)
    for u,v,f,k in B.EDGES:
        x=a[B.FI[f]];outgoing[u].append(x);incoming[v].append(x);uses[f]+=1
    for u,f,k,c in B.TERMINALS:
        x=a[B.FI[f]];outgoing[u].append(x);terminal.append(x);uses[f]+=1
    assert len(uses)==len(B.FEATURES) and all(n==1 for n in uses.values())
    assert not incoming[0] and not incoming[1]
    solver.add(z3.PbEq([(x,1) for x in outgoing[0]+outgoing[1]],1))
    solver.add(z3.PbEq([(x,1) for x in terminal],1))
    for i in range(2,len(B.NODES)):
        solver.add(z3.AtMost(*incoming[i],1))
        solver.add(z3.AtMost(*outgoing[i],1))
        solver.add(z3.Or(incoming[i])==z3.Or(outgoing[i]))
    return solver,a


PATH_OUT=[[] for _ in B.NODES]
for u,v,f,k in B.EDGES:PATH_OUT[u].append((B.FI[f],v,k,None))
for u,f,k,c in B.TERMINALS:PATH_OUT[u].append((B.FI[f],None,k,c))


def extract_flow_path(model,a):
    """Read only the unique start component; disconnected cycles are irrelevant."""
    starts=[(u,edge) for u in (0,1) for edge in PATH_OUT[u]
            if z3.is_true(model.eval(a[edge[0]],model_completion=True))]
    assert len(starts)==1
    u,edge=starts[0];visited={u};pairs=[];path=[];features=set()
    while True:
        fi,v,k,c=edge;features.add(B.FEATURES[fi]);path.append(k)
        if v is None:
            word=(tuple(pairs),c)
            assert features==B.word_features(word)
            assert len(features)==len(path)<=len(B.NODES)
            return word,features
        assert v not in visited, 'start path entered a cycle despite flow constraints'
        visited.add(v);pairs.append(B.FE[k][1]);u=v
        selected=[e for e in PATH_OUT[u] if z3.is_true(model.eval(a[e[0]],model_completion=True))]
        assert len(selected)==1
        edge=selected[0]


def load_proofs(paths):
    proofs=[];seen=set()
    for path in paths:
        for proof in json.loads(Path(path).read_text()):
            B.verify_derivation(proof)
            key=tuple(sorted(tuple(f) for f in proof['initial']))
            if key not in seen:seen.add(key);proofs.append(proof)
    return proofs


def trim_derivation(proof):
    """Retain only concrete witnesses on a dependency path to the bad word."""
    owner={tuple(f):None for f in proof['initial']};words={};requirements={}
    for r,row in enumerate(proof['rounds']):
        previous=set(owner)
        for j,word in enumerate(row):
            key=(r,j);inputs=B.word_features(word)
            assert inputs<=previous
            words[key]=word;requirements[key]=inputs
            for f in B.word_features(B.numeric_step(word)):owner.setdefault(f,key)
    required=list(B.word_features(proof['bad_word']));used=set();seen=set()
    while required:
        f=required.pop()
        if f in seen:continue
        seen.add(f);key=owner[f]
        if key is not None and key not in used:
            used.add(key);required.extend(requirements[key])
    rows=[]
    for r in range(len(proof['rounds'])):
        row=[words[key] for key in sorted(used) if key[0]==r]
        if row:rows.append(row)
    result=dict(initial=proof['initial'],rounds=rows,bad_word=proof['bad_word'])
    assert B.verify_derivation(result)
    return result


def run(seconds=600,cap=100000,resume=(),prefix='run'):
    setup_start=time.monotonic();records=load_proofs(resume);solver,a=nonempty_flow()
    seen=set()
    for proof in records:
        core=tuple(sorted(tuple(f) for f in proof['initial']));seen.add(core)
        solver.add(z3.Or([z3.Not(a[B.FI[f]]) for f in core]))
    setup=time.monotonic()-setup_start;retained=len(records)
    start=time.monotonic();deadline=start+seconds;attempts=0;unknowns=0
    timings=defaultdict(float);model_seconds=[];max_graph_seen=0;last_stage='start';last_word=None
    result=dict(status='unknown',reason='wall-clock budget',encoding='rank-free path flow',context=2,features=len(B.FEATURES),nonempty_nodes=len(B.NODES),graph_cap=cap,setup_seconds=setup,search_budget_seconds=seconds,resumed_verified_clauses=retained)
    signal.signal(signal.SIGALRM,B.alarm_handler);signal.setitimer(signal.ITIMER_REAL,seconds)
    try:
        while time.monotonic()<deadline:
            last_stage='SMT nonemptiness';t=time.monotonic()
            solver.set(timeout=max(1,int(1000*(deadline-t))))
            status=solver.check();dt=time.monotonic()-t;timings['solver']+=dt;model_seconds.append(dt)
            if status!=z3.sat:
                result.update(status='unknown' if status==z3.unknown else 'solver_unsat_template',reason=solver.reason_unknown() if status==z3.unknown else 'path template exhausted by numerically verified unsafe-core clauses')
                break
            attempts+=1;last_stage='model extraction';t=time.monotonic();model=solver.model()
            word,initial=extract_flow_path(model,a);last_word=word
            timings['model_extraction']+=time.monotonic()-t
            last_stage='exact least closure';t=time.monotonic()
            status,fixed,sizes,max_graph=B.closure_features(initial,cap,deadline)
            timings['closure']+=time.monotonic()-t;max_graph_seen=max(max_graph_seen,max_graph)
            if status=='candidate':
                result.update(status='candidate',reason=None,word=word,allowed_features=sorted(fixed),closure_sizes=sizes,max_graph=max_graph)
                break
            if status=='unknown':
                unknowns+=1;result.update(reason='exact closure graph cap or time limit',last_word=word,last_sizes=sizes,max_graph=max_graph)
                break
            # This initial feature set is exactly one simple accepted path.
            # Every proper subset accepts no word, so reduction cannot shrink it.
            core=sorted(initial)
            key=tuple(core);assert key and key not in seen
            last_stage='concrete unsafe derivation';t=time.monotonic()
            proof=B.derive_unsafe(core,cap,deadline);proof=trim_derivation(proof)
            assert B.verify_derivation(proof)
            timings['proof_generation_and_checks']+=time.monotonic()-t
            last_stage='learn validated clause';t=time.monotonic()
            solver.add(z3.Or([z3.Not(a[B.FI[f]]) for f in core]));seen.add(key);records.append(proof)
            timings['clause_addition']+=time.monotonic()-t
            if (len(records)-retained)%25==0 or attempts<=3:
                print(json.dumps(dict(learned=len(records)-retained,total_verified=len(records),attempts=attempts,last_core=len(core),last_pairs=len(word[0]),seconds=time.monotonic()-start,last_solver_seconds=dt)),flush=True)
    except B.BudgetExpired:
        result.update(status='unknown',reason='wall-clock budget')
    except B.GraphUnknown as e:
        result.update(status='unknown',reason=str(e));unknowns+=1
    finally:signal.setitimer(signal.ITIMER_REAL,0)
    result.update(search_seconds=time.monotonic()-start,attempts=attempts,validated_clauses=len(records),new_verified_clauses=len(records)-retained,unknown_checks=unknowns,max_graph_seen=max_graph_seen,last_stage=last_stage,last_word=last_word,timings=dict(timings),solver_checks_completed=len(model_seconds),first_model_seconds=model_seconds[0] if model_seconds else None,max_completed_solver_seconds=max(model_seconds,default=None),infinite_existence_proved=False)
    proofpath=HERE/f'{prefix}_unsafe_derivations.json'
    proofpath.write_text(json.dumps(records,separators=(',',':'))+'\n')
    result.update(derivations_file=proofpath.name,derivations_sha256=hashlib.sha256(proofpath.read_bytes()).hexdigest())
    (HERE/f'{prefix}_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=600);ap.add_argument('--cap',type=int,default=100000);ap.add_argument('--resume',type=Path,action='append',default=[]);ap.add_argument('--prefix',default='run600');ap.add_argument('--verify',type=Path);args=ap.parse_args()
    if args.verify:
        proofs=load_proofs([args.verify]);print(json.dumps(dict(verified=len(proofs),status='all concrete unsafe derivations checked numerically')))
    else:run(args.seconds,args.cap,args.resume,args.prefix)
