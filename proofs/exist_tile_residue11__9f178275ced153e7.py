"""Full-carry-tile languages strengthened by digit-sum residue and width parity.

At time t, each accepted word must have half its symmetric q sum congruent to
r_t mod 9; r_{t+1}=2*r_t mod 9. Distinct even/odd languages are propagated,
with overflow changing parity exactly. All-width projection is a finite
residue-product reachability computation, not sampled word enumeration.
"""
from exist_tile_timevarying import *

class Residue:
    def __init__(self):
        self.states,self.edges,self.terms=composed_tiles();self.adj=defaultdict(list);self.end=defaultdict(list)
        for u,v,a,b in self.edges:self.adj[u].append((v,a,b))
        for u,a,extra,b in self.terms:self.end[u].append((a,extra,b))
        self.sstates,self.sinitial,se,st=trim(safety_graph());self.sadj=defaultdict(list);self.send=defaultdict(list)
        for u,v,cost in se:self.sadj[u].append((v,next(iter(cost))))
        for u,cost in st:self.send[u].append(next(iter(cost)))
    def safety(self,aa,parity,residue,restrict11):
        paths={(u,0,0,0):[] for u in self.sinitial};todo=deque(paths)
        while todo:
            u,r,j,b=todo.popleft();path=paths[u,r,j,b]
            for k in self.send[u]:
                if k not in aa:continue
                x,c,e,oc=TS[k-len(FE)]
                if (c is not None)!=bool(parity) or (r+(0 if c is None else c//2))%9!=residue:continue
                if restrict11 and c is not None and (j+(1 if b==0 else -1)*c)%11:continue
                w=word_of(path,c);assert set(history_path(w))<=aa and bad(qstep(w));return w
            for v,k in self.sadj[u]:
                if k not in aa:continue
                ns=(v,(r+FE[k][1])%9,(j+2*(1 if b==0 else -1)*FE[k][1])%11,b^1)
                if ns not in paths:paths[ns]=path+[k];todo.append(ns)
        return None
    def image(self,aa,parity,residue,restrict11):
        answers=[{},{}];stats=[]
        for overflow in (0,1):
            initial=[u for u,(x,y) in enumerate(self.states[:4]) if x==overflow]
            fw={(u,0,0,0):[] for u in initial};todo=deque(fw);adj=defaultdict(list);rev=defaultdict(list);ends={}
            while todo:
                u,r,j,bit=todo.popleft()
                for a,extra,b in self.end[u]:
                    if a not in aa:continue
                    x,c,e,oc=TS[a-len(FE)]
                    if (c is not None)!=bool(parity) or (r+(0 if c is None else c//2))%9!=residue:continue
                    if restrict11 and c is not None and (j+(1 if bit==0 else -1)*c)%11:continue
                    ends.setdefault((u,r,j,bit),[]).append((a,extra,b))
                for v,a,b in self.adj[u]:
                    if a not in aa:continue
                    ns=(v,(r+FE[a][1])%9,(j+2*(1 if bit==0 else -1)*FE[a][1])%11,bit^1);adj[u,r,j,bit].append((ns,a,b));rev[ns].append(((u,r,j,bit),a,b))
                    if ns not in fw:fw[ns]=fw[u,r,j,bit]+[a];todo.append(ns)
            bw={u:[term[0][0]] for u,term in ends.items()};todo=deque(bw)
            while todo:
                v=todo.popleft()
                for u,a,b in rev[v]:
                    if u not in bw:bw[u]=[a]+bw[v];todo.append(u)
            target=parity^overflow;ws=answers[target]
            def add(path,outputtiles):
                x,c,e,oc=TS[path[-1]-len(FE)];w=word_of(path[:-1],c);im=qstep(w)
                assert (sum(w[0])+(0 if c is None else c//2))%9==residue
                assert (im[1] is not None)==bool(target)
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

def derive(seed,limit=100,start11=6):
    engine=Residue();p=int(seed[1] is not None);r=(sum(seed[0])+(0 if seed[1] is None else seed[1]//2))%9
    aa=[set(),set()];aa[p]=set(history_path(seed));levels=[];seen={};t0=time.monotonic()
    for t in range(limit):
        key=(t>=start11,r,tuple(sorted(aa[0])),tuple(sorted(aa[1])))
        if key in seen:return dict(seed=seed,status='periodic_candidate',preperiod=seen[key],period=t-seen[key],levels=levels,decimal_existence_proved=False,seconds=time.monotonic()-t0)
        seen[key]=t
        for p in (0,1):
            w=engine.safety(aa[p],p,r,t>=start11)
            if w is not None:return dict(seed=seed,status='obstruction',unsafe_time=t,unsafe=w,unsafe_image=qstep(w),unsafe_residue=r,unsafe_parity=p,levels=levels,decimal_existence_proved=False,seconds=time.monotonic()-t0)
        bb=[{},{}];stats=[]
        for p in (0,1):
            if not aa[p]:continue
            ws,ss=engine.image(aa[p],p,r,t>=start11);stats.append(dict(parity=p,graphs=ss))
            for q in (0,1):
                for k,w in ws[q].items():bb[q].setdefault(k,w)
        rows=[[dict(tile=k,**w) for k,w in sorted(b.items())] for b in bb];levels.append(dict(residue=r,restrict11=t>=start11,rows=rows,stats=stats));aa=[set(b) for b in bb];r=2*r%9
        print('stage',t+1,'residue',r,'tiles',list(map(len,aa)),flush=True)
    return dict(seed=seed,status='incomplete',levels=levels,decimal_existence_proved=False,seconds=time.monotonic()-t0)

if __name__=='__main__':
    for name,seed in [('196',((7,),18)),('18887',((8,16),16))]:
        cc=derive(seed,60,6);cc['mod11_start']=6;json.dump(cc,open(f'exist_tile_residue11_{name}.json','w'),indent=2);print(name,{k:v for k,v in cc.items() if k!='levels'},flush=True)
