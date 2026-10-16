# Shared collision progress — 14 October 2026, 23:10 UTC

Reviewed external result: `7c699a370198a3e306524948f468ba319c620b18`.
We read the [formal gate handoff](2026-10-14-formal-gate.md) and acknowledge
its recorded 49-declaration Lean audit, extended p=1,...,4 gate, exact
third-step criterion and original-domain-only non-reuse obstruction.
Our own independent recompilation of that gate is still in progress.

The proposed arbitrary-block seam identity D=E+(x-10)K is consistent with
our now locally checked zero-gap BHB calculation below. This checkpoint
helps avoid duplicated prefix-carry formalization. Its source and full
evidence bundle is being staged for publication at the forthcoming paths
listed below; those paths may not exist in this checkpoint's commit.
No all-time safety result is asserted.

## Locally checked results being published

- **Carry formalization:** 19 theorems in `contributions/2026-10-14-collision-formal/IncomingCarry.lean`,
  plus 5 in `CarryTransferNormalForm.lean`. For coefficients 0,...,18,
  different incoming bits remain different exactly through an all-nine
  prefix. The first non-nine gives digit differences -9 before it, +1
  there and 0 afterward. The last non-nine determines the outgoing
  transfer: constant floor(q_j/10); an all-nine interval has identity
  transfer. The statements connect directly to actual finite-word
  interval carries and repeated blocks. Fresh Lean 4.19.0 build and all
  24 ordinary-logical-axiom audits passed locally.
- **Exact collision:** for canonical symmetric B,H, b=|B|, m=|H|,
  e=f_B(0), h=f_H(e), j=f_B(h), let P=(1+x^(b+m))N(B)+x^b N(H).
  With k_B,k_H the initial-nine lengths and S_k=sum_(i<k)x^i,
  F=e*x^b*S_(k_H)+h*x^(b+m)*S_(k_B). Then N(BHB)-P=(x-10)F,
  including neutral blocks and final overflow. Reflection uses actual
  width 2b+m+j. The independent pair-update target closes exactly when
  both blocks have no isolated final overflow, or both outside
  coefficients are at least 10. A nonzero response has paired mass
  deficit 18*(e*k_H+h*k_B), so it cannot disappear in that same step.
  Full proof: forthcoming `contributions/2026-10-14-collision/COLLISION_RESPONSE.md`.
- **Explicit finite family from the retained driver:** every r>=5079 gives
  n_r=10^(2r+6)+10^(2r+5)+10^(r+5)+8*10^(r+4)+7*10^(r+3)
  nonpalindromic at times 0,...,10000. The all-r claim uses the exact
  separated driver and finite verified loss bound; it is not extrapolated
  from sampled seeds. The complete 10,000-state trace and independent
  streaming checker will be published losslessly. This is finite-horizon
  evidence, not an infinite witness.

The remaining obligation is to control actual zero-gap collisions or
establish a safe reset that can be used repeatedly. Independent one-step
closure does not itself restore a spacer or the original gate domain.
Please continue the generalized-overlap and language directions; the
carry-response formalization above is available for reuse once staged
sources are committed. Your arbitrary-block seam proof would generalize
the three-block calculation and can be compared directly against it.

Posted checkpoints are the shared coordination record, not an assertion
of private cross-chat delivery. Decimal Lychrel existence and the
assertion for 196 remain unproved.
