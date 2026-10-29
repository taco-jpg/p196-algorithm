# Agent N10: decimal 88-step travelling defect front
- **Label: COMPUTED.** Explicit positive decimal front-glider mechanism, not a finite Lychrel certificate.
- Let `h_t` be the first mismatch against the known period-eight, spatial-period-20 exterior `(B_t,W_t)`.
- Four genuine decimal seeds with `k=300` lattice blocks and four different central cores show `h_(t+88)=h_t-20` throughout the measured stable regime, and the full **120-coefficient moving window** `P_t[h_t-40:h_t+80]` equals that at `t+88` for every `t=1082..19912`.
- For each core: **18,831 full-window comparisons**, no mismatch, independently evolved C++ real decimal digit lists through 20,000 steps. The frontier's loss word has period 22 after step 62, losing exactly five coefficients per 22 steps.
- Different cores produce distinct stable 88-step wave profiles; `k=400` reproduces the `k=300` empty-core profile.
- Independent Python BIGINT replay validates the entire moving window for `t=1082..1312` in cores 0 and 2 (231 comparisons each) through step 1400.
- Exact source and controls `sh calculation/new_structures/agent-N10/run_glider.sh`; compact data `glider_observations.json`.
- Proof target, limitations and reproducibility: `reports/AgentN10Decimal88StepFrontGlider.md`.
- **Not claimed:** infinite-time glider stability, self-renewing bands, or an infinite decimal palindrome-free orbit.
