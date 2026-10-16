"""Synthesize finite centers using exact signed-core decimal column equations.

The opposite incoming/outgoing carries at every step preserve the neutral
annuli. Each overflow appends the appropriate neutral high digit to the core.
SAT witnesses are independently checked by ordinary integer arithmetic.
"""
import json,time
from pathlib import Path
import z3
from persist_arithmetic_signed_core import CLOCK,INCOMING,check_actual,run

def solve(width,steps=22,timeout=15000,two_single_emissions=False):
    s=z3.SolverFor('QF_BV');s.set(timeout=timeout)
    initial=[z3.BitVec(f'x{i}',4) for i in range(width)]
    for x in initial:s.add(z3.ULE(x,9))
    # Each pair sum has this unique digit split. The first addition depends
    # only on the pair sums, so this removes no possible core trajectory.
    for i in range(width//2):s.add(z3.Or(initial[i]==0,initial[-1-i]==9))
    if two_single_emissions:
        s.add(z3.ZeroExt(1,initial[0])+z3.ZeroExt(1,initial[-1])!=9)
    digits=initial.copy()
    for t in range(steps):
        a=INCOMING[t%11];h=CLOCK[t%11];carry=z3.BitVecVal(a,5)
        out=[]
        for i in range(len(digits)):
            d=z3.BitVec(f'd{t}_{i}',4)
            c=z3.If(z3.Bool(f'c{t}_{i}'),z3.BitVecVal(1,5),z3.BitVecVal(0,5))
            s.add(z3.ULE(d,9),z3.ZeroExt(1,d)+10*c==
                  z3.ZeroExt(1,digits[i])+z3.ZeroExt(1,digits[-1-i])+carry)
            carry=c;out.append(d)
        s.add(carry==1-a)
        if h:out.append(z3.BitVecVal(9 if a else 0,4))
        if two_single_emissions and t in (10,21):
            count=1 if t==10 else 2
            for j in range(count):s.add(z3.ZeroExt(1,out[j])+z3.ZeroExt(1,out[-1-j])==9)
            s.add(z3.ZeroExt(1,out[count])+z3.ZeroExt(1,out[-1-count])!=9)
        digits=out
    start=time.monotonic();status=s.check()
    row={'width':width,'steps':steps,'status':str(status),'seconds':time.monotonic()-start,
         'timeout_ms':timeout,'two_single_emissions':two_single_emissions,
         'scope':'bounded finite-center synthesis; no infinite claim'}
    if status==z3.sat:
        model=s.model();C=sum(model.eval(x).as_long()*10**i for i,x in enumerate(initial))
        assert check_actual(width,C,m=30,steps=steps)==steps
        row['center']=str(C).zfill(width)
        row['signed_trace']=run(width,C,steps)
    elif status==z3.unknown:row['reason']=s.reason_unknown()
    return row

if __name__=='__main__':
    rows=[]
    for width in (3,5,7,8,9,10,12,16,20,28,40,60):
        row=solve(width);rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='signed_trace'}),flush=True)
        Path('persist_root_signed_sat_results.json').write_text(json.dumps(rows,indent=2))
        if row['status']=='sat':break
