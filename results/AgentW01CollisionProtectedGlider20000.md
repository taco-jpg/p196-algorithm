# Agent W01: collision-protected 88-step decimal glider, four 20,000-step orbits
- **COMPUTED**: four explicit 24,000-digit decimal seeds (clean / patch X / patch Y / both), independently digit-vector and GMP replayed for steps 0..20,000; zero palindromes and final length 34,000.
- Two-pulse support first overlaps at t=2154; first nonlinear daughter outside either single-pulse support at t=2161.
- All 19,001 windows t=1000..20000 satisfy `f(t)-f(t-88)=-20` for clean/B and clean/D fronts, and 9,234,486 low/high actual-digit matches across 88 time steps.
- All four evolving pairwords have the rooted period-8 / spatial-period-20 exterior, with >=1456 exact intact paired positions at every step (298,285,792 comparisons). Nonpalindrome witnessed by an odd coefficient within first 39.
- Independent GNU GMP `n+reverse(n)` replay: all four seeds, 20,001 full states each, 29,121,456 periodic-prefix checks per seed; six D full-string FNV64 digests match the digit-vector engine. Corrupted phase negative control is rejected.
- Label applies **only** to the finite steps and stated starting seeds. **UNDECIDED**: whether the nonlinear centre ever regenerates a glider or yields an infinite decimal certificate; no 196 claim and no Lean proof.
- Reproduce: `bash calculation/new_structures/agent-W01/run.sh` (C++17/GMP/Python3).
- Sources, checker, control: `calculation/new_structures/agent-W01/{w01_collision.cpp,w01_independent.cpp,verify_results.py,run.sh,expected.txt}`.
- Detailed scope/limitations: `reports/AgentW01CollisionProtectedGlider20000.md`.
