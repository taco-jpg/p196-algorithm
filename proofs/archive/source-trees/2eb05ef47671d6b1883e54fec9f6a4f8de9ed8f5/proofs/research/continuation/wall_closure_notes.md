# Fixed-distance wall closure: an exact quotient test and the C=1 obstruction

Integration update, 14 October 2026: the subsequent general theorem in
`UnboundedDigitSums.pdf` and `LychrelDigitSums.lean` rules out the all-time
fixed-C construction for every finite C. Its conditions would force constant
digit sum 9*C. The identities and C=1 proof below remain valid; references
below to an unresolved larger-C case describe this branch before integration.

Status: no finite decimal Lychrel witness is asserted. The statements below
are proved algebraically. Finite controls check the implementations only.
This file does not assert a general fixed-C impossibility theorem.

## 1. A finite quotient characterization of the carried-digit ordering

Use the moving-wall notation in `research/astra_moving_boundary_notes.md`.
For an admissible anti-complement wall W of width w, put

    A(W) = 2*10^w - sum_i W[i]*10^i.

Since 0 <= W[i] <= 18, A(W) >= 2. If f is the full 0/W/18 profile,
normalization of f gives its digit profile r, equal to 0 at negative
indices and eventually 9 at positive indices. Let e_i be the ordinary
decimal digit in position i of A(W)-1, extended by zero above its width.
Then the following exact identity holds for every i >= 0:

    r_i = 9-e_i.                                           (1)

Proof without infinite arithmetic: choose any N >= w+2. The first N
coefficients of f represent

    sum_(0<=i<N) f_i*10^i = 2*10^N-A(W).

The carry entering position N is 1. Thus their first N normalized digits
represent 10^N-A(W), which is the digitwise 9-complement, in N places, of
A(W)-1. Increasing N proves (1) at every nonnegative index.

Consequently the moving-wall condition

    r_i >= r_(i-C) for every i

is equivalent to

    e_i <= e_(i-C) for every i >= C.                        (2)

The comparisons with 0 <= i < C are automatic because the negative r
tail is zero. Thus each of the C residue classes of digits of A(W)-1
must be nonincreasing when read from low positions toward high positions.
This equivalence does not assume the separate coefficient condition (F).

The finite difference q_i=f_i-f_(i-C), whether or not its coefficients are
all nonnegative, has the exact polynomial evaluation

    sum_i q_i*10^i = (10^C-1)*A(W).                         (3)

When (F) holds, the left side is the actual reverse-and-add output of any
ordinary decimal realization of q. Thus A(W) is its positive quotient by
10^C-1. Equation (2) gives a compact test on that quotient for the exact
digit-ordering condition used by the wall theorem.

An equivalent finite decomposition follows from (2). Define

    lambda_(j,m) = e_(j+(m-1)C)-e_(j+mC),   m>=1.

Every lambda is nonnegative, all but finitely many vanish, and
sum_m lambda_(j,m)=e_j<=9. Therefore

    A(W)-1 = sum_(j=0)^(C-1) 10^j *
             sum_(m>=1) lambda_(j,m)*(10^(Cm)-1)/(10^C-1). (4)

Conversely, a decomposition (4) with nonnegative integer lambdas and
sum_m lambda_(j,m)<=9 produces exactly the digit monotonicity (2), because
the represented digit at j+kC is sum_(m>k)lambda_(j,m), which is at most 9.
No inter-column carry occurs in that representation. There are at most
9C unit summands, but their lengths m are unbounded. This observation
alone is not a finite-state termination proof.

## 2. Every digit-sum-9 integer reaches a palindrome within three steps

Let T(n)=n+reverse(n), and let S be ordinary decimal digit sum. If c is
the number of carries in this addition, including a final overflow carry,
then

    S(T(n)) = 2*S(n)-9*c.                                  (5)

Assume S(n)=9. Write n's L digits as d_i, low first, and put
q_i=d_i+d_(L-1-i). If i is not the actual center, its two digit positions
are distinct and hence

    q_i <= S(n) = 9.

An initial carry cannot start at such a position. There are two cases.

* If L is even, or if the central digit x (when L is odd) is at most 4,
  no carry starts anywhere. T(n) has the symmetric digit word q and is a
  palindrome.

* If L is odd and x>=5, the only possible initiating carry is at the
  center. The sum of every other digit is 9-x<=4, so every off-center q_i
  is at most 4. The center carry therefore stops immediately in the next
  column. There is exactly one carry, so S(T(n))=9.

For L>=3 in the second case there is no final overflow, the width stays
L, and the new central digit is

    x' = 2*x-10.                                          (6)

The leading digit of n is positive and lies outside the center, so x<=8.
If x is 5, 6, or 7, then x' is 0, 2, or 4, and the next addition has no
carries and produces a palindrome. If x=8, the central digits on successive
sum-preserving steps are 8 -> 6 -> 2, and the third addition produces a
palindrome. Finally the sole one-digit number of digit sum 9 is 9, whose
orbit starts 9 -> 18 -> 99.

This proves the stated three-step bound. It is sharp:

    180 -> 261 -> 423 -> 747.

In particular, at most two consecutive reverse-and-add steps can preserve
digit sum 9. This is stronger than merely saying that such a trajectory
cannot preserve its digit sum forever.

## 3. Consequence for fixed C=1 moving walls

For C=1, the telescoping identity of the wall construction gives
sum_i q_i=18. Every ordinary decimal realization n of q therefore has
S(n)=9. Each successful wall step preserves this digit sum. Section 2
therefore rules out a third consecutive successful wall step from any
valid fixed-C=1 state. In particular, no finite wall with C=1 can satisfy
(F) initially and the ordering condition (R) at every future time.

This is a theorem for arbitrary wall width, not an inference from the
finite enumeration below. It does not settle any C>=2.

## 4. Reproducible controls

Run:

    python continuation/wall_closure_check.py

The script independently checks the digit-sum-9 theorem on all decimal
digit words of widths 1 through 8 and digit sum 9, checks longer random
digit-sum-9 words, and checks the quotient identities on exhaustive short
anti-complement walls plus reproducible random longer walls. It also
checks the arbitrary-width C=1 obstruction on a family of long monotone
anti-complement walls. Counts and the sharp example are written beside
the script in `wall_closure_results.json`.

Remaining gap: for C>=2, equations (2) and (4) merely characterize the
ordering at one time. They do not prove that the wall update eventually
destroys it, nor supply an all-time orbit that preserves it. In particular,
the bounded number of summands in (4) does not bound their positions or
their future interactions.
