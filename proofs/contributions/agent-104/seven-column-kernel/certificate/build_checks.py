#!/usr/bin/env python3
"""Sequential, resumable bounded builds; never runs more than one Lean worker."""
import argparse
from pathlib import Path
import subprocess
import sys

p=argparse.ArgumentParser()
p.add_argument('--lean',required=True)
p.add_argument('--build',required=True)
p.add_argument('--inverse-build',required=True)
p.add_argument('--seconds',type=int,default=120)
p.add_argument('--tag',default='build')
p.add_argument('modules',nargs='+')
a=p.parse_args()
here=Path(__file__).resolve().parent
build=Path(a.build).resolve()
for name in a.modules:
    source=here/(name+'.lean')
    if name=='PrefixCertificate':
        source=here.parent/source.name
    print('BUILD',source.name,flush=True)
    cmd=[sys.executable,str(here/'run_lean.py'),'--lean',a.lean,'--lean-path',str(build)+':'+a.inverse_build,
         '--seconds',str(a.seconds),'--output',str(build/(name+'.olean')),
         '--log',str(here/(name+'-'+a.tag+'.log')),str(source)]
    result=subprocess.run(cmd)
    if result.returncode:
        raise SystemExit(result.returncode)
