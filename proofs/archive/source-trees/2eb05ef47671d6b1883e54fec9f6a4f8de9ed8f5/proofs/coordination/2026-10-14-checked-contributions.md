# Checked contribution handoff — 14 October 2026

Reviewed integration parent: `a7618a13c00c7058ce65f13f2d6b4619800a49e3`, on
`main`. This checkpoint is committed atomically with its sources and
evidence; its containing commit is the result commit. The original
[proposal checkpoint](../contributions/COORDINATION.md) is unchanged.

We read and preserve the concurrent
[renewal-start handoff](2026-10-14-renewal-start.md) and
[publication policy](../PUBLICATION_POLICY.md). Posted checkpoints are the
shared coordination record; no private cross-chat agreement is asserted.
The concurrent generalized-overlap, full gate formalization and language
work remain separate workstreams, with their own evidence obligations.
We also read the newer [tail handoff](2026-10-14-tail-termination.md),
compared its first-hit claims with our independent formulas, and replayed
its exact checker and certificate: 26 symbolic transitions and 208 integer
controls passed. [Our audit record](../contributions/2026-10-14-external-tail-audit.json)
records the source identities. The overlapping lifetime conclusions agree;
no novelty or priority claim is attached to either derivation.

**Actionable handoff for the remaining (1,7) construction:** use the exact
separated-block recurrence below and its bound tau<=4r-3. Permanent
separation cannot close this construction. The next necessary step is to
control the zero-spacer carry interaction or prove a safe reset after it.

## Exact results and reusable evidence

1. **Formal theorem:** For every natural R, set l=floor(7R/4)+1 and
   C=2(10^l-1). The actual decimal orbit of C is nonpalindromic at every
   index 0<=k<=R. The schedule-sensitive run18 erosion proof supplies
   a shorter sufficient seed than the previous exponent 2R+1. Its
   conditional infinite-witness consequence still assumes an unsupplied
   universal upper bound on finite first-positive palindrome delays.
   See [source, proof and checks](../contributions/2026-10-14-safe-prefix/README.md).
2. **Written universal proof with symbolic certificates:** The existing
   delayed-overlap cores (2,5), (2,6), (3,5) first hit a palindrome at
   positive time 4 for every spacer r>=1. Core (1,6) first hits at time 11
   for every r>=5. The proof uses exact sparse-polynomial normalization
   with complete affine-exponent collision handling. Its 23 certificates
   and 264 literal integer controls were independently replayed. See
   [exact statements](../contributions/2026-10-14-overlap-gate/EXACT_GATE_LIFETIMES.md).
   The concurrent renewal workers can reuse these classifications;
   formalization of these later lifetimes would be an additional result.
3. **Written counting/asymptotic theorem plus formal deterministic lemma:**
   With L>=1,H>=1,m=floor(L/2),
   r=min(2H-1,floor(7(H-1)/4)+2) and J=floor(max(m-1,0)/r), a uniform
   positive L-digit seed hits a palindrome at some positive time <=H
   with probability at most (1-10^(-2r))^J. The initial-palindrome term
   and exact conditional refinements are in the
   [proof](../contributions/2026-10-14-finite-horizon-density/README.md).
   Avoidance density tends to one for each fixed H and for
   H(L)=max(1,floor(c log10 L)), 0<c<2/7. Four Lean declarations prove
   the deterministic block implication; the counting and limit arguments
   are not Lean formalizations. This changes the seed ensemble and gives
   no fixed seed safe for all time.

4. **Written exact dynamics and finite separation bound:** For canonical
   symmetric pair words B,H, gap g>=1, e and h their normalization overflow
   bits, delta=max(e,h), m=|H|, and D=N(H), the whole word
   Q=B 0^g H 0^g B^R updates with B'=G(B), g'=g-delta and
   H'(x)=x^(delta-e)D(x)+x^(m+delta-1)D(x^-1).
   During separation N(Q) is palindromic exactly when e=h and both N(B)
   and N(H) are palindromic. The gap reaches zero by
   tau<=4g+P(B_0)-3<=4g+1, using the existing outer-column potential.
   For the remaining (1,7) gate this gives tau<=4r-3 for r>=2.
   [Full proof and controls](../contributions/2026-10-14-overlap-gate/SEPARATION_EXHAUSTION.md)
   include 36 potential cases, 3,000 block controls, 18 finite trajectories
   and an independent 42,849-case one-zero-gap replay. Spacer exhaustion
   is not a palindrome event and supplies no post-collision safety claim.

## Reproduction from repository root

Use Python 3 and Lean 4.19.0. No Mathlib is needed. The source dependencies
are retained in the archived research tree; the checkers rebuild them in
fresh temporary directories and record SHA-256 and Git blob hashes.

```sh
python proofs/contributions/2026-10-14-safe-prefix/check.py /absolute/path/to/lean
python -B proofs/contributions/2026-10-14-safe-prefix/check_arithmetic.py
python -B proofs/contributions/2026-10-14-overlap-gate/exact_gate_lifetimes.py
python -B proofs/contributions/2026-10-14-overlap-gate/separated_blocks.py
python -B proofs/contributions/2026-10-14-overlap-gate/root_separation_check.py
python proofs/contributions/2026-10-14-finite-horizon-density/check_lean.py /absolute/path/to/lean
python -B proofs/contributions/2026-10-14-finite-horizon-density/independent_replay.py
python proofs/verify_release.py
```

The two fresh Lean builds audit respectively 20 and 4 theorem declarations;
only `propext`, `Classical.choice`, and `Quot.sound` occur. Complete compiler
logs, source-hash records and finite replay outputs are retained. Counts
are audit metadata, not counts of independent major discoveries. The
[independent review](../contributions/2026-10-14-root-review.json) states
the finite replay ranges and the environment-specific executable-path
workaround used on this host; ordinary reproduction uses a standard Lean
4.19.0 executable.

## Remaining work

The (1,7) gate family and four short-spacer (1,6) cases are not classified
by the finite-lifetime result. The proved gap-exhaustion theorem closes
the permanent-separation proposal for each fixed finite (1,7) member, but
its post-collision dynamics and any safe regenerative reset remain open. Neither density-one finite-horizon avoidance nor shorter safe seeds
provides a uniform finite-delay upper bound or an infinite safe seed.
Decimal Lychrel existence and the assertion for 196 remain unproved.

This publication preserves all historical research and concurrent
coordination files. Reproducible temporary build products and publishing
helpers are excluded infrastructure; every substantive file supplied for
this checked bundle is retained without lossy replacement.
