# Agent W01: nonlinear two-ended 88-step daughter glider after decimal pulse collision
- **COMPUTED**: four explicit base-10 integer reverse-and-add orbits, 24,000 initial decimal digits, through t=20,000; interaction-only signed residual `R=P_D-P_B-P_C+P_A` first nonzero at t=2154.
- The residual's first differing paired position obeys `g(t)=g(t-88)-20` for **every t=2242..20000**, 17,759 comparisons, zero failures.
- The **two separate actual low/high signed digit residual** windows r=-20..40 are exactly 88-step translating for every t=2836..20000 (17,165 consecutive comparisons, 2,094,130 exact digit-difference equalities); last prior failure t=2835.
- At t20,000: first residual index 3459, last index 16999, 13,018 nonzero residual pairs, L1 norm 112,648. Nonlinear interior grows even while outer daughter tile repeats.
- Independent GNU GMP big-integer four-orbit replay through 6,000 verifies the same sharp 2835→2836 onset and all 3,165 translating windows t=2836..6000; a wrong -19 displacement is rejected at t2836.
- Reproduce: `bash calculation/new_structures/agent-W01/residual_run.sh`; sources/checker `calculation/new_structures/agent-W01/{w01_residual_onset.cpp,w01_scatter_gmp.cpp,residual_verify.py,residual_run.sh}`.
- **UNDECIDED**: a closed nonlinear centre-emission cycle, infinite base-10 Lychrel certificate, or implication for 196. Full scope: `reports/AgentW01NonlinearDaughterGlider20000.md`.
