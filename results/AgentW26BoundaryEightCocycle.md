# AgentW26BoundaryEightCocycle
**COMPUTED:** The full 1025-state base-10, all-k>=111 affine-polynomial chain of AgentW26FiveTermAffine1024 has a *partial 8-step renormalization* on its two extreme coefficients.
Write N_t(k)=sum_{e in {0,20,68,116,136}} a_{t,e}(10^(k-111))^e (exact rationals from the earlier source).
For EVERY t=0..1016, a_(t+8,0)=a_(t,0) and a_(t+8,136)=10^4 a_(t,136); 1,017 pairs, no failures, exact Fraction comparisons.
This isolates a two-coordinate periodic/scaling boundary controller while the three intermediate coefficients carry the nonautonomous junction dynamics.
The natural fixed 5x5 rational matrix for the whole 8-step update is not supported: five sample vectors have rank 5 modulo 1,000,000,007, and the resulting unique matrix fails at its sixth transition (t=40 to 48). **Redirect:** add a seam/wall-state variable rather than a fixed homogeneous 5x5 map.
This is not an infinite recurrence: all equalities have the exact finite scope above; no decimal Lychrel certificate.
Reproduce: `python3 calculation/new_structures/agent-W26/run_fast.py && python3 calculation/new_structures/agent-W26/boundary_cocycle.py`.
Source/data: `calculation/new_structures/agent-W26/{boundary_cocycle.py,boundary_cocycle_expected.json}`; explanation: `reports/AgentW26BoundaryEightCocycle.md`.
No Lean toolchain or repository verifier run; no Lean files changed.
