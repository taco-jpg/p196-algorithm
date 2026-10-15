#!/usr/bin/env python3
"""Exhaustive functional-graph cycle search of the neutral one-band quotient (finite scope).

States (B, C) as in quotient.py.  Every canonical start with |B| <= SB and |C| <= SC is
followed under qstep until the template breaks (None), a size cap is exceeded
(|B| > CB or |C| > CC), or a state repeats.  Every reached cycle is recorded with its
period, total gap change sum(u + v - gamma) and maximal interface sizes.
A cap is not an exclusion: only the explicit finite scope is examined.
"""
import itertools, json, sys, time
from quotient import qstep

def canonical_B(b, s):
    n = b - 1
    for B in itertools.product(range(2 * n + 1), repeat=s):
        if s and (B[0] == 0 or B[-1] == n):
            continue
        yield B

def canonical_C(b, m):
    n = b - 1
    for half in itertools.product(range(2 * n + 1), repeat=(m + 1) // 2):
        C = half + tuple(reversed(half[: m // 2]))
        if m % 2 and C[m // 2] % 2:
            continue
        if C[0] == n:
            continue
        yield C

def search(b, SB, SC, CB, CC):
    outcome = {}
    cycles = []
    starts = 0
    for s in range(SB + 1):
        for B in canonical_B(b, s):
            for m in range(1, SC + 1):
                for C in canonical_C(b, m):
                    starts += 1
                    path = []; idx = {}; cur = (B, C); res = None
                    while True:
                        if cur in outcome:
                            res = outcome[cur]; break
                        if cur in idx:
                            cyc = path[idx[cur]:]
                            gain = 0; steps = []
                            st = cyc[0]
                            for _ in range(len(cyc)):
                                B2, C2, gam, u, v = qstep(b, *st)
                                gain += u + v - gam
                                steps.append((gam, u, v))
                                st = (B2, C2)
                            cid = len(cycles)
                            cycles.append({'period': len(cyc), 'gain': gain,
                                           'states': [[list(x[0]), list(x[1])] for x in cyc],
                                           'steps': steps,
                                           'max_B': max(len(x[0]) for x in cyc),
                                           'max_C': max(len(x[1]) for x in cyc)})
                            res = ('cycle', cid)
                            for st in cyc: outcome[st] = res
                            break
                        if len(cur[0]) > CB or len(cur[1]) > CC:
                            res = 'cap'; break
                        idx[cur] = len(path); path.append(cur)
                        nxt = qstep(b, *cur)
                        if nxt is None:
                            res = 'break'; break
                        cur = (nxt[0], nxt[1])
                    for st in path:
                        outcome.setdefault(st, res)
    return starts, len(outcome), cycles

if __name__ == '__main__':
    b, SB, SC, CB, CC = map(int, sys.argv[1:6])
    t0 = time.time()
    starts, states, cycles = search(b, SB, SC, CB, CC)
    good = [c for c in cycles if c['gain'] >= 0]
    rec = {'base': b, 'start_caps': {'B': SB, 'C': SC}, 'follow_caps': {'B': CB, 'C': CC},
           'starts': starts, 'states_visited': states, 'cycles': len(cycles),
           'nonnegative_gain_cycles': len(good), 'seconds': round(time.time() - t0, 1),
           'cycle_list': cycles}
    print(json.dumps({k: v for k, v in rec.items() if k != 'cycle_list'}))
    for c in sorted(cycles, key=lambda c: (-c['gain'], c['period']))[:6]:
        print('  period', c['period'], 'gain', c['gain'], 'maxB', c['max_B'], 'maxC', c['max_C'], 'first', c['states'][0])
    if len(sys.argv) > 6:
        with open(sys.argv[6], 'w') as f:
            json.dump(rec, f)
