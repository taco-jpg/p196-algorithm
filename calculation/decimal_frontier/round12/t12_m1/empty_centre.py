#!/usr/bin/env python3
"""r12a: the EMPTY centre (|C| = 0, word U^k rev(U)^k) for all 30 U: exact window simulation (satc.simulate,
boundary exact for m=54) and AC46 two-inlet cone (cone.iterate).  Needed as base case of the centre-defect lemma."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from satc import simulate, all_U
from cone import iterate
clock = [1, 0, 0, 0] * 30
bad = 0
for i, U in enumerate(all_U()):
    s, _ = simulate(U, [], 54, clock)
    tgt = list(U) * 59 + list(U[::-1]) * 59
    ret = (s == tgt)
    mis = [j - len(s) // 2 for j in range(len(s)) if s[j] != tgt[j]]
    core, shift, _ = iterate(U, (), k=100, clock=clock)
    a0 = (len(s) - len(core)) // 2
    agree = s[a0:a0 + len(core)] == core if a0 >= 0 else None
    print('U', i, U, 'returns', ret, 'mismatch offsets from centre (first 6)', sorted(mis, key=abs)[:6], 'sim==AC46core', agree, flush=True)
    bad += ret
print('RESULT empty centre returns for', bad, 'of 30 U')
