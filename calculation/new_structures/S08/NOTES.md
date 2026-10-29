# S08 notes

2026-10-29: Read the repository mission and current #475 history, then claimed the R18 second-epoch erosion mechanism route.

Reproduction command: python3 calculation/new_structures/S08/verify.py

The verifier has two checks:
1. A fail-closed affine run-length symbolic simulation, adapted from the repository R30 parametric verifier, checks 120 and 240 steps for all 17 mod-11-admissible fixed centres and all independent q,k >= 512. It refuses parameter-dependent cut phases, ambiguous affine boundaries, nonpositive run lengths, atom explosion, and incomplete periodic comparisons.
2. A separate canonical-root ordinary-integer oracle, cross-checked at every step against an LSD-first digit-vector normalization, checks all 16 q,k pairs in {20,40,80,160} x {20,40,80,160} for the original centre. It checks the exact overflow clock, t=120 endpoint, t=136 phase-8 W mismatch, and t=240 endpoint.

Expected final line: S08_ALL_CHECKS_PASSED. The symbolic engine is a computation, not a Lean proof; its claim is scoped to this fixed J/U/phase and the 17 listed centres. No ALERT is justified. The #475 FEED redirects S09/S14 toward changing the junction-induced upper carry, not C alone.
