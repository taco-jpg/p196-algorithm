#!/usr/bin/env python3
"""r12b exploratory: size of the coarsest forward bisimulation of a khx kept graph (dump file), with node attributes
(t, lc, dig-if-overflow-phase) -- the only node data that buildChild() uses.  usage: bisim.py DUMP WORD"""
import sys
dump, word = sys.argv[1], sys.argv[2]
pat = [int(c) for c in word]; b = 10
ids = []; t = {}; o0 = {}; o1 = {}; att = {}
for l in open(dump):
    if l.startswith("#"): continue
    head, xs = l.split(":"); h = head.split(); i = int(h[0]); x = [int(v) for v in xs.split()]
    tt = int(h[1]); lc = 0
    for d in x: lc = (d + lc) // b
    ids.append(i); t[i] = tt; o0[i] = int(h[2]); o1[i] = int(h[3])
    att[i] = (tt, lc, x[-1] if pat[tt] else -1)
# Moore refinement
cls = {}; key2id = {}
for i in ids:
    k = att[i]; cls[i] = key2id.setdefault(k, len(key2id))
n = len(set(cls.values()))
while True:
    key2id = {}; new = {}
    for i in ids:
        k = (cls[i], cls.get(o0[i], -1) if o0[i] >= 0 else -1, cls.get(o1[i], -1) if o1[i] >= 0 else -1)
        new[i] = key2id.setdefault(k, len(key2id))
    m = len(key2id); cls = new
    if m == n: break
    n = m
print("kept nodes=%d  bisimulation classes=%d  (attributes only: %d)" % (len(ids), n, len(set(att.values()))))
