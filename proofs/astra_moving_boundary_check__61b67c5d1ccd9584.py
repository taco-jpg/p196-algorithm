"""Exact moving 0/18 walls and finite-shift differentiation.

No decimal Lychrel witness is asserted.  The all-length proof is in the
companion notes; this independent integer checker validates the formulas.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import json
import random


def wall_profile(W, i):
    return 0 if i < 0 else (W[i] if i < len(W) else 18)


def wall_step(W):
    """Return W', actual exterior h, low output digits through index |W|."""
    w = len(W)
    assert all(0 <= x <= 18 for x in W)
    assert all(W[i] + W[w-1-i] == 18 for i in range(w))
    assert not W or W[0] > 0
    a = [0]
    r = []
    for x in list(W) + [18]:
        r.append((x + a[-1]) % 10)
        a.append((x + a[-1]) // 10)
    b = [0] * (w + 1)
    b[w] = 1
    u = [0] * w
    for i in range(w-1, -1, -1):
        u[i] = (W[i] + b[i+1]) % 10
        b[i] = (W[i] + b[i+1]) // 10
    h = b[0]
    assert a[w] == 1-h
    assert all(u[i] + r[w-1-i] == 9 for i in range(w))
    V = tuple(r[i] + (h if i-h == -1 else u[i-h])
              for i in range(w+h))
    assert len(V) == w+h
    assert not V or V[0] > 0
    assert all(V[i] + V[-1-i] == 18 for i in range(len(V)))
    return V, h, tuple(r)


def difference_word(W, C):
    assert C >= 1
    return tuple(wall_profile(W, i) - wall_profile(W, i-C)
                 for i in range(len(W)+C))


def word_valid(q):
    return (bool(q) and q[0] > 0 and q == q[::-1]
            and all(0 <= x <= 18 for x in q)
            and (len(q) % 2 == 0 or q[len(q)//2] % 2 == 0))


def digit_monotone(r, C):
    # The extended low digit profile is 0 to the left and 9 after len(r)-1.
    return all(r[i] >= (0 if i < C else r[i-C]) for i in range(len(r)))


def realize(q):
    """A positive same-width integer realizing arbitrary admissible q."""
    assert word_valid(q)
    L = len(q)
    d = [0]*L
    for i in range(L//2):
        high = min(9, q[i])
        d[L-1-i] = high
        d[i] = q[i]-high
    if L % 2:
        d[L//2] = q[L//2]//2
    assert d[-1] > 0
    n = sum(x*10**i for i,x in enumerate(d))
    assert pair_sums(n) == q
    return n


def pair_sums(n):
    d = tuple(map(int, str(n)[::-1]))
    return tuple(x+y for x,y in zip(d,d[::-1]))


def integer_step(n):
    return n + int(str(n)[::-1])


def bad(q):
    return all(x <= 9 for x in q) or (q[0] == 11 and all(x in (0,11) for x in q))


def wall_words(max_half=2):
    yield ()
    for m in range(max_half+1):
        for U in product(range(19), repeat=m):
            for middle in ((), (9,)):
                W = U + middle + tuple(18-x for x in U[::-1])
                if W and W[0] > 0:
                    yield W


def check_case(W, C, counts):
    V,h,r = wall_step(W)
    q = difference_word(W,C)
    if not word_valid(q):
        counts['invalid_initial_difference'] += 1
        return
    n = realize(q)
    N = integer_step(n)
    Q = pair_sums(N)
    good = digit_monotone(r,C)
    # All valid differences, including failed ordering: the theoretical
    # wall carries majorize the actual carries and have one 1 per class.
    L = len(q)
    a = [0]
    c = [0]
    for i in range(L):
        a.append((wall_profile(W,i)+a[-1])//10)
        c.append((q[i]+c[-1])//10)
    K = [a[i]-(a[i-C] if i >= C else 0) for i in range(L+1)]
    assert all(0 <= c[i] <= K[i] <= 1 for i in range(L+1))
    assert all(sum(K[i+1] for i in range(j,L,C)) == 1 for j in range(C))
    missing = [1-sum(c[i+1] for i in range(j,L,C)) for j in range(C)]
    assert all(x in (0,1) for x in missing)
    outdigits = tuple(map(int,str(N)[::-1]))
    assert all(sum(outdigits[j::C]) == 9+10*missing[j]-missing[(j-1)%C]
               for j in range(C))
    assert good == (sum(missing) == 0)
    assert sum(outdigits) == 9*(C+sum(missing))
    counts['carry_hole_identities'] += 1
    if good:
        predicted = difference_word(V,C)
        assert Q == predicted, (W,C,q,Q,predicted)
        assert word_valid(predicted)
        assert len(str(N)) == len(q)+h
        outdigits = tuple(map(int,str(N)[::-1]))
        assert all(sum(outdigits[j::C]) == 9 for j in range(C))
        assert N % (10**C-1) == 0
        assert not bad(q)
        assert str(N) != str(N)[::-1]
        counts['monotone_exact_steps'] += 1
        counts['overflow_steps' if h else 'nonoverflow_steps'] += 1
        if len(W) > C:
            counts['overlapping_exact_steps'] += 1
        if len(W) == C:
            counts['first_collision_exact_steps'] += 1
    else:
        # The exact digit identity, rather than shape failure alone, is what
        # the monotonicity theorem certifies. Some q images can accidentally
        # agree despite a carry defect; no converse is claimed here.
        counts['ordering_failures'] += 1
    if C > len(W):
        assert good
        M = C-len(W)
        assert q == W + (18,)*M + W[::-1]
        assert Q == V + (18,)*(M-h) + V[::-1]
        counts['positive_reservoir_steps'] += 1
    if C == len(W):
        assert good == (h == 0 or W[0] >= 10)
        counts['first_collision_cases'] += 1


def initial_wall_trace(C, limit=10000):
    W = ()
    n = 10**C-1
    trace = []
    for t in range(limit):
        assert pair_sums(n) == difference_word(W,C)
        V,h,r = wall_step(W)
        good = digit_monotone(r,C)
        N = integer_step(n)
        trace.append(dict(t=t,width=len(str(n)),wall_width=len(W),h=h,
                          monotone=good,n=str(n),next=str(N),
                          digit_sum_next=sum(map(int,str(N))),
                          palindrome_next=str(N)==str(N)[::-1],
                          wall=list(W),low_output=list(r)))
        if not good:
            return trace
        assert pair_sums(N) == difference_word(V,C)
        W,n=V,N
    raise AssertionError('finite control did not meet a failure within the cap')


def run():
    counts = dict(invalid_initial_difference=0, monotone_exact_steps=0,
                  overflow_steps=0, nonoverflow_steps=0,
                  overlapping_exact_steps=0, first_collision_exact_steps=0,
                  ordering_failures=0, positive_reservoir_steps=0,
                  first_collision_cases=0, carry_hole_identities=0)
    # Exhaustive short walls, including odd widths and neutral prefixes.
    for W in wall_words(2):
        for C in range(1,len(W)+5):
            check_case(W,C,counts)
    # Longer independent random controls, including after wall collision.
    rng = random.Random(20261013)
    for _ in range(15000):
        m = rng.randrange(1,35)
        U = tuple([rng.randrange(1,19)] + [rng.randrange(19) for _ in range(m-1)])
        middle = (9,) if rng.randrange(2) else ()
        W = U + middle + tuple(18-x for x in U[::-1])
        C = rng.randrange(max(1,len(W)-15),len(W)+8)
        check_case(W,C,counts)
    traces = {str(C):initial_wall_trace(C) for C in range(1,25)}
    result = dict(status='exact identities checked; no all-time monotone wall supplied',
                  counts=counts,
                  first_failure={C:dict(t=z[-1]['t'],wall_width=z[-1]['wall_width'],
                     palindrome_next=z[-1]['palindrome_next'],
                     digit_sum_next=z[-1]['digit_sum_next']) for C,z in traces.items()},
                  small_traces={C:traces[C] for C in ('1','2','3')})
    out = Path(__file__).with_name('astra_moving_boundary_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(counts=counts, first_failure=result['first_failure']),indent=2))


if __name__ == '__main__':
    run()
