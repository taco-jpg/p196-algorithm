from exist_uniform_outer import graph
import json,time

def clocks(p,g):
 qs,es=graph(1);out=[set() for q in qs]
 for u,v,c,b in es:out[u].add((v,(1-c)//2))
 mask=(1<<p)-1
 def canonical(w):return min(((w<<i)|(w>>(p-i)))&mask for i in range(p))
 accepted=set();calls=0
 def dfs(start,u,t,h,w):
  nonlocal calls
  calls+=1
  if h>g or h+p-t<g:return
  if t==p:
   if u==start and h==g:accepted.add(canonical(w))
   return
  for v,b in out[u]:dfs(start,v,t+1,h+b,(w<<1)|b)
 for start in range(len(qs)):dfs(start,start,0,0,0)
 return sorted(accepted),calls
if __name__=='__main__':
 st=time.monotonic();ws,c=clocks(24,9)
 out={'period':24,'growth':9,'necklaces':len(ws),'calls':c,'seconds':time.monotonic()-st,'clocks':[list(map(int,f'{w:024b}')) for w in ws]}
 json.dump(out,open('exist_uniform_outer_clocks_results.json','w'),indent=2)
 print({k:v for k,v in out.items() if k!='clocks'})
