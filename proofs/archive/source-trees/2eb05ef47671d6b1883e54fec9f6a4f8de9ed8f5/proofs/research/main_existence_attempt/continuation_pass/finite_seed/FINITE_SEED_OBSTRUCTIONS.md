# Finite-seed extraction: an exact arithmetic countermodel and a safe-fiber obstruction

14 October 2026. **Decimal Lychrel existence remains unproved.** Neither
result below is a Lychrel witness or an obstruction to every possible
existence proof. The first shows precisely which collection of existing
facts is insufficient. The second is an actual reverse-and-add theorem
excluding a stated family of weighted inverse-counting arguments.

This branch read the correlation and renewal status reports and the prior
`return_pass/probability/PROBABILITY_RESULT.md`. In particular, the
finite-atom observation and the exact one-step counts are prior work, not
new claims here. The present countermodel preserves the exact actual
one-step palindrome predecessor set, so it goes beyond the bare example
of decreasing nonempty sets with empty intersection.

## 1. Notation and the exact terminal constraint

Let `T(n)=n+reverse10(n)` for positive ordinary decimal integers. Let `P`
be the set of decimal palindromes and put

    B = {n > 0 : T(n) is in P}.

If `q_i` is the sum of a digit and its reflected digit, the existing exact
classification says that `n` is in `B` if and only if either:

1. every `q_i` is at most 9; or
2. the outer coefficient is 11 and every coefficient belongs to `{0,11}`.

The countermodel below preserves this set `B` exactly, and uses the true
reverse-and-add map on every member of `B`. It does **not** claim to
preserve the complete reverse-and-add update outside `B`.

## 2. A fully terminating map with the same exact predecessor set

Fix any function `ell : {3,4,...} -> N` whose values are finite. It may
grow arbitrarily quickly. Define the sparse chain nodes

    c(a,j) = 10^(a+j) + 10a + 9,
    a >= 3,  0 <= j <= ell(a).

Their width is `a+j+1`: the inequality `10a+9 < 10^a` holds for every
`a>=3`. Every chain node starts with 1 and ends with 9. It is therefore
nonpalindromic, and its outer pair sum 10 excludes both classes defining
`B`. The labels are unique. The width determines `a+j`; after subtracting
its leading power of ten, the remainder `10a+9` determines `a`, and then
`j`.

Set

    b(a) = 10^(a+ell(a)+1) + 2.

This number is nonpalindromic and lies in `B`: its outer pair sum is 3
and every other pair sum is zero. Its true next iterate is the palindrome

    T(b(a)) = 3 * 10^(a+ell(a)+1) + 3.

Now define a map `F_ell` on all positive integers in this order:

| Input | Output |
|---|---|
| `n in B` | `T(n)` |
| `n=c(a,j)` with `j<ell(a)` | `c(a,j+1)` |
| `n=c(a,ell(a))` | `b(a)` |
| remaining one-digit `n` | `19` |
| remaining two-digit `n` | `109` |
| remaining `L`-digit `n`, `L>=3` | `c(L,0)` |

The cases are unambiguous because no chain node is in `B`. Also
`19` and `109` are outside `P` and `B`; their true next outputs are
`110` and `1010`. Thus their artificial path is

    19 -> 109 -> c(3,0).

### Exact preservation and complete termination

For every positive `n`,

    F_ell(n) is palindromic  if and only if  n is in B.

The forward direction uses the table: every displayed output for an
input outside `B` is nonpalindromic. The reverse direction follows from
the unchanged true map on `B`.

Every orbit reaches a palindrome after finitely many positive steps.
An input in `B` does so in one step. A chain input has a finite remaining
chain followed by `b(a)` and its palindromic output. Any other input
enters a chain after at most three steps.

More precisely, if an `L`-digit input with `L>=3` is outside `B` and
is not a chain node, its **first positive** palindrome time is exactly

    tau(n) = ell(L) + 3.

Indeed, its times `1,...,ell(L)+1` are respectively
`c(L,0),...,c(L,ell(L))`; time `ell(L)+2` is `b(L)`; and only time
`ell(L)+3` is palindromic. If the initial input is also nonpalindromic,
the whole segment indexed `0,...,ell(L)+2` is safe.

### Numeric and width growth are also preserved

Every positive input satisfies

    n < F_ell(n) < 11n,
    width(n) <= width(F_ell(n)) <= width(n)+1.

On `B`, these are true reverse-and-add bounds. Every artificial step
from outside `B` increases width by exactly one. For a generic width
`L>=3`,

    c(L,0) = 10^L+10L+9
           < 10^L+10^(L-1)
           <= 11n.

The strict middle inequality holds already at `L=3` and then by
induction. A chain step, including the final step to `b(a)`, is less
than ten times its input. For the two small-width branches the smallest
possible inputs outside `B` are 5 and 19 respectively, so the claimed
bound holds directly.

The prior five-step growth bound is preserved on **every** orbit:

    width(F_ell^t(n)) >= width(n) + floor(t/5).

Here is an independent justification. If five consecutive artificial
steps had no width increase, their five sources would all be in `B`.
All five steps would then be genuine no-overflow reverse-and-add steps.
After the first such step both endpoint digits are positive and the
leading digit is at least the trailing digit. The trailing digit then
at least doubles at each further no-overflow step. Five no-overflow
steps would require a trailing digit at least 16, a contradiction.
Grouping steps into blocks of five gives the bound.

### Arbitrarily strong width-dependent survival density

At a fixed width `L`, there are at most `L-3` chain nodes. In fact, a
chain node at this width has `3<=a<=L-1` and the uniquely determined
`j=L-a-1`; the condition `j<=ell(a)` only removes possibilities.

There are exactly `9*10^(L-1)` canonical inputs of width `L` and
`9*10^(ceil(L/2)-1)` palindromes. The already established one-step
counts are, for `m>=1`,

    |B at width 1| = 4,
    |B at width 2m| = 45*55^(m-1) + 8*9^(m-1),
    |B at width 2m+1| = 225*55^(m-1) + 8*9^(m-1).

Consequently the fraction of inputs safe through index `ell(L)+2` is
at least

    1 - (|B at width L| + 9*10^(ceil(L/2)-1) + (L-3))
            / (9*10^(L-1)),              L>=3.

This lower bound tends to 1. It is independent of the size of `ell(L)`.
For any prescribed finite horizon function `h(L)`, choosing
`ell(L)=max(L,h(L)-2)` therefore gives density-one survival through
`h(L)`, while **every individual integer still terminates**. If `h` is
computable, the countermap is computable as well.

The elementary choice `ell(L)=L` already gives density-one survival
through `L+2`, substantially beyond a horizon proportional to `log L`.
No assertion is made that one map outlasts every horizon function at
once; the quantifiers are `for every h, there is a terminating F_ell`.

### The same explicit finite-prefix seed family survives

Take `ell(L)=L`. The existing actual-RAA finite-prefix family is

    C_R = 2 * (10^(floor(7R/4)+1) - 1).

It also survives through index `R` in this fully terminating countermap.
For `R=0`, `C_R=18` is nonpalindromic and its first positive hit is 1.
For `R>=1`, put `k=floor(7R/4)+1>=2`. The decimal word is

    C_R = 1 9^(k-1) 8.

It is nonpalindromic. Its outer pair sum is 9 and an interior pair sum
is 18, so it is outside `B`. It is not a chain node, since it ends in 8.
Its width is `k+1`, and its exact countermap first-hit time is

    tau(C_R) = k+4 = floor(7R/4)+5 > R.

Thus the concrete finite-prefix construction, not merely the statement
that arbitrary finite delays exist, is compatible with complete
termination when only the preserved properties are used.

### What this countermodel excludes

The following facts, even in conjunction, cannot imply a fixed surviving
finite seed without additional update-specific information:

- the exact actual one-step palindrome predecessor classes;
- the exact true update on those predecessor classes;
- strict numeric growth, the bound `<11n`, at most one new digit per step,
  and at least one new digit per five steps;
- the displayed explicit finite-prefix seed construction;
- density-one avoidance at all width-dependent horizons under discussion,
  even if those horizons are increased arbitrarily before choosing the
  countermap.

The true map has many further arithmetic correlations. This result does
not exclude using those correlations, an invariant, a recurrent finite
return, or a genuinely uniform first-hit estimate on one fixed ensemble.

### The countermodel can also preserve the complete pair-word quotient

The same construction can be strengthened further. Write `Q(n)` for the
complete symmetric mirrored-pair word of a canonical input. Replace each
special chain node in the table by its entire class

    E(a,j) = {n : Q(n)=Q(c(a,j))}.

Every member of `E(a,j)` is outside `B`, since its outer pair sum is 10.
Give every member the same outgoing value prescribed for `c(a,j)`.
All other cases remain unchanged. The resulting map `F*_ell` has all the
properties proved above and in addition satisfies

    Q(n)=Q(n')  implies  F*_ell(n)=F*_ell(n').

Thus the fact that the true update factors through its complete pair
word can be retained as well. This does not preserve the true arithmetic
value of that update outside `B`.

Here are the checks needed for this strengthening. At width `L`, a
special label has `3<=a<=L-1`. For `L>=4`,

    L-1 < 10^floor((L-2)/2).

The inequality follows at `L=4,5` directly and then by induction in
steps of two. Therefore the decimal digits of `a` in `c(a,j)` occupy
only one side of the interior and do not overlap their reflection. Its
outer pair coefficient is 10; the low interior half lists the decimal
digits of `a` followed by zeros; and an odd center is zero. This makes
the classes at a fixed width disjoint and determines their labels
uniquely. Their exact sizes are

    |E(a,j)| = 9 * product_(digits d of a) (d+1) <= 90a.

There are nine outer digit pairs summing to 10, while an interior sum
`d<=9` has exactly `d+1` realizations. Every zero pair and an odd zero
center are forced. The classes at width `L` thus contain at most
`45L(L-1)` inputs altogether, still a negligible fraction of
`9*10^(L-1)`.

All outputs remain exactly those already shown in the table. The
termination proof and exact generic delay are unchanged. For a class
input of width `L`, the next chain value is `10^L+10a+9`, or its final
output is `10^L+2`; since `a<=L-1`, the same `<11n` bound holds. The
same density proof uses `45L(L-1)` in place of `L-3`. Finally, every
`C_R` has outer pair sum 9, so it belongs to none of these enlarged
special classes and retains exactly the stated delay.

The executable audit separately checks this stronger map on all
`1,...,99999`, including equality of outputs for every shared pair word,
the exact special-class counts through width five, and complete
terminating trajectories on `1,...,9999`.

## 3. Actual safe states have unbounded incoming weight amplification

This section is about the **true** map `T`, not the countermap. Let

    S = {n>0 : n is not palindromic and T(n) is not palindromic}.

For every `m>=2` define

    y_m = 10^(2m) + 99*10^(m-1) - 1
        = 1 0^(m-1) 9 8 9^(m-1)  (decimal word).

The first and last digits are 1 and 9, so `y_m` is nonpalindromic.
Its outer pair sum is 10; hence `y_m` is outside `B` and belongs to `S`.

Let `A` be any canonical `(m-1)`-digit word and let `bar(A^rev)` mean
the digitwise 9-complement of its reversal, with its full width retained.
Form

    n_A = A || 99 || bar(A^rev).

There are exactly `9*10^(m-2)` distinct inputs of this form, all of
width `2m`. Their mirrored pair coefficients are 9 everywhere except
the two central coefficients, which are 18. Therefore

    T(n_A) = (10^(2m)-1) + 9*(10^(m-1)+10^m)
           = y_m.

Every `n_A` is nonpalindromic, because its outer reflected digits sum
to the odd number 9. The coefficient 18 excludes the all-small class,
and the outside coefficient 9 excludes the overflow class. Thus every
`n_A` belongs to `S`, as does its target. Also

    n_A < 10^(2m) < y_m.

Let `w` be any positive nonincreasing function on positive integers
(monotonicity on `S` alone suffices). Define the safe incoming-weight
operator by

    (L_S w)(y) = sum_{n in S, T(n)=y} w(n),    y in S.

All these sums are finite because true reverse-and-add strictly
increases a positive input. The explicit fiber proves

    (L_S w)(y_m) / w(y_m) >= 9*10^(m-2).

The right side is unbounded. In particular **no finite constant `C`**
can satisfy `L_S w <= Cw` at every safe state, and a uniform contraction
with `C<1` is impossible. This excludes such pointwise inverse estimates
for every positive polynomially decreasing, exponentially decreasing,
or otherwise nonincreasing seed-size weight, even after deleting both
palindromes and their immediate predecessors.

The amplification has the square-root scale of the target. Since
`y_m < (11/10)*10^(2m)`, the displayed ratio is strictly larger than

    (9/100)*sqrt(10/11)*sqrt(y_m).

For example, `y_2=10989` has the nine certified safe predecessors
`1998,2997,3996,4995,5994,6993,7992,8991,9990`. At `m=6`, the same
construction gives 90,000 distinct safe predecessors of
`1000009899999`.

This is an obstruction to one **specified** weighting method. It does
not exclude target-dependent weights that heavily favor merging states,
aggregate estimates allowing a large exceptional set, widths with
separate normalizations, or cancellation methods. No novelty claim is
made for the high-fiber phenomenon.

## 4. Fixed-target inverse depth is automatically finite

For completeness, the actual five-step width-growth lemma also yields a
uniform bound for a fixed target. If `T^t(n)=p` with `n>0` and `p` of
decimal width `M`, then

    1 + floor(t/5) <= M,
    t <= 5M-1.

Strict numeric growth separately gives `t<=p-1`. Thus every fixed
palindrome target has a finite inverse tree of depth at most
`min(p-1,5M-1)`, independently of whether Lychrel seeds exist. Arbitrarily
deep inverse chains must change their targets. A compactness argument
anchored to one finite target therefore cannot supply an infinite
forward survivor; the required unbounded fixed-target depth is itself
impossible. This elementary consequence is included to make the
target-dependence explicit, not as a new existence theorem.

## 5. Verification and remaining obligation

Run from the project root:

    python main_existence_attempt/continuation_pass/finite_seed/check_finite_seed_obstructions.py

The executable audit writes `check_finite_seed_obstructions.json` and
checks:

- the exact predecessor classification, identical immediate-hit sets,
  numeric bounds and width bounds on every integer `1,...,99999`;
- complete first-positive-hit trajectories of all `1,...,9999` in the
  linear-delay countermap, including the exact generic delay formula and
  the five-step width inequality;
- exact one-step counts and sparse-chain counts through width five;
- the same `C_R` family at `R=0,...,64,128,256`, all eventually terminating
  in the model but all safe through their asserted horizons;
- a quadratic-delay variant at widths `3,...,15`;
- the pair-word-preserving strengthened countermap on all
  `1,...,99999`, with all its first-hit trajectories on `1,...,9999`;
- all 99,999 displayed safe predecessors from `m=2,...,6`, using ordinary
  integer reversal and addition, with hashes and extrema retained.

Every check passed. The all-parameter results are the written proofs
above; this branch adds no Lean theorem and makes no external peer-review
claim. No remote writes were performed.

The remaining positive obligation is unchanged: use additional exact
reverse-and-add information to produce one finite seed with all-time
safety. The countermodel identifies a collection of strong but
insufficient premises, and the actual inverse-fiber theorem removes a
broad simple class of weighted contractions from the proposed extraction
routes. Neither settles decimal Lychrel existence.
