# S12 even-centre modular structural lemma
**PAPER PROOF** of the identities below (all q,k and finite J,C).
**UNDECIDED** for physical seam regeneration and decimal Lychrel existence.

Let coefficients be LSD-first in 0..18. Fix B34,W9 from
calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt.
For an even-length palindromic C let C_left be its first half,
X=B34 W9^q J U3^k C_left, P=X reverse(X), and m=|X|.
Define E(A)=sum_r (-1)^r A_(2r), O(A)=sum_r (-1)^r A_(2r+1)
modulo 101. Because 10^2=-1 modulo 101,
V_10(A)=E+10O and V_(-10)(A)=E-10O.
A one-site position shift rotates R(E,O)=(-O,E).

## Folded endpoint lemma
Pair coefficient positions i and 2m-1-i. When m is even, their
mod-101 weights for i mod4 are 9*(-,+,+,-), yielding
V_10(P)=9*(O(X)-E(X)). When m is odd, the pair weights are
11*(+,+,-,-), yielding V_10(P)=11*(E(X)+O(X)).
These are exact polynomial equalities modulo101, for every X.

Increase k by five. At position h=34+9q+|J|+3k insert U^5
(15 coefficient positions), moving C_left fifteen positions to the right.
Let (ec,oc) be the unshifted moment of C_left and (eu,ou) that of U^5.
The new halfword X' therefore satisfies exactly

  (E,O)(X')=(E,O)(X)+R^h(eu+oc-ec, ou-ec-oc) (mod101).

Here R^15(ec,oc)=(oc,-ec), and |X'|=|X|+15 has opposite parity.
For U=(9,a,18-a), even a in [0,18], (eu,ou)=(a-9,a).
For its cyclic rotations use the same formula with actual U^5 charges.
Thus the proposed 120-step return must switch the two folded endpoint
channels. Because h=2+q+|J|+3k mod4, it must satisfy all 16
independent (q mod4,k mod4) classes. The commonly used four diagonal
q,k multiples of 20 check only residue class (0,0).

## Mod 9 and mod 11
The full P has even palindromic coefficient length, so its alternating
sum A(P)=0 (mod11) for ANY J,U,q,k. Odd-centre Q39 congruences are
inapplicable here (R33 and R07 independently corrected this).
Since sum(U)=27, increasing k by 5 changes the sum of all pair
coefficients by 2*5*27=270=0 mod9. Moreover 2^120=1 mod9, so
the 120-step mod9 endpoint charge condition is automatic.
These statements give no physical-carry return.

## Admissible junction moment theorem
For j=|J|>=1,
V(J)=E(J)+10O(J),
V(reverse(J))=10^(j-1)*(E(J)-10O(J)) (mod101).
The map from (E,O) to these ordered moments is invertible modulo101.
There are ne=ceil(j/2) independently chosen even-index digits and
no=floor(j/2) odd-index digits. Each signed sum ranges over a contiguous
integer interval of 18*ne+1 or 18*no+1 values respectively.
Reduction modulo101 gives exactly
  min(101,18*ceil(j/2)+1)*min(101,18*floor(j/2)+1)
attainable pairs. Exact counts j=0..12:
  1,19,361,703,1369,2035,3025,4015,5329,6643,8281,9191,10201.
At j>=12 all 101^2 ordered moments are attainable.
For palindromic even C of length c, V(C) is 9 (c=0 mod4)
or 11 (c=2 mod4) times a signed sum of c/2 digits, so its
attainable residue count is min(101,9*c+1). All residues occur at c>=12.
These are COMPLETE residue projection counts, not physically admissible
junctions: the actual carry trace still imposes additional conditions.

## Physical mod101 carry cocycle (R05 independently rederived)
Let P_t be any genuine palindromic pairword of length L_t, S_t=V(P_t),
c_(t,i) the actual decimal carry INTO column i (i=1..L_t),
gamma_t=c_(t,L_t), and K_t=sum_i c_(t,i)*(-10)^i (mod101).
Normalization gives V_(-10)(digits(V(P_t)))=V_(-10)(P_t)+2*K_t,
because carry at i contributes (-10)^i-10*(-10)^(i-1)=2*(-10)^i.
Reversal and symmetry imply for EVERY physical step

  S_(t+1)=(1-10^(gamma_t-2))*S_t
            +2*10^(L_t+gamma_t-1)*K_t (mod101).

Under actual gamma=(1000)^30, every four-step packet has multiplier 88,
and carries weights (8,4,2,1). Iterating 30 packets (R05 formula) yields

  S_120=84*S_0+57*10^L0 *
    sum_(r=0..29) 7^r*(8K_(4r)+4K_(4r+1)+2K_(4r+2)+K_(4r+3))
    (mod101).

The S12 folded endpoint lemma supplies a direct parity-complete
right-hand target for this physical-carry test. It cannot be checked
from J charges alone; any valid T* cycle must satisfy it at all 16
q,k classes AND physically regenerate the whole seam.

Reproduction: run python3 calculation/new_structures/S12/mod101_even.py.
It checks modulo-moment counts, folded source/target identities,
20 actual 120-step native-bigint/digit-vector trajectories including
all 16 classes and diagonal q=k=20,40,80,160. Finite controls only
check the identities; they are not evidence of a returning seam.