"""Bounded integer CEGIS for genuine conditional carry-history scores.

Bounds apply to raw tile weights and the separately represented offset;
there is no gauge fixing, scalar multiplier, or global monotonicity condition.
"""
from pathlib import Path
from itertools import product
import sys,json,time,argparse
from fractions import Fraction
from math import lcm
import numpy as np
import z3
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
import persist_spacetime_weighted as m
import creative_regular_invariant as r
from checker import check,score
HERE=Path(__file__).resolve().parent

def expression(w,b,word):
    return b+z3.Sum([w[j]*a for j,a in m.history_weights(word).items()])

def evaluate(w,b,features):return b+sum(w[j]*a for j,a in features.items())

def make_solver(seed,bound,offset_bound,orbit_samples):
    s=z3.SolverFor('QF_LIA' if bound is not None else 'QF_LRA')
    var=z3.Int if bound is not None else z3.Real
    w=[var('weight_%d'%i) for i in range(m.NW)]
    b=var('offset')
    if bound is not None:
        for x in w:s.add(x>=-bound,x<=bound)
        s.add(b>=-offset_bound,b<=offset_bound)
    states,initial,edges,terms=m.trim(m.safety_graph())
    p=[var('safe_%d'%j) for j in range(len(states))]
    # A shortest simple path has at most |V|-1 edges. These bounds preserve
    # completeness for raw tile weights in [-bound,bound].
    if bound is not None:
        for x in p:s.add(x>=-len(states)*bound,x<=len(states)*bound)
    for j in initial:s.add(p[j]==0)
    for u,v,cost in edges:s.add(p[v]<=p[u]+z3.Sum([w[j]*a for j,a in cost.items()]))
    for u,cost in terms:s.add(p[u]+z3.Sum([w[j]*a for j,a in cost.items()])-b>=0)
    word=seed
    for _ in range(orbit_samples):
        s.add(expression(w,b,word)>=1);word=r.qstep(word)
    return s,w,b,p,(states,initial,edges,terms)

def samples(maxpairs=2):
    result=[]
    for n in range(maxpairs+1):
        for pairs in product(range(19),repeat=n):
            if pairs and not pairs[0]:continue
            for center in [None]+list(range(0,19,2)):
                word=(pairs,center)
                if r.valid(word):result.append((word,m.history_weights(word),m.history_weights(r.qstep(word))))
    return result

def verify_safety(w,b,p,graph):
    _,initial,edges,terms=graph
    assert all(p[i]==0 for i in initial)
    assert all(p[v]<=p[u]+sum(w[j]*a for j,a in cost.items()) for u,v,cost in edges)
    assert all(p[u]+sum(w[j]*a for j,a in cost.items())-b>=0 for u,cost in terms)

def main(seed_number=196,bound=1,offset_bound=2,seconds=180,orbit_samples=80,maxpairs=2):
    start=time.monotonic();digits=tuple(map(int,str(seed_number)))
    seed=r.fold(tuple(a+b for a,b in zip(digits,digits[::-1])))
    s,w,b,p,safety=make_solver(seed,bound,offset_bound,orbit_samples)
    data=samples(maxpairs);history=[];constraints=set()
    stem=f'seed{seed_number}_bound{bound}_offset{offset_bound}'
    result=dict(seed_number=seed_number,seed=seed,bound=bound,offset_bound=offset_bound,
                orbit_samples=orbit_samples,maxpairs=maxpairs,sample_words=len(data),history=history,
                closure_words=[],candidate=None,status='NO_CERTIFICATE')
    for iteration in range(1000):
        remaining=seconds-(time.monotonic()-start)
        if remaining<1:break
        s.set(timeout=int(1000*min(12,remaining)))
        status=s.check();record=dict(iteration=iteration,synthesis=str(status),elapsed=time.monotonic()-start)
        history.append(record)
        if status!=z3.sat:
            if status==z3.unknown:record['reason']=s.reason_unknown()
            if status==z3.unsat:
                record['scope']=('No score within the stated raw-weight/offset bounds is positive at this seed and satisfies the necessary constraints.' if bound is not None else 'Unbounded QF_LRA necessary constraints are UNSAT; solver result with SMT-LIB archived, not an independently replayed proof.')
                (HERE/f'{stem}_unsat.smt2').write_text(s.to_smt2())
            print(json.dumps(record),flush=True);break
        model=s.model()
        if bound is not None:
            ww=[model.eval(x).as_long() for x in w];bb=model.eval(b).as_long()
            pp=[model.eval(x).as_long() for x in p]
        else:
            values=[model.eval(x,model_completion=True) for x in w+[b]+p]
            rational=[Fraction(x.numerator_as_long(),x.denominator_as_long()) for x in values]
            den=lcm(*(x.denominator for x in rational))
            integer=[int(x*den) for x in rational]
            ww=integer[:m.NW];bb=integer[m.NW];pp=integer[m.NW+1:]
        verify_safety(ww,bb,pp,safety)
        if bound is not None:assert all(-bound<=x<=bound for x in ww) and -offset_bound<=bb<=offset_bound
        assert score(ww,bb,seed)>=1
        bad=[i for i,(_,a,c) in enumerate(data) if evaluate(ww,bb,a)>0 and evaluate(ww,bb,c)<=0]
        record.update(offset=bb,nonzero_tiles=sum(x!=0 for x in ww),finite_counterexamples=len(bad))
        if bad:
            count=min(128,len(bad));chosen=[bad[j*len(bad)//count] for j in range(count)]
            for i in chosen:
                word,a,c=data[i];key=tuple(sorted(a.items())),tuple(sorted(c.items()))
                if key in constraints:continue
                constraints.add(key)
                result['closure_words'].append(word)
                left=b+z3.Sum([w[j]*v for j,v in a.items()])
                right=b+z3.Sum([w[j]*v for j,v in c.items()])
                s.add(z3.Or(left<=0,right>=1))
        else:
            remaining=seconds-(time.monotonic()-start)
            if remaining<2:break
            (HERE/f'{stem}_pairs{maxpairs}_candidate_{iteration}.json').write_text(json.dumps(dict(weights=ww,offset=bb,safety_potentials=pp,seed=seed),indent=2))
            filename=HERE/f'{stem}_flow_{iteration}.smt2'
            verdict=check(ww,bb,seconds=min(45,remaining),save_smt=filename)
            record['all_length_closure']=verdict
            if verdict['status']=='SAT':
                word=(tuple(verdict['word'][0]),verdict['word'][1]);nxt=r.qstep(word)
                result['closure_words'].append(word)
                s.add(z3.Or(expression(w,b,word)<=0,expression(w,b,nxt)>=1))
            else:
                candidate=dict(weights=ww,offset=bb,safety_potentials=pp,
                               seed=seed,seed_score=score(ww,bb,seed),closure=verdict)
                result['candidate']=candidate
                result['status']='EXACT_CANDIDATE_REQUIRES_AUDIT' if verdict['status']=='UNSAT' else 'UNVERIFIED_CANDIDATE'
                print(json.dumps(record),flush=True);break
        record['necessary_closure_constraints']=len(constraints)
        print(json.dumps(record),flush=True)
        (HERE/f'{stem}.json').write_text(json.dumps(result,indent=2))
    result['seconds']=time.monotonic()-start
    (HERE/f'{stem}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('history','candidate')}),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=196)
    ap.add_argument('--bound',type=int,default=1);ap.add_argument('--offset-bound',type=int,default=2)
    ap.add_argument('--seconds',type=float,default=180);ap.add_argument('--orbit-samples',type=int,default=80)
    ap.add_argument('--unbounded-rational',action='store_true')
    ap.add_argument('--maxpairs',type=int,default=2)
    a=ap.parse_args();main(a.seed,None if a.unbounded_rational else a.bound,None if a.unbounded_rational else a.offset_bound,a.seconds,a.orbit_samples,a.maxpairs)
