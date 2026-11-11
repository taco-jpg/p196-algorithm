#!/usr/bin/env python3
"""r12e: turn a khxt TOP99 hit (khxt -top -stophit -dump FILE) into an exterior candidate and test it exactly.
Reads the TOP99_HIT block (nodes on closed L-walks inside TOP99_K, with full windows and edges), follows the unique wire edges
(each TOP99 node has one edge to a TOP99 node), extracts one closed walk of length L, trims the 9s (B_t), and replays it with
r12b's verify_ext.verify (mirror step Bstep + one true reverse-and-add per step with a one-digit centre, exact integers).
usage: extract_hit.py DUMP WORD [L]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import verify_ext as V, neutral_band_search as m
fn, word = sys.argv[1], sys.argv[2]; P = len(word); L = int(sys.argv[3]) if len(sys.argv) > 3 else P
b = 10; nodes = {}; inblock = False
for l in open(fn):
    if l.startswith('# TOP99_HIT'): inblock = True; nodes = {}; continue
    if l.startswith('#'): inblock = False; continue
    if inblock and ':' in l:
        h, xs = l.split(':'); hh = h.split()
        nodes[int(hh[0])] = (int(hh[1]), int(hh[2]), int(hh[3]), [int(v) for v in xs.split()])
print(f"TOP99 hit block: {len(nodes)} nodes")
start = min(i for i, n in nodes.items() if n[0] == 0)
walk = [start]
for _ in range(L - 1):
    t, o0, o1, x = nodes[walk[-1]]
    nxt = [o for o in (o0, o1) if o >= 0 and o in nodes]
    walk.append(nxt[0])
t, o0, o1, x = nodes[walk[-1]]
assert start in (o0, o1), "walk does not close"
def trim(x):
    x = list(x)
    while x and x[-1] == b - 1: x.pop()
    return x
Bts = [trim(nodes[i][3]) for i in walk]
gL = (word * (L // P))
e = ''.join(str(m.e1(b, B)) for B in Bts)
ok, msgs = V.verify(b, gL, e, Bts)
print(f"widths {sorted(set(len(B) for B in Bts))}  e={e}  ->", 'VERIFIED' if ok else 'FAILED', *msgs[:3])
