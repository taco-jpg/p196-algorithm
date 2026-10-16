#!/usr/bin/env python3
"""Build generated data sequentially, one Lean worker and bounded modules."""
import argparse
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser()
p.add_argument('--lean', required=True)
p.add_argument('--build', required=True)
p.add_argument('--start', type=int, default=0)
p.add_argument('--tag', default='build')
a=p.parse_args()
here=Path(__file__).resolve().parent
build=Path(a.build).resolve()
modules=sorted(here.glob('Rank739Data*.lean'))[a.start:]+[here/'Rank739.lean']
for source in modules:
    print('BUILD',source.name,flush=True)
    cmd=[sys.executable,str(here/'run_lean.py'),'--lean',a.lean,'--lean-path',str(build),
         '--output',str(build/(source.stem+'.olean')),
         '--log',str(here/(source.stem+'-'+a.tag+'.log')),str(source)]
    result=subprocess.run(cmd)
    if result.returncode:
        raise SystemExit(result.returncode)
