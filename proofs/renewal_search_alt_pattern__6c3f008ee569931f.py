import sys,json
from pathlib import Path
import z3 as Z
sys.path.insert(0,str(Path(__file__).parent))
from renewal_search_scan import *

def solve(m0):
 C=4*m0+2;L=3*C-1;D=3*C//2
 support={2*i for i in range(m0)}
 support|={L-1-i for i in support};support.add(L//2)
 c=[0]+[int(i in support) for i in range(L)]
 s=Z.Solver();s.set(timeout=1000)
 q=[Z.Int(f'q{i}') for i in range(L)]
 s.add(q[0]==10)
 s.add(*[Z.And(x>=0,x<=18) for x in q])
 s.add(*[q[i]==q[L-1-i] for i in range(L//2)],q[L//2]%2==0)
 s.add(*[Z.Sum(q[j::C])==18 for j in range(C)])
 d=[q[i]+c[i]-10*c[i+1] for i in range(L)]+[1]
 s.add(*[Z.And(x>=0,x<=9) for x in d]);qq=[d[i]+d[-1-i] for i in range(len(d))]
 s.add(*[qq[j]+qq[j+D]==18 for j in range(D)])
 r=s.check()
 if r!=Z.sat:return {'m':m0,'status':str(r)}
 md=s.model();q=tuple(md.eval(x).as_long() for x in q);Q,d=qstep(q)
 return {'m':m0,'status':'sat','q':q,'halfq':q[:L//2+1],'W':balance(q)[0],'newW':balance(Q)[0]}
out=[solve(k) for k in range(1,11)]
Path(__file__).with_name('renewal_search_alt_pattern_results.json').write_text(json.dumps(out,indent=2))
for r in out:print({k:v for k,v in r.items() if k not in ['q','W']})
