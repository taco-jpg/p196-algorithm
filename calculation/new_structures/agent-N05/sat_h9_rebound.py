#!/usr/bin/env python3
"""SAT synthesis of nine-step phase-7 collapsing/rebounding decimal defect.
Run: python3 calculation/new_structures/agent-N05/sat_h9_rebound.py
Uses adjacent sat_glider.py, phase_packet.py and libz3.so.4.
"""
from sat_glider import smt,solve,model_p
from phase_packet import bulk,local_step
H,phase,origin,M,first,wide,drift,margin=9,7,990,48,18,4,1,8
formula=smt(H,phase,origin,M,first,wide,drift,margin,None,False,True)
formula+='\n(assert (= p_0_18 17))\n(assert (= p_0_19 8))\n'
state,model,why=solve(formula,15000,True)
assert state==1,('not SAT',state,why)
p0=model_p(model,0,M)
p9=model_p(model,H,M)
source=[p0[first+j] for j in range(wide)]
assert source==[17,8,0,2],source
x=origin+first

def start(pat):
    return {x+j:v for j,v in enumerate(pat) if v!=bulk(phase,x+j)}

patch=start(source)
other=start([17,3,10,6])
trajectory=[]
for k in range(H+1):
    offsets=sorted(z-x for z in patch)
    trajectory.append([k,len(offsets),offsets[0],offsets[-1]])
    if k>=2: assert patch==other,('coalescence',k,patch,other)
    if k==H:break
    patch=local_step(phase+k,patch)
    other=local_step(phase+k,other)
assert trajectory==[[0,3,0,2],[1,3,0,2],[2,4,0,3],
                    [3,5,0,4],[4,5,0,4],[5,5,0,4],
                    [6,3,3,5],[7,3,3,5],[8,4,1,4],[9,4,1,4]],trajectory
expected={j-origin:v for j,v in patch.items()}
actual={j:p9[j] for j in range(M) if p9[j]!=bulk(phase+H,origin+j)}
assert expected==actual,(expected,actual)
assert [(j-x,patch[j]) for j in sorted(patch)]==[(1,2),(2,17),(3,13),(4,16)]
print('SAT_9_STEP_REBOUND_PASS')
print('source',source,'alternate_coalescing_source',[17,3,10,6])
print('2-step coalescence and trajectory',trajectory)
