#!/usr/bin/env python3
"""r12g3: cross-check the numbers of FINAL.md table 4.1 against the forward-run logs (on the Mac mirror)."""
import re
L='~/Desktop/p196_studio/r12g/logs/'
files={('rec0',20,0):L+'fwd/rec0_K20_k4_o0.log',('rec0',21,0):L+'fwd/rec0_K21_k4_o0.log',('rec0',22,0):L+'fwd2/rec0_K22_k4_o0.log',('rec0',23,0):L+'fwd2/rec0_K23_k4_o0.log',
('rec2',21,0):L+'fwd/rec2_K21_k4_o0.log',('rec2',21,1):L+'fwd/rec2_K21_k4_o1.log',('rec2',23,0):L+'fwd/rec2_K23_k4_o0.log',('rec2',23,1):L+'fwd/rec2_K23_k4_o1.log',
('rec2',24,0):L+'g3/kfwd_rec2_K24_o0.log',('rec2',24,1):L+'g3/kfwd_rec2_K24_o1.log',('rec2',27,0):L+'fwd2/rec2_K27_k4_o0.log',('rec2',27,1):L+'fwd2/rec2_K27_k4_o1.log'}
txt=open('~/Desktop/p196_studio/r12g/FINAL.md').read()
bad=0
for line in txt.split('\n'):
    m=re.match(r'\| (rec\d) \| (\d+) \| (\d+) \| (\d) \| \((\d+),(\d+),(\d)\) \| ([\d,]+) \| ([\d,]+) \| (\d+) \| (\d+) \|',line)
    if not m: continue
    lat,K,Kb,o,t0,j0,p0,A0,A8,E,life=m.groups(); K=int(K); o=int(o)
    fn=files.get((lat,K,o)); s=open(fn).read()
    a0=re.search(r'A_0: .* = (\d+)',s).group(1); a8=re.search(r'^STEP 8 size (\d+)',s,re.M).group(1)
    e=re.search(r'EMPTY at step (\d+).*lifetime from phi0 = (\d+)',s)
    ph=re.search(r'phi0=\((\d+),(\d+),(\d)\)',s).groups()
    ok = (a0==A0.replace(',','') and a8==A8.replace(',','') and e.group(1)==E and e.group(2)==life and ph==(t0,j0,p0))
    print(lat,K,'o%d'%o,'OK' if ok else ('MISMATCH',a0,a8,e.groups(),ph)); bad+= (not ok)
print('mismatches',bad)
