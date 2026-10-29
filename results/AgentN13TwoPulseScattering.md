# Agent N13: decimal two-pulse nonlinear scattering and daughter disturbance
**COMPUTED**, finite four-orbit base-10 statement, steps 0..4000; no infinite Lychrel certificate.
Construct from the p8/m20 pairword exterior a clean 10400-digit seed A, independently perturb paired positions 1800..1849 (B), 2600..2649 (C), or BOTH simultaneously (D); evolve all four by literal decimal reverse-and-add.
At each time compare the two single-pulse affected-position sets `S_B={j:P_B(j)!=P_A(j)}` and `S_C={j:P_C(j)!=P_A(j)}` with the combined-pulse result `P_D`.
The affected sets first intersect at **t=836** (one position). For every earlier step the combined pairword equals the unique single-pulse pairword in each affected position and the clean pairword elsewhere.
Outside the intersection, the first breakdown of that superposition is at **t=841** (two locations). The first *newly affected position outside the union* `S_B ∪ S_C` is **t=858, j=2415**.
This is a constructive pulse-pulse collision mechanism: a daughter disturbance arises where neither pulse alone had changed the pairword, with exact measured onset latency 22 steps from first overlap.
A second, independent Python arbitrary-precision replay checks all fields for **every t=0..900** (901 full four-orbit rows), reproducing all three event times. The C++ primary continues through 4000 steps.
Reproduce `bash calculation/new_structures/agent-N13/pulse_train_run.sh`; source `pulse_train.cpp`, `pulse_train_check.py`, `pulse_train_independent.py`, `pulse_train_keyframes.csv` in the same directory.
Details and conditional interpretation: `reports/AgentN13TwoPulseScattering.md`. No repeated daughter macro-tile or autonomous source is established.
