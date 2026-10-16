"""Full-carry-tile languages strengthened by digit-sum residue and width parity.

At time t, each accepted word must have half its symmetric q sum congruent to
r_t mod 9; r_{t+1}=2*r_t mod 9. Distinct even/odd languages are propagated,
with overflow changing parity exactly. All-width projection is a finite
residue-product reachability computation, not sampled word enumeration.
"""
from exist_tile_timevarying import *

class Residue:
    def __init__(self,modulus=4):
        assert modulus>=2 and modulus%2==0;self.modulus=modulus;self.half=modulus//2
        self.states,self.edges,self.terms=composed_tiles();self.adj=defaultdict(list);self.end=defaultdict(list)
        for u,v,a,b in self.edges:self.adj[u].append((v,a,b))
        for u,a,extra,b in self.terms:self.end[u].append((a,extra,b))
        self.sstates,self.sinitial,se,st=trim(safety_graph());self.sadj=defaultdict(list);self.send=defaultdict(list)
        for u,v,cost in se:self.sadj[u].append((v,next(iter(cost))))
        for u,cost in st:self.send[u].append(next(iter(cost)))
    def safety(self,aa,parity,residue):
        paths={(u,0,0):[] for u in self.sinitial};todo=deque(paths)
        while todo:
            u,r,z=todo.popleft();path=paths[u,r,z]
            for k in self.send[u]:
                if k not in aa:continue
                x,c,e,oc=TS[k-len(FE)]
                if (2*z+int(c is not None))%self.modulus!=parity or (r+(0 if c is None else c//2))%9!=residue:continue
                w=word_of(path,c);assert set(history_path(w))<=aa and bad(qstep(w));return w
            for v,k in self.sadj[u]:
                if k not in aa:continue
                ns=(v,(r+FE[k][1])%9,(z+1)%self.half)
                if ns not in paths:paths[ns]=path+[k];todo.append(ns)
        return None
    def image(self,aa,parity,residue):
        answers=[{} for _ in range(self.modulus)];stats=[]
        for overflow in (0,1):
            initial=[u for u,(x,y) in enumerate(self.states[:4]) if x==overflow]
            fw={(u,0,0):[] for u in initial};todo=deque(fw);adj=defaultdict(list);rev=defaultdict(list);ends={}
            while todo:
                u,r,z=todo.popleft()
                for a,extra,b in self.end[u]:
                    if a not in aa:continue
                    x,c,e,oc=TS[a-len(FE)]
                    if (2*z+int(c is not None))%self.modulus!=parity or (r+(0 if c is None else c//2))%9!=residue:continue
                    ends.setdefault((u,r,z),[]).append((a,extra,b))
                for v,a,b in self.adj[u]:
                    if a not in aa:continue
                    ns=(v,(r+FE[a][1])%9,(z+1)%self.half);adj[u,r,z].append((ns,a,b));rev[ns].append(((u,r,z),a,b))
                    if ns not in fw:fw[ns]=fw[u,r,z]+[a];todo.append(ns)
            bw={u:[term[0][0]] for u,term in ends.items()};todo=deque(bw)
            while todo:
                v=todo.popleft()
                for u,a,b in rev[v]:
                    if u not in bw:bw[u]=[a]+bw[v];todo.append(u)
            target=(parity+overflow)%self.modulus;ws=answers[target]
            def add(path,outputtiles):
                x,c,e,oc=TS[path[-1]-len(FE)];w=word_of(path[:-1],c);im=qstep(w)
                assert (sum(w[0])+(0 if c is None else c//2))%9==residue
                assert (2*len(im[0])+int(im[1] is not None))%self.modulus==target
                assert (sum(im[0])+(0 if im[1] is None else im[1]//2))%9==2*residue%9
                hp=set(history_path(im))
                for k in outputtiles:
                    assert k in hp
                    if k not in ws:ws[k]=dict(input=w,image=im,input_parity=parity,output_parity=target)
            for u,ee in adj.items():
                for v,a,b in ee:
                    if v in bw and b not in ws:add(fw[u]+[a]+bw[v],[b])
            for u,tt in ends.items():
                for a,extra,b in tt:add(fw[u]+[a],[b] if extra is None else [extra,b])
            stats.append(dict(overflow=overflow,reachable=len(fw),cofinal=len(bw),edges=sum(map(len,adj.values()))))
        return answers,stats

def derive(seed,limit=100,modulus=4):
    engine=Residue(modulus);p=(2*len(seed[0])+int(seed[1] is not None))%modulus;r=(sum(seed[0])+(0 if seed[1] is None else seed[1]//2))%9
    aa=[set() for _ in range(modulus)];aa[p]=set(history_path(seed));levels=[];seen={};t0=time.monotonic()
    for t in range(limit):
        key=(r,tuple(tuple(sorted(a)) for a in aa))
        if key in seen:return dict(seed=seed,status='periodic_candidate',preperiod=seen[key],period=t-seen[key],levels=levels,decimal_existence_proved=False,seconds=time.monotonic()-t0)
        seen[key]=t
        for p in range(modulus):
            w=engine.safety(aa[p],p,r)
            if w is not None:return dict(seed=seed,status='obstruction',unsafe_time=t,unsafe=w,unsafe_image=qstep(w),unsafe_residue=r,unsafe_parity=p,levels=levels,decimal_existence_proved=False,seconds=time.monotonic()-t0)
        bb=[{} for _ in range(modulus)];stats=[]
        for p in range(modulus):
            if not aa[p]:continue
            ws,ss=engine.image(aa[p],p,r);stats.append(dict(parity=p,graphs=ss))
            for q in range(modulus):
                for k,w in ws[q].items():bb[q].setdefault(k,w)
        rows=[[dict(tile=k,**w) for k,w in sorted(b.items())] for b in bb];levels.append(dict(residue=r,rows=rows,stats=stats));aa=[set(b) for b in bb];r=2*r%9
        print('stage',t+1,'residue',r,'tiles',list(map(len,aa)),flush=True)
    return dict(seed=seed,status='incomplete',levels=levels,decimal_existence_proved=False,seconds=time.monotonic()-t0)

if __name__=='__main__':
    for modulus in (4,8,16,32):
        name='196';seed=((7,),18);cc=derive(seed,60,modulus);cc['length_modulus']=modulus;json.dump(cc,open(f'exist_tile_length_residue_{name}_{modulus}.json','w'),indent=2);print(name,modulus,{k:v for k,v in cc.items() if k!='levels'},flush=True)
