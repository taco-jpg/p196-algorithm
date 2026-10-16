#!/usr/bin/env python3
"""Search for a SHORT cycle witness: backward BFS from the long initial rows (layer by
layer), and for each newly reached state a forward BFS (two successors per state)
with a depth limit, looking for a return to that state.  The first return found gives
entry path = BFS path, cycle = forward return reversed into backward order.
usage: short_witness.py K PREFIX [FWD_DEPTH] [BACK_CAP]"""
import sys, json, pathlib
from collections import deque
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import prefix_cycles as pc

def forward_return(u, fwd_depth):
    """forward BFS from u; returns forward path u -> ... -> u (list) or None."""
    parent = {u: None}; dq = deque([(u, 0)])
    while dq:
        v, d = dq.popleft()
        if d >= fwd_depth:
            continue
        for w in pc.forward_prefixes(v):
            if w == u:
                path = [u]; x = v
                seq = []
                while x is not None:
                    seq.append(x); x = parent[x]
                return seq[::-1] + [u]        # u ... v u  (forward order)
            if w not in parent:
                parent[w] = v; dq.append((w, d + 1))
    return None

def search(prefix, k, fwd_depth=12, back_cap=400_000):
    P = pc.Pred(k)
    init = [s for s in pc.initial_states(prefix, k) if len(s) == k]
    parent = {s: None for s in init}
    dq = deque(init)
    while dq:
        u = dq.popleft()
        ret = forward_return(u, fwd_depth)
        if ret is not None:
            entry = []; x = u
            while x is not None:
                entry.append(x); x = parent[x]
            entry = entry[::-1]                       # p0 ... u (backward order)
            cyc = ret[::-1]                           # u ... u in backward order (each next is a pred)
            return {'prefix': prefix, 'k': k, 'status': 'CYCLE', 'states': len(parent),
                    'entry_path': [list(c) for c in entry[:-1]],
                    'cycle_len': len(cyc) - 1, 'cycle': [list(c) for c in cyc],
                    'note': 'short witness: backward BFS entry, forward return cycle'}
        for v in P.preds(u):
            if v not in parent:
                parent[v] = u; dq.append(v)
        if len(parent) > back_cap:
            return {'prefix': prefix, 'k': k, 'status': 'NO_SHORT_WITNESS', 'states': len(parent)}
    return {'prefix': prefix, 'k': k, 'status': 'ACYCLIC_LONG_ONLY', 'states': len(parent)}

if __name__ == '__main__':
    k, prefix = int(sys.argv[1]), sys.argv[2]
    fd = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    cap = int(sys.argv[4]) if len(sys.argv) > 4 else 400_000
    print(json.dumps(search(prefix, k, fd, cap)))
