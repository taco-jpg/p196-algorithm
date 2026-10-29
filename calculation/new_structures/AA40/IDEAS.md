# AA40 ideas log

## 2026-10-29 — mod-101 digit-class cocycle (NOT a closure lemma)

For a decimal digit string with LSD-first digits d_i, let S_r be the sum of digits at positions i congruent to r modulo 4. Since 10^2 = -1 (mod 101), the number itself satisfies
N = S_0 + 10 S_1 - S_2 - 10 S_3 (mod 101).
For length n, its reversal is the same four-class expression with classes permuted by i -> n-1-i. Thus N + rev(N) mod 101 can be computed from the four position-class sums before decimal normalization.

This is a valid carry-cocycle observable, but by itself it does not give a necessary condition on the template seam (J,C,U): the next digit-class sums depend on the full normalized carry history, not only the seam letters. No candidate was pruned and no two-epoch return was established. Do not promote this as a result.

Next attempt: combine the four-class residue with the exact carry-port state at the W9|J and J|U interfaces, rather than treating the residue as a seam-only invariant. The needed object is a finite-state cocycle on the interface MDD; if that state cannot be made closed under normalization, abandon this route.
