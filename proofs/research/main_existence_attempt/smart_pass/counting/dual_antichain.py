import json,time,pickle,gzip
from pathlib import Path
from functools import lru_cache
p=Path(__file__).with_name('compact_transitions.txt');tau=[list(map(int,line.split())) for line in p.read_text().splitlines()];N=len(tau)
@lru_cache(100000)
def move(s,y):
 out=0
 for v in range(N):
  a,b=tau[v][y],tau[v][y+8]
  if a>=0 and b>=0 and(s>>a&1)and(s>>b&1):out|=1<<v
 return out

def maximal(xs):
 xs=sorted(set(xs),key=lambda x:(-x.bit_count(),-x));out=[]
 if len(xs)<500:
  for v in xs:
   if not any(v&w==v for w in out):out.append(v)
  return tuple(sorted(out))
 size=(len(xs)+7)//8;raw=[bytearray(size) for _ in range(N)]
 for i,v in enumerate(xs):
  while v:
   b=v&-v;v-=b;raw[b.bit_length()-1][i//8]|=1<<(i%8)
 indices=[int.from_bytes(v,'little') for v in raw];order=sorted(range(N),key=lambda b:indices[b].bit_count());prefix=0
 for i,v in enumerate(xs):
  candidates=prefix
  for b in order:
   if v>>b&1:
    candidates &= indices[b]
    if not candidates:break
  if not candidates:out.append(v)
  prefix=(prefix<<1)|1
 return tuple(sorted(out))

front=((1<<N)-1,);seen={front:0};levels=[front];t0=time.time()
for k in range(1,101):
 raw={move(s,y) for s in front for y in range(8)}
 print('raw',k,len(raw),flush=True)
 front=maximal(raw);print('level',k,'size',len(front),'bits',min(map(int.bit_count,front)),max(map(int.bit_count,front)),'seconds',time.time()-t0,flush=True)
 levels.append(front)
 with gzip.open(Path(__file__).with_name('dual_antichain_checkpoint.pkl.gz'),'wb') as f:pickle.dump((k,front,[(len(v),min(map(int.bit_count,v)),max(map(int.bit_count,v))) for v in levels]),f)
 if front==(0,):
  result=dict(status='extinction',depth=k,levels=levels,seconds=time.time()-t0);break
 if front in seen:
  result=dict(status='repeat',depth=k,previous=seen[front],levels=levels,seconds=time.time()-t0);break
 if len(front)>2000000:
  result=dict(status='capped',depth=k,size=len(front),seconds=time.time()-t0);break
 seen[front]=k
else:result=dict(status='horizon',depth=k,seconds=time.time()-t0)
json.dump(result,open(Path(__file__).with_name('dual_antichain.json'),'w'))
print({k:v for k,v in result.items() if k!='levels'},flush=True)
