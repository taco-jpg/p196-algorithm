import sys,json,time
from collections import Counter
from pathlib import Path
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
from renewal_search_scan import *
r=[]
for n in ('scan','half4'):
 r+=json.load(open(BASE / ('renewal_search_'+n+'_results.json')))['events']
res=[];hist=Counter();seen=set()
for ev in r:
 q=m.difference_word(ev['W'],ev['C']);key=q
 if key in seen:continue
 seen.add(key);lost=False;returns=[];oldC=ev['C'];chain=0;streak=0
 for t in range(250):
  Q,d=qstep(q);z=balance(Q)
  if d==d[::-1]:break
  if z and lost:
   returns.append({'t':t+1,'C':z[1],'W':z[0]});lost=False
  if z:
   if z[1]>oldC:chain+=1
  else:lost=True
  q=Q;oldC=sum(q)//18
 hist[('pal' if d==d[::-1] else 'capped')]+=1
 if returns:res.append({'seed':ev,'delayed_returns':returns,'steps':t+1,'pal':d==d[::-1],'safe_renewals':chain})
out={'seeds':len(seen),'outcomes':dict(hist),'returned':res}
open(BASE / 'renewal_search_delayed_results.json','w').write(json.dumps(out,indent=2))
print(json.dumps({'seeds':len(seen), 'outcomes':dict(hist), 'seeds_with_delayed_returns':len(res), 'delayed_events':sum(len(x['delayed_returns']) for x in res)},indent=2))
