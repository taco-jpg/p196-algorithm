#!/usr/bin/env python3
"""Reproduce phase-2 repaired-wake decimal 8-step moving-front SAT witness.
Run from the repository root:
python3 calculation/new_structures/agent-N05/sat_h8_partial.py
Requires libz3.so.4, and imports adjacent sat_glider.py and phase_packet.py.
"""
from sat_glider import smt,solve,model_p
from phase_packet import bulk,local_step
H,phase,origin,M,first,wide,drift,margin=8,2,990,48,18,4,1,8
formula=smt(H,phase,origin,M,first,wide,drift,margin,None,False,True)
formula+='\n(assert (= p_0_18 6))\n'
state,model,why=solve(formula,15000,True)
assert state==1,('not SAT',state,why)
start=model_p(model,0,M)
end=model_p(model,H,M)
source=[start[j] for j in range(first,first+wide)]
assert source==[6,1,17,18],source
for t in range(H+1):
    assert all(0<=v<=18 for v in model_p(model,t,M).values())
changes={origin+j:start[j] for j in range(first,first+wide)
         if start[j]!=bulk(phase,origin+j)}
trajectory=[]
for t in range(H+1):
    offsets=sorted(j-origin-first for j in changes)
    trajectory.append([t,len(offsets),offsets[0],offsets[-1]])
    if t==H:break
    changes=local_step(phase+t,changes)
assert trajectory==[[0,4,0,3],[1,4,0,3],[2,4,0,3],
                    [3,4,1,4],[4,4,1,4],[5,4,1,4],
                    [6,4,1,4],[7,4,1,4],[8,4,1,4]],trajectory
expected={j-origin:v for j,v in changes.items()}
actual={j:end[j] for j in range(M) if end[j]!=bulk(phase+H,origin+j)}
assert expected==actual,(expected,actual)
print('SAT_8_STEP_PASS')
print('source',source)
print('target',[(j-origin-first,v) for j,v in sorted(changes.items())])
print('trajectory step,count,first_offset,last_offset:',trajectory)
