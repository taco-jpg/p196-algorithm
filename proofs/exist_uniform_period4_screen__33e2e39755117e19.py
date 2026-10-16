"""Exact clock-only exterior screen for the geometry agent's periodic cores."""
import json,subprocess
from exist_uniform_clock8_catalog import segments
from continuation_theory_multigrowth import transitions
from collections import deque

def python_graph(periods):
 g=len(periods);start=((1,)*g,tuple(1<<(p-1) for p in periods),(0,)*g)
 seen={start:0};queue=deque([start]);edges=0;depth=0
 while queue:
  s=queue.popleft();depth=max(depth,seen[s])
  for ns,dp in transitions(10,periods,s):
   edges+=1
   if ns not in seen:seen[ns]=seen[s]+1;queue.append(ns)
 return len(seen),edges,depth

def main():
 data=json.load(open('exist_geom_periodic_bulk_graph_results.json'))
 clocks={}
 for i,component in enumerate(data['outer_control_product']['positive_components']):
  for j,cycle in enumerate(component['cycles']):
   c=tuple(cycle['clock']);c=min(c[k:]+c[:k] for k in range(len(c)))
   clocks.setdefault(c,[]).append((i,j))
 out=[]
 for c,origins in clocks.items():
  ps=segments(c)
  row=json.loads(subprocess.check_output(['./exist_uniform_spatial_check','5','1000000']+list(map(str,ps))))
  row['origins']=origins;row['clock']=c
  if row['complete'] and row['states']<=20000:
   py=python_graph(ps);assert py==(row['states'],row['edges'],row['maxdepth']);row['python_counts_match']=True
  out.append(row);print(json.dumps(row),flush=True)
  json.dump(out,open('exist_uniform_period4_screen_results.json','w'),indent=2)
if __name__=='__main__':main()
