"""Conditional parity invariant over full decimal carry-history tiles.

Accept a history iff XOR of its tile labels is 1. Safety forces XOR 0 for
bad outputs. Closure forbids only (current total, next total)=(1,0), leaving
(0,1) permitted. Exact graph products cover every finite word length.
"""
import sys,json,time,subprocess,hashlib
from pathlib import Path
from collections import defaultdict,deque,Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research'))
import persist_spacetime_weighted as w
from persist_spacetime_tile_grammar import composed_tiles

class CNF:
    def __init__(self):self.n=0;self.clauses=[]
    def var(self):self.n+=1;return self.n
    def add(self,*lits):
        ls=set(lits);assert 0 not in ls
        if any(-a in ls for a in ls):return
        self.clauses.append(tuple(sorted(ls,key=lambda x:(abs(x),x))))
    def xor(self,a,b):
        if a==0:return b
        if b==0:return a
        if a==b:return 0
        v=self.var()
        self.add(a,b,-v);self.add(a,-b,v);self.add(-a,b,v);self.add(-a,-b,-v)
        return v

def linear_safety():
    states,initial,edges,terms=w.trim(w.safety_graph());n=w.NW+len(states)
    rows=[]
    def row(*ids):
        z=0
        for i in ids:z^=1<<i
        rows.append(z)
    for i in initial:row(w.NW+i)
    for u,v,c in edges:row(w.NW+u,w.NW+v,next(iter(c)))
    for u,c in terms:row(w.NW+u,next(iter(c)))
    seen={0,1};todo=deque(seen);gauge=[]
    while todo:
        u=todo.popleft()
        for q,o,v,k in w.OUT[u]:
            if v not in seen:seen.add(v);todo.append(v);gauge.append(k);row(k)
    assert len(seen)==len(w.FS)
    pivots={}
    for z in rows:
        while z:
            k=(z&-z).bit_length()-1
            if k in pivots:z^=pivots[k]
            else:pivots[k]=z;break
    expression={}
    for k in reversed(range(n)):
        if k not in pivots:expression[k]=1<<k;continue
        z=pivots[k]^(1<<k);out=0
        while z:
            j=(z&-z).bit_length()-1;out^=expression[j];z^=1<<j
        expression[k]=out
    for z in rows:
        out=0
        while z:
            j=(z&-z).bit_length()-1;out^=expression[j];z^=1<<j
        assert out==0
    # In this graph every tile is either forced zero or an independent bit.
    assert all(expression[k].bit_count()<=1 for k in range(w.NW))
    return [expression[k] for k in range(w.NW)],dict(rank=len(pivots),gauge=gauge,variables=n,rows=len(rows))

def composition():
    states,ee,tt=composed_tiles()
    graph=(states,[0,1,2,3],[(u,v,(a,b)) for u,v,a,b in ee],[(u,(a,ex,b)) for u,a,ex,b in tt])
    return w.trim(graph)

def build(seed=None):
    cnf=CNF();expr,meta=linear_safety()
    variables={z:cnf.var() for z in sorted(set(expr)) if z}
    tile=[variables.get(z,0) for z in expr]
    states,initial,edges,terms=composition();R=[[cnf.var() for _ in range(4)] for _ in states]
    for u in initial:cnf.add(R[u][0])
    def options(v):return (0,1) if v else (0,)
    def guard(v,value):return [v if value==0 else -v] if v else []
    for u,v,(a,b) in edges:
        wa,wb=tile[a],tile[b]
        for av in options(wa):
            for bv in options(wb):
                shift=av+2*bv;gg=guard(wa,av)+guard(wb,bv)
                for s in range(4):cnf.add(-R[u][s],*gg,R[v][s^shift])
    pair_xors={}
    for u,(a,extra,b) in terms:
        wa,wb=tile[a],tile[b]
        if extra is not None:
            key=tuple(sorted((wb,tile[extra])))
            if key not in pair_xors:pair_xors[key]=cnf.xor(*key)
            wb=pair_xors[key]
        for av in options(wa):
            for bv in options(wb):
                badprefix=(1^av)+2*bv
                cnf.add(-R[u][badprefix],*guard(wa,av),*guard(wb,bv))
    if seed is None:
        # Under the zero-tree gauge, all complete scores vanish iff all
        # tile labels vanish. Thus this imposes exact finite nonemptiness.
        cnf.add(*sorted(set(tile)-{0}))
    else:
        score=0
        for k in w.history_path(seed):score=cnf.xor(score,tile[k])
        if score:cnf.add(score)
        else:cnf.add()
    meta.update(tiles=w.NW,free_tile_bits=len(variables),fixed_zero_tiles=tile.count(0),composition_states=len(states),composition_edges=len(edges),composition_terminals=len(terms),cnf_variables=cnf.n,cnf_clauses=len(cnf.clauses),seed=seed)
    return cnf,tile,meta

def check_and_witness(values):
    # Independent forward graph reachability; no SAT reachability variables.
    ss,si,se,st=w.trim(w.safety_graph());adj=defaultdict(list)
    for u,v,c in se:adj[u].append((v,next(iter(c))))
    reach={(u,0) for u in si};todo=deque(reach)
    while todo:
        u,s=todo.popleft()
        for v,k in adj[u]:
            t=(v,s^values[k])
            if t not in reach:reach.add(t);todo.append(t)
    assert all((u,1^values[next(iter(c))]) not in reach for u,c in st)
    cs,ci,ce,ct=composition();adj=defaultdict(list)
    for u,v,(a,b) in ce:adj[u].append((v,a,b))
    reach={(u,0,0) for u in ci};todo=deque(reach)
    while todo:
        u,a,b=todo.popleft()
        for v,i,j in adj[u]:
            t=(v,a^values[i],b^values[j])
            if t not in reach:reach.add(t);todo.append(t)
    for u,(a,extra,b) in ct:
        nextbit=values[b]^(values[extra] if extra is not None else 0)
        assert (u,1^values[a],nextbit) not in reach
    todo=deque([(0,0),(1,0)]);paths={(0,0):(),(1,0):()}
    while todo:
        u,s=todo.popleft()
        for (x,c),(ex,oc,k) in w.TERMS.items():
            if x==u and s^values[k]:return dict(word=(paths[u,s],c),safety_states=len(ss),closure_reachable=len(reach),verified=True)
        for q,o,v,k in w.OUT[u]:
            t=v,s^values[k]
            if t not in paths:paths[t]=paths[u,s]+(q,);todo.append(t)
    raise AssertionError('claimed nonempty language has no accepted word')

def main():
    seconds=int(sys.argv[1]) if len(sys.argv)>1 else 60
    seed=None if len(sys.argv)<3 or sys.argv[2]=='any' else ((8,16),16) if sys.argv[2]=='18887' else ((7,),18)
    name='any' if seed is None else sys.argv[2];outdir=Path(__file__).parent
    t=time.monotonic();cnf,tile,meta=build(seed);path=outdir/(name+'.cnf')
    with path.open('w') as f:
        f.write(f'p cnf {cnf.n} {len(cnf.clauses)}\n')
        for c in cnf.clauses:f.write(' '.join(map(str,c))+' 0\n')
    meta['build_seconds']=time.monotonic()-t
    (outdir/(name+'_encoding.json')).write_text(json.dumps(dict(meta=meta,tile_variables=tile),indent=2))
    print(json.dumps(meta),flush=True)
    cmd=[str(ROOT/'lean-runtime/lean-4.19.0-linux/bin/cadical'),'--lrat','--no-binary','-t',str(seconds),str(path),str(outdir/(name+'.lrat'))]
    with (outdir/(name+'.log')).open('w') as log:
        result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=seconds+20)
    log=(outdir/(name+'.log')).read_text();status='sat' if result.returncode==10 else 'unsat' if result.returncode==20 else 'unknown'
    report=dict(meta,status=status,returncode=result.returncode,seconds=time.monotonic()-t,cnf_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),infinite_existence_proved=False)
    if status=='sat':
        model={abs(x):x>0 for line in log.splitlines() if line.startswith('v ') for x in map(int,line[2:].split()) if x}
        assert all(any(model[abs(x)]==(x>0) for x in c) for c in cnf.clauses)
        vals=[int(model[v]) if v else 0 for v in tile];report['tile_values']=vals
        report['exact_check']=check_and_witness(vals);report['status']='candidate_pending_root_audit'
    (outdir/(name+'_result.json')).write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='tile_values'}),flush=True)

if __name__=='__main__':main()
