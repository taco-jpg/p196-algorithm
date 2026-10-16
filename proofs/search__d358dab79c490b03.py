"""Exact finite-field additive carry-history invariant search.

Seek F(next)=c*F(current) for all accepted two-step histories and F=0
when the output is a palindrome predecessor. No finite sample is a closure test.
"""
from pathlib import Path
from collections import deque
import sys, json, time, hashlib, argparse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import persist_spacetime_weighted as m

HERE = Path(__file__).resolve().parent

def combine(*terms):
    out = {}
    for factor,row in terms:
        for k,v in row.items():
            out[k] = out.get(k,0)+factor*v
            if out[k] == 0: del out[k]
    return out

def eliminate_potentials(graph):
    states,initial,edges,terms = m.trim(graph)
    out = [[] for _ in states]
    for u,v,cost in edges: out[u].append((v,cost))
    paths = [None for _ in states]
    todo = deque(initial)
    for u in initial: paths[u] = {}
    while todo:
        u = todo.popleft()
        for v,cost in out[u]:
            if paths[v] is None:
                paths[v] = combine((1,paths[u]),(1,cost))
                todo.append(v)
    assert all(x is not None for x in paths)
    rows = [combine((1,paths[v]),(-1,paths[u]),(-1,cost))
            for u,v,cost in edges]
    rows += [combine((1,paths[u]),(1,cost)) for u,cost in terms]
    rows += [paths[u] for u in initial]
    return rows,paths,dict(states=len(states),edges=len(edges),terminals=len(terms))

def make_rows(c):
    rows=[]; potentials=[]; meta=[]
    for graph in (m.safety_graph(),m.closure_graph(str(c))):
        rr,pp,mm = eliminate_potentials(graph)
        rows.extend(rr);potentials.extend(pp);meta.append(mm)
    return rows,potentials,meta

def echelon2(rows):
    basis={}
    for row in sorted(rows,key=len):
        v=sum(1<<j for j,a in row.items() if a%2)
        while v:
            j=(v&-v).bit_length()-1
            if j in basis: v ^= basis[j]
            else:
                basis[j]=v;break
    return {j:{k:1 for k in range(m.NW) if (v>>k)&1}
            for j,v in basis.items()}

def echelon_sparse(rows,p):
    basis={}
    for row in sorted(rows,key=len):
        v={j:a%p for j,a in row.items() if a%p}
        while v:
            j=min(v)
            if j not in basis:
                inv=pow(v[j],-1,p)
                basis[j]={k:(a*inv)%p for k,a in v.items()}
                break
            factor=v[j]
            for k,a in basis[j].items():
                b=(v.get(k,0)-factor*a)%p
                if b: v[k]=b
                elif k in v: del v[k]
    return basis

def kernel_basis(echelon,p):
    free=[j for j in range(m.NW) if j not in echelon]
    for j in free:
        w=[0]*m.NW; w[j]=1
        for pivot in sorted(echelon,reverse=True):
            w[pivot]=-sum(a*w[k] for k,a in echelon[pivot].items() if k!=pivot)%p
        yield j,w

def nonzero_word(w,p):
    # The exact finite product tracks every possible path residue.
    todo=deque([(0,0),(1,0)])
    paths={(0,0):(),(1,0):()}
    while todo:
        x,s=todo.popleft(); path=paths[x,s]
        for (xx,center),(_,_,tile) in m.TERMS.items():
            if xx==x and (s+w[tile])%p:
                word=(tuple(m.FE[e][1] for e in path),center)
                assert m.history_path(word)==list(path)+[tile]
                return dict(word=word,path=list(path)+[tile],residue=(s+w[tile])%p)
        for q,o,y,tile in m.OUT[x]:
            dest=(y,(s+w[tile])%p)
            if dest not in paths:
                paths[dest]=path+(tile,);todo.append(dest)
    return None

def canonical_integer(word):
    pairs,center=word
    high=[max(1 if i==0 else 0,q-9) for i,q in enumerate(pairs)]
    low=[q-a for q,a in zip(pairs,high)]
    ds=high+([] if center is None else [center//2])+low[::-1]
    assert ds and ds[0]>0 and all(0<=a<=9 for a in ds)
    return int(''.join(map(str,ds)))

def solve(p,c):
    start=time.monotonic()
    rows,potentials,meta=make_rows(c)
    echelon=echelon2(rows) if p==2 else echelon_sparse(rows,p)
    result=dict(p=p,c=c,weights=m.NW,rank=len(echelon),
                nullity=m.NW-len(echelon),graphs=meta,
                projected_rows=len(rows),candidate=None)
    kernel=[]
    full_n,full_rows,_,_=m.constraints(str(c),((7,),18))
    full_rows=full_rows[:-1]
    result['full_rows_sha256']=hashlib.sha256(json.dumps(
        [sorted(row.items()) for row in full_rows],separators=(',',':')).encode()).hexdigest()
    for free,w in kernel_basis(echelon,p):
        assert all(sum(a*w[j] for j,a in row.items())%p==0 for row in rows)
        full=w+[sum(a*w[j] for j,a in row.items())%p for row in potentials]
        assert len(full)==full_n
        # This uses independently assembled original2429-variable rows.
        assert all(sum(a*full[j] for j,a in row.items())%p==0 for row in full_rows)
        witness=nonzero_word(w,p)
        kernel.append(dict(free_column=free,weights={j:a for j,a in enumerate(w) if a}))
        if witness is not None:
            n=canonical_integer(witness['word']);n1=n+int(str(n)[::-1]);n2=n1+int(str(n1)[::-1])
            result['candidate']=dict(weights=w,full_variables=full,witness=witness,
                                     realized_input=str(n),first_iterate=str(n1),
                                     lychrel_candidate=str(n2))
            break
    result['kernel_basis']=kernel
    result['every_basis_vector_full_row_checked']=True
    result['all_basis_scores_identically_zero']=result['candidate'] is None
    result['seconds']=time.monotonic()-start
    result['existence_proved']=False
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--primes',default='2,3,5,7');args=ap.parse_args()
    summary=[]
    for p in map(int,args.primes.split(',')):
        for c in range(1,p):
            file=HERE/f'p{p}_c{c}.json'
            if file.exists(): result=json.loads(file.read_text())
            else:
                print(json.dumps(dict(starting=True,p=p,c=c)),flush=True)
                result=solve(p,c);file.write_text(json.dumps(result,indent=2))
            brief={k:v for k,v in result.items() if k not in ('kernel_basis','candidate')}
            brief['has_candidate']=result['candidate'] is not None
            summary.append(brief);print(json.dumps(brief),flush=True)
            (HERE/'results.json').write_text(json.dumps(summary,indent=2))
            if result['candidate'] is not None:
                (HERE/'POSITIVE_CANDIDATE.json').write_text(json.dumps(result,indent=2))
                return

if __name__=='__main__':main()
