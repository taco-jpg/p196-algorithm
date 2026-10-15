#!/usr/bin/env python3
"""Independent per-class rank certificate (Python, prefix_cycles relation) and comparison
with the whole-space C++ catalogue (classes<k>.tsv from wellfounded7.cpp).

For a prefix class abc at k columns: backward closure of S_0^{abc} (long + short), Kahn
ranks (rank 0 = no predecessor, else 1 + max over predecessors), bound = 1 + max rank over
the initial set; UNBOUNDED if some initial state never receives a rank.

usage: rank_certificate.py K CLASSES.tsv [PREFIX ...]   (default: every closed class)
"""
import sys, json, pathlib
from collections import defaultdict, deque
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import prefix_cycles as pc

def certificate(prefix, k, cap=5_000_000):
    P = pc.Pred(k)
    short = pc.short_table(k)
    def preds(p):
        ps = set(short.get(p, ()))
        if len(p) == k:
            ps |= P.preds(p)
        return ps
    init = pc.initial_states(prefix, k)
    todo, seen = list(init), set(init)
    parents, children = {}, defaultdict(list)
    while todo:
        p = todo.pop()
        ps = preds(p)
        parents[p] = ps
        for s in ps:
            children[s].append(p)
            if s not in seen:
                seen.add(s); todo.append(s)
        if len(seen) > cap:
            return {'prefix': prefix, 'k': k, 'status': 'CAP', 'states': len(seen)}
    rank = {p: 0 for p in seen if not parents[p]}
    degree = {p: len(parents[p]) for p in seen}
    queue = deque(rank)
    while queue:
        s = queue.popleft()
        for p in children[s]:
            degree[p] -= 1
            if degree[p] == 0:
                rank[p] = 1 + max(rank[q] for q in parents[p])
                queue.append(p)
    if len(rank) != len(seen):
        return {'prefix': prefix, 'k': k, 'status': 'UNBOUNDED', 'states': len(seen),
                'ranked': len(rank)}
    return {'prefix': prefix, 'k': k, 'status': 'ACYCLIC', 'states': len(seen),
            'bound': 1 + max(rank[p] for p in init)}

def load_classes(path, D=3):
    d = {}
    for l in open(path):
        if l.startswith('#'):
            continue
        f = l.rstrip('\n').split('\t')
        if f[0] == str(D):
            d[f[1]] = (int(f[2]), int(f[3]))
    return d

if __name__ == '__main__':
    k = int(sys.argv[1]); table = load_classes(sys.argv[2])
    prefixes = sys.argv[3:] or sorted(p for p, v in table.items() if v[0] == 1)
    bad = 0
    for p in prefixes:
        r = certificate(p, k)
        closed, bound = table[p]
        ok = (r['status'] == 'ACYCLIC' and closed == 1 and r['bound'] == bound) or \
             (r['status'] == 'UNBOUNDED' and closed == 0)
        if not ok:
            bad += 1
        print(json.dumps(r), 'catalogue', (closed, bound), 'OK' if ok else 'MISMATCH', flush=True)
    print('compared', len(prefixes), 'classes, mismatches', bad)
    sys.exit(1 if bad else 0)
