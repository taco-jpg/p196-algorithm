"""Replay complete clock catalog and spatial closures with independent C++ arithmetic.

Build first:
  g++ -O3 -std=c++17 exist_uniform_spatial_check.cpp -o exist_uniform_spatial_check
"""
import json,subprocess,time
from pathlib import Path
def segments(clock):
    assert clock[-1] == 1
    ps = []; length = 0
    for h in clock:
        length += 1
        if h: ps.append(length); length = 0
    assert length == 0
    return tuple(ps)

def main():
 st=time.monotonic()
 catalog=json.loads(subprocess.check_output(['./exist_uniform_spatial_check','--clock-catalog']))
 py=json.load(open('exist_uniform_outer_clocks_results.json'))
 assert catalog['count']==len(catalog['clocks'])==1077
 assert catalog['clocks']==[''.join(map(str,x)) for x in py['clocks']]
 completed={}
 for f in ['exist_uniform_period24_catalog_results.json','exist_uniform_period24_refine_results.json','exist_uniform_period24_deep_results.json','exist_uniform_independent_spatial_results.json']:
  for row in json.load(open(f)):
   if row['complete']:completed[tuple(row['periods'])]=row
 results=[]
 for i,word in enumerate(catalog['clocks']):
  periods=segments(tuple(map(int,word)))
  row=json.loads(subprocess.check_output(['./exist_uniform_spatial_check','15','2000000']+list(map(str,periods))))
  assert row['complete'] and row['found'] is None and row['cyclic_remainder']==0,row
  old=completed[periods]
  for key in ('states','edges','maxdepth'):assert row[key]==old[key],(periods,key,row[key],old[key])
  results.append(row)
  if (i+1)%200==0:print(json.dumps({'verified':i+1,'seconds':time.monotonic()-st}),flush=True)
 summary={'period':24,'growth':9,'clock_necklaces':1077,'all_complete':True,'all_acyclic':True,'uniform_target_reached':False,'independent_clock_catalog_match':True,'independent_spatial_count_matches':1077,'total_states':sum(r['states'] for r in results),'total_edges':sum(r['edges'] for r in results),'maximum_depth':max(r['maxdepth'] for r in results),'seconds':time.monotonic()-st,'cases':results}
 Path('exist_uniform_period24_verified.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='cases'}),flush=True)
if __name__=='__main__':main()
