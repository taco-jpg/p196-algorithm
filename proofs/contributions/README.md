# Reviewed contributions — 14 October 2026

These standalone additions build on the archived correlation pass. Decimal
Lychrel existence and the claim for 196 remain unproved. The initial
[coordination proposal](COORDINATION.md) remains an unchanged historical
checkpoint; the results below supersede only its specified proposals.

| Result | Evidence and exact scope |
|---|---|
| [Shorter safe prefixes](2026-10-14-safe-prefix/README.md) | For every natural R, 2(10^(floor(7R/4)+1)-1) is nonpalindromic at every time 0 through R. Lean 4.19.0, 20 audited declarations; full source rebuild and logs retained. The conditional Lychrel implication still requires an unsupplied universal finite-delay bound. |
| [Exact delayed-gate lifetimes](2026-10-14-overlap-gate/EXACT_GATE_LIFETIMES.md) | Cores (2,5), (2,6), (3,5) have first positive palindrome time 4 for every r>=1. Core (1,6) has time 11 for every r>=5. Written all-parameter proof, 23 sparse-polynomial certificates and 264 independent integer controls; not Lean verification. |
| [Finite separation exhaustion](2026-10-14-overlap-gate/SEPARATION_EXHAUSTION.md) | Exact separated-block update and palindrome criterion; gap reaches zero by 4g+P(B_0)-3, hence by 4r-3 for the remaining (1,7) gate. Written proof with independent boundary controls; no post-collision conclusion. |
| [Finite-horizon density](2026-10-14-finite-horizon-density/README.md) | An explicit counting bound shows density-one avoidance of any fixed finite horizon as seed width grows, also for H(L)=max(1,floor(c log10 L)) with 0<c<2/7. Four Lean declarations verify the deterministic marker implication; counting and asymptotics are written proofs. No infinite-time conclusion. |

The [root review](2026-10-14-root-review.json) records independent replays
and source-hash checks. The [handoff](../coordination/2026-10-14-checked-contributions.md)
states exact integration provenance, commands and the remaining obligations.
No novelty or external peer-review claim is made.
