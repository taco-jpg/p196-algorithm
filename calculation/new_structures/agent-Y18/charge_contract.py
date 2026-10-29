#!/usr/bin/env python3
"""All-width p12/m9 centre-charge arithmetic controls (PAPER PROOF in results).
Run: python3 calculation/new_structures/agent-Y18/charge_contract.py
Independent reference: ordinary Python decimal integers, not the pairword engine.
"""
from pathlib import Path
LAT = Path("calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt")

def data():
    a = list(map(int, LAT.read_text().split()))
    p, bwidth, m, base = a[:4]
    assert (p, bwidth, m, base) == (12,34,9,10)
    i = 4
    gam = a[i:i+p]; i += p
    rows = [tuple(a[i+j*m:i+(j+1)*m]) for j in range(p)]
    i += p*m
    i += p*m  # Ascending carry rows.
    roots = [tuple(a[i+j*bwidth:i+(j+1)*bwidth]) for j in range(p)]
    assert len(a) == i+p*bwidth
    return gam, rows, roots

def templ(root, row, q, centre):
    assert tuple(centre) == tuple(reversed(centre))
    h = root + row*q
    return h + tuple(centre) + h[::-1]

def realize(p):
    digits = [0]*len(p)
    for i in range(len(p)//2):
        digits[i] = max(p[i]-9, 0)
        digits[-1-i] = min(p[i], 9)
    if len(p) % 2:
        assert p[len(p)//2] % 2 == 0
        digits[len(p)//2] = p[len(p)//2]//2
    assert digits[-1] > 0
    return int("".join(map(str, digits[::-1])))

def pair(n):
    d = list(map(int, str(n)))
    return tuple(d[i]+d[-i-1] for i in range(len(d)))

def main():
    gam, rows, roots = data()
    assert gam == [1,0,0,0,1,0,0,0,1,0,0,0]
    assert [sum(row)%9 for row in rows] == [6,3]*6
    assert pow(2,72,9) == 1
    for phase, row in enumerate(rows):
        for k in range(1,13):
            # For a putative 72k-step band return, the centre charge change.
            dc = (-2*k*sum(row)) % 9
            assert dc == (6*k if phase%2 == 0 else 3*k) % 9
            assert (dc == 0) == (k%3 == 0)
    # Four independent ordinary-decimal big-integer trajectories.
    for q, centre in ((5,()), (6,(2,)), (7,(4,0,4)), (7,(0,6,0,6,0))):
        p0 = templ(roots[0], rows[0], q, centre)
        n = realize(p0)
        assert pair(n) == p0
        residue = n%9
        for t in range(145):
            actual = pair(n)
            assert sum(actual)%9 == 2*n%9
            assert n%9 == pow(2,t,9)*residue%9
            if t in (72,144):
                impossible = templ(roots[0], rows[0], q+t//72, centre)
                assert (sum(impossible)-sum(p0))%9 == (3*(t//72))%9
                assert actual != impossible
                assert sum(actual)%9 != sum(impossible)%9
            if t < 144:
                before = len(str(n))
                n = n + int(str(n)[::-1])
                if t < 72:
                    assert len(str(n))-before == gam[t%12], (q,centre,t)
    print("Y18_P12_CHARGE_216_PASS: 12 rows, k=1..12, four 144-step ordinary-bigint controls")

if __name__ == "__main__":
    main()
