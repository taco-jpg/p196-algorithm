"""Exact finite-clock extension of full-carry tile grammar closure.

Allowed tile sets may differ at every phase modulo P. All-length closure is
checked from each phase to its successor. Horn propagation is exact and has
no numeral-width or iteration cutoff. A conflict rules out only this grammar
class for the specified phase count and seed.
"""
from exist_tile_horn import *
from array import array

class Phases:
    def __init__(self):
        self.n,self.clauses,self.meta=horn_clauses();self.m=len(self.clauses);self.inc=[[] for _ in range(self.n)];self.zero=[]
        self.left=array('B')
        for j,(body,head) in enumerate(self.clauses):
            self.left.append(len(body))
            if not body:self.zero.append(head)
            for v in body:self.inc[v].append(j)
    def close(self,seed,period):
        t=time.monotonic();left=self.left*period;seen=bytearray(self.n*period);queue=deque()
        for phase in range(period):queue.extend(phase*self.n+x for x in self.zero)
        queue.extend(history_path(seed));derived=0;tiles=0
        while queue:
            x=queue.popleft()
            if seen[x]:continue
            seen[x]=1;derived+=1;phase,local=divmod(x,self.n)
            if local<NW:tiles+=1
            for j in self.inc[local]:
                jj=phase*self.m+j;left[jj]-=1
                if not left[jj]:
                    body,head=self.clauses[j]
                    if head is None:return dict(period=period,status='conflict',conflict_phase=phase,clause=j,derived=derived,tiles=tiles,seconds=time.monotonic()-t,decimal_existence_proved=False)
                    target=(phase+1)%period if head<NW else phase
                    y=target*self.n+head
                    if not seen[y]:queue.append(y)
        return dict(period=period,status='candidate',allowed_tiles=[[k for k in range(NW) if seen[p*self.n+k]] for p in range(period)],derived=derived,tiles=tiles,seconds=time.monotonic()-t,decimal_existence_proved=False)

if __name__=='__main__':
    pp=Phases();out=[]
    for name,seed in [('196',((7,),18)),('18887',((8,16),16))]:
        for p in [1,2,3,4,5,6,7,8,11,12,16,24,32,48,64,96,128]:
            rr=pp.close(seed,p);rr['seed_name']=name;rr['seed']=seed;out.append(rr);print(json.dumps({k:v for k,v in rr.items() if k!='allowed_tiles'}),flush=True)
            json.dump(out,open('exist_tile_phases_results.json','w'),indent=2)
