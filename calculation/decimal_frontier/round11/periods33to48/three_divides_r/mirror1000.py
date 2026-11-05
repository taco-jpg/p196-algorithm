"""Exact exterior map Phi of the Agent120 format (base 10), copied from calculation/neutral_band_search.py:
B -> nextB(B, C) with e2 = 1 - e1 (the exterior system; nextB depends on B and e2 only), trailing 9s trimmed."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../calculation'))
import neutral_band_search as nb
b = 10
def e1(B): return nb.e1(b, B)
def step(B):
    """returns (B', gam, e1) for the exterior system: centre chosen so that e2 = 1 - e1 (only e2 enters nextB)."""
    E1 = e1(B)
    C = [0] if E1 == 1 else [10]          # one-coefficient centre: e2(C) = 1 - e1 exactly (Lemma 2a)
    assert nb.e2(b, B, C) == 1 - E1
    g = nb.gam(b, B, C)
    B2 = nb.nextB(b, B, C)
    while B2 and B2[-1] == 9: B2 = B2[:-1]
    return B2, g, E1
N12_0 = [1,5,11,10,5,8,3,7,4,6,4,2,3,0,7,12,9,3,3,2,3,2,4,7,5,9,9,0,6,7,9,7,4,5,4,0,3,5,2,10,17,5,5,11,11,12,10,4,4,4,7,2,14]
def orbit(B, n):
    out = []
    for t in range(n):
        B2, g, E = step(B); out.append((B, g, E)); B = B2
    return out, B
if __name__ == '__main__':
    o, B = orbit(N12_0, 12)
    print('N12 closes:', B == N12_0, 'gam', ''.join(str(x[1]) for x in o), 'e1', ''.join(str(x[2]) for x in o), 'widths', [len(x[0]) for x in o])
    # padding check: B ++ 9^j gives same trimmed successor
    import random
    bad = 0
    for _ in range(20000):
        n = random.randint(1, 12); B = [random.randint(1, 18)] + [random.randint(0, 18) for _ in range(n - 1)]
        while B and B[-1] == 9: B.pop()
        if not B: continue
        j = random.randint(1, 5)
        s1 = step(B); s2 = step(B + [9] * j)
        if s1 != (s2[0], s2[1], s2[2]): bad += 1
    print('padding mismatches', bad)
