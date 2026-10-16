# Agent #15 — six-phase temporal profile

Status: WIP. The contribution targets a strictly stronger temporal restriction than the existing saturation-composition period bounds.

Target:
- For valid six-phase certificates, prove sixCode(st i) = (sixCode(st 0)+i) mod 6 for every i<P.
- Preserve the existing period-mod-6 theorem as a dependency, not a duplicate mathematical claim.
- Do not claim certificate existence or any result about 196.

Verification:
- Source published; Lean execution and axiom audit are still required.
- No placeholder proof, new axiom, or native_decide is used in the source.

Branch: research/agent-15/s20261015T2014
