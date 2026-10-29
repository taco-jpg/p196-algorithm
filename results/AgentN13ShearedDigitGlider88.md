# Agent N13: two-ended decimal 88-step translating digit window
Label: **COMPUTED** (finite two-orbit, finite-time statement, NOT a decimal Lychrel certificate).
With the explicit 10400-digit base-10 pair of seeds in the generator `glider.cpp` (unperturbed and last-100-pair perturbation), for every integer `1000 <= t <= 20000` the first differing pair position `f(t)` obeys `f(t) = f(t-88)-20` and both orbit lengths grow by exactly 44 relative to step `t-88`.
For every `r = -100..74`, the actual **low and high decimal digits** of **both** orbits at paired position `f(t)+r` equal those at paired position `f(t-88)+r` 88 steps earlier: exactly **13,300,700** checked digit equalities, with no mismatches.
The low side moves -20 digit places, while the high-side absolute least-significant-first position moves +64, a sheared two-ended translating local window (not just identical paired sums).
The immediately adjacent `r=75` fails at `t=1000,1001`, so no stronger boundary or all-time recurrence is claimed; a wrong shift of -19 fails on 18,137 sampled times.
Independent Python built-in arbitrary-precision reverse-and-add verifies the same digit-window law at every `1000 <= t <= 2000` (700,700 digit equalities) and reproduces the two `r=75` failures.
Reproduce: `bash calculation/new_structures/agent-N13/glider_run.sh` (C++17, Python 3.11+).
Code: `calculation/new_structures/agent-N13/{glider.cpp,glider_independent.py,glider_run.sh}`; details: `reports/AgentN13ShearedDigitGlider88.md`.
No persistence past `t=20000`, independent carry-cut closure, opposite-velocity front, Lean theorem, or infinite base-10 orbit is asserted.
