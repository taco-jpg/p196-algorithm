"""One exact exterior-graph pass for the four two-pair-compatible bulk clocks."""
import json,subprocess
from exist_uniform_period4_screen import python_graph
from exist_uniform_clock8_catalog import segments

def main():
 data=json.load(open('exist_geom_bulk_two_outer_results.json'));clocks={}
 for i,component in enumerate(data['positive_components']):
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
  json.dump(out,open('exist_uniform_two_outer_screen_results.json','w'),indent=2)
if __name__=='__main__':main()
