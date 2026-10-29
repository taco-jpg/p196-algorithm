#!/usr/bin/env python3
"""AC42: exact mod-11 two-epoch necessary gate for rooted phase-9 p12/m9.

PAPER PROOF (not a Lychrel certificate). The modular DP exhausts every
19^6 junction word, but no full 120-step junction census is claimed.
"""
from __future__ import annotations
import argparse
from collections import Counter
from pathlib import Path

B9 = (1,5,10,10,5,8,17,1,4,11,9,9,15,16,7,12,4,3,3,2,3,2,4,7,6,8,6,4,8,12,12,12,9,7)
W9 = (10,4,5,10,14,13,12,9,7)
ODD_C = (4,14,4)
EVEN_C = (4,4)


def alternating(word):
    return sum(x if i % 2 == 0 else -x for i, x in enumerate(word))


def words_u():
    # Exactly the 30 distinct cyclic rotations, rank 1..30.
    return [(b[i:] + b[:i]) for a in range(0, 19, 2)
            for b in [(9, a, 18-a)] for i in range(3)]


def load_rows(path):
    ls = [list(map(int, s.split())) for s in Path(path).read_text().splitlines()]
    assert tuple(ls[0]) == (12,34,9,10)
    assert len(ls) == 2 + 12 + 12 + 12
    return tuple(ls[2+9]), tuple(ls[2+24+9])


def mod11_dp(junction_len=6, j0=None, residue=9):
    """Exact count by carry-free residue convolution, not 19^6 trial replays."""
    assert junction_len >= 1
    dp = [0] * 11
    if j0 is None:
        dp[0] = 1
        start = 0
    else:
        assert 0 <= j0 <= 18
        dp[j0 % 11] = 1
        start = 1
    for i in range(start, junction_len):
        ndp = [0] * 11
        sgn = 1 if i % 2 == 0 else -1
        for old in range(11):
            for d in range(19):
                ndp[(old + sgn*d) % 11] += dp[old]
        dp = ndp
    assert sum(dp) == 19 ** (junction_len - (j0 is not None))
    return dp, dp[residue % 11]


def pair(B,W,J,U,C,q,k):
    h = list(B) + list(W)*q + list(J) + list(U)*k
    p = h + list(C) + h[::-1]
    assert p == p[::-1]
    return p


def a_formula(B,W,J,U,C,q,k):
    """Exact identity for odd palindromic C and even-length B/J, odd W/U."""
    assert len(B)%2 == len(J)%2 == 0
    assert len(W)%2 == len(U)%2 == len(C)%2 == 1
    return (2*alternating(B) + 2*alternating(W)*(q%2) +
            2*((-1)**q)*alternating(J) +
            2*((-1)**q)*(k%2)*alternating(U) +
            ((-1)**(q+k))*alternating(C))


def gate(B=B9,W=W9,C=ODD_C,junction_len=6):
    """Two consecutive restored epochs, q>=14 and k>=100, U^k -> U^(k+5).

    Source length is odd. Thirty overflows force an even digit-length
    intermediate, hence subsequent N_t ≡ 0 mod 11; P_{120} and P_{240}
    therefore have zero alternating coefficient sum modulo 11.

    Difference of restored parities forces A(U)=A(C) mod 11.
    For phase 9, A(B)=-6 and A(W)=12=-2A(B); so any q parity forces
    2A(J)+A(C)=-2A(B) (mod 11), i.e. A(J)=9 with C=(4,14,4).
    """
    assert junction_len == 6
    assert alternating(B)==-6 and alternating(W)==12
    assert alternating(C)==-6
    allowed=[(i+1,u) for i,u in enumerate(words_u())
             if (alternating(u)-alternating(C))%11==0]
    assert allowed==[(1,(9,0,18)), (29,(18,0,9))]
    residue=(-2*alternating(B)-alternating(C))*6%11  # inverse of 2 mod11
    assert residue==9
    return allowed,residue


def report():
    allowed,r=gate()
    dp0,n0=mod11_dp(j0=0,residue=r)
    dpa,na=mod11_dp(j0=None,residue=r)
    print('phase=9; |J|=6; odd C=(4,14,4); A(B9)=-6; A(W9)=12')
    print('necessary two-epoch U ranks:',allowed)
    print('necessary A(J) residue:',r,'mod 11')
    print('J[0]=0: exact residue-count vector',dp0,'pass',n0,'of',19**5)
    print('all J: exact residue-count vector',dpa,'pass',na,'of',19**6)
    print('J[0]=0: conditional survivors',len(allowed)*n0,'of',30*19**5,
          'ruled out',30*19**5-len(allowed)*n0)
    print('all J: conditional survivors',len(allowed)*na,'of',30*19**6,
          'ruled out',30*19**6-len(allowed)*na)
    print('NOTICE: endpoint-only 120-step return not exhaustively tested, and EVEN C has no mod-11 gate.')


def main():
    a=argparse.ArgumentParser()
    a.add_argument('--lattice',type=str,default=None)
    args=a.parse_args()
    if args.lattice:
        assert load_rows(args.lattice)==(W9,B9)
    report()

if __name__ == '__main__':main()
