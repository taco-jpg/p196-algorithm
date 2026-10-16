"""Replay the arbitrary-group Tietze certificate without running the search.

Each certificate step uses one original defining relation, after only the
already certified substitutions, to solve for a generator occurring once.
Every generator is eliminated, and its replacement contains only generators
eliminated strictly later. Thus reverse induction proves they all equal e.
"""
import sys,json,hashlib
from pathlib import Path
from collections import Counter
import presentation as p

def multiply(*words):
    result=[]
    for word in words:
        for x in word:
            if result and result[-1]+x==0:result.pop()
            else:result.append(x)
    return tuple(result)
def inverse(word):return tuple(-a for a in reversed(word))
def cyclic(word):
    word=multiply(word)
    while len(word)>1 and word[0]+word[-1]==0:word=word[1:-1]
    return word

def audit_twisted_gauge():
    # Abstract distinct free generators, not a particular finite group.
    h=20
    def phi(a):return multiply((-h,),a,(h,))
    gu,gv=(1,),(2,)
    ax,ay,axx,ayy=(3,),(4,),(5,),(6,)
    du,dv=(7,),(8,)
    gc=multiply(inverse(ax),gu,axx)
    gn=multiply(inverse(ay),gv,ayy)
    dp=multiply(inverse(phi(ax)),du,ay)
    dpp=multiply(inverse(phi(axx)),dv,ayy)
    lhs=multiply(inverse(phi(gc)),dp,gn,inverse(dpp))
    original=multiply(inverse(phi(gu)),du,gv,inverse(dv))
    expected=multiply(inverse(phi(axx)),original,phi(axx))
    assert lhs==expected
    # Terminal with one extra next edge plus terminal; the no-extra case is
    # the same telescoping identity with the middle state absent.
    tc,tn,extra=(9,),(10,),(11,)
    transformed=multiply(inverse(phi(multiply(inverse(ax),tc))),dp,
        multiply(inverse(ay),extra,ayy),multiply(inverse(ayy),tn))
    assert transformed==multiply(inverse(phi(tc)),du,extra,tn)
    pu=(12,)
    assert multiply(pu,ax,inverse(ax),gu,axx)==multiply(pu,gu,axx)
    assert multiply(pu,ax,inverse(ax),tc)==multiply(pu,tc)

def main():
    audit_twisted_gauge()
    name='conjugacy' if '--conjugacy' in sys.argv else 'presentation'
    path=Path(__file__).parent;data=json.loads((path/(name+'.json')).read_text())
    if name=='conjugacy':
        from conjugacy import build
    else:build=p.build
    original,nv,meta=build();subs={};used_relations=set();lengths=Counter()
    def expand(word):
        pending=list(reversed(word));answer=[]
        while pending:
            a=pending.pop();replacement=subs.get(abs(a))
            if replacement is not None:
                if a<0:replacement=inverse(replacement)
                pending.extend(reversed(replacement))
            elif answer and answer[-1]+a==0:answer.pop()
            else:answer.append(a)
        return tuple(answer)
    for idx,x,claimed,claimed_rhs in data['steps']:
        assert idx not in used_relations and x not in subs
        used_relations.add(idx)
        actual=cyclic(expand(original[idx]));claimed=tuple(claimed);claimed_rhs=tuple(claimed_rhs)
        assert actual==claimed,(idx,actual,claimed)
        assert sum(abs(a)==x for a in actual)==1
        assert all(abs(a) not in subs for a in claimed_rhs)
        assert x not in set(map(abs,claimed_rhs))
        at=next(j for j,a in enumerate(actual) if abs(a)==x)
        if actual[at]>0:rhs=multiply(inverse(actual[:at]),inverse(actual[at+1:]))
        else:rhs=multiply(actual[at+1:],actual[:at])
        assert rhs==claimed_rhs
        subs[x]=rhs;lengths[len(actual)]+=1
    expected_eliminated=set(range(1,nv+1))
    if name=='conjugacy':expected_eliminated.remove(nv)
    assert set(subs)==expected_eliminated
    # Every original relation and every tile is exactly the empty group word.
    assert all(expand(r)==() for r in original)
    assert all(expand((k,))==() for k in range(1,p.w.NW+1))
    # Check the group relations against the prior additive finite formulation.
    n,rows,rhs,m=p.w.constraints('1',((7,),18));assert n==nv-(name=='conjugacy')
    expected=[]
    for row in rows[:-1]:
        ds={k+1:v*(-1 if p.w.NW<=k<p.w.NW+48 else 1) for k,v in row.items()}
        expected.append(ds)
    def normalize(ds):
        ds={k:v for k,v in ds.items() if v}
        if not ds:return ()
        sign=1 if ds[min(ds)]>0 else -1
        return tuple((k,sign*v) for k,v in sorted(ds.items()))
    got=[]
    for r in original[:-len(meta['gauge'])]:
        ds=Counter()
        for a in r:ds[abs(a)]+=1 if a>0 else -1
        got.append(normalize(ds))
    # Original inequalities have duplicate opposite initial-potential rows.
    assert set(got)==set(map(normalize,expected))
    result=dict(verified=True,variables=nv,original_relations=len(original),steps=len(subs),relation_lengths=dict(lengths),all_nonconjugating_generators_identity=True,all_tile_scores_identity=True,additive_cross_check=True,twisted_gauge_free_group_audit=True,certificate_sha256=hashlib.sha256((path/(name+'.json')).read_bytes()).hexdigest(),infinite_existence_proved=False)
    (path/(name+'_check_result.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
