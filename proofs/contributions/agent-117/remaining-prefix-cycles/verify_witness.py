#!/usr/bin/env python3
"""Independently check CYCLE witnesses produced by prefix_cycles.py.

For each JSONL record with status CYCLE it checks, using only the forward
column equations (forward_prefixes) and the exact short-word map F:

  1. entry_path[0] is a member of the standard initial set S_0^{abc} (long
     prefix rows a,b,c,d3..d_{k-1} or a complete short palindrome word);
  2. every consecutive pair (p, q) along entry_path + cycle is a backward edge,
     i.e. q is a predecessor of p: either q is a complete short word with
     F(q) = p, or q is a k-prefix with p in forward_prefixes(q);
  3. the cycle closes (cycle[0] == cycle[-1]) and has length >= 1.

A verified witness shows that the k-column backward closure of S_0^{abc}
contains a directed cycle, so no rank certificate of the seven-column kind
(strict rank descent along every backward edge) exists at this k.
It proves nothing about the palindrome class itself.
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from prefix_cycles import forward_prefixes, F, initial_states

def is_edge(p, q, k):
    if len(q) < k:
        return F(q) == p
    return p in forward_prefixes(q)

def check(rec):
    k = rec['k']
    if rec['status'] != 'CYCLE':
        return 'SKIP'
    init = initial_states(rec['prefix'], k)
    path = [tuple(x) for x in rec['entry_path']] + [tuple(x) for x in rec['cycle']]
    if path[0] not in init:
        return 'FAIL:initial'
    cyc = [tuple(x) for x in rec['cycle']]
    if len(cyc) < 2 or cyc[0] != cyc[-1]:
        return 'FAIL:closure'
    for p, q in zip(path, path[1:]):
        if not is_edge(p, q, k):
            return 'FAIL:edge %s -> %s' % (p, q)
    return 'OK'

if __name__ == '__main__':
    bad = 0; n = 0
    for fn in sys.argv[1:]:
        for line in open(fn):
            rec = json.loads(line)
            if rec['status'] != 'CYCLE':
                continue
            n += 1
            r = check(rec)
            if r != 'OK':
                bad += 1
                print(rec['prefix'], rec['k'], r)
    print('checked', n, 'witnesses,', bad, 'failures')
    sys.exit(1 if bad else 0)
