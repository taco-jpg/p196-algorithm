#!/usr/bin/env python3
"""Exact independent verifier, 01010101 F1 ternary-centre bound.

Usage:
 python3 verify_rotation.py /path/to/all_n24.tsv
Each independent Python replay batch runs in a fresh subprocess to cap
heap size. No third-party modules or network access are needed.
"""
from pathlib import Path
from itertools import permutations
import subprocess,sys
import independent_rotation as m

rowsfile=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('all_n24.tsv'))
rows=[line.split('\t') for line in rowsfile.read_text().splitlines()]
triples=list(permutations(range(19),3))
assert len(rows)==5814,('partial',len(rows))
assert len(m.factors(28))==72 and len(m.factors(24))==64 and len(m.factors(32))==80
exceptions=[];nhits=0;maximum=0
for j,row in enumerate(rows):
    assert len(row)==6,(j,row)
    i,abc,source,hit,cap,states=row
    assert int(i)==j and tuple(map(int,abc.split(',')))==triples[j]
    assert int(source)==72 and int(cap)==0 and 0<int(states)<=50000
    maximum=max(maximum,int(states))
    if int(hit)>0:exceptions.append((tuple(map(int,abc.split(','))),int(hit)))
    nhits+=int(hit)
assert len(exceptions)==18 and nhits==72 and maximum==1260,(len(exceptions),nhits,maximum)
print('PRIMARY COMPLETE: 5814 injective tables x72 source factors, 18 exceptional tables, 72 short-window matches; 0 caps; max 1260 states',flush=True)
if '--batch' not in sys.argv:
    # Full independent checks, chunked into fresh processes. No result is
    # accepted until every batch exits with status zero.
    for i in range(0,len(exceptions),4):
        subprocess.run([sys.executable,__file__,str(rowsfile),'--batch',str(i),str(min(i+4,len(exceptions)))],check=True)
    m.corpus_cross_check()
    m.random_arithmetic(3000)
    m.crop_controls(5000)
    print('ROTATED P8 BOUNDED OBSTRUCTION: ALL INDEPENDENT CHECKS PASSED')
    raise SystemExit(0)
start=int(sys.argv[sys.argv.index('--batch')+1]);end=int(sys.argv[sys.argv.index('--batch')+2])
pat24={m.pat(t) for t in m.factors(24)}
pat28={m.pat(t) for t in m.factors(28)}
for A,expected_hits in exceptions[start:end]:
    m.next_words.cache_clear()
    h24=0
    for src in m.factors(28):
        states,_=m.evolve(tuple(A[int(v)] for v in src))
        h24+=int(any(m.pat(v) in pat24 for v in states))
    assert h24==expected_hits,(A,h24,expected_hits)
    m.next_words.cache_clear()
    h28=0
    for src in m.factors(32):
        states,_=m.evolve(tuple(A[int(v)] for v in src))
        h28+=int(any(m.pat(v) in pat28 for v in states))
    assert h28==0,(A,h28)
    print('INDEPENDENT EXCEPTION PASS',A,'short',h24,'long',h28,flush=True)
