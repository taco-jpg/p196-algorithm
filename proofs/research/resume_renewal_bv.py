"""Search finite-boundary matches to a specified nonneutral periodic bulk."""
import z3,json,time

def search(k,j,odd,seconds=8,W=(3,10,15,8),period=16):
 s=z3.SolverFor('QF_BV');s.set(timeout=1000*seconds)
 bv=lambda x:z3.BitVecVal(x,5)
 P=[z3.BitVec('p%d'%i,5) for i in range(k)]
 C=[z3.BitVec('c%d'%i,5) for i in range(j)]
 c=z3.BitVec('center',5) if odd else None
 for v in P+C+([c] if odd else []):s.add(z3.ULE(v,bv(18)))
 if odd:s.add(c&bv(1)==bv(0))
 s.add(P[0]==8)
 mid=C+([c] if odd else [])+C[::-1]
 # 8 bulk cells: possible interfaces remain independent over the temporal period.
 for m in [5]:
  left=P+[bv(x) for x in W]*m
  q=left+mid+left[::-1]
  for t in range(period):
   h=t%2
   s.add(q[0]==(17 if h else 8))
   carry=bv(0);out=[]
   for i,a in enumerate(q):
    cout=z3.If(z3.UGE(a+carry,bv(10)),bv(1),bv(0))
    d=z3.BitVec('d_%s_%s_%s'%(m,t,i),5)
    s.add(d==a+carry-bv(10)*cout);out.append(d);carry=cout
   s.add(carry==h)
   if h:out.append(bv(1))
   q=[out[i]+out[-1-i] for i in range(len(out))]
  left=P+[bv(x) for x in W]*(m+1)
  target=left+mid+left[::-1]
  assert len(q)==len(target)
  s.add(*[a==b for a,b in zip(q,target)])
 t=time.time();status=s.check();data={'prefix':k,'middle_pairs':j,'odd':odd,'word':W,'status':str(status),'seconds':time.time()-t}
 if status==z3.sat:
  model=s.model();data['P']=[model.eval(v).as_long() for v in P];data['C']=[model.eval(v).as_long() for v in C];data['center']=model.eval(c).as_long() if odd else None
 print(json.dumps(data),flush=True);return data
if __name__=='__main__':
 result=[]
 for k,j in [(1,0),(2,1),(4,2),(6,3),(8,4),(12,6)]:
  for odd in [False,True]:
   for W in [(3,10,15,8),(15,10,3,8),(10,15,8,3),(10,3,8,15)]:
    r=search(k,j,odd,W=W);result.append(r)
    json.dump(result,open('resume_renewal_bv_results.json','w'),indent=2)
    if r['status']=='sat':raise SystemExit
