"""Literal finite-center synthesis for the neutral exterior; bounded only.

All decimal column equations are imposed for 22 steps. No periodicity of
the growing center is required. Any SAT model is independently evaluated.
"""
from pathlib import Path
import json,time
import z3
from persist_wake_neutral_center import P,CLOCK,candidate,step11

def solve(width,timeout=15000):
    s=z3.SolverFor('QF_BV');s.set(timeout=timeout)
    vs=[z3.BitVec(f'x{i}',5) for i in range((width+1)//2)]
    for x in vs:s.add(z3.ULE(x,18))
    if width%2:s.add(vs[-1]&1==0)
    if width:s.add(vs[0]!=9)
    core=vs+vs[:width//2][::-1]
    if width%2:core=vs+vs[:-1][::-1]
    assert len(core)==width
    q=list(candidate(core));cut=len(P)+8
    for t,h in enumerate(CLOCK*2):
        carry=0;ds=[]
        for i,x in enumerate(q):
            if isinstance(x,int) and isinstance(carry,int):
                z=x+carry;ds.append(z%10);carry=z//10
            else:
                d=z3.BitVec(f'd{t}_{i}',5);c=z3.Bool(f'c{t}_{i}')
                bit=z3.If(c,z3.BitVecVal(1,5),z3.BitVecVal(0,5))
                s.add(z3.ULE(d,9),d+10*bit==x+carry)
                ds.append(d);carry=bit
        s.add(carry==h)
        if h:ds.append(1)
        q=[a+b for a,b in zip(ds,ds[::-1])]
        if t in (10,21):
            for i,a in enumerate(P+(9,)*8):s.add(q[i]==a)
    start=time.monotonic();status=s.check()
    result={'core_width':width,'status':str(status),'seconds':time.monotonic()-start,
            'timeout_ms':timeout,'encoding':'QF_BV 5-bit arithmetic; all sums <=19',
            'scope':'22-step finite core; initial first core sum != 9'}
    if status==z3.sat:
        model=s.model();half=[model.eval(x).as_long() for x in vs]
        core=half+half[:width//2][::-1] if width%2==0 else half+half[:-1][::-1]
        q=candidate(core);trajectory=[core]
        for _ in range(2):
            q,flags=step11(q)
            assert flags==CLOCK and q[:cut]==P+(9,)*8
            trajectory.append(q[cut:-cut])
        result['core']=core;result['macro_cores']=trajectory
    elif status==z3.unknown:result['reason']=s.reason_unknown()
    return result

if __name__=='__main__':
    results=[]
    for width in (3,7,8,9,10,12,16,20,28,40):
        row=solve(width);results.append(row);print(json.dumps(row),flush=True)
        Path('persist_root_center_sat_results.json').write_text(json.dumps(results,indent=2))
        if row['status']=='sat':break
