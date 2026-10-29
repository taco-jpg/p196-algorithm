#!/usr/bin/env python3
"""Independent ordinary-bigint regression for the p8 80-step root shield.
Does not import or execute the prefix algorithm. Standard library only.
"""
import json, random, sys
from pathlib import Path
sys.set_int_max_str_digits(100000)
ROOT = Path(__file__).resolve().parents[3]
P = json.loads((ROOT/'calculation/new_structures/agent-N10/phase.json').read_text())

def source(half, mid=None):
    pair = half + ([] if mid is None else [mid]) + half[::-1]
    d = [0] * len(pair)
    for i in range(len(pair)//2):
        d[i] = min(pair[i], 9)
        d[-1-i] = pair[i] - d[i]
    if mid is not None: d[len(pair)//2] = mid//2
    assert d[-1] > 0
    return int(''.join(map(str, d[::-1])))

def run():
    rng = random.Random(20261029)
    total = 0
    for centre_length in (42, 43, 44, 45):
        for q in (5,6,7,8,12,30):
            for _ in range(25):
                h = [rng.randrange(19) for _ in range(centre_length//2)]
                mid = 2*rng.randrange(10) if centre_length % 2 else None
                N = source(P['B0'] + P['W0']*q + h, mid)
                for t in range(81):
                    s = str(N)
                    pair = [int(s[-1-i]) + int(s[i]) for i in range(59)]
                    assert pair == P['phase_B'][t%8] + P['phase_W'][t%8]
                    assert any(x%2 for x in pair[:39])
                    assert s != s[::-1]
                    if t != 80:
                        nxt = N + int(s[::-1])
                        assert len(str(nxt)) - len(s) == P['gammas'][t%8]
                        N = nxt
                total += 1
    assert total == 600
    print(f'PASS {total} independent true-decimal trajectories, {80*total} steps,')
    print('four source parities, six band counts, arbitrary sampled centres.')

if __name__ == '__main__': run()
