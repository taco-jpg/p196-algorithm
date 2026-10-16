"""Two-state carry-tile automaton with all four transformations permitted.

Each tile may preserve, flip, or reset the Boolean state. Start is 0 and
acceptance is terminal result 1. Safety and closure are implication-shaped.
"""
import parity as p
from pathlib import Path
from collections import defaultdict,deque
from itertools import product
import json,time,subprocess,hashlib,sys
w=p.w

class CNF(p.CNF):
    def conjunction(self,lits):
        lits=list(dict.fromkeys(lits))
        if 0 in lits or any(-x in lits for x in lits):return 0
        if len(lits)==1:return lits[0]
        z=self.var()
        for x in lits:self.add(-z,x)
        self.add(z,*[-x for x in lits]);return z
    def truth(self,inputs,fn):
        v=self.var();variables=sorted(set(abs(x) for x in inputs if x))
        for vals in product((False,True),repeat=len(variables)):
            assignment=dict(zip(variables,vals))
            args=[False if x==0 else assignment[abs(x)]==(x>0) for x in inputs]
            self.add(*[(-x if assignment[x] else x) for x in variables],v if fn(*args) else -v)
        return v
    def less(self,a,b):
        lt=0
        for x,y in zip(a,b):lt=self.truth([x,y,lt],lambda x,y,z:(not x and y) or (x==y and z))
        return lt

def build():
    cnf=CNF();tile=[[cnf.var(),cnf.var()] for _ in range(w.NW)]
    # Per-FST-state swap gauge: forest paths remain in automaton state 0.
    seen={0,1};todo=deque([0,1]);gauge=[]
    while todo:
        u=todo.popleft()
        for q,o,v,k in w.OUT[u]:
            if v not in seen:seen.add(v);todo.append(v);gauge.append(k);cnf.add(-tile[k][0])
    assert len(seen)==len(w.FS)
    ss,si,se,st=w.trim(w.safety_graph());S=[[cnf.var(),cnf.var()] for _ in ss]
    for u in si:cnf.add(S[u][0])
    for u,v,c in se:
        k=next(iter(c))
        for a in (0,1):
            for b in (0,1):cnf.add(-S[u][a],tile[k][a] if b==0 else -tile[k][a],S[v][b])
    for u,c in st:
        k=next(iter(c))
        for a in (0,1):cnf.add(-S[u][a],-tile[k][a])
    cs,ci,ce,ct=p.composition();R=[[cnf.var() for _ in range(4)] for _ in cs]
    for u in ci:cnf.add(R[u][0])
    for u,v,(i,j) in ce:
        for a,b in product((0,1),repeat=2):
            x,y=tile[i][a],tile[j][b]
            for c,d in product((0,1),repeat=2):
                cnf.add(-R[u][a+2*b],x if c==0 else -x,y if d==0 else -y,R[v][c+2*d])
    for u,(i,extra,j) in ct:
        for a,b in product((0,1),repeat=2):
            if extra is None:cnf.add(-R[u][a+2*b],-tile[i][a],tile[j][b])
            else:
                for c in (0,1):cnf.add(-R[u][a+2*b],-tile[i][a],tile[extra][b] if c==0 else -tile[extra][b],tile[j][c])
    # Every (FST state,0) is reachable by a zero-gauge forest path. If an
    # accepted path ever enters state 1, use its last entry from 0 and then
    # keep state 1 until the terminal. A simple suffix uses <=46 vertices.
    witness=[cnf.var() for _ in w.FS];rank=[[cnf.var() for _ in range(6)] for _ in w.FS]
    incoming=defaultdict(list);lt={}
    for k,(u,q,o,v) in enumerate(w.FE):
        incoming[v].append(tile[k][0])
        if u==v:continue
        if (u,v) not in lt:lt[u,v]=cnf.less(rank[u],rank[v])
        incoming[v].append(cnf.conjunction([witness[u],tile[k][1],lt[u,v]]))
    for v in range(len(w.FS)):cnf.add(-witness[v],*incoming[v])
    accept=[]
    for (u,c),(ex,oc,k) in w.TERMS.items():
        accept.append(tile[k][0]);accept.append(cnf.conjunction([witness[u],tile[k][1]]))
    cnf.add(*accept)
    meta=dict(tiles=w.NW,gauge=gauge,safety_states=len(ss),composition_states=len(cs),composition_edges=len(ce),composition_terminals=len(ct),cnf_variables=cnf.n,cnf_clauses=len(cnf.clauses),nonemptiness='exact forest-gauge last-entry ranked witness',rank_bits=6)
    return cnf,tile,meta

def check_and_witness(values):
    ss,si,se,st=w.trim(w.safety_graph());adj=defaultdict(list)
    for u,v,c in se:adj[u].append((v,next(iter(c))))
    reach={(u,0) for u in si};todo=deque(reach)
    while todo:
        u,a=todo.popleft()
        for v,k in adj[u]:
            nxt=v,values[k][a]
            if nxt not in reach:reach.add(nxt);todo.append(nxt)
    assert all(not values[next(iter(c))][a] for u,c in st for a in (0,1) if (u,a) in reach)
    cs,ci,ce,ct=p.composition();adj=defaultdict(list)
    for u,v,(i,j) in ce:adj[u].append((v,i,j))
    reach={(u,0,0) for u in ci};todo=deque(reach)
    while todo:
        u,a,b=todo.popleft()
        for v,i,j in adj[u]:
            nxt=v,values[i][a],values[j][b]
            if nxt not in reach:reach.add(nxt);todo.append(nxt)
    for u,(i,extra,j) in ct:
        for a,b in product((0,1),repeat=2):
            if (u,a,b) not in reach:continue
            bb=b if extra is None else values[extra][b]
            assert not values[i][a] or values[j][bb]
    paths={(0,0):(),(1,0):()};todo=deque(paths)
    while todo:
        u,a=todo.popleft()
        for (x,c),(ex,oc,k) in w.TERMS.items():
            if x==u and values[k][a]:return dict(verified=True,word=(paths[u,a],c),closure_reachable=len(reach))
        for q,o,v,k in w.OUT[u]:
            nxt=v,values[k][a]
            if nxt not in paths:paths[nxt]=paths[u,a]+(q,);todo.append(nxt)
    raise AssertionError('empty language')

def main():
    seconds=int(sys.argv[1]) if len(sys.argv)>1 else 45;outdir=Path(__file__).parent
    t=time.monotonic();cnf,tile,meta=build();path=outdir/'monoid.cnf'
    with path.open('w') as f:
        f.write(f'p cnf {cnf.n} {len(cnf.clauses)}\n')
        for c in cnf.clauses:f.write(' '.join(map(str,c))+' 0\n')
    meta['build_seconds']=time.monotonic()-t
    (outdir/'monoid_encoding.json').write_text(json.dumps(dict(meta=meta,tile_variables=tile),indent=2));print(json.dumps(meta),flush=True)
    cmd=[str(p.ROOT/'lean-runtime/lean-4.19.0-linux/bin/cadical'),'--lrat','--no-binary','-t',str(seconds),str(path),str(outdir/'monoid.lrat')]
    with (outdir/'monoid.log').open('w') as log:result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=seconds+20)
    status='sat' if result.returncode==10 else 'unsat' if result.returncode==20 else 'unknown'
    report=dict(meta,status=status,returncode=result.returncode,seconds=time.monotonic()-t,infinite_existence_proved=False)
    if status=='sat':
        lines=(outdir/'monoid.log').read_text().splitlines();model={abs(x):x>0 for line in lines if line.startswith('v ') for x in map(int,line[2:].split()) if x}
        assert all(any(model[abs(x)]==(x>0) for x in c) for c in cnf.clauses)
        vals=[[int(model[v]) for v in row] for row in tile];report['tile_values']=vals
        report['exact_check']=check_and_witness(vals);report['status']='candidate_pending_root_audit'
    (outdir/'monoid_result.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='tile_values'}),flush=True)

if __name__=='__main__':main()
