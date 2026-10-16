from exist_uniform_slow_forward import run
import json,time
if __name__=='__main__':
 base=json.load(open('exist_uniform_period24_catalog_results.json'));pending=[r for r in base if not r['complete']]
 out=[];st=time.monotonic()
 for i,old in enumerate(pending):
  r=run(old['periods'],cap=50000,seconds=0.3);r['clock']=old['clock'];out.append(r)
  if r['found'] is not None:print('FOUND',json.dumps(r),flush=True);break
  if i%10==9:print(json.dumps({'done':i+1,'complete':sum(a['complete'] for a in out),'incomplete':sum(not a['complete'] for a in out),'seconds':time.monotonic()-st}),flush=True)
 json.dump(out,open('exist_uniform_period24_refine_results.json','w'),indent=2)
 print(json.dumps({'done':len(out),'complete':sum(a['complete'] for a in out),'incomplete':sum(not a['complete'] for a in out),'seconds':time.monotonic()-st}))
