"""For each width k: first time the 196 orbit enters SCC(w(196,100)) (S<k>.bin from scc.c),
whether it ever leaves (t <= 200000), and a shortest forward cycle through w(196,100)
(carry list = input for Lean cycleOK). Usage: entry_and_cycle.py K... (run in the work dir)."""
import sys, json
sys.path.insert(0, __import__("os").path.dirname(__file__))
from fwdref import forward_prefix, prefix_predecessors
def code(w):
    c = 0
    for x in reversed(w): c = c*19 + x
    return c
def inset(data, w):
    c = code(w); return (data[c >> 3] >> (c & 7)) & 1
rows = []
for line in open("orb200k.txt"):
    a = line.split()
    rows.append((int(a[0]), int(a[1]), [int(x) for x in a[5:17]], [int(x) for x in a[17:29]]))
out = {}
for k in map(int, sys.argv[1:]):
    S = open(f"S{k}.bin","rb").read()
    D = open(f"D{k}.bin","rb").read()
    first = None; outside_after = []
    for (t, L, q, e) in rows:
        if L < k: continue
        w = q[:k]
        if inset(S, w):
            if first is None: first = t
        elif first is not None:
            outside_after.append(t)
    w100 = rows[100][2][:k]
    # shortest cycle through w100: predecessor p of w100 with minimal BFS distance from w100
    best = None
    for p in prefix_predecessors(w100):
        if p[0] == 0 or len(p) != k: continue
        d = D[code(p)]
        if d != 255 and (best is None or d < best[0]): best = (d, p)
    # backtrack from best[1] to w100 along decreasing distance
    d, p = best
    path = [p]
    while d > 0:
        for x in prefix_predecessors(path[-1]):
            if x[0] > 0 and D[code(x)] == d - 1:
                path.append(x); d -= 1; break
        else:
            raise SystemExit("backtrack failed")
    assert path[-1] == w100
    path.reverse()                       # w100 -> ... -> p
    walk = path + [w100]
    carries = []
    for a, b in zip(walk, walk[1:]):
        es = [e for e in (0, 1) if forward_prefix(a, e) == b]
        assert es, (a, b)
        carries.append(es[0])
    print(f"k={k}: orbit first enters SCC at t={first}; times after entry outside SCC (t<=200000): {len(outside_after)}; "
          f"shortest cycle through w100 has length {len(walk)-1}")
    out[k] = dict(first_entry=first, outside_after=len(outside_after), cycle=walk, carries=carries)
json.dump(out, open("cycles_" + "_".join(sys.argv[1:]) + ".json", "w"))
