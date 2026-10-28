#!/usr/bin/env python3
"""Reproduce rec2 width-11 finite window exclusion and width-8 controls.
Run: nice -n 10 python3 calculation/decimal_frontier/lattice_kinks/code/agent18_width11_reproduce.py
Flags: --quick runs only integer replay and a small SAT/UNSAT pair; --full is default.
Requires system libz3.so and <=8 GiB virtual memory per SAT worker.
SAT is exhaustive with no state/node cap; UNKNOWN is a failure, not an exclusion.
"""
import json, subprocess, sys
from pathlib import Path
here=Path(__file__).resolve().parent
root=here.parent
info=json.loads((root/'data'/'agent18_width11_witness.json').read_text())
quick='--quick' in sys.argv
cases=[(8,o,v,'SAT') for o,v in enumerate(info['published_width8_sat'])]
cases += [(8,o,v,'UNSAT') for o,v in enumerate(info['published_width8_unsat'])]
cases += [(11,o,40,'SAT') for o in range(4)]
cases += [(11,o,v,'UNSAT') for o,v in enumerate(info['unsat_horizon'])]
if quick:cases=[(8,0,28,'SAT'),(8,0,29,'UNSAT')]
for o,win in info['initial_windows_bottom_to_centre'].items():
    cmd=[sys.executable,str(here/'agent18_width11_check.py'),o,'40',','.join(map(str,win))]
    subprocess.run(cmd,check=True)
for w,o,h,expected in cases:
    result=subprocess.run([sys.executable,str(here/'agent18_width11_z3.py'),str(w),str(o),str(h)],capture_output=True,text=True)
    print(result.stdout,flush=True)
    if result.returncode!=0 or f'RESULT {w} {o} {h} {expected} ' not in result.stdout:
        print(result.stderr,file=sys.stderr)
        raise AssertionError(f'SAT control failed: {w=} {o=} {h=} {expected=}')
print('ALL_AGENT18_WIDTH11_CHECKS_PASSED', 'QUICK' if quick else 'FULL')
