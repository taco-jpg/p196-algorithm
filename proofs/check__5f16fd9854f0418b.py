#!/usr/bin/env python3
"""Check the exact retained data used by the written rotation corollary."""
from pathlib import Path
import gzip, hashlib, json
HERE=Path(__file__).resolve().parent
C=HERE.parent
P=C/'2026-10-14-component-specific-bound'
report=json.loads((P/'component_bound.json').read_text())
artifact=P/'component_certificates.json.gz'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(artifact)==report['certificate']['sha256']
job=json.loads(gzip.decompress(artifact.read_bytes()))['jobs'][0]
assert job['hierarchy']=='scalar' and job['width']==1
assert job['path_vertices_bound_by_start_phase']==[659]*7
assert job['components']==[[0,1,2,3,4,5,6]] and job['cyclic_components']==[0]
clock=[4,8,16,7,15,6,13]
overflows=[int(x>=10) for x in clock]
assert overflows==[0,0,1,0,1,0,1]
assert all(sum(overflows[(s+t)%7] for t in range(7))==3 for s in range(7))
def step(q):
 c=0;d=[]
 for a in q:
  c,r=divmod(a+c,10);d.append(r)
 if c:d.append(c)
 return [a+b for a,b in zip(d,reversed(d))]
controls=[]
for s,a in enumerate(clock):
 if a%2: continue
 q=[a];trajectory=[q]
 for t in range(1,8):
  q=step(q);trajectory.append(q)
  if q[0]!=clock[(s+t)%7]:break
 assert t=={4:4,8:3,16:2,6:1}[a]
 controls.append(dict(start_phase=s,initial=a,first_failure=t,trajectory=trajectory))
out=dict(result='PASS_ROTATION_COROLLARY_DATA',certificate_sha256=sha(artifact),proof_sha256=sha(HERE/'CLOCK_ROTATIONS.md'),phase_vertex_bounds=[659]*7,width14_period_bound=658//7,uniform_period_bound=658//7+4,width_one_controls=controls,scope='Exact existing certificate extraction and four exceptional trajectories; written proof uses previously reviewed full hierarchy, not a fresh hierarchy audit or a new Lean numerical theorem.')
(HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['result'])
