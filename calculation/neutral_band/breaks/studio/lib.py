"""lib.py -- thin helpers on top of calculation/neutral_band_search.py (the exact Python mirror of the Lean definitions).
Set the environment variable P196_ALGO to the repo clone (default /home/claude/p196-algorithm)."""
import os, sys, random, collections
ALGO = os.environ.get('P196_ALGO', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ALGO, 'calculation'))
import neutral_band_search as N
from neutral_band_search import (norm, e1, e2, DB, DC, DR, gam, xd, yd, nextB, nextC, hyp, trim, step, run, is_cert,
                                 cycleOK)


def phiB(b, B):
    """Autonomous B-system (feedback e2 = 1 - e1).  Returns (B_next_trimmed, u, e1, gam).
    Uses a dummy centre that forces e2 = 1 - e1; next B depends on nothing else (verified on >27k real transitions)."""
    n = b - 1
    E1 = e1(b, B)
    C = [0] if E1 == 1 else [2 * n]
    assert e2(b, B, C) == 1 - E1
    nb = nextB(b, B, C)
    g = gam(b, B, C)
    u = 0
    while nb and nb[-1] == n:
        nb = nb[:-1]
        u += 1
    return nb, u, E1, g


def rand_state(b, rng, mB=(1, 8), mC=(0, 8)):
    n = b - 1
    m = rng.randint(*mB)
    B = [rng.randint(1, 2 * n)] + [rng.randint(0, 2 * n) for _ in range(m - 1)]
    c = rng.randint(*mC)
    h = [rng.randint(0, 2 * n) for _ in range((c + 1) // 2)]
    C = h + h[:c // 2][::-1]
    return B, C
