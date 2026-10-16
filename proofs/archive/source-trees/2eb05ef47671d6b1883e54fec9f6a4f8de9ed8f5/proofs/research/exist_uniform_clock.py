"""Necessary free-clock exterior search using exact three-pair arithmetic."""
import z3 as z,json,time
from continuation_brown_boolean import trans,v,v4,v1

def search(p,g,k=3,timeout=3000,clock=None):
 s=z.SolverFor('QF_BV');s.set(timeout=timeout)
 q=[[z.BitVec(f'q_{t}_{i}',5) for i in range(k)] for t in range(p)]
 h=[]
 for t in range(p):
  for a in q[t]:s.add(z.ULE(a,18))
  s.add(q[t][0]!=0)
  c=z.BoolVal(False);lo=[]
  for a in q[t]:d,c=trans(a,c);lo.append(z.ZeroExt(1,d))
  c=z.Bool(f'inner_{t}');hi=[None]*k
  for i in range(k-1,-1,-1):d,c=trans(q[t][i],c);hi[i]=z.ZeroExt(1,d)
  h.append(c)
  for i in range(k):
   o=lo[0]+1 if i==0 else lo[i]+hi[i-1]
   n=lo[i]+hi[i]
   s.add(q[(t+1)%p][i]==z.If(c,o,n))
  if clock is not None:s.add(c==bool(clock[t]))
 w=(p+1).bit_length()
 s.add(sum([z.If(a,z.BitVecVal(1,w),z.BitVecVal(0,w)) for a in h],z.BitVecVal(0,w))==g)
 st=time.monotonic();r=s.check();out={'period':p,'growth':g,'pairs':k,'result':str(r),'seconds':time.monotonic()-st}
 if r==z.sat:
  m=s.model();out['q']=[[m.eval(a).as_long() for a in row] for row in q];out['clock']=[int(z.is_true(m.eval(a))) for a in h]
 return out
if __name__=='__main__':
 out=[]
 for p,g in [(8,3),(18,9),(24,9),(30,9),(42,18),(48,18)]:
  r=search(p,g);print(json.dumps(r),flush=True);out.append(r)
 json.dump(out,open('exist_uniform_clock_results.json','w'),indent=2)
