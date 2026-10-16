"""Complete seven-necklace catalog of eight-step/three-overflow clocks."""
import itertools,json
from exist_uniform_slow_forward import run

def necklaces(p,g):
 out=set()
 for ps in itertools.combinations(range(p),g):
  a=tuple(int(i in ps) for i in range(p))
  out.add(min(a[j:]+a[:j] for j in range(p)))
 return sorted(out)

def segments(clock):
 # Canonical representative always starts with zero and ends in one here.
 assert clock[-1]==1
 ps=[];n=0
 for h in clock:
  n+=1
  if h:ps.append(n);n=0
 assert n==0
 return tuple(ps)
if __name__=='__main__':
 out=[]
 for clock in necklaces(8,3):
  ps=segments(clock)*3;r=run(ps,cap=100000,seconds=3);r['clock']=clock
  out.append(r);print(json.dumps(r),flush=True)
  json.dump(out,open('exist_uniform_clock8_catalog_results.json','w'),indent=2)
