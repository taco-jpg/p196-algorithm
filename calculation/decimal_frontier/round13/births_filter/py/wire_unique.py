#!/usr/bin/env python3
"""r12b: verify the STABLE-WIRE structure of a khx kept set at two consecutive levels K0, K0+1 (dumps from `khxd ... -dump`).
Known stream: B_t (t = 0..q-1) from the WIT line of `bx -w -nosym` (q = period of the stream; pattern phase t <-> time t mod q).
Checks (PASS needs all):
 (1)/(2) every kept node at level K is either C(t) = pad_K(B_t)  or  D(t) = pad_{K-1}(B_t) ++ [w], w != 9  (nothing else);
 (3) the attributed induced graphs at K0 and K0+1 coincide under C(t)<->C(t), D(t,w)<->D(t,w): same node keys, same attributes
     (phase, top digit, forward carry L_K into the next position), same labelled edges (bit h) between keys.
usage: wire_unique.py DUMP_K0 DUMP_K1 WITFILE"""
import sys, re
b = 10
def load(fn):
    K = None; nodes = {}
    for l in open(fn):
        if l.startswith("#"):
            m = re.search(r" K=(\d+)", l)
            if m: K = int(m.group(1))
            continue
        head, xs = l.split(":"); h = head.split()
        nodes[int(h[0])] = (int(h[1]), int(h[2]), int(h[3]), [int(v) for v in xs.split()])
    return K, nodes
line = [l for l in open(sys.argv[3]) if l.startswith("WIT")][0]
Bs = [[int(v) for v in grp.split(",")] for grp in re.findall(r"\[([0-9,]+)\]", line)]
q = len(Bs)
def analyse(fn):
    K, nodes = load(fn)
    key = {}; bad = []
    for i, (t, o0, o1, x) in nodes.items():
        B = Bs[t % q]
        if len(B) > K - 1: bad.append((i, "stream wider than K-1")); continue
        padK = B + [9] * (K - len(B)); padK1 = B + [9] * (K - 1 - len(B))
        if x == padK: key[i] = ("C", t, 9)
        elif x[:K - 1] == padK1 and x[K - 1] != 9: key[i] = ("D", t, x[K - 1])
        else: bad.append((i, "other window"))
    attr = {}; edges = set()
    for i, (t, o0, o1, x) in nodes.items():
        if i not in key: continue
        lc = 0
        for d in x: lc = (d + lc) // b
        attr[key[i]] = (t, x[-1], lc)
        for hbit, o in ((0, o0), (1, o1)):
            if o >= 0: edges.add((key[i], hbit, key.get(o, ("?", o))))
    return K, nodes, key, bad, attr, edges
K0, n0, k0, bad0, a0, e0 = analyse(sys.argv[1])
K1, n1, k1, bad1, a1, e1 = analyse(sys.argv[2])
ok = True
print("level %d: kept=%d  C=%d D=%d other=%d" % (K0, len(n0), sum(1 for v in k0.values() if v[0] == "C"), sum(1 for v in k0.values() if v[0] == "D"), len(bad0)))
print("level %d: kept=%d  C=%d D=%d other=%d" % (K1, len(n1), sum(1 for v in k1.values() if v[0] == "C"), sum(1 for v in k1.values() if v[0] == "D"), len(bad1)))
if K1 != K0 + 1: print("FAIL: levels not consecutive"); ok = False
if bad0 or bad1: print("FAIL: nodes outside C u D:", bad0[:5], bad1[:5]); ok = False
if set(a0) != set(a1): print("FAIL: node keys differ", set(a0) ^ set(a1)); ok = False
elif a0 != a1: print("FAIL: attributes differ", [(k, a0[k], a1[k]) for k in a0 if a0[k] != a1[k]][:5]); ok = False
if e0 != e1: print("FAIL: edges differ", list(e0 ^ e1)[:6]); ok = False
if any(k[0] == "?" for (_, _, k) in e0 | e1): print("FAIL: edge to unclassified node"); ok = False
phases = sorted(set(k[1] for k in a0))
cph = sorted(k[1] for k in a0 if k[0] == "C")
print("C phases:", len(cph), " D keys:", sorted((k[1], k[2]) for k in a0 if k[0] == "D")[:60])
print("edges:", len(e0))
print("RESULT", "PASS" if ok else "FAIL")
