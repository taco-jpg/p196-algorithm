#!/usr/bin/env python3
"""Project k-column CYCLE witnesses to (k-1) columns by dropping the last pair sum of
every long state.  The projected walk is again a backward walk of the (k-1)-column
abstraction (Lemma 2 in METHOD_LIMIT.md); the output is re-checked independently by
verify_witness.py.  usage: project_witness.py IN_k.jsonl OUT_k-1.jsonl"""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
with open(dst, 'w') as out:
    for line in open(src):
        r = json.loads(line)
        if r['status'] != 'CYCLE':
            continue
        k = r['k']
        proj = lambda w: w[:k - 1] if len(w) == k else w
        out.write(json.dumps({'prefix': r['prefix'], 'k': k - 1, 'status': 'CYCLE',
                              'states': r['states'],
                              'entry_path': [proj(w) for w in r['entry_path']],
                              'cycle_len': r['cycle_len'],
                              'cycle': [proj(w) for w in r['cycle']],
                              'note': 'projected from k=%d witness' % k}) + '\n')
