#!/usr/bin/env python3
"""Independent exact-integer edge tests for the adversarial-centre cone rule."""
import random


def predict(low, high):
    """Two-ended abstract step with *no access to the middle*."""
    k = len(low)
    r = k
    while r and low[r - 1] + high[r - 1] == 9:
        r -= 1
    if not r:
        return None
    carry = 0
    lout = []
    for i in range(r):
        carry, d = divmod(low[i] + high[i] + carry, 10)
        lout.append(d)
    carry = int(low[r - 1] + high[r - 1] >= 10)
    hout = [None] * r
    for i in range(r - 2, -1, -1):
        carry, hout[i] = divmod(low[i] + high[i] + carry, 10)
    overflow = carry
    nk = r if overflow else r - 1
    if nk == 0:
        return None
    return lout[:nk], [1 if (overflow and i == 0) else
                         hout[i - 1 if overflow else i]
                         for i in range(nk)], overflow


def run():
    rng = random.Random(302026)
    cases = 0
    for _ in range(25000):
        k = rng.randint(2, 36)
        low = [rng.randrange(10) for _ in range(k)]
        high = [rng.randrange(10) for _ in range(k)]
        high[0] = rng.randrange(1, 10)
        state = predict(low, high)
        if state is None:
            continue
        lnext, hnext, predicted_ov = state
        for _ in range(2):
            m = rng.randint(1, 100)
            core = ''.join(str(rng.randrange(10)) for _ in range(m))
            s = ''.join(map(str, high)) + core + ''.join(map(str, low[::-1]))
            value = int(s)
            result = value + int(s[::-1])
            t = str(result)
            assert len(t) - len(s) == predicted_ov, (s, t, predicted_ov)
            assert [int(t[-1-i]) for i in range(len(lnext))] == lnext
            assert [int(t[i]) for i in range(len(hnext))] == hnext
            cases += 1
    print(f'PASS {cases} randomized exact-integer one-step centre variations')


if __name__ == '__main__':
    run()
