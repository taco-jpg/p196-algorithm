#!/usr/bin/env python3
"""Agent #115: mechanically patch a COPY of the original generate_hierarchy.py with
only (a) names/namespaces, (b) job count 16->15, (c) links read from the certificate
(ids 16..30 renumbered), (d) root width 1->2 and bound 659->636; write output into OUTDIR.
usage: python3 -I patch_orig_hierarchy.py ORIG_generate_hierarchy.py CERT.json.gz OUTDIR
"""
import gzip, json, re, sys
from pathlib import Path
orig, cert, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
jobs = json.loads(gzip.decompress(cert.read_bytes()))['jobs']
links = {j['id'] - 16: [(l['component'], l['child_job'] - 16) for l in j['children']]
         for j in jobs if j['hierarchy'] == 'broader' and j['children']}
src = orig.read_text()
src = re.sub(r'^links=.*$', 'links=' + repr(links).replace(' ', ''), src, count=1, flags=re.M)
src = src.replace('p=Path(__file__).resolve().parent', 'p=Path(%r)' % str(out))
src = src.replace('range(16)', 'range(15)')
src = src.replace('ScalarJobData', 'BroaderJobData').replace('ScalarHierarchy', 'BroaderHierarchy')
src = re.sub(r'\bJobChecks', 'BJobChecks', src); src = re.sub(r'\bJobData', 'BJobData', src)
old = 'q L 1 a s path n) : n ≤ 659'; assert src.count(old) == 1
src = src.replace(old, 'q L 2 a s path n) : n ≤ 636')
print('links', links)
out.mkdir(parents=True, exist_ok=True)
(out / 'patched_generate_hierarchy.py.txt').write_text(src)
exec(compile(src, 'patched_generate_hierarchy', 'exec'), {'__name__': '__main__', '__file__': str(out / 'x.py')})
