#!/usr/bin/env python3
"""Verify C++ exhaustive n24 result and run independent Python checker."""
from pathlib import Path
import sys,subprocess
if len(sys.argv)!=2:raise SystemExit('Usage: python3 verify.py /path/to/n24.tsv')
rows=[s.split('\t') for s in Path(sys.argv[1]).read_text().splitlines()]
assert len(rows)==5814,('incomplete census',len(rows))
positive={134:(0,8,17),279:(0,17,8),5534:(18,1,10),5679:(18,10,1)}
hits=0
for i,row in enumerate(rows):
    assert len(row)==6,(i,row)
    index,abc,source,h,c,maximum=row
    assert int(index)==i
    assert int(source)==72
    assert int(c)==0
    assert 1<=int(maximum)<=50000
    vec=tuple(int(x) for x in abc.split(','))
    assert len(vec)==3 and len(set(vec))==3 and all(0<=x<=18 for x in vec)
    if i in positive:
        assert vec==positive[i] and int(h)==4,(i,h,vec)
    else:
        assert int(h)==0,(i,h)
    hits+=int(h)
assert hits==16
print('PRIMARY FULL N24 CENSUS PASS:',len(rows),'coefficient tables x72 exact L28 factors, 16 survivors at precisely four tables, zero caps')
subprocess.run([sys.executable,str(Path(__file__).with_name('independent.py'))],check=True)
