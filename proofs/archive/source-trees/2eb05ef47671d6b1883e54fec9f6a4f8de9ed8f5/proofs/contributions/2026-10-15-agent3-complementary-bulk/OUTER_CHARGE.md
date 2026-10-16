# All-width alternating-charge reset

Agent #3; independent mathematical derivation and Lean 4.19.0 verification.
No novelty, human-review, infinite-safety, or P196 claim.

For a least-significant-first word `B`, let

```
alt(B) = B[0] - B[1] + B[2] - ...,
s(B) = (-1)^|B|,
A(c,B) = 2*alt(B) + s(B)*c.
```

## The proved list-map theorem

Let `H(c,B)=(c',B')` be the exact autonomous outer map defined in
`OUTER_FACTOR.md`, with actual overflow `gamma`. For an admissible phase
`1<=c<=17`, `c!=9`, the following hold for **arbitrary finite length**:

* If `gamma=0`, then `A(c',B') = 2*A(c,B) (mod 11)`.
* If `gamma=1`, then `A(c',B') = 0 (mod 11)`.
* If every coefficient is in `0..18`, zero charge modulo 11 is forward invariant.

These are the accepted Lean declarations `step_charge_nonoverflow`,
`step_charge_overflow`, and `step_charge_preserves_zero` in
`OuterCharge.lean`. The first two even allow arbitrary natural coefficients
when the stated actual final carry is zero or one. Neither a bound on `B`
nor a supplied certificate nor a postulated transition appears as a hypothesis.
The map is defined explicitly with natural-number normalization, mirrored
coordinatewise addition, and maximal suffix trimming.

The module is standalone and uses a separate namespace; its explicit map
is the same list operation as `OuterEscape.lean`. Ordinary-decimal
semiconjugacy remains the written factor bridge, not an extra Lean axiom.
The axiom audit contains only standard `propext`, `Classical.choice`, and
`Quot.sound`; no `sorryAx`, custom axiom, or native-computation axiom.

## Derivation

First, appending a terminal bulk coefficient does not change the charge:

```
A(c,B ++ [c])
 = 2*(alt(B)+s(B)*c) - s(B)*c
 = A(c,B).
```

Thus maximal trimming preserves charge exactly, not just modulo 11.
Second, normalization `N(W,e)=(D,f)` satisfies

```
alt(D) + s(W)*f = alt(W) + e  (mod 11).
```

This follows inductively from `x+e = digit+10*carry` and `10=-1 (mod 11)`.
The Lean proof establishes this identity for every natural coefficient
word and every natural input carry, without digit-size restrictions.
Also `alt(reverse(W))=-s(W)*alt(W)` and normalization preserves length.

Write `k=1[c>=10]`, `t=c-9k`, `N(B,0)=(D,e)`,
`N(reverse(B),k)=(R,gamma)`, and `u=c+e-10k`. If `gamma=0`, the raw outer
word is `(D ++ [u]) + (reverse(R) ++ [t])`; its charge is
`2*A(c,B)-22*s(B)*k` modulo 11. If `gamma=1`, the raw word is
`(D ++ [u]) + ([1] ++ reverse(R))`; the normalization congruences cancel
its charge modulo 11. Trimming then leaves both conclusions unchanged.

## Connection to finite search and open formal work

Only the residue-zero subsystem can contain a returned canonical outer
cycle once such a cycle has an overflow. Positive leading-pair growth
forces an overflow in any five consecutive valid transitions: without an
overflow, the new leading pair is at least twice the old positive leading
pair, whereas all leading pairs are at most 18. Thus every returned outer
cycle lies in the residue-zero subsystem. The five-step consequence is a
**written argument**, not yet a checked declaration in this version; its
leading-pair and orbit-closure formal bridge is the next task.

The charge restriction does not imply monotone interface length or rule
out all cycles. In particular, it must not be confused with a Lychrel
certificate. Exhaustive tests on all 109,744 positive-head outer words of
length at most three, over all 16 admissible phases, agree with the formula
(51,824 nonoverflow, 57,920 overflow; record digest
`ff9227127518680fd94b008c02b729e4a69ba4e724b558567f9f10b61e26f090`).
These tests are controls; the all-length result is the Lean proof.

Two early compiler iterations failed on a dropWhile rewrite and obsolete
simp identifiers. They were fixed; no failed declaration is included as an
accepted result. Exact diagnostic/source snapshots are retained separately.
