"""Candidate search only. SAT requires separate unbounded-family proof."""
import z3,json,time
from resume_renewal_bulk import transform

def search(k,j,center,seconds=12,W=(13,13,16),period=12):
 s=z3.SolverFor('QF_LIA');s.set(timeout=1000*seconds)
 P=[z3.Int('p%d'%i) for i in range(k)]
 C=[z3.Int('c%d'%i) for i in range(j)]
 c=z3.Int('center') if center else None
 for v in P+C+([c] if center else []):s.add(0<=v,v<=18)
 if center:s.add(c%2==0)
 s.add(P[0]==8)
 mid=C+([c] if center else [])+C[::-1]
 for m in [2,3]:
  left=P+list(W)*m
  q=left+mid+left[::-1]
  for t in range(period):
   h=t%2
   s.add(q[0]==(17 if h else 8))
   carr=[z3.Int('b_%s_%s_%s'%(m,t,i)) for i in range(len(q)+1)]
   s.add(carr[0]==0,carr[-1]==h)
   out=[]
   for i,a in enumerate(q):
    s.add(carr[i+1]>=0,carr[i+1]<=1)
    d=z3.Int('d_%s_%s_%s'%(m,t,i));s.add(0<=d,d<=9,d==a+carr[i]-10*carr[i+1]);out.append(d)
   if h:out.append(z3.IntVal(1))
   q=[out[i]+out[-1-i] for i in range(len(out))]
  left=P+list(W)*(m+1)
  target=left+mid+left[::-1]
  assert len(q)==len(target)
  for a,b in zip(q,target):s.add(a==b)
 t=time.time();status=s.check();data={'prefix':k,'middle_pairs':j,'odd':center,'word':W,'status':str(status),'seconds':time.time()-t}
 if status==z3.sat:
  model=s.model();data['P']=[model.eval(v).as_long() for v in P];data['C']=[model.eval(v).as_long() for v in C];data['center']=model.eval(c).as_long() if center else None
 print(json.dumps(data),flush=True);return data
if __name__=='__main__':
 result=[]
 for k,j in [(1,0),(2,0),(2,1),(3,1),(4,2),(6,3),(8,4)]:
  for odd in [False,True]:
   for W in [(13,13,16),(13,16,13),(16,13,13)]:
    r=search(k,j,odd,W=W);result.append(r)
    json.dump(result,open('resume_renewal_family_results.json','w'),indent=2)
    if r['status']=='sat':raise SystemExit
