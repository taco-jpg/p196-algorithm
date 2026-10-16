"""Independent semantic-family and ordinary-arithmetic audit of saved CNF.

No import from synthesize_dfa.py, its transducer, or its normalization code.
Expected clauses are constructed using the saved variable-name bijection,
then compared as a multiset against every literal of the archived DIMACS.
The finite controls audit the implementation; the unrestricted bridge is
the explicit mathematical proof in METHOD_AND_PROOF.md.
"""
from collections import Counter, defaultdict
from pathlib import Path
import argparse, gzip, hashlib, itertools, json, time

C = [None] + list(range(0, 19, 2))


def freeze(x):
    return tuple(map(freeze, x)) if isinstance(x, list) else x


def folded(n):
    digits = [int(x) for x in str(n)]
    p = tuple(digits[i] + digits[-1-i] for i in range(len(digits)//2))
    return p, 2*digits[len(digits)//2] if len(digits)%2 else None


def representative(p,c):
    s = ''.join(str(min(q,9)) for q in p)
    if c is not None:
        s += str(c//2)
    s += ''.join(str(max(q-9,0)) for q in reversed(p))
    return int(s)


def independent_relation():
    # Derive high-side transitions by the equation q+inner=10*outer+digit,
    # rather than by reversing a single direction of carry propagation.
    states = [(0,0,0,-1,False),(1,0,1,1,False)]
    lookup = {x:i for i,x in enumerate(states)}
    edges, final = [], []
    for source, (h,lo_c,hi_c,last,started) in enumerate(states):
        for pair in range(0 if started else 1,19):
            low_total=pair+lo_c
            low_digit=low_total%10
            low_next=(low_total-low_digit)//10
            for inner in (0,1):
                high_digit=pair+inner-10*hi_c
                if high_digit<0 or high_digit>9:
                    continue
                state=(h,low_next,inner,high_digit if h else -1,True)
                if state not in lookup:
                    lookup[state]=len(states);states.append(state)
                emitted=low_digit+(last if h else high_digit)
                edges.append((source,pair,emitted,lookup[state]))
        for ci,middle in enumerate(C):
            if not started and middle in (None,0):
                continue
            if middle is None:
                if lo_c!=hi_c:
                    continue
                suffix=[] if not h else []
                center=2*last if h else None
            else:
                digit=middle+lo_c-10*hi_c
                if not 0<=digit<=9:
                    continue
                suffix=[digit+last] if h else []
                center=None if h else 2*digit
            final.append((source,ci,tuple(suffix),C.index(center)))
    return states,edges,final


def main(stem):
    start=time.monotonic();stem=Path(stem)
    meta=json.loads(stem.with_suffix('.json').read_text())
    n=meta['states'];sym=meta.get('state_name_symmetry',False)
    with gzip.open(str(stem)+'.variables.json.gz','rt') as f:
        names=[freeze(x) for x in json.load(f)]
    assert len(names)==len(set(names))==meta['variables']
    ids={name:i+1 for i,name in enumerate(names)}
    used=set()
    def v(*name):
        used.add(name)
        return ids[name]
    expected=Counter();families=Counter()
    def clause(kind,*lits):
        expected[tuple(sorted(lits))]+=1;families[kind]+=1
    def exactly(kind,lits):
        clause(kind,*lits)
        for a,b in itertools.combinations(lits,2):clause(kind,-a,-b)
    d=lambda a,q,b:v('d',a,q,b)
    f=lambda a,c:v('end',a,c)
    for a,q in itertools.product(range(n),range(19)):
        exactly('determinism',[d(a,q,b) for b in range(n)])
    if sym:
        preceding=[]
        for a in range(n):
            for q in list(range(1,19))+[0]:
                for b in range(2,n):
                    clause('renaming',-d(a,q,b),*[d(aa,qq,b-1) for aa,qq in preceding])
                preceding.append((a,q))
    monitor=lambda a,m:v('safety',a,m)
    clause('safety_initial',monitor(0,0))
    for a,m in itertools.product(range(n),range(4)):
        for q in range(1 if m==0 else 0,19):
            if m==0:
                mm=({**dict.fromkeys(range(1,10),1),11:2}).get(q,3)
            else:
                remains=(q<=9 if m==1 else q in (0,11) if m==2 else False)
                mm=m if remains else 3
            for b in range(n):clause('safety_edges',-monitor(a,m),-d(a,q,b),monitor(b,mm))
        bad_centers=range(2,6) if m==0 else range(6) if m==1 else range(2) if m==2 else []
        for c in bad_centers:clause('safety_terminals',-monitor(a,m),-f(a,c))
    states,edges,terms=independent_relation()
    r=lambda x,a,b:v('closure',x,a,b)
    clause('closure_initial',r(0,0,0));clause('closure_initial',r(1,0,0))
    for x,q,o,y in edges:
        for a,b,aa,bb in itertools.product(range(n),repeat=4):
            clause('closure_edges',-r(x,a,b),-d(a,q,aa),-d(b,o,bb),r(y,aa,bb))
    for x,ci,suffix,co in terms:
        for a,b in itertools.product(range(n),repeat=2):
            if suffix:
                for bb in range(n):clause('closure_terminals',-r(x,a,b),-f(a,ci),-d(b,suffix[0],bb),f(bb,co))
            else:
                clause('closure_terminals',-r(x,a,b),-f(a,ci),f(b,co))
    w=lambda j,a:v('witness',j,a)
    for a in range(n):clause('witness_initial',w(0,a) if a==0 else -w(0,a))
    for j in range(n):
        exactly('witness_state',[w(j+1,a) for a in range(n)])
        qs=list(range(1,19)) if j==0 else list(range(20))
        exactly('witness_letter',[v('letter',j,q) for q in qs])
        for q in qs:
            lit=v('letter',j,q)
            for a in range(n):
                if q==19:clause('witness_edges',-w(j,a),-lit,w(j+1,a))
                else:
                    for b in range(n):clause('witness_edges',-w(j,a),-lit,-d(a,q,b),w(j+1,b))
    ends=[]
    for a,c in itertools.product(range(n),range(11)):
        z=v('witness_end',a,c);ends.append(z)
        clause('witness_end',-z,w(n,a));clause('witness_end',-z,f(a,c))
    clause('nonempty',*(ends+[f(0,c) for c in range(2,11)]))

    evidence=[]
    if meta['terminating_pair_depth']:
        with gzip.open(str(stem)+'.terminating.json.gz','rt') as source:evidence=json.load(source)
    labels={};maxhit=0;orbit_steps=0
    for item in evidence:
        p=tuple(item['pairs']);c=item['center'];chain=item['orbit']
        assert (p,c) not in labels
        assert chain[0]==representative(p,c)
        assert folded(chain[0])==(p,c)
        for i,(a,b) in enumerate(zip(chain,chain[1:]),1):
            assert b==a+int(str(a)[::-1])
            palindrome=str(b)==str(b)[::-1]
            assert palindrome==(i==len(chain)-1)
        assert 1<len(chain)<=61
        labels[p,c]=chain;maxhit=max(maxhit,len(chain)-1);orbit_steps+=len(chain)-1
    assert len(labels)==meta['certified_terminating_labels']
    # Independently enumerate the precise finite input range and compare every
    # known/unknown label; absence is never construed as nontermination.
    complete=0;unknown=0
    for k in range(meta['terminating_pair_depth']+1):
        ps=[()] if k==0 else ((a,)+b for a in range(1,19) for b in itertools.product(range(19),repeat=k-1))
        for p in ps:
            for c in C:
                if not p and c in (None,0):continue
                complete+=1;value=representative(p,c);hit=None
                for t in range(1,61):
                    value=value+int(str(value)[::-1])
                    if str(value)==str(value)[::-1]:hit=t;break
                assert (hit is not None)==((p,c) in labels)
                if hit is None:unknown+=1
    # Negative-prefix deterministic evaluation is a trie, with special
    # initial-state handling for its first pair.
    prefix_set={p[:i] for p,c in labels for i in range(1,len(p)+1)}
    for p in prefix_set:
        row=[v('negative_prefix',p,a) for a in range(n)]
        exactly('negative_prefix',row)
        for a,b in itertools.product(range(n),repeat=2):
            if len(p)==1:
                if a==0:clause('negative_prefix_edges',-d(0,p[-1],b),row[b])
            else:clause('negative_prefix_edges',-v('negative_prefix',p[:-1],a),-d(a,p[-1],b),row[b])
    for p,c in labels:
        ci=C.index(c)
        if p:
            for a in range(n):clause('negative_labels',-v('negative_prefix',p,a),-f(a,ci))
        else:clause('negative_labels',-f(0,ci))
    assert used==set(names), ('unknown or unused variable names',set(names)-used)

    actual=Counter()
    with stem.with_suffix('.cnf').open() as source:
        for line in source:
            if line.startswith('p'):
                _,_,nv,nc=line.split();assert int(nv)==len(names)
                continue
            if line.startswith('c') or not line.strip():continue
            row=list(map(int,line.split()));assert row[-1]==0
            actual[tuple(sorted(row[:-1]))]+=1
    assert sum(actual.values())==int(nc)==meta['clauses']
    assert actual==expected,('clause mismatch',list((actual-expected).items())[:3],list((expected-actual).items())[:3])

    # Concrete arithmetic cross-check of every canonical input through five
    # digits, plus every positive ordinary integer below 100,000. Uses the
    # complete accepting paths of the independently constructed relation.
    by=defaultdict(list);termby=defaultdict(list)
    for x,q,o,y in edges:by[x,q].append((y,o))
    for x,ci,suffix,co in terms:termby[x,ci].append((suffix,co))
    cache={};counts=Counter()
    def control(value):
        source=folded(value)
        expected_word=folded(value+int(str(value)[::-1]))
        if source not in cache:
            paths=[(0,()),(1,())]
            for pair in source[0]:
                paths=[(y,p+(o,)) for x,p in paths for y,o in by[x,pair]]
            outputs=[(p+suffix,C[co]) for x,p in paths for suffix,co in termby[x,C.index(source[1])]]
            assert outputs==[expected_word],(value,source,outputs,expected_word)
            cache[source]=outputs[0]
        assert cache[source]==expected_word
        coeff=list(source[0])+([] if source[1] is None else [source[1]])
        bad=all(q<=9 for q in coeff) or (bool(source[0]) and source[0][0]==11 and all(q in (0,11) for q in coeff))
        out=value+int(str(value)[::-1]);assert bad==(str(out)==str(out)[::-1])
    for value in range(1,100000):control(value)
    for k in range(3):
        ps=[()] if not k else ((a,)+b for a in range(1,19) for b in itertools.product(range(19),repeat=k-1))
        for p in ps:
            for c in C:
                if not p and c in (None,0):continue
                control(representative(p,c));counts['canonical_words_through_width_five']+=1
    source=Path(__file__).parents[2]/'renewal_pass/seam_audit/METHOD_AND_PROOF.md'
    out=dict(verified=True,states=n,state_name_symmetry=sym,cnf_variables=len(names),cnf_clauses=sum(actual.values()),
             clause_families=dict(families),complete_input_range=complete,terminating_labels=len(labels),
             unknown_at_sixty=unknown,negative_orbit_steps=orbit_steps,max_negative_first_hit=maxhit,
             transducer_states=len(states),transducer_edges=len(edges),transducer_terminals=len(terms),
             ordinary_integer_controls=99999,**counts,distinct_folded_controls=len(cache),
             cnf_sha256=hashlib.sha256(stem.with_suffix('.cnf').read_bytes()).hexdigest(),
             palindrome_classification_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             seconds=time.monotonic()-start,
             scope='Exact saved CNF clause families and finite arithmetic controls; all-width bridge in METHOD_AND_PROOF.md',
             positive_lychrel_proof=False)
    Path(str(stem)+'.encoding_check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stem');args=p.parse_args();main(args.stem)
