"""Counterexample-guided synthesis using exact least-Horn-closure cores."""
from exist_tile_horn import *

class Horn:
    def __init__(self):
        self.n,self.clauses,self.meta=horn_clauses();self.inc=[[] for _ in range(self.n)];self.zero=[]
        for j,(body,head) in enumerate(self.clauses):
            if not body:self.zero.append((head,j))
            for v in body:self.inc[v].append(j)
        self.left=[len(body) for body,head in self.clauses]
    def close(self,seed):
        # Dependency bitsets extract a sound subset of the assumed input tiles.
        left=self.left.copy();proof=[None]*self.n;seen=[False]*self.n;queue=deque();seed=list(dict.fromkeys(seed))
        for i,x in enumerate(seed):proof[x]=1<<i;queue.append(x)
        for x,j in self.zero:
            if proof[x] is None:proof[x]=0;queue.append(x)
        while queue:
            x=queue.popleft()
            if seen[x]:continue
            seen[x]=True
            for j in self.inc[x]:
                left[j]-=1
                if left[j]==0:
                    body,head=self.clauses[j];deps=0
                    for v in body:deps|=proof[v]
                    if head is None:return None,[seed[i] for i in range(len(seed)) if deps>>i&1]
                    if proof[head] is None:proof[head]=deps;queue.append(head)
        return [i for i in range(NW) if seen[i]],None


def accepting_path(allowed):
    aa=set(allowed);queue=deque([0,1]);paths={0:[],1:[]}
    while queue:
        u=queue.popleft()
        for (x,c),(extra,oc,k) in TERMS.items():
            if x==u and k in aa:return paths[u]+[k]
        for q,o,v,k in OUT[u]:
            if k in aa and v not in paths:paths[v]=paths[u]+[k];queue.append(v)
    return None


def build():
    xs=[z3.Bool(f'a{i}') for i in range(NW)];s=z3.Solver();w=[z3.Bool(f'w{i}') for i in range(len(FS))];rank=[z3.BitVec(f'r{i}',6) for i in range(len(FS))]
    s.add(w[0],w[1],rank[0]==0,rank[1]==0);inc=defaultdict(list)
    for k,(u,q,o,v) in enumerate(FE):inc[v].append(z3.And(w[u],xs[k],z3.ULT(rank[u],rank[v])))
    for i in range(2,len(FS)):s.add(z3.Implies(w[i],z3.Or(inc[i])))
    s.add(z3.Or([z3.And(w[x],xs[k]) for (x,c),(extra,oc,k) in TERMS.items()]))
    return s,xs


def run(seconds=60):
    t=time.monotonic();h=Horn();s,xs=build();cores=[];iterations=0;stats=defaultdict(int)
    while time.monotonic()-t<seconds:
        s.set(timeout=max(1,int(1000*(seconds-time.monotonic()+t))));rr=s.check()
        if rr!=z3.sat:
            out=dict(status=str(rr),iterations=iterations,seconds=time.monotonic()-t,cores=cores,histogram=dict(stats),decimal_existence_proved=False)
            if rr==z3.unknown:out['reason']=s.reason_unknown()
            return out
        aa=[i for i in range(NW) if z3.is_true(s.model().eval(xs[i],model_completion=True))];path=accepting_path(aa);assert path is not None
        tiles,core=h.close(path);iterations+=1
        if tiles is not None:
            check=path_and_check(tiles);assert check['nonempty'] and check['safe'] and check['closed']
            return dict(status='certificate',tiles=tiles,independent_check=check,iterations=iterations,seconds=time.monotonic()-t,decimal_existence_proved=True)
        assert core
        # Greedy deletion is unnecessary for soundness, but makes the learnt clause stronger.
        for k in core.copy():
            test=[j for j in core if j!=k];_,smaller=h.close(test)
            if smaller is not None:core=smaller
        s.add(z3.Or([z3.Not(xs[k]) for k in core]));cores.append(core);stats[len(core)]+=1
        if iterations%50==0:print('progress',iterations,round(time.monotonic()-t,3),dict(stats),flush=True)
    return dict(status='time',iterations=iterations,seconds=time.monotonic()-t,cores=cores,histogram=dict(stats),decimal_existence_proved=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=60);args=p.parse_args();out=run(args.seconds);json.dump(out,open('exist_tile_lazy_results.json','w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='cores'},indent=2))
