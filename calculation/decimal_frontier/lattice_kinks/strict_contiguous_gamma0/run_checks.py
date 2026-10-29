#!/usr/bin/env python3
"""Single-command two-algorithm reproducibility runner, Python 3 standard library."""
import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
lat=root/'lattice_input.txt'
counts=root/'counts.json'
res=subprocess.run([sys.executable,str(root/'classify.py'),str(lat)],capture_output=True,text=True,check=True)
print(res.stdout,end='')
assert 'STRICT_CONTIGUOUS_ALL_WIDTH_EXCLUSION_PASS 81 rooted start states' in res.stdout
assert json.loads(res.stdout.split('COUNTS_JSON ',1)[1])==json.loads(counts.read_text())
subprocess.run([sys.executable,str(root/'independent_check.py'),str(lat),str(counts)],check=True)
print('FULL_TWO_ENGINE_REPRODUCIBILITY_PASS')
