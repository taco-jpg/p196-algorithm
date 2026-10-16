#!/usr/bin/env python3
"""Summarize diagnosis JSONL files: status counts, cycle-length classes, entry-path and
closure statistics.  usage: summarize.py FILE.jsonl..."""
import json, sys
from collections import Counter
for fn in sys.argv[1:]:
    recs = [json.loads(l) for l in open(fn)]
    st = Counter(r['status'] for r in recs)
    cl = Counter(r.get('cycle_len') for r in recs if r['status'] == 'CYCLE')
    ent = [len(r.get('entry_path', [])) for r in recs if r['status'] == 'CYCLE']
    sz = [r['states'] for r in recs]
    print(fn.split('/')[-1], 'records', len(recs), dict(st))
    print('  cycle lengths:', sorted(cl.items(), key=lambda x: -x[1])[:12])
    if ent:
        print('  entry path length: min %d median %d max %d' % (min(ent), sorted(ent)[len(ent)//2], max(ent)))
    print('  states explored before verdict: min %d median %d max %d' % (min(sz), sorted(sz)[len(sz)//2], max(sz)))
    print('  seconds total %.0f' % sum(r['seconds'] for r in recs))
