from persist_arithmetic_signed_core import *
import time,random
random.seed(196)
start=time.monotonic();best=0;records=[]
for c in [6,8,10,12,16,24,32,48,64,96,128,256,512]:
 hist={};locbest=0
 for j in range(20000):
  C=random.randrange(10**c)
  rows=run(c,C,110);k=sum(x[-1] for x in rows)
  hist[k]=hist.get(k,0)+1;locbest=max(locbest,k)
  if k>best:
   best=k;records.append(dict(c=c,C=str(C),steps=k))
   print('record',records[-1],flush=True)
 print('width',c,'best',locbest,'time',round(time.monotonic()-start,2),flush=True)
 with open('persist_arithmetic_signed_search_results.json','w') as f:json.dump(dict(records=records,lastwidth=c,seconds=time.monotonic()-start),f,indent=2)
