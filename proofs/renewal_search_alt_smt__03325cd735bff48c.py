import sys,json,time
from pathlib import Path
import z3 as Z
sys.path.insert(0,str(Path(__file__).parent))
from renewal_search_scan import *

def solve(L,C,h,phase,timeout=500):
 s=Z.Solver();s.set(timeout=timeout)
 D=3*C//2;q=[Z.Int(f'q{i}') for i in range(L)]
 c=[Z.Int(f'c{i}') for i in range(L+1)]
 s.add(q[0]>0,c[0]==0,c[-1]==h)
 s.add(*[Z.And(x>=0,x<=18) for x in q]);s.add(*[Z.And(x>=0,x<=1) for x in c])
 s.add(*[q[i]==q[L-1-i] for i in range(L//2)])
 if L%2:s.add(q[L//2]%2==0)
 s.add(*[Z.Sum(q[j::C])==18 for j in range(C)])
 s.add(*[Z.Sum(c[j+1::C])==1-(j+phase)%2 for j in range(C)])
 d=[q[i]+c[i]-10*c[i+1] for i in range(L)]
 s.add(*[Z.And(x>=0,x<=9) for x in d])
 if h:d.append(Z.IntVal(1))
 qq=[d[i]+d[-1-i] for i in range(len(d))]
 s.add(*[Z.Sum(qq[j::D])==18 for j in range(D)])
 r=s.check()
 if r!=Z.sat:return str(r)
 md=s.model();q=tuple(md.eval(x).as_long() for x in q)
 Q,d=qstep(q)
 return {'L':L,'C':C,'h':h,'phase':phase,'q':q,'wall':balance(q),'nextwall':balance(Q),'d':d,'pal':d==d[::-1]}

def run():
 T=time.monotonic();cnt=Counter();trials=[];sat=[]
 for C in range(2,13,2):
  for L in range(C,3*C+5):
   for h in [0,1]:
    for phase in [0,1]:
     r=solve(L,C,h,phase)
     trials.append([L,C,h,phase,r if isinstance(r,str) else 'sat'])
     if isinstance(r,str):cnt[r]+=1
     else:cnt['sat']+=1;sat.append(r)
     if sat or time.monotonic()-T>40:
      res={'counts':dict(cnt),'sat':sat,'trials':trials,'seconds':time.monotonic()-T};Path(__file__).with_name('renewal_search_alt_smt_results.json').write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='trials'},indent=2));return
 print(dict(cnt))
if __name__=='__main__':run()
