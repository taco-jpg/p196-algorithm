"""Exact, explicitly capped forward spatial screening of all scalar-compatible clocks."""
from exist_uniform_slow_forward import run
from exist_uniform_clock8_catalog import segments
import json,time
if __name__=='__main__':
 data=json.load(open('exist_uniform_outer_clocks_results.json'));out=[];start=time.monotonic()
 for i,clock in enumerate(data['clocks']):
  r=run(segments(clock),cap=2000,seconds=0.05);r['clock']=clock;out.append(r)
  if r['found'] is not None:print('FOUND',json.dumps(r),flush=True);break
  if i%100==99:print(json.dumps({'done':i+1,'complete':sum(a['complete'] for a in out),'incomplete':sum(not a['complete'] for a in out),'seconds':time.monotonic()-start}),flush=True)
 json.dump(out,open('exist_uniform_period24_catalog_results.json','w'),indent=2)
 print(json.dumps({'done':len(out),'complete':sum(a['complete'] for a in out),'incomplete':sum(not a['complete'] for a in out),'seconds':time.monotonic()-start}))
