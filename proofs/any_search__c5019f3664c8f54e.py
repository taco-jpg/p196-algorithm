"""Exact any-seed nonemptiness for a bounded conditional integer score.

Weights in {-1,0,1}, offset in [-2,2]. Unknown walk multiplicities remain
unbounded; their products with weights are finite QF_LIA case splits.
"""
from pathlib import Path
import sys,time,json
import importlib.util
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parent))
from search import m,r,z3,make_solver,samples,evaluate,verify_safety,expression,check,score
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('threshold_positive_path',HERE.parent/'weighted_positive'/'search.py')
path_detector=importlib.util.module_from_spec(spec);spec.loader.exec_module(path_detector)

def nonempty(s,w,b):
    source=len(m.FS);sink=source+1;n=sink+1
    edges=[(source,j,None,'start',None) for j in (0,1)]
    edges += [(u,v,k,'pair',q) for k,(u,q,o,v) in enumerate(m.FE)]
    edges += [(u,sink,k,'terminal',center) for (u,center),(_,_,k) in m.TERMS.items()]
    count=[z3.Int('witness_count_%d'%j) for j in range(len(edges))]
    rank=[z3.Int('witness_rank_%d'%j) for j in range(n)]
    incoming=[[] for _ in range(n)];outgoing=[[] for _ in range(n)]
    for j,(u,v,*_) in enumerate(edges):
        incoming[v].append(j);outgoing[u].append(j);s.add(count[j]>=0)
    s.add(rank[source]==0)
    for v in range(n):
        s.add(rank[v]>=0,rank[v]<n)
        s.add(z3.Sum([count[j] for j in outgoing[v]])-
              z3.Sum([count[j] for j in incoming[v]])==
              (1 if v==source else -1 if v==sink else 0))
        if v!=source:
            activity=z3.Or([count[j]>0 for j in incoming[v]+outgoing[v]])
            parent=z3.Or([z3.And(count[j]>0,rank[edges[j][0]]<rank[v]) for j in incoming[v]])
            s.add(z3.Implies(activity,parent))
    total=b+z3.Sum([z3.If(w[k]==-1,-count[j],z3.If(w[k]==1,count[j],0))
                    for j,(u,v,k,kind,label) in enumerate(edges) if k is not None])
    s.add(total>=1)
    return source,sink,edges,count,outgoing

def word_from_model(model,graph):
    source,sink,edges,count,outgoing=graph
    mult=[model.eval(x).as_long() for x in count]
    total=sum(mult)
    if total>100000:return None
    adj=[[j for j in es if mult[j]] for es in outgoing]
    stack=[(source,None)];reverse=[]
    while stack:
        u=stack[-1][0]
        while adj[u] and mult[adj[u][-1]]==0:adj[u].pop()
        if adj[u]:
            j=adj[u][-1];mult[j]-=1;stack.append((edges[j][1],j))
        else:
            _,j=stack.pop()
            if j is not None:reverse.append(j)
    trail=reverse[::-1];assert len(trail)==total and not any(mult)
    current=source;pairs=[];center=None;ended=False
    for j in trail:
        u,v,k,kind,label=edges[j];assert u==current and not ended;current=v
        if kind=='pair':pairs.append(label)
        if kind=='terminal':center=label;ended=True
    assert ended and current==sink
    return tuple(pairs),center

def main(seconds=120):
    start=time.monotonic();s,w,b,p,safety=make_solver(None,1,2,0)
    witness_graph=nonempty(s,w,b);data=samples(3)
    known_negative=[]
    for word,features,_ in samples(2):
        current=word
        for step in range(80):
            nxt=r.qstep(current)
            if r.bad(nxt):
                s.add(expression(w,b,word)<=0)
                known_negative.append(dict(word=word,bad_output_after=step+1))
                break
            current=nxt
    (HERE/'short_word_negative_paths.json').write_text(json.dumps(known_negative,indent=2))
    doc=dict(scope='all1123 raw weights in{-1,0,1};offset in[-2,2];any finite accepted seed',
             known_negative_words=len(known_negative),history=[],status='NO_CERTIFICATE')
    for iteration in range(300):
        remaining=seconds-(time.monotonic()-start)
        if remaining<1:break
        s.set(timeout=int(1000*min(20,remaining)));status=s.check()
        rec=dict(iteration=iteration,synthesis=str(status),elapsed=time.monotonic()-start)
        doc['history'].append(rec)
        if status!=z3.sat:
            if status==z3.unknown:rec['reason']=s.reason_unknown()
            if status==z3.unsat:(HERE/'any_bound1_unsat.smt2').write_text(s.to_smt2())
            print(json.dumps(rec),flush=True);break
        model=s.model();ww=[model.eval(x).as_long() for x in w];bb=model.eval(b).as_long();pp=[model.eval(x).as_long() for x in p]
        verify_safety(ww,bb,pp,safety)
        shifted=[Fraction(x) for x in ww]
        for j in range(len(m.FE),m.NW):shifted[j]+=bb
        positive=path_detector.positive_word(shifted)
        assert positive is not None and 'word' in positive
        seed=positive['word']
        assert r.valid(seed) and score(ww,bb,seed)>=1
        rec.update(seed=seed,seed_score=score(ww,bb,seed),offset=bb,nonzero_tiles=sum(bool(x) for x in ww))
        bad=[i for i,(_,a,c) in enumerate(data) if evaluate(ww,bb,a)>0 and evaluate(ww,bb,c)<=0]
        rec['finite_counterexamples']=len(bad)
        if bad:
            count=min(128,len(bad))
            for j in range(count):
                word,a,c=data[bad[j*len(bad)//count]]
                s.add(z3.Or(b+z3.Sum([w[k]*v for k,v in a.items()])<=0,
                            b+z3.Sum([w[k]*v for k,v in c.items()])>=1))
        # A concrete future bad-output state yields a necessary negative
        #constraint on this seed. No orbit survival is treated as evidence.
        current=seed;hit=None
        for j in range(160):
            nxt=r.qstep(current)
            if r.bad(nxt):hit=j;break
            current=nxt
        if hit is not None:
            s.add(expression(w,b,seed)<=0);rec['seed_forced_nonpositive_by_bad_future']=hit
        if not bad and hit is None:
            candidate=dict(weights=ww,offset=bb,safety_potentials=pp,seed=seed)
            (HERE/f'any_bound1_candidate_{iteration}.json').write_text(json.dumps(candidate,indent=2))
            remaining=seconds-(time.monotonic()-start)
            verdict=check(ww,bb,min(45,remaining),save_smt=HERE/f'any_bound1_flow_{iteration}.smt2')
            rec['all_length_closure']=verdict
            if verdict['status']=='SAT':
                word=tuple(verdict['word'][0]),verdict['word'][1]
                s.add(z3.Or(expression(w,b,word)<=0,expression(w,b,r.qstep(word))>=1))
            else:
                doc['status']='EXACT_CANDIDATE_REQUIRES_AUDIT' if verdict['status']=='UNSAT' else 'UNVERIFIED_CANDIDATE'
                doc['candidate']=candidate;print(json.dumps(rec),flush=True);break
        brief={k:v for k,v in rec.items() if k!='seed'};brief['seed_pairs']=len(seed[0])
        print(json.dumps(brief),flush=True)
        (HERE/'any_bound1.json').write_text(json.dumps(doc,indent=2))
    doc['seconds']=time.monotonic()-start
    (HERE/'any_bound1.json').write_text(json.dumps(doc,indent=2))

if __name__=='__main__':main(float(sys.argv[1]) if len(sys.argv)>1 else 120)
