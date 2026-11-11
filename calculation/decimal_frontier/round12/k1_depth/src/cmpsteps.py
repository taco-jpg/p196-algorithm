#!/usr/bin/env python3
"""r12g3: compare the STEP lines (n, size) and the final verdict of two forward-iteration logs (kfwd/kfwd3 vs indep fwd).
Sizes of steps 1..s0-1 are chunk sums ('<=') in chunked runs and exact in unchunked runs; with one chunk they coincide,
so only the numbers are compared (the '<=' flags are reported)."""
import re, sys
def parse(fn):
    st, fl, fin = {}, {}, None
    for line in open(fn):
        m = re.match(r'^STEP (\d+) size (<= )?(\d+)', line)
        if m: st[int(m.group(1))] = int(m.group(3)); fl[int(m.group(1))] = m.group(2) is not None
        m = re.match(r'^(EMPTY|STABLE|UNDECIDED)( at step (\d+))?', line)
        if m: fin = (m.group(1), m.group(3))
    return st, fl, fin
a, la, fa = parse(sys.argv[1]); b, lb, fb = parse(sys.argv[2])
keys = sorted(set(a) | set(b)); bad = [k for k in keys if a.get(k) != b.get(k)]
fd = [k for k in keys if la.get(k) != lb.get(k)]
print(f'{sys.argv[1]} vs {sys.argv[2]}: steps {len(a)} / {len(b)}, verdict {fa} / {fb}, differing sizes at steps {bad[:10]}'
      f' (chunk-sum flag differs at {fd[:8]})', '=> IDENTICAL' if not bad and fa == fb and a else '=> DIFFERENT')
