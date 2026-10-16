#!/usr/bin/env python3
"""Cross-check prefix_cycles.Pred against the repository relation on random states
(verify_certificates.prefix_predecessors, k = 7) and reproduce the 739/620 closures."""
import random, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / '2026-10-15-seven-column-prefix'))
import prefix_cycles as pc
import verify_certificates as vc

P = pc.Pred(7)
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
mismatch = 0
for _ in range(trials):
    p = tuple(random.randrange(19) for _ in range(7))
    if p[0] == 0:
        continue
    if set(P.preds(p)) != set(vc.prefix_predecessors(p)):
        mismatch += 1
print('random seven-column states compared:', trials, 'mismatches:', mismatch)
for pre, expect in (('739', 58501), ('620', 59189), ('217', 186686), ('218', 38587), ('777', 151754)):
    r = pc.analyze(pre, 7, 3_000_000)
    print(pre, r['status'], r['states'], 'expected', expect, 'OK' if (r['status'] == 'ACYCLIC' and r['states'] == expect) else 'MISMATCH')
