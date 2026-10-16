"""Exact noncommutative carry-history invariant presentation.

All words are products in an arbitrary group, with negative generator IDs
denoting inverses. No finite group or commutativity assumption is used in
the Tietze eliminations. A reduced nontrivial presentation is not a witness.
"""
import sys,json,time,heapq
from collections import defaultdict,Counter,deque
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'research'))
import persist_spacetime_weighted as w

def inv(a): return tuple(-x for x in a[::-1])
def reduce(a):
    b=[]
    for x in a:
        if b and b[-1]==-x:b.pop()
        else:b.append(x)
    while len(b)>1 and b[0]==-b[-1]: b=b[1:-1]
    return tuple(b)
def free_reduce(a):
    b=[]
    for x in a:
        if b and b[-1]==-x:b.pop()
        else:b.append(x)
    return tuple(b)

def build():
    rel=[]; nv=w.NW;meta={}
    ss,si,se,st=w.trim(w.safety_graph()); base=nv;nv+=len(ss)
    rel.extend([(base+i+1,) for i in si])
    for u,v,c in se:
        k=next(iter(c));assert c[k]==-1
        rel.append((base+u+1,k+1,-base-v-1))
    for u,c in st:
        k=next(iter(c));assert c[k]==-1
        rel.append((base+u+1,k+1))
    meta['safety']=[len(ss),len(se),len(st)]
    states=[(a,b) for a in (0,1) for b in (0,1)];ids={s:i for i,s in enumerate(states)}
    edges=[];terms=[]
    for x,y in states:
        u=ids[x,y]
        for (xx,c),(extra,oc,k) in w.TERMS.items():
            if xx!=x:continue
            ends=[(y,())] if extra is None else [(yy,(j+1,)) for q,o,yy,j in w.OUT[y] if q==extra]
            for yy,part in ends:
                if (yy,oc) in w.TERMS:
                    terms.append((u,(k+1,part+(w.TERMS[yy,oc][2]+1,))))
        for q,o,xx,k in w.OUT[x]:
            for q2,o2,yy,j in w.OUT[y]:
                if q2!=o:continue
                ns=(xx,yy)
                if ns not in ids:ids[ns]=len(states);states.append(ns)
                edges.append((u,ids[ns],(k+1,j+1)))
    cs,ci,ce,ct=w.trim((states,[0,1,2,3],edges,terms));base=nv;nv+=len(cs)
    rel.extend([(base+i+1,) for i in ci])
    for u,v,(k,j) in ce:rel.append((-k,base+u+1,j,-base-v-1))
    for u,(k,part) in ct:rel.append((-k,base+u+1)+part)
    meta['closure']=[len(cs),len(ce),len(ct)]
    # Gauge g(u,v) -> a(u)^-1*g(u,v)*a(v), g_term -> a(u)^-1*g_term.
    # a(0)=a(1)=e. A BFS forest permits all these labels to be set to e.
    seen={0,1};todo=deque([0,1]);gauge=[]
    while todo:
        u=todo.popleft()
        for q,o,v,k in w.OUT[u]:
            if v not in seen:seen.add(v);todo.append(v);gauge.append(k+1)
    assert len(seen)==len(w.FS)
    rel.extend([(k,) for k in gauge]);meta['gauge']=gauge
    meta.update(variables=nv,relations=len(rel),tiles=w.NW)
    return rel,nv,meta

class Presentation:
    def __init__(self,rels,nv):
        self.rels={};self.occ=defaultdict(set);self.heap=[];self.subs={};self.steps=[]
        for i,r in enumerate(rels):self.put(i,r)
    def put(self,i,r):
        r=reduce(r)
        if not r:return
        self.rels[i]=r
        for x in set(map(abs,r)):self.occ[x].add(i)
        heapq.heappush(self.heap,(len(r),i,r))
    def delete(self,i):
        r=self.rels.pop(i)
        for x in set(map(abs,r)):self.occ[x].remove(i)
    def eliminate(self,seconds=90,maxlen=8):
        t=time.monotonic()
        while self.heap and time.monotonic()-t<seconds:
            n,i,r=heapq.heappop(self.heap)
            if self.rels.get(i)!=r:continue
            if n>maxlen:break
            counts=Counter(map(abs,r));choices=[x for x,n in counts.items() if n==1]
            if not choices:continue
            # Smallest substitution footprint; prefer auxiliary variables in ties.
            x=min(choices,key=lambda x:(len(self.occ[x]),x<=w.NW,x))
            p=next(j for j,z in enumerate(r) if abs(z)==x)
            # r=A*x*B=e gives x=A^-1*B^-1; if inverse, invert RHS.
            rhs=inv(r[:p])+inv(r[p+1:])
            if r[p]<0:rhs=inv(rhs)
            rhs=free_reduce(rhs);self.steps.append((i,x,r,rhs));self.subs[x]=rhs
            targets=list(self.occ[x]);self.delete(i)
            for j in targets:
                if j==i:continue
                old=self.rels[j];self.delete(j)
                new=[]
                for z in old:new.extend(rhs if z==x else inv(rhs) if z==-x else (z,))
                self.put(j,new)
        return time.monotonic()-t
    def expand(self,word):
        cache={}
        def rec(x):
            if x not in cache:
                cache[x]=free_reduce(z for t in self.subs.get(x,(x,)) for z in ((rec(t) if t>0 else inv(rec(-t))) if abs(t)!=x else (t,)))
            return cache[x]
        return free_reduce(z for x in word for z in (rec(x) if x>0 else inv(rec(-x))))

if __name__=='__main__':
    t=time.monotonic();rels,nv,meta=build();p=Presentation(rels,nv)
    print(json.dumps(meta),flush=True)
    elapsed=p.eliminate(float(sys.argv[1]) if len(sys.argv)>1 else 90)
    rem=sorted(set(abs(x) for r in p.rels.values() for x in r));tiles=[p.expand((i+1,)) for i in range(w.NW)]
    out=dict(meta=meta,elapsed=elapsed,remaining_generators=len(rem),remaining_relations=len(p.rels),lengths=dict(Counter(map(len,p.rels.values()))),eliminations=len(p.steps),nonidentity_tile_words=sum(bool(a) for a in tiles),relations=list(p.rels.values()),tile_words=tiles,substitutions=p.subs,steps=p.steps,infinite_existence_proved=False)
    out['seed18887']=p.expand(tuple(k+1 for k in w.history_path(((8,16),16))))
    out['seed196']=p.expand(tuple(k+1 for k in w.history_path(((7,),18))))
    path=Path(__file__).parent/'presentation.json';path.write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ('relations','tile_words','substitutions','steps')}),flush=True)
