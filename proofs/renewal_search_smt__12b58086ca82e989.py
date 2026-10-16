import z3 as Z, json,itertools,time,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from renewal_search_scan import qstep,balance,m

def solve(L0,C0,hs,timeout=1500):
 s=Z.Solver();s.set(timeout=timeout);qs=[];cs=[];ds=[];L=L0
 for t in range(len(hs)+1):
  C=C0+t
  q=[Z.Int(f'q{t}_{i}') for i in range(L)];qs.append(q)
  s.add(q[0]>0)
  s.add(*[Z.And(x>=0,x<=18) for x in q])
  s.add(*[q[i]==q[L-1-i] for i in range(L//2)])
  if L%2:s.add(q[L//2]%2==0)
  s.add(*[Z.Sum(q[j::C])==18 for j in range(C)])
  if t==len(hs):break
  h=hs[t];c=[Z.Int(f'c{t}_{i}') for i in range(L+1)];cs.append(c)
  s.add(c[0]==0,c[-1]==h)
  s.add(*[Z.And(x>=0,x<=1) for x in c])
  d=[q[i]+c[i]-10*c[i+1] for i in range(L)]
  s.add(*[Z.And(x>=0,x<=9) for x in d])
  if h:d.append(Z.IntVal(1))
  ds.append(d);L+=h
 for t,d in enumerate(ds):
  s.add(*[qs[t+1][i]==d[i]+d[-1-i] for i in range(len(d))])
 r=s.check()
 if r!=Z.sat:return str(r)
 md=s.model();qq=[tuple(md.eval(x).as_long() for x in q) for q in qs]
 for i in range(len(hs)):
  assert qstep(qq[i])[0]==qq[i+1]
  assert balance(qq[i]) is not None and qstep(qq[i])[1]!=qstep(qq[i])[1][::-1]
 return dict(L0=L0,C0=C0,hs=hs,q=qq,walls=[balance(q) for q in qq])

def main():
 T=time.monotonic();counts={};witnesses=[]
 # Exactly three consecutive +1 renewals, across all overflow schedules.
 for L0 in range(10,21):
  for C0 in range(3,min(9,L0-2)):
   for hs in itertools.product([0,1],repeat=3):
    if time.monotonic()-T>45:
     out={'counts':counts,'witnesses':witnesses,'cutoff':[L0,C0,hs],'seconds':time.monotonic()-T};Path(__file__).with_name('renewal_search_smt_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));return
    r=solve(L0,C0,hs,350)
    if isinstance(r,str):counts[r]=counts.get(r,0)+1
    else:
     counts['sat']=counts.get('sat',0)+1;witnesses.append(r)
     out={'counts':counts,'witnesses':witnesses,'seconds':time.monotonic()-T};Path(__file__).with_name('renewal_search_smt_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));return
 print(counts)
if __name__=='__main__':main()
