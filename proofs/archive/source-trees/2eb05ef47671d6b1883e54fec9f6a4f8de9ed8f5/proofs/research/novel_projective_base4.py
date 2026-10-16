"""Exact bounded-template search; UNSAT is not a global Lychrel result."""
import json
import time
from pathlib import Path
import z3 as z


def search(k, period=18, background=14, outer=8, timeout=10000):
    core = 2 * period + 5
    solver = z.Solver()
    solver.set(timeout=timeout)
    def v(n): return z.BitVecVal(n, 5)
    edge = [v(outer)] + [z.BitVec(f'u_{i}',5) for i in range(1,k)]
    for x in edge: solver.add(z.ULE(x,v(18)))
    solver.add(edge[0] == v(outer))
    q = edge + [v(background)]*core + edge[::-1]
    growth = 0
    for t in range(period):
        L = len(q)
        expected_carry = int(t % 3 == 2)
        c = [v(0)]
        s = []
        for i in range(L):
            if z.is_bv_value(q[i]):
                num=q[i].as_long()
                nxt=v(0) if num<9 else v(1) if num>9 else c[i]
            else:
                nxt=z.BitVec(f"c_{t}_{i}",5)
                solver.add(nxt==z.If(z.UGE(q[i]+c[i],v(10)),v(1),v(0)))
            s.append(z.simplify(q[i]+c[i]-v(10)*nxt))
            c.append(nxt)
        solver.add(c[-1] == v(expected_carry))
        if expected_carry:
            new = [v(1)+s[0]] + [s[i]+s[L-i] for i in range(1,L)] + [v(1)+s[0]]
            growth += 1
        else:
            new = [s[i]+s[L-1-i] for i in range(L)]
        q = []
        for i,b in enumerate(new):
            b=z.simplify(b)
            if z.is_bv_value(b): q.append(b)
            else:
                a=z.BitVec(f'q_{t+1}_{i}',5)
                solver.add(a==b)
                q.append(a)
    target = edge+[v(background)]*(core+growth)+edge[::-1]
    assert len(target)==len(q)
    for a,b in zip(q,target): solver.add(a==b)
    start=time.monotonic()
    result=solver.check()
    out={'width':k,'period':period,'core':core,'outer':outer,'background':background,
         'growth':growth,'status':str(result),'seconds':time.monotonic()-start}
    if result==z.sat:
        model=solver.model()
        out['edge']=[model.eval(x).as_long() for x in edge]
    return out



if __name__=="__main__":
    results=[]
    for k in (4,8,12,16):
        for outer in (2,3):
            r=search(k,period=18,background=6,outer=outer,timeout=12000)
            print(json.dumps(r),flush=True);results.append(r)
            Path("novel_projective_base4_results.json").write_text(json.dumps(results,indent=2))
