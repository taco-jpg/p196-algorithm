#!/usr/bin/env python3
"""Wall time and peak memory of `lake env lean FILE` for each given module file (sequential).
GNU time is not installed on the sprint machine; each file runs in a fresh helper process whose
getrusage(RUSAGE_CHILDREN).ru_maxrss is the peak RSS of that one Lean run.
Run from lean/ after `lake build` of the imports. Usage: leantime.py FILE.lean [...]"""
import json
import resource
import subprocess
import sys
import time

if len(sys.argv) > 2 and sys.argv[1] == '--one':
    t0 = time.time()
    p = subprocess.run(['lake', 'env', 'lean', sys.argv[2]], capture_output=True, text=True)
    wall = time.time() - t0
    peak_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    out = p.stdout.splitlines() + p.stderr.splitlines()
    err = [l for l in out if 'error' in l]
    ax = [l.split("depends on axioms:")[-1].strip() for l in out if 'depends on axioms' in l]
    print(json.dumps({'file': sys.argv[2], 'rc': p.returncode, 'wall_s': round(wall, 1),
                      'peak_rss_mb': round(peak_kb / 1024), 'errors': err[:3],
                      'axiom_sets': sorted(set(ax))}), flush=True)
else:
    for path in sys.argv[1:]:
        subprocess.run([sys.executable, __file__, '--one', path])
