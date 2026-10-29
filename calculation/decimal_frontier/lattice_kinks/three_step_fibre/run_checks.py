#!/usr/bin/env python3
"""Source-complete one-command three-step coalescence fibre reproduction."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(r/'composition_certificate.py')],check=True)
for k in (1,2,3,4,8,12):
    subprocess.run([sys.executable,str(r/'independent_integer.py'),str(k)],check=True)
print('ALL_K_THREE_STEP_EXPONENTIAL_FIBRE_REPRODUCIBILITY_PASS')
