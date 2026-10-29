#!/usr/bin/env python3
"""One-command source-complete reproduction for two-step connected collisions."""
import json,re,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
lat=root/'lattice_input.txt';motifs=root/'motifs.json'
cases=json.loads(motifs.read_text())
assert len(cases)==15
subprocess.run([sys.executable,str(root/'local_certificate.py'),str(lat),str(motifs)],check=True)
subprocess.run([sys.executable,str(root/'independent_bigint.py'),str(lat),str(motifs)],check=True)
with tempfile.TemporaryDirectory() as td:
    exe=Path(td)/'two_step_discover'
    subprocess.run(['c++','-O3','-std=c++17',str(root/'discover.cpp'),'-o',str(exe)],check=True)
    out=subprocess.run([str(exe),str(lat)],capture_output=True,text=True,check=True)
    lines=out.stdout.splitlines()
    hits=[]
    for line in lines:
        if line.startswith('TWO_STEP_HIT'):
            m=re.search(r't=(\d+) n=(\d+) r=(\d+) width=(\d+) pos=(\d+) vals=([\d,]+)',line)
            assert m,line
            t,n,r,w,j,values=m.groups()
            vals=[int(v) for v in values.split(',') if v]
            assert int(w)==3
            assert int(j)==52+int(r)
            hits.append((int(t),int(n),int(r),tuple(vals)))
    expected={(e['phase'],n,e['residue'],tuple(e['replace'])) for e in cases for n in (400,401)}
    assert len(hits)==30 and set(hits)==expected,(len(hits),set(hits)^expected)
    assert len([x for x in lines if x.startswith('COMPLETE_SOURCE_PHASE')])==18
    assert 'candidates=1000188 distinct_first_step=1000188 hit=30' in out.stderr
print('UNCAPPED_CXX_1000188_WIDTH_LE3_DISCOVERY_CONTROL_PASS')
print('TWO_STEP_POSITIVE_FAMILY_COMPLETE_REPRODUCTION_PASS')
