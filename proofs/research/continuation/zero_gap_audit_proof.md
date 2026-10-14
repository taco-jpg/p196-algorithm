# Independent audit: bounded digit sum is impossible

**Verdict:** the argument in `sparse_orbits_theorem.md` is valid as written.
I found no endpoint, canonical-width, carry-index, or short-word exception.
It proves that the digit sums on every positive decimal reverse-and-add
orbit are unbounded on every tail. It does not prove that the individual
digit sums tend to infinity, or decide any Lychrel question.

This is an independent mathematical audit, supplemented by exact finite
checks. It is not a claim that the whole theorem is already Lean-checked.

## 1. Definitions and canonical width

Let a positive integer have its canonical little-endian digit word
`d_0,...,d_(L-1)`, with `L>=1` and `d_(L-1)>=1`. Its units digit may be zero.
Set `q_i=d_i+d_(L-1-i)`; therefore both endpoints of q are positive,
`0<=q_i<=18`, and its total mass is `M=2S(n)`.

With forward carries `a_0=0` and

    q_i+a_i=r_i+10a_(i+1),

all carries are bits and all r are decimal digits. Put `h=a_L`. Since
`n+reverse(n)>=n`, its width cannot be below L. Its column representation
has width at most L+1. Hence it has canonical width L+h: when h=0 the
last r digit must be positive, and when h=1 the additional leading digit
is 1. This justifies the same-width or shifted reflection exactly; no
uncanonical padding remains in either branch.

Numerical reversal may delete leading zeros produced from trailing zeros
of n, but this has no effect on its fixed-width positional value. The
argument never assumes that the numerical reversal itself has width L.

For `b_i=a_(L-i)` and `u_i=r_(L-1-i)`, symmetry of q gives

    q_i+b_(i+1)=u_i+10b_i.

Thus the exact next pair sums are `r_i+u_i` in the no-overflow case. With
overflow they are `r_0+1` at both endpoints, and `r_i+u_(i-1)` at interior
positions `1<=i<L`. The formula includes L=1 (empty interior).

## 2. An independently derived local proof

At a site where both r and u vanish, regard `(a_i,b_i)` as the state on
its left and `(a_(i+1),b_(i+1))` as the state on its right. The two zero
equations are

    q_i=10a_(i+1)-a_i=10b_i-b_(i+1).

Because all four carries are bits and q is nonnegative, their complete
list of solutions is:

| Left state | Right state | q |
|---|---|---:|
| (0,0) | (0,0) | 0 |
| (0,1) | (1,0) | 10 |
| (1,1) | (1,1) | 9 |

The omitted formal possibility would have q=-1. The edge labelled 10
has neither a predecessor nor a successor in this graph. Therefore a
simultaneous-zero interval of length at least two is entirely q=0 or
entirely q=9. This does not assume anything about the outside carries.

It is necessary to retain the interval-length restriction. An isolated
simultaneous zero really can have q=10. For example `950+59=1009` has
old q=(9,10,9) and new q=(10,0,0,10). The overflow short-run exception
of length two is therefore real, though a coarser mass bound can absorb it.

## 3. Overflow extension and boundaries

Suppose a new overflow zero run is `[A,B]`, of length k>=3. Its endpoints
are strictly internal, so `1<=A<=B<=L-1`. The common r/u-zero core is
`[A,B-1]` of length k-1>=2. If its q values are nine, it uses mass
`9(k-1)<=M`.

If the core values are zero, both carry directions vanish throughout
the core and at its two boundaries, so `a_A=a_B=b_A=b_B=0`.

At the left adjacent column the new run also gives `u_(A-1)=0`. Hence
`q_(A-1)=10b_(A-1)`. But the forward output carry `a_A=0` forces
`q_(A-1)+a_(A-1)<10`. Consequently `q_(A-1)=0`.

At the right adjacent column the new run gives `r_B=0`. Hence
`q_B=10a_(B+1)`. But the backward output carry `b_B=0` forces
`q_B+b_(B+1)<10`. Consequently `q_B=0`.

Thus `[A-1,B]` was one old zero interval, of length k+1. All indices are
valid, including A=1 and B=L-1. If the extended interval would reach an
outer endpoint of q, this branch is simply impossible because that q
endpoint is positive. There is no missing special transition there.

This also settles potential merging of distant gaps: a new long zero
interval is either produced from one old zero interval or has an all-nine
core with the stated mass cost. It cannot acquire an uncharged extra gap.

For L=1 and L=2, there are no long new interior zero runs to classify.
For every L, the exceptional new runs of lengths one (no overflow) and
one or two (overflow) are covered explicitly by the constants below.

## 4. The quantitative bounds

For Z(q) the longest consecutive zero run (zero if absent), the proof gives

    no overflow: Z(q') <= max(Z(q),1,floor(M/9));
    overflow:    Z(q') <= max(max(Z(q)-1,0),2,floor(M/9)+1).

Consequently a putative bound `S(n_t)<=B`, with B>=1, gives

    K=max(Z(q_0),2,floor(2B/9)+1),
    Z(q_t)<=K,
    H=2B+(2B-1)K,
    L_t<=H.

For the last inequality, q_t has m positive positions with `1<=m<=2B`.
Both endpoints are positive, so at most m-1 zero gaps separate them.
Thus `L_t<=m+(m-1)K<=H`. This counting remains valid for L=1 and m=1.

Since every positive reverse-and-add step strictly increases its integer,
the orbit cannot stay among the finitely many positive integers of width
at most H. This already proves the theorem without any pre-existing
linear width-growth result. A very coarse self-contained escape bound
is `t<=10^H-n_0` whenever S(n_0)<=B.

The sharper bound in the audited note also checks out. The existing
`DecimalWidthGrowth.width_lower_bound` establishes

    t+4L_0<=4L_t+4.

I independently inspected its outer-column potential proof. Its values
are `P(1)=4`, `P(2)=3`, `P(3..5)=2`, `P(6..10)=1`, and `P(11..18)=0`.
For outer sum a and incoming top carry c, no overflow sends a to 2a+c
and satisfies `P(next)+1<=P(a)`. Overflow sends it to `(a mod 10)+1`
and satisfies `P(next)+1<=P(a)+4`. Telescoping and `0<=P<=4` prove the
displayed bound. These are precisely the concrete outer transitions.

Hence bounded mass through time N forces `N<=4(H-L_0)+4`. Some digit sum
exceeds B by time

    0<=t<=4(H-L_0)+5

when S(n_0)<=B; otherwise t=0 suffices. The off-by-one is correct.
With the initial potential retained, 4 can be replaced by P(q_0) in the
corresponding bound, but the stated uniform constant is valid.

## 5. Exact independent checks and their scope

Run `python3 continuation/zero_gap_audit_check.py`. It imports no discovery
or proof-author code, and writes `zero_gap_audit_results.json`.

The completed run checked:

- The complete bit-carry local simultaneous-zero transition table, and
  every concatenable pair of those edges.
- All 198,909 realizable canonical symmetric q-words of lengths 1 through
  8 (odd-length center entries restricted to even values).
- 288 structured words of lengths 9, 10, 31, 32, 99, 100, 299, and 300,
  covering long zero or nine interiors and all 18 possible positive outer
  sums, plus 13 explicit numeric edge cases.
- Both exact transition formulas, mirrored carry equations, canonical
  endpoint positivity, both precise gap inequalities, every classified
  long zero run, and agreement with ordinary integer addition using a
  canonical representative of each q-word.

All 199,210 complete word checks passed, including 105,132 overflow steps.
The general proof, rather than this finite scope, supplies the all-time
and unbounded-width conclusions.
