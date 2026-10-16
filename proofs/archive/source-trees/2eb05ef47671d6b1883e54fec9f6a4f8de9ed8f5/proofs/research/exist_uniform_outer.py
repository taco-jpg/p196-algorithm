"""Exact finite exterior graph for arbitrary inner carry; no inner completion assumed."""
import itertools, json

def trans(q,b):
 c=0;lo=[]
 for a in q:
  lo.append((a+c)%10);c=(a+c)//10
 c=b;hi=[0]*len(q)
 for i in range(len(q)-1,-1,-1):
  hi[i]=(q[i]+c)%10;c=(q[i]+c)//10
 h=c
 if h:r=(lo[0]+1,)+tuple(lo[i]+hi[i-1] for i in range(1,len(q)))
 else:r=tuple(a+b for a,b in zip(lo,hi))
 return r,h

def graph(k):
 qs=list(itertools.product(range(19),repeat=k))
 qs=[q for q in qs if q[0]>0]
 ids={q:i for i,q in enumerate(qs)}
 edges=[]
 for q in qs:
  for b in (0,1):
   r,h=trans(q,b)
   if r in ids:edges.append((ids[q],ids[r],1-2*h,b))
 return qs,edges

def critical(k):
 qs,edges=graph(k);dist=[0]*len(qs)
 for iteration in range(len(qs)):
  changed=False
  for u,v,c,b in edges:
   if dist[v]>dist[u]+c:dist[v]=dist[u]+c;changed=True
  if not changed:break
 else:raise RuntimeError('negative cycle')
 zero=[(u,v,c,b) for u,v,c,b in edges if dist[v]==dist[u]+c]
 # Iteratively prune sources/sinks; every directed-cycle vertex remains.
 live=set(range(len(qs)))
 while True:
  out={u for u,v,c,b in zero if u in live and v in live};inc={v for u,v,c,b in zero if u in live and v in live}
  new=live&out&inc
  if new==live:break
  live=new
 ze=[(qs[u],qs[v],c,b) for u,v,c,b in zero if u in live and v in live]
 return {'width':k,'states':len(qs),'edges':len(edges),'iterations':iteration+1,'critical_vertices':[qs[u] for u in sorted(live)],'critical_edges':ze}
if __name__=='__main__':
 out=[critical(k) for k in (1,2,3)]
 json.dump(out,open('exist_uniform_outer_results.json','w'),indent=2)
 for r in out:print(json.dumps(r))
