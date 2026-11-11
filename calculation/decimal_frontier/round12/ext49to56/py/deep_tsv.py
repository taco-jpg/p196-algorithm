#!/usr/bin/env python3
"""r12e2: one compact TSV of all deep-pass verdicts (out/deep1, deep53, deep54, deep5556 = deep pass 1; out/deep2 = deep pass 2;
out/decisive = the long run).  Columns: T word root pass verdict K kept reason maxnodes secs top99_first topUU_first file.
usage: deep_tsv.py > out/deep_verdicts.tsv"""
import os, re, glob
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the route directory (Studio: ~/p196_run/r12e)
P1 = ['deep1', 'deep53', 'deep54', 'deep5556']
print('T\tword\troot\tpass\tverdict\tK\tkept\treason\tmaxnodes\tsecs\ttop99_first\ttopUU_first\tfile')
def rows(d, tag):
    for f in sorted(glob.glob(f'{D}/out/{d}/*.out')):
        txt = open(f).read(); m = re.search(r'word=([01]+) root=([01]+)', txt)
        k = [l for l in txt.splitlines() if l.startswith('KHXT ')]
        if not m or not k: continue
        l = k[-1]; g = lambda p: (re.search(p, l).group(1) if re.search(p, l) else '')
        v = 'DIES' if ' DIES ' in l else 'SURVIVES'
        print('\t'.join([str(len(m.group(1))), m.group(1), m.group(2), tag, v, g(r'(?:DIES|SURVIVES) K=(\d+)'), g(r'kept=(\d+)'),
                         g(r'reason=(\w+)'), g(r'maxnodes=(\d+)'), g(r'secs=([\d.]+)'), g(r'top99_first=(-?\d+)'),
                         g(r'topUU_first=(-?\d+)'), os.path.relpath(f, D)]))
for d in P1: rows(d, 'deep1')
rows('deep2', 'deep2')
