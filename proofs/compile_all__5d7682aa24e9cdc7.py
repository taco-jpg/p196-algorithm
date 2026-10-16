"""Replay every formal module with an installed Lean 4.19.0 executable.

Usage: python compile_all.py /path/to/lean
The generated .olean files are disposable build outputs.
"""
from pathlib import Path
import os, subprocess, sys, time

HERE=Path(__file__).resolve().parent
LEAN=sys.argv[1] if len(sys.argv)>1 else 'lean'
MODULES=[
    'ReverseClosure', 'SoficProof', 'BoundaryData', 'BoundaryCertificate',
    'ArithmeticBridge', 'BulkTargets', 'BulkDerivation',
]
env=dict(os.environ,LEAN_PATH=str(HERE))
start=time.monotonic()
chunks=[]
def record(text):
    # Reopen on each checkpoint: no log descriptor remains open throughout
    # a long compiler run or across workspace checkpoint synchronizations.
    chunks.append(text)
    (HERE/'compile_all.log').write_text(''.join(chunks))

version=subprocess.run([LEAN,'--version'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
record(version.stdout)
if version.returncode or 'version 4.19.0' not in version.stdout:
    raise SystemExit('Expected a working Lean 4.19.0 executable.')
for module in MODULES:
    begin=time.monotonic()
    result=subprocess.run([LEAN,'-o',module+'.olean',module+'.lean'],
                          cwd=HERE,env=env,text=True,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    record('\nMODULE '+module+'\n'+result.stdout+
           f'EXIT {result.returncode}; SECONDS {time.monotonic()-begin:.3f}\n')
    print(f'{module}: exit {result.returncode}',flush=True)
    if result.returncode:
        print(result.stdout)
        raise SystemExit(result.returncode)
summary=f'ALL SEVEN MODULES PASSED; SECONDS {time.monotonic()-start:.3f}\n'
record(summary)
print(summary,end='',flush=True)
