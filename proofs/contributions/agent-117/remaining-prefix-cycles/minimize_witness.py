#!/usr/bin/env python3
"""Shorten a CYCLE witness for the Lean instance: keep the recorded cycle, replace the
DFS entry path by a shortest path (BFS over long states only) from a long initial row.
Optionally shortens the cycle by trying short BFS returns from each cycle state.
usage: minimize_witness.py IN.jsonl PREFIX [BFS_CAP]  -> prints the minimized record"""
import sys, json, pathlib
from collections import deque
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import prefix_cycles as pc

def shorten_cycle(cyc, preds, effort=20000):
    """Try to find a shorter cycle through some state of cyc using bounded BFS."""
    best = cyc
    for start in cyc:
        parent = {start: None}; dq = deque([start]); found = None; n = 0
        while dq and found is None and n < effort:
            u = dq.popleft(); n += 1
            for v in preds(u):
                if v == start:
                    found = u; break
                if v not in parent:
                    parent[v] = u; dq.append(v)
        if found is None:
            continue
        seq = []; u = found
        while u is not None:
            seq.append(u); u = parent[u]
        seq = seq[::-1] + [start]
        if len(seq) < len(best):
            best = seq
    return best

def minimize(rec, bfs_cap=3_000_000, shorten=True):
    k = rec['k']; prefix = rec['prefix']
    P = pc.Pred(k)
    def preds(p):          # long states only
        return P.preds(p) if len(p) == k else frozenset()
    cyc = [tuple(c) for c in rec['cycle']]
    assert cyc[0] == cyc[-1]
    if shorten:
        cyc = shorten_cycle(cyc, preds)
    target = set(cyc)
    init = [s for s in pc.initial_states(prefix, k) if len(s) == k]
    parent = {s: None for s in init}
    hit = next((s for s in init if s in target), None)
    dq = deque(init)
    while dq and hit is None:
        u = dq.popleft()
        for v in preds(u):
            if v not in parent:
                parent[v] = u; dq.append(v)
                if v in target:
                    hit = v; break
        if len(parent) > bfs_cap:
            return None
    entry = []; u = hit
    while u is not None:
        entry.append(u); u = parent[u]
    entry = entry[::-1]
    i = cyc.index(hit)
    cyc_rot = cyc[i:-1] + cyc[:i] + [hit]
    return {'prefix': prefix, 'k': k, 'status': 'CYCLE', 'states': rec['states'],
            'entry_path': [list(c) for c in entry[:-1]],
            'cycle_len': len(cyc_rot) - 1, 'cycle': [list(c) for c in cyc_rot],
            'bfs_states': len(parent)}

if __name__ == '__main__':
    fn, prefix = sys.argv[1], sys.argv[2]
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 3_000_000
    for line in open(fn):
        rec = json.loads(line)
        if rec['prefix'] == prefix and rec['status'] == 'CYCLE':
            print(json.dumps(minimize(rec, cap)))
            break
