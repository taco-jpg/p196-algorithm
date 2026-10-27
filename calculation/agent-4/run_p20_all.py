#!/usr/bin/env python3
"""Agent 4: finite base-10 p=20 B-cycle census, not a Lean proof."""
from collections import Counter
from pathlib import Path
import re, subprocess, sys
HERE=Path(__file__).resolve().parent
words=subprocess.check_output(
    [str(HERE/'low_digit_automaton'),'--emit','20'],text=True
).splitlines()
weights=Counter(w.count('1') for w in words)
assert weights=={5:1,6:23,7:164,8:219,9:41,10:1},weights
results=[]
for w in words:
    try:
        p=subprocess.run(
            [str(HERE/'fixed_g_B_probe'),w,'2000000','100'],
            capture_output=True,text=True,timeout=25
        )
    except subprocess.TimeoutExpired:
        results.append((w,'TIMEOUT',0,0));continue
    line=p.stdout.strip().splitlines()[-1] if p.stdout.strip() else 'ERROR'
    status=line.split(' ')[0]
    m=re.search(r'depth=(\d+) states=(\d+)',line)
    depth,states=(int(m[1]),int(m[2])) if m else (0,0)
    results.append((w,status,depth,states))
counts=Counter(r[1] for r in results)
print('p20 admissible_overflow_necklaces=',len(words))
print('counts_by_overflow_weight=',dict(sorted(weights.items())))
print('status=',dict(sorted(counts.items())))
print('max_states_word=',max((r[3],r[0],r[2]) for r in results))
for w,s,d,n in results:
    if s!='EXHAUSTED-NO-B-CYCLE':print('UNRESOLVED',w,s,d,n)
if any(r[1]!='EXHAUSTED-NO-B-CYCLE' for r in results):sys.exit(1)
print('COMPUTED: ALL p20 B POSITION STATES EXHAUSTED, ZERO ACCEPT')
