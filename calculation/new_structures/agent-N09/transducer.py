#!/usr/bin/env python3
"""Exact two-ended rational relation on folded pairwords.

A fold is (outer_pairs, centre), where centre=None for even digit count
and the coefficient at the central position for odd digit count.
Each outer coefficient x encodes two symmetric positions in P.
A transition guesses only the high-half carry in {0,1}.
For a physical pairword, exactly one choice of gamma and high carries
survives the centre boundary condition.
"""
from itertools import product
from random import Random


def pairs(d):
    n = len(d)
    return [d[i] + d[n - 1 - i] for i in range(n)]


def fold(p):
    assert p == p[::-1]
    n = len(p)
    return p[:n // 2], p[n // 2] if n % 2 else None


def unfold(outer, centre):
    return outer + ([centre] if centre is not None else []) + outer[::-1]


def normalize(p):
    c = 0
    out = []
    for x in p:
        v = x + c
        out.append(v % 10)
        c = v // 10
    if c: out.append(c)
    return out


def step_digits(d):
    c, out, n = 0, [], len(d)
    for i, x in enumerate(d):
        v = x + d[n - 1 - i] + c
        out.append(v % 10)
        c = v // 10
    if c: out.append(c)
    return out


def states_after(outer, gamma, target=None, palindrome_only=False):
    """DP over ≤40 carry/high-digit states, with no large-number arithmetic.

    If target is specified, match the emitted output pair coordinates.
    If palindrome_only, enforce equality of normalized opposite digits.
    States (low_forward_carry, high_backward_carry, prior_high_digit).
    """
    states = {(0, gamma, -1)}
    for i, x in enumerate(outer):
        new = set()
        for c, t, prev in states:
            low = (x + c) % 10
            next_c = (x + c) // 10
            for next_t in (0, 1):
                if (x + next_t) // 10 != t:
                    continue
                high = (x + next_t) % 10
                emitted = (low + high) if gamma == 0 else (low + 1 if i == 0 else low + prev)
                if target is not None and target[i] != emitted:
                    continue
                if palindrome_only:
                    if gamma == 0 and low != high:
                        continue
                    if gamma == 1 and (low != 1 if i == 0 else low != prev):
                        continue
                new.add((next_c, next_t, high))
        states = new
        if not states:
            break
    return states


def relation(src, dst):
    """True exactly if dst is the folded pairword of norm(src).
    This is membership in a finite-state rational relation, not a replay.
    """
    xs, centre = src
    ys, newcentre = dst
    n = 2 * len(xs) + (centre is not None)
    m = 2 * len(ys) + (newcentre is not None)
    gamma = m - n
    if gamma not in (0, 1): return False
    if len(ys) != len(xs) + (1 if gamma == 1 and n % 2 == 1 else 0):
        return False
    if len(xs) and gamma == 1 and ys[0] != ((xs[0] % 10) + 1):
        return False
    if centre is not None and (centre & 1): return False  # physical odd-length source
    for c, t, prev in states_after(xs, gamma, ys):
        if centre is None:
            if c != t: continue
            if gamma == 0: return True
            if newcentre != 2 * prev: continue
            return True
        dig = (centre + c) % 10
        if (centre + c) // 10 != t: continue
        if gamma == 0:
            if newcentre != 2 * dig: continue
            return True
        last = dig + (prev if len(xs) else 1)
        if ys[-1] != last: continue
        return True
    return False


def successor_is_pal(src):
    """Regular-language recognizer for preimages of palindromes.
    It depends on only finitely many states, independent of word length.
    """
    xs, centre = src
    for g in (0, 1):
        for c, t, prev in states_after(xs, g, palindrome_only=True):
            if centre is None:
                if c == t: return True
            else:
                if (centre + c) // 10 != t: continue
                if g == 0: return True
                dig = (centre + c) % 10
                if dig == (prev if len(xs) else 1): return True
    return False


def exhaustive_short():
    # Exhaust every actual decimal seed of length ≤3; check relation and safety.
    for n in range(1, 1000):
        d = list(map(int, reversed(str(n))))
        q = step_digits(d)
        src, dst = fold(pairs(d)), fold(pairs(q))
        assert relation(src, dst), ('relation false', n, src, dst)
        assert successor_is_pal(src) == (q == q[::-1]), ('pal mismatch', n)
    r = Random(9009)
    for _ in range(12000):
        length = r.randrange(1, 90)
        d = [r.randrange(10) for i in range(length)]
        d[-1] = r.randrange(1, 10)
        q = step_digits(d)
        src = fold(pairs(d)); dst=fold(pairs(q))
        assert relation(src, dst)
        assert successor_is_pal(src) == (q == q[::-1])
        badouter, badcentre = dst
        if badouter:
            bad = badouter[:]
            bad[0] = (bad[0] + 1) % 19
            if bad[0] != badouter[0]:
                assert not relation(src, (bad, badcentre))
    print('SHORT_TRANS' , 999 + 12000, 'exact length/pairword/safety tests PASS')


def orbit_sample():
    d=[6,9,1]
    all_even=[]
    for t in range(2500):
        q=step_digits(d)
        s=fold(pairs(d))
        assert relation(s, fold(pairs(q))), t
        assert successor_is_pal(s) == (q==q[::-1]),t
        if all(x%2==0 for x in pairs(d)):
            all_even.append(t)
        d=q
    print('196_TRANS',2500,'full folded-output and palindrome tests PASS; all-even P at steps',all_even)

if __name__=='__main__':
    exhaustive_short()
    orbit_sample()
