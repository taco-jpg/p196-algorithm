from itertools import product
import json

def bulk_step(B,h):
 r=len(B)
 if all(x==9 for x in B):return {tuple([x]*r) for x in [0,9,18]}
 backward=[];forward=[]
 for i,x in enumerate(B):
  a=next(B[(i-d)%r] for d in range(1,r+1) if B[(i-d)%r]!=9)
  b=next(B[(i+d)%r] for d in range(1,r+1) if B[(i+d)%r]!=9)
  cb=int(a>=10);cf=int(b>=10)
  backward.append((x+cb)%10);forward.append((x+cf)%10)
 return {tuple(backward[i]+forward[(i-h)%r] for i in range(r))}

def candidates(r,sched):
 result=[]
 for B in product(range(19),repeat=r):
  states={B}
  for h in sched:states={v for U in states for v in bulk_step(U,h)}
  if B in states:result.append(B)
 return result
if __name__=='__main__':
 out=[]
 for r,schedules in [(2,[[0,1]*4,[1,0]*4]),(3,[[0,1]*6,[1,0]*6]),(2,[[int((i+phase)%3==0) for i in range(12)] for phase in range(3)])]:
  for sched in schedules:
   C=candidates(r,sched);rec={'blocklen':r,'schedule':sched,'candidates':C};out.append(rec);print(json.dumps(rec),flush=True)
 open('family_search_bulk_periods_results.json','w').write(json.dumps(out,indent=2))
