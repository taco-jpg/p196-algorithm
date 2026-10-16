# Independent digit-mass audit and an obstruction to length–sum invariants

This is an algebraic audit, not a proof of a decimal Lychrel witness. The
palindrome digit-sum lemma is correct. A stronger negative result is proved
below: no nonempty universally safe, forward-closed family of positive
integers can be specified using only decimal length and digit sum. This
does **not** rule out an individual orbit with bounded digit sum, a family
with additional word information, or an invariant using carry information.

## 1. Conventions and the exact mass equation

Let `n>0` have `L` decimal digits `a_0,...,a_(L-1)`, indexed from the low
end, and write

    T(n) = n + reverse(n),
    S = S(n) = sum_i a_i,
    q_i = a_i + a_(L-1-i).

The word `q` is symmetric, every entry is in `0,...,18`, its outer entry is
positive, and its middle entry is even when `L` is odd. Conversely every
word with these properties has a positive `L`-digit decimal realization.

Use entering carries `c_0=0` and

    c_(i+1) = floor((q_i+c_i)/10),
    d_i = q_i+c_i-10*c_(i+1)                 (0 <= i < L).

Each carry is binary. Put `h=c_L` and `C=sum_(i=1)^L c_i`. If `h=1`, append
the new leading digit `d_L=1`; otherwise `T(n)` has length `L`. Summing all
output digits, including the final carry, gives exactly

    S(T(n)) = 2*S(n) - 9*C.                 (1)

In particular `S(T(n))=2*S(n)` if and only if there are no carries. In that
case the output is exactly the symmetric word `q`, so it is a palindrome.

## 2. Independent proof of both palindrome cases

This proof uses only the column equations above, not the archived
palindrome-predecessor theorem.

**No overflow.** If `h=0` and the output is a palindrome, comparison of
columns `i` and `L-1-i` cancels their equal `q` entries and gives

    c_i-c_(L-1-i) = 10*(c_(i+1)-c_(L-i)).

The left side has absolute value at most one. Thus both sides vanish.
The two resulting reflection equations imply `c_i=c_(i+2)` wherever the
indices exist. Also `c_(L-1)=c_0=0` and `c_L=0`; these two consecutive zero
values force every carry to be zero. The one-digit case follows directly
from the zero boundary carries. Conversely, zero carries give a palindrome.

**Overflow.** Now suppose `h=1` and the output is a palindrome of length
`L+1`. Its lowest digit must equal its new highest digit, so `d_0=1` and

    q_0 = 1+10*c_1.

The possibility `q_0=1` would give `q_(L-1)=1` and make a final carry
impossible. Therefore `q_0=11` and `c_1=c_L=1`.

Inductively suppose `q_(i-1)=11*c_i` and `c_i=c_(L+1-i)`. Palindromicity
gives `d_i=d_(L-i)`, while symmetry gives `q_(L-i)=q_(i-1)`. Substitution
into the column equations yields

    q_i = c_(L-i) + 10*c_(i+1).              (2)

If the two binary carries on the right differ, then either:

* `c_(L-i)=1, c_(i+1)=0`, giving `q_i=1`; or
* `c_(L-i)=0, c_(i+1)=1`, giving `q_i=10`.

Both are impossible at the mirrored column `L-1-i`, whose coefficient is
also `q_i`: coefficient 1 can never produce carry 1, and coefficient 10
can never produce carry 0. Consequently the two carries are equal and

    q_i = 11*c_(i+1),
    c_(i+1) = c_(L-i).

This advances the induction through the entire word. Thus an overflow
palindrome requires every `q_i` to lie in `{0,11}`, with outer coefficient
11. Conversely, for such a word set `b_i=q_i/11`; the outgoing carry is
`b_i` and the output digits are `b_i+b_(i-1)`, taking exterior `b` values
as zero. Symmetry of `b` makes this output a palindrome.

We have therefore independently obtained the exact criterion

    T(n) palindrome
      iff C=0
       or [h=1, q_0=11, and every q_i is 0 or 11]. (3)

## 3. Scalar and shape consequences

In the overflow case, write `B=#{i:q_i=11}`. Then `C=B` and `2*S=11*B`.
The number `B` is even: off-center entries occur in pairs, and an odd
word's even central entry cannot be 11. Consequently

    S(n) = 11*k,
    C = 2*k,
    S(T(n)) = 4*k                       (k >= 1).  (4)

Together with the no-carry case, this proves the proposed lemma:

    T(n) palindrome implies
      S(T(n)) = 2*S(n)
      or 11*S(T(n)) = 4*S(n).                (5)

Additional necessary features of the exceptional overflow case are:

* `2*k <= L`, and in fact `2*k <= L-1` if `L` is odd;
* every output digit belongs to `{0,1,2}`;
* the output begins and ends with 1;
* its digits are the convolution of a symmetric binary word with `(1,1)`;
* if the output has odd length, its central digit is 0 or 2;
* if the output has even length, its two central digits are 0 or 1.

Every palindrome produced by reverse-and-add has even digit sum and even
carry count. An odd carry count therefore guarantees safety for that step.
These are consequences of the exact criterion, not converses.

The upper scalar equality in (5) **is** sufficient for palindromicity,
because it forces `C=0`. The lower equality is not sufficient:

    3199 -> 13112,
    S=22, S'=8, C=4, q=(12,10,10,12),
    11*S'=4*S,

but the output is not a palindrome.

The strict interval

    4*S(n)/11 < S(T(n)) < 2*S(n)              (6)

is a correct one-step safety certificate. In carry language it is exactly

    0 < C < 2*S(n)/11.                       (7)

It is not forward invariant. The short counterexample is

    39 -> 132 -> 363,
    digit sums 12 -> 6 -> 12.

The first ratio is `1/2`, strictly inside (6), and the second step is a
no-carry palindrome. The other exceptional exit also occurs after safe
ratios:

    59 -> 154 -> 605 -> 1111,
    digit sums 14 -> 10 -> 11 -> 4.

The first two ratios lie inside (6), while the last is exactly `4/11` and
produces an overflow palindrome. Conversely (6) is not necessary for a
safe step: `1099 -> 11000` has digit sums `19 -> 2` and is nonpalindromic.

## 4. No universal invariant using only length and digit sum

For a set `A` of attainable pairs `(L,S)`, let

    F_A = {positive integers n : (length(n), S(n)) belongs to A}.

Call this family universally safe if `T(n)` is nonpalindromic for every
`n` in it, and forward closed if `T(n)` belongs to it for every `n` in it.

**Theorem.** If `F_A` is universally safe and forward closed, then it is
empty.

The proof uses two constructive lemmas.

**Lemma A.** For every `L>=1` and `1<=S<=floor(9*L/2)`, an `L`-digit
integer of digit sum `S` has a carry-free reverse-and-add step.

For `L=2m`, choose `m` independent symmetric pair coefficients in `0,...,9`,
with the outer one positive and their sum equal to `S`. Every integer sum
from 1 through `9m` is attainable. For `L=2m+1`, the central coefficient
can be `0,2,4,6,8`, contributing an additional `0,...,4` to `S`; again
every sum from 1 through `9m+4` is attainable, with the one-digit case
handled by digits 1 through 4. Realize the resulting `q` word as a positive
integer. Every coefficient is at most 9, so all carries are zero and the
output is palindromic.

**Lemma B.** For every `L>=1` and `floor(9*L/2)<S<=9*L`, an `L`-digit
integer of digit sum `S` can overflow with output digit sum at most `S`.

For `L=1`, choose the one-digit integer `S` (which is 5 through 9). Its
output has two digits and digit sum `2*S-9<=S`.

For even `L>=2`, start with symmetric coefficients

    q_0=q_(L-1)=10, all other q_i=9.

Their total is `9*L+2`. Increase symmetric coefficient pairs, never above
18, to reach total `2*S`; every intervening even total is attainable.
The first coefficient starts a carry, and all later coefficients are at
least 9, so all `L` columns produce a carry. Therefore the output has
length `L+1` and

    S'=2*S-9*L <= S.

For odd `L>=3` and `S>=(9*L+3)/2`, use the same baseline but raise its
central coefficient from 9 to 10. The baseline total is `9*L+3`.
Increase symmetric pairs and the even central coefficient to reach every
admissible total `2*S`. All columns again carry, with the same inequality.

The only remaining case is odd `L=2m+1>=3` and `S=(9*L+1)/2`. Use outer
coefficients 10, central coefficient 8, and all other coefficients 9.
The first `m` columns carry. The center clears the carry; the following
neutral coefficients 9 do not restart it; the final outer 10 does. Thus
`C=m+1=(L+1)/2`, the step overflows, and

    S'=2*S-9*(L+1)/2 = S-4 <= S.

This proves Lemma B in every case.

**Proof of the theorem.** Universal safety and Lemma A force every pair
in `A` to satisfy `S>floor(9*L/2)`. Start with any pair in `A`. Lemma B
provides an integer in its entire scalar class whose output has length
`L+1` and digit sum `S'<=S`. Forward closure forces that new pair into `A`.
Repeat. The lengths increase by one each time while digit sums remain at
most their initial value. Eventually the inequality demanded by universal
safety fails, a contradiction.

The argument even rules out arbitrary time-indexed families `A_t` if
every associated whole scalar class is safe and `T(F_(A_t))` is contained
in `F_(A_(t+1))`.

The witnesses chosen at successive scalar pairs need not be successive
members of one actual orbit. This distinction is essential: the theorem
obstructs a universal scalar abstraction, not individual low-mass orbits.
Additional digit arrangement, carry arrangement, or history information
can prevent the adversarial transitions used in the proof.

## 5. Finite independent controls

Run from any working directory with

    python /workspace/scratch/fe6abe1df721/continuation/digit_mass_audit_check.py

The script uses ordinary integer reversal and addition and independently
realizes every admissible symmetric `q` word of lengths 1 through 8:

* 198,909 total words;
* 93,931 no-overflow and 104,978 overflow steps;
* 14,998 no-carry palindrome cases and 22 exceptional palindrome cases;
* 182,809 steps satisfying the strict ratio interval, all nonpalindromic.

It verifies the exact column output, mass equation, complete palindrome
criterion, scalar lemma, and exceptional digit-shape restrictions.
It also verifies both constructors at every `(L,S)` cell through `L=80`:
14,560 carry-free cells and 14,600 nonincreasing-overflow cells. These
checks validate the implementation; the proofs establish all-length
claims. Complete counts and short counterexamples are saved in
`digit_mass_audit_results.json`.

No all-time safe finite decimal seed is established here. The mass route
needs a proved constraint on the actual digit or carry arrangement; a
universally closed set of length-and-sum cells cannot supply it.
