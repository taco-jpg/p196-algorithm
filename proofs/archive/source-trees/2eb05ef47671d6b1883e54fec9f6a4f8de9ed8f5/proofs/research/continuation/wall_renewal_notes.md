# Exact limits of two carry-hole renewal mechanisms

Status: no finite decimal Lychrel witness and no all-time renewal chain are
established here. These are exact obstructions for particular renewal
mechanisms, not impossibility results for decimal Lychrel numbers. The
positive parameter-growing family used in Section 2 is proved separately
in `renewal_search_notes.md`.

All words below are written from the low digit end. We use the wall and
finite-difference definitions from `astra_moving_boundary_notes.md`:

* a wall W has width w, entries between 0 and 18, and
  W_i + W_(w-1-i) = 18;
* its finite word at parameter C is q_i = f_i - f_(i-C), of length w+C;
* r is the normalized wall digit profile, h is its exterior carry;
* E missing carries increase the next digit sum from 9C to 9(C+E).

A restart with a balanced wall must therefore use D=C+E. Its necessary
and sufficient residue condition is

    sum(q'_i : i congruent j modulo D) = 18 for every j.

When 0 < E < C, the failure itself is safe: the next digit sum lies strictly
between the old digit sum and twice that sum. The exact palindrome-output
cases require a ratio of 2 or 4/11. Equivalently, at least one actual carry
remains, while the exceptional 0/11 predecessor is excluded by the original
residue sums 18.

## 1. A safe failure at the first collision can never rebalance

**Theorem.** Suppose w=C and the carried-digit ordering fails. Then either
the output is already a palindrome, or its q word fails the residue test
for D=C+E. In particular, no safe one-step renewal occurs exactly at this
first collision.

At w=C the input is q=W reverse(W). The known first-collision criterion
says failure is possible only when W_0=9 and h=1.

First suppose W is not all 9. Let k be the first position with W_k != 9.
Then k>=1, and h=1 implies W_k>=10: a neutral prefix transmits the carry
set by the first non-neutral entry in the reverse scan. Anti-complementarity
makes the opposite non-neutral entry low. Consequently the normalized low
digits satisfy

    r_0 = ... = r_(k-1) = 9,
    r_(C-k) = ... = r_(C-1) = 9,
    0 <= r_k <= 8.

Write s_j for the output digits from the second half reverse(W). The
complementary theoretical carry is initially 1, while the actual carry
arriving from the first half is 0. The first k coefficients are 9, so this
carry discrepancy persists through them. At position k the coefficient is
18-W_k<=8, which resets both outgoing carries to 0. Thereafter they agree.
Thus the **entire discrepancy** is

    s_j = 9              for 0 <= j < k,
    s_k = 8-r_k,
    s_j = 9-r_j          for k < j < C.

There are exactly E=k missing carries. The actual last carry is 1, so the
output has length 2C+1 and the only possible restart parameter is D=C+k.
Its outer q coefficient is

    q'_0 = 9+1 = 10.

At position C-k, the digit and its mirror have values 9 and 8-r_k, hence

    q'_(C-k) = 17-r_k.

Symmetry gives q'_D=q'_(C-k). Since 2D>2C, the entire residue-zero sum
modulo D is therefore

    q'_0 + q'_D = 27-r_k, which lies in [19,27].

It cannot equal 18. This directly proves failure of the restart condition.
Moreover k<C, so this is a safe failure, not a hidden palindrome case.

If W is all 9, every input coefficient is 9 and the actual addition has
no carries. The output is a palindrome, E=C, and its digit sum doubles.
This completes both cases.

The theorem excludes a particularly attractive replenishment scheme:
a successful restart at this location would have created a fresh central
18 reservoir of length 2k-1. That replenishment is prevented by the exact
outer residue discrepancy above. It does not exclude renewals after the
walls have already overlapped.

## 2. The exact 3:2 family does not close after its next failure

The positive family in `renewal_search_notes.md` gives, for every m>=1,
a safe renewal from C_old=4m+2 to C=6m+3. Its resulting wall is

    V_m = 1,9^(2m-1),8,2,9^(2m-1),16,10,9^(2m-1),17,
    |V_m| = C.

Starting at V_m, exactly the next eight updates obey the ordering condition.
Their overflow flags are

    0,0,0,1,0,0,1,1.

For m>=3 the wall after these eight updates is exactly

    W8_m = (1,6,6,5,13),18^(2m-5),(13,8,6,5,2),
           9^(2m-4),(16,13,12,10,5),0^(2m-5),(5,13,12,12,17).

It has width C+3. This identity follows from finite constant-run carry
normalization; no limit in m is taken. A precise symbolic implementation
is described in Section 3. The m=2 wall is

    (1,6,6,5,8,8,6,5,2,16,13,12,10,10,13,12,12,17).

Its relevant first and last coefficients agree with the general case.

For every m>=2, the only nontrivial ordering comparisons for W8 are

    (r_C,r_(C+1),r_(C+2),r_(C+3)) = (3,3,8,9),
    (r_0,r_1,r_2,r_3)             = (1,6,6,5).

Only the second comparison fails. The input q word has central triple
(11,6,11), and a carry 1 enters that triple. Its actual output digits are
(2,7,1), with the carry after its middle column missing and agreement
restored after the last column. Therefore E=1 exactly.

This ninth output is nonpalindromic. It has unchanged width

    L = 2C+3 = 2D+1, where D=C+1=6m+4.

The q word at the output nevertheless has

    q'_1 = 12,       q'_(D+1) = 3.

The first identity follows from the stable outer digit pairs 6 and 6; the
second follows from the central neighboring digits 2 and 1. These are the
only two entries in residue class 1 modulo D, so that residue sums to
15, not 18. **The parameter-growing family cannot be restarted after this
ninth update by its only possible balanced parameter.**

For m=1 the eighth wall is

    (1,5,9,15,1,1,17,17,3,9,13,17).

The next failure has E=2, hence D=11, and output length 21=2D-1. Its
central q coefficient is 16. This coefficient is the sole entry of its
residue class modulo D, again violating the required sum 18. The output
is safe because E=2<C=9.

This establishes a genuine parameter-growing renewal followed by an exact,
uniformly bounded continuation and a proved failure of immediate renewal.
It does not prove that later returns to balanced walls are impossible.
Nor does it prove that these integers subsequently reach palindromes.

## 3. Symbolic verification and independent integer controls

`wall_renewal_check.py` represents a constant-digit run by its digit and
an affine length a*k+b for every integer k>=0. Every normalization input
run is required to have strictly positive minimum length. The first
column fixes its carry; all remaining columns then use that fixed carry.
Pointwise addition aligns runs only when their affine boundary ordering
holds for every k>=0. A crossing which depends on k raises an error.

For m=k+4, these exact operations derive all eight wall phases, the
displayed W8 identity, and every ordering comparison. The full symbolic
phases and their affine lengths are saved in `wall_renewal_results.json`.
The cases m=1,2,3 are separate exact finite calculations. This covers
every positive m; the larger sample calculations are independent controls,
not the basis of the all-m claim.

Independent controls realize each q word as an ordinary positive decimal
integer and use literal reversal and addition. They verify 384 short-wall
first-collision instances, including the all-nine case, and the complete
continuations for m=1,...,24,50,100. The symbolic checker, the mathematical
proofs, and the integer controls are not Lean formalizations.

Run from the archive root with

    python continuation/wall_renewal_check.py

## 4. The remaining constructive obligation

A finite all-time construction still needs a rule that handles genuine
overlap and keeps producing safe states after residue imbalance. Two
precise possibilities remain:

1. A family of proved later return maps which rebalances after one or more
   intermediate unbalanced states, with a closed parameter update and
   safety proved at every intervening step.
2. A larger invariant allowing nonuniform residue budgets or several
   interacting walls, with exact carry control that prevents both
   palindrome-predecessor patterns indefinitely.

Neither is supplied by the 3:2 renewal alone. Repeating only renewals of
the form C -> 3C/2 also cannot give an infinite chain from a finite integer
C: each such update consumes one factor of 2. A usable construction must
include another parameter rule or a different invariant.

## 5. Divisibility cannot replace the q-residue restart condition

For ordinary digits, a positive multiple of 10^C-1 has digit sum at least
9C, with equality exactly when every digit-position residue has sum 9.
It is essential not to apply this statement directly to q coefficients,
which can exceed 9.

In particular, the two conditions

    S(n)=9C,       (10^C-1) divides n+reverse(n)

do **not** imply that n has balanced q residues 18. Here is an explicit
certificate at C=36. Its symmetric cyclic q budgets are

    (8,19,8,19,8,19,8,19,8,19,8,19,8,19,8,9,109,9,
     8,9,109,9,8,19,8,19,8,19,8,19,8,19,8,19,8,19).

They have sum 648=18C and satisfy B_j=10c_(j+1)-c_j cyclically for

    c=(2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,1,11,
       2,1,1,11,2,1,2,1,2,1,2,1,2,1,2,1,2,1).

Hence their base-10 value is divisible by 10^36-1. To realize them with
valid q coefficients, take length 505=14C+1. Put q_0=q_504=4 and
q_18=q_486=4. For each j=1,...,17, distribute B_j in chunks at most 18
over positions j,j+C,...,j+6C, and put equal coefficients at the reflected
positions. All unused entries are zero. The center is zero, the outer
coefficient is positive, and the resulting q word is valid and has exactly
the displayed residue budgets. Any decimal realization n has S(n)=324,
and T(n) is divisible by 10^36-1, but its q residues are not balanced.

The checker reconstructs this finite certificate directly. No solver or
unproved minimality assertion is needed for the counterexample.
