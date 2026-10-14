"""Context-two finite-language CEGIS with numerically checked unsafe proofs.
No solver timeout or graph cap is a nonexistence result.
"""
from pathlib import Path
import sys, json, time, signal, argparse, hashlib
from collections import deque, defaultdict
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'main_existence_attempt'/'invariant'))
sys.path.insert(0,str(ROOT/'research'))
import context_closure as cc
from persist_spacetime_weighted import FS, FE, OUT, TERMS
import z3
sys.set_int_max_str_digits(0)
ORDER=2
TERM_OUT=cc.TERM_OUT
FS_ID={s:i for i,s in enumerate(FS)}
FE_ID={e:i for i,e in enumerate(FE)}

class BudgetExpired(Exception):pass
class GraphUnknown(Exception):pass

def alarm_handler(*_):raise BudgetExpired()

def numeric_history(word):
    """Recover tile IDs from ordinary integer carries, with no guessed paths."""
    p,c=word;p=tuple(p)
    assert (p and 1<=p[0]<=18) or (not p and c in range(2,19,2))
    assert all(0<=x<=18 for x in p)
    assert c is None or c in range(0,19,2)
    q=p+(() if c is None else (c,))+p[::-1];L=len(q)
    carries=[0];digits=[]
    for x in q:
        ca,d=divmod(x+carries[-1],10);carries.append(ca);digits.append(d)
    h=carries[-1];path=[]
    for i,x in enumerate(p):
        delay=(1 if i==0 else digits[L-i]) if h else -1
        u=FS_ID[h,carries[i],carries[L-i],delay,i>0]
        v=FS_ID[h,carries[i+1],carries[L-i-1],digits[L-i-1] if h else -1,True]
        o=digits[i]+(delay if h else digits[L-i-1])
        path.append(FE_ID[u,x,o,v])
    i=len(p);delay=(1 if i==0 else digits[L-i]) if h else -1
    u=FS_ID[h,carries[i],carries[L-i],delay,i>0]
    path.append(TERMS[u,c][2])
    return path

def feats(path):
    prev=-1;out=set()
    for k in path:out.add((prev,k));prev=k
    return out

def word_features(word):return feats(numeric_history(word))

def realize(word):
    p,c=word;p=tuple(p);L=2*len(p)+(c is not None);ds=[0]*L
    for i,x in enumerate(p):ds[i]=max(0,x-9);ds[L-i-1]=min(9,x)
    if c is not None:ds[len(p)]=c//2
    assert ds and ds[-1]>0
    return int(''.join(map(str,ds[::-1])))

def numeric_step(word):
    n=realize(word);s=n+int(str(n)[::-1]);ds=tuple(map(int,str(s)))
    q=tuple(a+b for a,b in zip(ds,ds[::-1]));m=len(q)//2
    return (q[:m],q[m] if len(q)%2 else None)

def numeric_bad_after_two(word):
    n=realize(word)
    for _ in range(2):n+=int(str(n)[::-1])
    return str(n)==str(n)[::-1]

def space():
    nodes=[(0,-1),(1,-1)]+[(v,k) for k,(u,q,o,v) in enumerate(FE)]
    index={s:i for i,s in enumerate(nodes)};edges=[];terms=[];features=set()
    for u,(x,last) in enumerate(nodes):
        for q,o,y,k in OUT[x]:
            f=(last,k);features.add(f);edges.append((u,index[y,k],f,k))
        for c,extra,oc,k in TERM_OUT[x]:
            f=(last,k);features.add(f);terms.append((u,f,k,c))
    features=sorted(features);fi={f:i for i,f in enumerate(features)}
    return nodes,edges,terms,features,fi

NODES,EDGES,TERMINALS,FEATURES,FI=space()
assert len(NODES)==874 and len(FE)==872 and len(FEATURES)==21409

def nonempty():
    solver=z3.Solver();solver.set(random_seed=196)
    a=[z3.Bool('a'+str(i)) for i in range(len(FEATURES))]
    witness=[z3.Bool('w'+str(i)) for i in range(len(NODES))]
    ranks=[z3.BitVec('r'+str(i),10) for i in range(len(NODES))]
    solver.add(witness[0],witness[1],ranks[0]==0,ranks[1]==0)
    incoming=[[] for _ in NODES]
    for u,v,f,k in EDGES:
        incoming[v].append(z3.And(witness[u],a[FI[f]],z3.ULT(ranks[u],ranks[v])))
    for i in range(2,len(NODES)):
        solver.add(z3.Implies(witness[i],z3.Or(incoming[i])))
    solver.add(z3.Or([z3.And(witness[u],a[FI[f]]) for u,f,k,c in TERMINALS]))
    return solver,a

def accepted_word(allowed):
    outgoing=defaultdict(list);terms=defaultdict(list)
    for u,v,f,k in EDGES:
        if f in allowed:outgoing[u].append((v,k))
    for u,f,k,c in TERMINALS:
        if f in allowed:terms[u].append((k,c))
    path={0:(),1:()};todo=deque(path)
    while todo:
        u=todo.popleft()
        if terms[u]:
            k,c=terms[u][0];word=(tuple(FE[j][1] for j in path[u]),c)
            initial=feats(path[u]+(k,))
            assert initial==word_features(word) and initial<=allowed
            return word,initial
        for v,k in outgoing[u]:
            if v not in path:path[v]=path[u]+(k,);todo.append(v)
    raise AssertionError('nonemptiness model has no accepted word')

def closure_features(initial,cap,deadline):
    allowed=set(initial);sizes=[];max_graph=0
    while time.monotonic()<deadline:
        sizes.append(len(allowed))
        safe,n=cc.safety(allowed,ORDER,cap);max_graph=max(max_graph,n)
        if safe is False:return 'unsafe',allowed,sizes,max_graph
        if safe is None:return 'unknown',allowed,sizes,max_graph
        fs,n=cc.image_features(allowed,ORDER,cap);max_graph=max(max_graph,n)
        if fs is None:return 'unknown',allowed,sizes,max_graph
        assert fs<=FI.keys()
        new=allowed|fs
        if new==allowed:return 'candidate',allowed,sizes,max_graph
        allowed=new
    return 'unknown',allowed,sizes,max_graph

def safety_witness(allowed,cap):
    starts=[(x,-1,(True,True,False)) for x in (0,1)]
    paths={s:() for s in starts};todo=deque(starts)
    while todo:
        x,last,flags=st=todo.popleft()
        for c,extra,oc,k in TERM_OUT[x]:
            if (last,k) not in allowed:continue
            ff=flags if extra is None else cc.advance(flags,extra)
            if cc.terminal_bad(ff,oc):
                word=(tuple(FE[j][1] for j in paths[st]),c)
                assert word_features(word)<=allowed and numeric_bad_after_two(word)
                return word
        for q,o,y,k in OUT[x]:
            if (last,k) not in allowed:continue
            ff=cc.advance(flags,o)
            if not(ff[0] or ff[1]):continue
            target=(y,k,ff)
            if target not in paths:
                if len(paths)>=cap:raise GraphUnknown('proof safety cap')
                paths[target]=paths[st]+(k,);todo.append(target)
    return None

def image_witnesses(allowed,cap):
    """Find finite input witnesses for every added image feature."""
    states=[(x,y,-1,-1) for x in (0,1) for y in (0,1)]
    ids={s:i for i,s in enumerate(states)};parents={i:None for i in range(4)}
    edges=[];reverse=defaultdict(list);terms=[]
    for u,(x,y,la,lb) in enumerate(states):
        for c,extra,oc,a in TERM_OUT[x]:
            if (la,a) not in allowed:continue
            if extra is None:
                if (y,oc) in TERMS:
                    b=TERMS[y,oc][2];terms.append((u,c,((lb,b),)))
            else:
                for q2,o2,yy,b in OUT[y]:
                    if q2==extra and (yy,oc) in TERMS:
                        bb=TERMS[yy,oc][2];terms.append((u,c,((lb,b),(b,bb))))
        for q,o,xx,a in OUT[x]:
            if (la,a) not in allowed:continue
            for q2,o2,yy,b in OUT[y]:
                if q2!=o:continue
                st=(xx,yy,a,b)
                if st not in ids:
                    if len(states)>=cap:raise GraphUnknown('proof image cap')
                    ids[st]=len(states);states.append(st);parents[ids[st]]=(u,a)
                v=ids[st];ei=len(edges);edges.append((u,v,a,(lb,b)));reverse[v].append(ei)
    finish={};todo=deque()
    for ti,(u,c,fs) in enumerate(terms):
        if u not in finish:finish[u]=('terminal',ti);todo.append(u)
    while todo:
        v=todo.popleft()
        for ei in reverse[v]:
            u=edges[ei][0]
            if u not in finish:finish[u]=('edge',ei);todo.append(u)
    sources={}
    for ei,(u,v,a,f) in enumerate(edges):
        if v in finish and f not in allowed:sources.setdefault(f,('edge',ei))
    for ti,(u,c,fs) in enumerate(terms):
        for f in fs:
            if f not in allowed:sources.setdefault(f,('terminal',ti))
    def prefix(u):
        out=[]
        while parents[u] is not None:u,a=parents[u];out.append(a)
        return out[::-1]
    words=set()
    for f,(kind,j) in sources.items():
        if kind=='terminal':
            u,c,fs=terms[j];p=prefix(u)
        else:
            u,v,a,ff=edges[j];p=prefix(u)+[a]
            while finish[v][0]=='edge':
                _,ei=finish[v];uu,v,aa,ff=edges[ei];p.append(aa)
            _,ti=finish[v];uu,c,fs=terms[ti]
        word=(tuple(FE[k][1] for k in p),c)
        assert word_features(word)<=allowed
        output=numeric_step(word)
        assert f in word_features(output)
        words.add(word)
    added=set()
    for word in words:added.update(word_features(numeric_step(word)))
    assert added-allowed==set(sources)
    return sorted(words,key=repr),added

def derive_unsafe(initial,cap,deadline):
    allowed=set(initial);rounds=[]
    while time.monotonic()<deadline:
        bad=safety_witness(allowed,cap)
        if bad is not None:return dict(initial=sorted(initial),rounds=rounds,bad_word=bad)
        words,added=image_witnesses(allowed,cap)
        if added<=allowed:raise AssertionError('unsafe core has a safe fixed point')
        rounds.append(words);allowed.update(added)
    raise BudgetExpired()

def verify_derivation(proof):
    """No reachability search: check every concrete derivation numerically."""
    allowed={tuple(f) for f in proof['initial']}
    for words in proof['rounds']:
        added=set()
        for word in words:
            assert word_features(word)<=allowed
            added.update(word_features(numeric_step(word)))
        assert added-allowed
        allowed.update(added)
    bad=proof['bad_word']
    assert word_features(bad)<=allowed
    assert numeric_bad_after_two(bad)
    return True

def run(seconds=180,cap=100000):
    setup_start=time.monotonic();solver,a=nonempty();setup=time.monotonic()-setup_start
    start=time.monotonic();deadline=start+seconds;records=[];seen=set();attempts=0;unknowns=0
    result=dict(status='unknown',reason='wall-clock budget',context=2,features=len(FEATURES),nonempty_nodes=len(NODES),rank_bits=10,graph_cap=cap,setup_seconds=setup,search_budget_seconds=seconds)
    signal.signal(signal.SIGALRM,alarm_handler);signal.setitimer(signal.ITIMER_REAL,seconds)
    try:
        while time.monotonic()<deadline:
            solver.set(timeout=max(1,int(1000*(deadline-time.monotonic()))))
            status=solver.check()
            if status!=z3.sat:
                result.update(status='unknown' if status==z3.unknown else 'solver_unsat_template',reason=solver.reason_unknown() if status==z3.unknown else 'finite Boolean template exhausted by verified unsafe-core clauses')
                break
            attempts+=1;model=solver.model()
            allowed={FEATURES[i] for i,x in enumerate(a) if z3.is_true(model.eval(x,model_completion=True))}
            word,initial=accepted_word(allowed)
            status,fixed,sizes,max_graph=closure_features(initial,cap,deadline)
            if status=='candidate':
                result.update(status='candidate',reason=None,word=word,allowed_features=sorted(fixed),closure_sizes=sizes,max_graph=max_graph)
                break
            if status=='unknown':
                unknowns+=1;result.update(reason='exact closure graph cap or time limit',last_word=word,last_sizes=sizes,max_graph=max_graph)
                break
            core=sorted(initial)
            for f in tuple(core):
                small=[g for g in core if g!=f]
                status,_,_,_=closure_features(small,cap,deadline)
                if status=='unsafe':core=small
                elif status=='unknown':unknowns+=1
            key=tuple(core)
            assert key and key not in seen
            proof=derive_unsafe(core,cap,deadline)
            assert verify_derivation(proof)
            # No mutation of the solver or retained clauses precedes validation.
            solver.add(z3.Or([z3.Not(a[FI[f]]) for f in core]))
            seen.add(key);records.append(proof)
            if len(records)%25==0:
                print(json.dumps(dict(learned=len(records),attempts=attempts,last_core=len(core),last_word=word,seconds=time.monotonic()-start)),flush=True)
    except BudgetExpired:
        result.update(status='unknown',reason='wall-clock budget')
    except GraphUnknown as e:
        result.update(status='unknown',reason=str(e));unknowns+=1
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
    result.update(search_seconds=time.monotonic()-start,attempts=attempts,validated_clauses=len(records),unknown_checks=unknowns,infinite_existence_proved=False)
    return result,records

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=180);p.add_argument('--cap',type=int,default=100000);p.add_argument('--verify',type=Path);args=p.parse_args()
    if args.verify:
        records=json.loads(args.verify.read_text())
        for proof in records:verify_derivation(proof)
        print(json.dumps(dict(verified=len(records),status='all concrete unsafe derivations checked numerically')))
    else:
        result,records=run(args.seconds,args.cap)
        directory=Path(__file__).resolve().parent
        suffix='180' if args.seconds==180 else str(args.seconds).replace('.','_')
        proofpath=directory/f'unsafe_derivations_{suffix}.json'
        proofpath.write_text(json.dumps(records,separators=(',',':'))+'\n')
        result['derivations_file']=proofpath.name
        result['derivations_sha256']=hashlib.sha256(proofpath.read_bytes()).hexdigest()
        (directory/f'result_{suffix}.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2),flush=True)
