"""CEGIS for an integer-weighted, unbounded-counter language S(word)>0.

Unlike the earlier globally monotone potential search, this requires closure
only when S(input)>0. Finite sample success is not an invariant certificate;
an all-length checker is required for that conclusion.
"""
from collections import Counter
from fractions import Fraction
from math import lcm
from itertools import product,permutations
import time,json
import numpy as np
from scipy.sparse import csr_matrix
import z3
import creative_regular_invariant as r

def cat(q):return 1 if q<9 else 2 if q==9 else 3
def features(word):
    p,c=word;last=0;f=Counter()
    for q in p:f[19*last+q]+=1;last=cat(q)
    f[76+11*last+r.terminal_index(c)]+=1
    return dict(f)
def row(vars,f):return z3.Sum([vars[i]*v for i,v in f.items()])
def synthesis(seed=((7,),18),orbit_samples=50,bounded=False,positive_cycle=None):
    s=z3.SolverFor('QF_BV' if bounded else 'QF_LRA');s.set(timeout=20000)
    w=[z3.BitVec('w%d'%i,32) if bounded else z3.Real('w%d'%i) for i in range(120)]
    if bounded:
        for v in w:s.add(v>=-8,v<=8)
    states=[(0,True,True,False)];ids={states[0]:0};edges=[];terms=[]
    for st in states:
        a,low,exc,started=st;u=ids[st]
        for c in [None]+list(range(0,19,2)):
            if not started and (c is None or c==0):continue
            bad=(low and (c is None or c<=9)) or (exc and started and (c is None or c==0))
            if bad:terms.append((u,w[76+11*a+r.terminal_index(c)]))
        for q in range(0 if started else 1,19):
            lo=low and q<=9;ex=exc and (q in (0,11) if started else q==11)
            if not (lo or ex):continue
            ns=(cat(q),lo,ex,True)
            if ns not in ids:ids[ns]=len(states);states.append(ns)
            edges.append((u,ids[ns],w[19*a+q]))
    p=[z3.BitVec('safe%d'%i,32) if bounded else z3.Real('safe%d'%i) for i in range(len(states))];s.add(p[0]==0)
    if bounded:
        for v in p:s.add(v>=-128,v<=128)
    for u,v,cost in edges:s.add(p[v]<=p[u]-cost)
    for u,term in terms:s.add(p[u]-term>=0)
    if positive_cycle is not None:
        s.add(z3.Sum([w[19*cat(positive_cycle[i-1])+q] for i,q in enumerate(positive_cycle)])>=1)
    elif seed is not None:
        q=seed
        for _ in range(orbit_samples):
            s.add(row(w,features(q))>=1);q=r.qstep(q)
    else:
        # Exact nonemptiness: either a positive cycle is reachable in the
        # three-category graph, or a positive accepting simple path exists.
        # Every category is reachable from a nonzero first pair.
        positive=[]
        for n in range(4):
            for ps in product(range(19),repeat=n):
                if n and (ps[0]==0 or len(set(map(cat,ps)))!=n):continue
                for center in [None]+list(range(0,19,2)):
                    if not n and (center is None or center==0):continue
                    positive.append(row(w,features((ps,center)))>=1)
        alphabet={a:[q for q in range(19) if cat(q)==a] for a in (1,2,3)}
        for n in (1,2,3):
            for cs in permutations((1,2,3),n):
                if cs[0]!=min(cs):continue
                dest=cs[1:]+cs[:1]
                for letters in product(*(alphabet[c] for c in dest)):
                    positive.append(z3.Sum([w[19*a+q] for a,q in zip(cs,letters)])>=1)
        s.add(z3.Or(positive))
    return s,w

def sample_data(maxpairs=3):
    words=[];xf=[];yf=[]
    for n in range(maxpairs+1):
        for p in product(range(19),repeat=n):
            if n and p[0]==0:continue
            for c in [None]+list(range(0,19,2)):
                if not n and (c is None or c==0):continue
                word=(p,c);words.append(word);xf.append(features(word));yf.append(features(r.qstep(word)))
    def matrix(fs):
        ii=[];jj=[];vv=[]
        for i,f in enumerate(fs):
            for j,v in f.items():ii.append(i);jj.append(j);vv.append(v)
        return csr_matrix((vv,(ii,jj)),shape=(len(fs),120),dtype=np.int64)
    return words,xf,yf,matrix(xf),matrix(yf)

def integer_model(m,vars):
    vals=[m.eval(v,model_completion=True) for v in vars]
    if z3.is_bv_value(vals[0]):
        return [v.as_signed_long() for v in vals]
    vals=[Fraction(v.numerator_as_long(),v.denominator_as_long()) for v in vals]
    den=lcm(*(v.denominator for v in vals))
    return [int(v*den) for v in vals]

def main(seed=((7,),18),rounds=100,orbit_samples=50,stem='resume_weighted_conditional',bounded=False,positive_cycle=None):
    ts=time.monotonic();s,vars=synthesis(seed,orbit_samples,bounded,positive_cycle)
    words,xf,yf,X,Y=sample_data();history=[]
    for iteration in range(rounds):
        result=s.check();rec={'iteration':iteration,'synthesis':str(result),'bounded_weights':bounded,'elapsed':time.monotonic()-ts}
        if result!=z3.sat:
            rec['scope']='finite sampled constraints for this specified additive-counter template'
            history.append(rec);print(json.dumps(rec),flush=True);break
        values=integer_model(s.model(),vars)
        # Exact integer evaluation; object arithmetic avoids fixed-width overflow.
        xv=np.array([sum(values[j]*v for j,v in f.items()) for f in xf],dtype=object)
        yv=np.array([sum(values[j]*v for j,v in f.items()) for f in yf],dtype=object)
        bad=np.flatnonzero((xv>0)&(yv<=0));rec['finite_counterexamples']=len(bad)
        if len(bad):
            # Distribute counterexamples across the enumerated words to avoid
            # adding many copies of essentially the same local constraint.
            chosen=bad[np.linspace(0,len(bad)-1,min(32,len(bad)),dtype=int)]
            for i in chosen:s.add(z3.Or(row(vars,xf[i])<=0,row(vars,yf[i])>=1))
        else:
            weights=[values[19*i:19*(i+1)]for i in range(4)]
            terminals=[values[76+11*i:76+11*(i+1)]for i in range(4)]
            rec.update(weights=weights,terminals=terminals,status='FINITE_SAMPLE_CANDIDATE')
            try:
                from resume_weighted_checker import check
                verdict=check(weights,terminals,seconds=30)
                rec['unbounded_check']=verdict
                if verdict['status']=='SAT':
                    word=verdict['word'];out=r.qstep(word)
                    s.add(z3.Or(row(vars,features(word))<=0,row(vars,features(out))>=1))
                else:
                    history.append(rec);print(json.dumps(rec),flush=True);break
            except ImportError:
                history.append(rec);print(json.dumps(rec),flush=True);break
        history.append(rec);print(json.dumps(rec),flush=True)
        open(stem+'_results.json','w').write(json.dumps(history,indent=2))
    open(stem+'_results.json','w').write(json.dumps(history,indent=2))
    if history[-1]['synthesis']=='unsat':open(stem+'_unsat.smt2','w').write(s.to_smt2())
    return history

if __name__=='__main__':main()
