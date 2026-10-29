# AA40 report — cocycle / p-adic closure, variant 8

**Status: PARTIAL. No T* candidate found; no two-epoch return proved; no all-time certificate.**

## Route and exact target

I registered `COCYCLE/P-ADIC variant-8 free choice` in issue #475. This attempt builds on the current strict W9 MDD / epoch-seam map status (r)-(t), and specifically on U16's full-pairword Q999 carry-cocycle identity. The fixed-seam and mod-101 standalone avenues are not being treated as universal obstructions.

The target remains the rooted decimal p12/m9 family
`P(q,k;J,U,C)=H(q,k) ++ C ++ reverse(H(q,k))`,
`H(q,k)=B ++ W^q ++ J ++ U^k`,
with the genuine 120-step map `(q,k;J,U,C)->(q,k+5;J,U,C)` (or a separately specified closed seam family), for all sufficiently large independent q,k, with non-palindrome guards at every intermediate step.

## Exact necessary cocycle condition already available

For a genuine decimal pairword P of length n, let `Q_m(P)=sum_i P_i 10^i mod m`, physical carries be `c_0=0,...,c_n=g`, and `kappa=sum_j c_j 10^{-j} mod 999`. The full-step identity reported by U16 is
`Q999(P') = (1+10^g) Q999(P) - 99*10^(n-1+g)*kappa (mod 999)`.

On the rooted 120-step p12 clock (90 steps with g=0, 30 with g=1), the macro multiplier is 73 modulo 999. Therefore every genuine return must satisfy
`(Q999(target)-73*Q999(source))/9 + 11*S = 0 (mod 111)`,
where S is the exact accumulated weighted physical-carry cocycle across the macro. This is necessary, not sufficient. It does not license replacing S with a seam-only constant.

## What I established in this attempt

- The mod-101 four-position digit-class expression is easy to state, but is not seam-closed on its own: the next class sums depend on normalized carry history. This dead end is recorded in IDEAS.md.
- The next meaningful reduction is to augment the strict W9 interface MDD with the accumulated cocycle coordinate S mod 111 (and the required phase/overflow state), then test whether any SCC admits the target residue and the required two-epoch counter ledger. The state augmentation must be shown transition-complete; otherwise it is only a heuristic.
- I have not run that lifted MDD or obtained a candidate-specific exclusion. No finite-horizon replay is claimed as progress.

## Exact missing lemma

A sound finite-state transition theorem for the W9|J|U interface augmented by `S mod 111), proving that the carry cocycle update is determined by the retained state, followed by either (i) a physical SCC containing a 240-step template return with correct counter drift, or (ii) a complete SCC exclusion for a clearly scoped interface class. This report supplies neither branch yet.

## Label

**PARTIAL** — mathematical reduction identified, but no new theorem or candidate-specific pruning result.