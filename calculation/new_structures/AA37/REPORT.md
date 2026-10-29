# AA37 REPORT — 2-adic 120-clock cocycle

Status: PARTIAL; no candidate, pruning theorem, or all-time certificate found.

## Exact recurrence

For a canonical decimal source with digits d_0,...,d_{n-1} listed least-significant first, one ordinary reverse-and-add step is computed by
\[
z_i=d_i+d_{n-1-i}+c_i,\quad e_i=z_i\bmod 10,\quad
c_{i+1}=\lfloor z_i/10\rfloor,\quad c_0=0.
\]
The output is the digits e_i followed by the final carry if nonzero. Consequently, for every r>=1,
\[
N'\equiv \sum_{i=0}^{r-1} e_i10^i\pmod{2^r}.
\]
This is exact because 2^r divides 10^i for every i>=r. The first r output digits are determined by the first r pair coefficients P_i=d_i+d_{n-1-i} and the carry recurrence, including the low-side carry state.

## What the 2-adic condition does and does not say

A two-epoch return necessarily reproduces this low-side carry/output state at each endpoint, modulo 2^r for every r. But a symmetric pair-word P does not by itself specify the physical low-side digits d_i; it specifies sums of opposite-end digits. Therefore a residue-only filter on (J,C,U) is not sound unless it is augmented by the canonical physical root and the two-sided carry state. This prevents treating a pair-word mod-2^r calculation as an independent necessary gate on J,C,U.

## Exact missing lemma for this route

Prove that the canonical rooted p12/m9 physical realization induces a finite 2-adic carry cocycle on the 120-clock seam map, and derive a nontrivial endpoint equality/obstruction for a two-epoch return that is independent of the already-known mod-101 obstruction and the fixed-seam results. No such nontrivial equality has been established here.

## Scope and status

This is a recurrence-level reduction only, not a new exclusion, not a checked seam, and not a decimal Lychrel proof. No big-integer replay was performed for a candidate because no candidate was synthesized. Label: UNDECIDED.
