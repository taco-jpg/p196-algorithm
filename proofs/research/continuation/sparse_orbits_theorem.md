# Every positive decimal reverse-and-add orbit has unbounded digit sum

This is an elementary proof using exact carries and the already proved
unboundedness of decimal width. It does not prove or disprove the existence
of decimal Lychrel numbers. It rules out every construction requiring an
eventually bounded digit sum, including the fixed-`C` all-time ordered-wall
criterion in `research/astra_moving_boundary_notes.md`.

No novelty claim is made. The argument below is a mathematical proof;
finite controls in the accompanying Python file are separate checks.

## 1. Definitions and exact transition

Let `n > 0` have canonical decimal digits `d_0,...,d_(L-1)`, indexed from
the least significant end. Thus `L >= 1` and `d_(L-1) > 0`; the units digit
may be zero. Write

    q_i = d_i + d_(L-1-i)                         (0 <= i < L).

Then `q` is symmetric, `0 <= q_i <= 18`, both its end entries are positive,
and

    sum_i q_i = 2 S(n),

where `S` is the ordinary decimal digit sum.

Define the ordinary forward carries and digits by

    a_0 = 0,
    q_i + a_i = r_i + 10 a_(i+1),
    a_i in {0,1},  r_i in {0,...,9}.

Put `h=a_L`, and define reflected carries and digits by

    b_i = a_(L-i)                                (0 <= i <= L),
    u_i = r_(L-1-i)                              (0 <= i < L).

Symmetry of `q` gives the second exact carry equation

    q_i + b_(i+1) = u_i + 10 b_i.                 (1)

The canonical width of `T(n)=n+reverse(n)` is `L+h`. If `h=0`, its next
pair-sum word is

    q'_i = r_i + u_i                             (0 <= i < L).  (2)

If `h=1`, its pair-sum word is

    q'_0 = r_0 + 1,
    q'_i = r_i + u_(i-1)                         (1 <= i < L),  (3)
    q'_L = 1 + r_0.

These formulas also cover `L=1`; the middle range in (3) is then empty.
In both branches the two endpoints of `q'` are positive. Consequently
every zero run of `q'` is strictly internal, and all indices used below
are valid. Dropping leading zeros in the numerical reversal causes no
problem: reversal is evaluated at the original fixed width, with any
new leading zeros contributing zero.

## 2. Simultaneous forward/backward zero digits

**Local lemma.** If `r_i=u_i=0` throughout an interval of at least two
consecutive positions, then throughout that interval `q` is identically
zero or identically nine.

At any position where both digits vanish, the two carry equations give

    q_i = 10 a_(i+1) - a_i = 10 b_i - b_(i+1).

Hence

    10 (a_(i+1)-b_i) = a_i-b_(i+1).

The right side belongs to `{-1,0,1}`, whereas the left side is divisible
by ten. They must both be zero, so

    a_(i+1)=b_i,       a_i=b_(i+1).                (4)

At two adjacent such positions `i,i+1`, (4) implies `a_(i+2)=a_i`.
Nonnegativity of both `q_i` and `q_(i+1)` now rules out unequal
`a_i,a_(i+1)`: the choices `(1,0)` and `(0,1)` would respectively give
`q_i=-1` and `q_(i+1)=-1`. Thus these three forward carries are equal,
and

    q_i = q_(i+1) = 9 a_i in {0,9}.

Applying this to every adjacent pair proves the local lemma. An isolated
simultaneous zero can also have `q_i=10`; this is why the minimum interval
length matters and why the short-run exceptions below are retained.

## 3. Exact zero-run inheritance, including overflow endpoints

Let `Z(q)` denote the maximum length of a consecutive run of zero entries
in the finite word `q`, with value zero when there are no zero entries.
Let `M=sum_i q_i`.

**No overflow.** A zero run `[A,B]` of `q'` of length `k >= 2` has
`r_i=u_i=0` on the same interval by (2). By the local lemma, either:

* the same old interval is all zero, so `k <= Z(q)`; or
* the same old interval is all nine, so `9 k <= M`.

Runs of length one need no classification. Therefore

    Z(q') <= max(Z(q), 1, floor(M/9))              if h=0.      (5)

**Overflow.** Consider a zero run `[A,B]` of `q'` of length `k >= 3`.
The positive outer entries imply `1 <= A <= B <= L-1`. By (3),

    r_i=0     for A <= i <= B,
    u_i=0     for A-1 <= i <= B-1.

Thus both digits vanish on the core `[A,B-1]`, whose length is `k-1 >= 2`.
By the local lemma this core is all zero or all nine. In the all-nine
case,

    9 (k-1) <= M.                                 (6)

In the all-zero case, zero input plus zero output in the carry equations
forces all the forward and backward carries within and at the ends of
this core to vanish. In particular,

    a_A=a_B=b_A=b_B=0.

At the left adjacent column, `u_(A-1)=0` and `b_A=0` give

    q_(A-1) = 10 b_(A-1).

But `a_A=0` gives `q_(A-1)+a_(A-1)<10`. These two facts imply
`q_(A-1)=0`.

At the right adjacent column, `r_B=0` and `a_B=0` give

    q_B = 10 a_(B+1).

But `b_B=0` gives `q_B+b_(B+1)<10`. Hence `q_B=0` as well.
The whole old interval `[A-1,B]` is therefore zero, of length `k+1`.

Runs of length one or two need no classification. In particular,

    Z(q') <= max(max(Z(q)-1,0), 2, floor(M/9)+1)  if h=1.      (7)

Equations (5) and (7) explicitly prevent a vanished nonzero block from
merging two arbitrarily long old zero gaps: every long inherited zero
run comes from a *single* old zero run. No claim about general sparse
cellular automata or eventual periodicity is used.

## 4. Bounded digit sum would bound width

Let `n_t=T^t(n_0)`, and suppose for contradiction that

    S(n_t) <= B                                    for all t>=0,

where `B` is a positive integer. Write `q_t,L_t` for the canonical
pair-sum word and width. Set

    K = max(Z(q_0), 2, floor(2B/9)+1),
    H = 2B + (2B-1)K.                             (8)

Since `sum q_t=2S(n_t)<=2B`, (5) and (7) show inductively that
`Z(q_t)<=K` at every time.

Let `m_t` be the number of nonzero entries of `q_t`. Each contributes at
least one to its mass, so `1<=m_t<=2B`. Both endpoints are nonzero; thus
there are at most `m_t-1` intervening zero runs. It follows that

    L_t <= m_t + (m_t-1)K <= 2B + (2B-1)K = H.     (9)

This contradicts unbounded canonical width. Even without a quantitative
width theorem, `T(n)>n` for every positive `n`, so an infinite orbit cannot
remain among the finitely many positive integers of width at most `H`.
For an explicit bound, the existing
`DecimalWidthGrowth.width_lower_bound` gives

    t + 4L_0 <= 4L_t + 4,                          (10)

so the contradiction has an explicit finite horizon.

**Theorem.** For every positive decimal integer `n` and every integer
`B>=1`, there exists a time `t>=0` with `S(T^t(n))>B`.

Applying the theorem to any iterate gives the equivalent tail statement:
on every tail the digit sums are unbounded. This is a `limsup=+infinity`
statement; the argument does not prove that digit sums tend to infinity.

## 5. Explicit finite-time bound and running maximum

If `S(n_0)<=B`, then (9) holds at time zero, so `H>=L_0`. If
`S(n_t)<=B` for every time `0<=t<=N`, the preceding induction and counting
argument apply on that finite interval. Combining (9) and (10) gives

    N <= 4(H-L_0)+4.                              (11)

Therefore some iterate satisfies `S(n_t)>B` with

    0 <= t <= 4(H-L_0)+5,
    H = 2B + (2B-1) max(Z(q_0),2,floor(2B/9)+1).  (12)

If `S(n_0)>B`, take `t=0` instead.

For a given finite horizon `N`, let

    D_N = max_(0<=t<=N) S(n_t).

Exactly the same proof, with `B=D_N`, gives the fully explicit inequality

    N + 4L_0
      <= 4 [2D_N + (2D_N-1)
                    max(Z(q_0),2,floor(2D_N/9)+1)] + 4.       (13)

In particular `D_N` grows at least on the order of `sqrt(N)` for a fixed
initial number. The displayed inequality is the precise claim; it is not
a lower bound for each individual `S(n_N)`.

## 6. Consequence for the fixed-distance moving wall

The all-time ordered-wall construction with one fixed finite `C>=1`
would, by its exact telescoping identity, produce a positive ordinary
reverse-and-add orbit with constant digit sum `9C` (from the first output
onward). The theorem rules this out.

Thus there are **no** finite `W_0,C` satisfying all the stated wall
admissibility and carried-digit ordering conditions at every time.
Every such fixed-`C` attempt must eventually fail one of those conditions.
The unconditional infinite-background wall orbit remains valid; the
impossibility concerns its proposed all-time embedding as one finite
integer orbit with fixed `C`.

This obstruction does not rule out a construction with an unbounded
renewal parameter `C`, and it gives no palindrome-attainment theorem.

## 7. General-base scope

The same unbounded-digit-sum theorem holds in every integer base `b>=2`.
Replace ten by `b`, nine by `b-1`, and the coefficient bound eighteen by
`2b-2` throughout the proof. Carries still lie in `{0,1}`. In the local
lemma, a multiple of `b` equal to an integer in `{-1,0,1}` must be zero;
the rest of the adjacent-column argument is unchanged. Newly created long
zero runs therefore come from old runs of the coefficient `b-1`, whose
length is bounded by pair-sum mass. Finally, strict increase of positive
reverse-and-add values supplies unbounded width in every base. The
decimal quantitative width bound (10) is used only for (11)--(13).

