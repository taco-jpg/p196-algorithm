# AgentN07PhaseDFAControl
**PAPER PROOF / COMPUTED:** The new folded-DFA all-length safety format compiles the **existing** base-9 period-10 absorbing lattice into ten regular phase languages, each accepting all band lengths `lmin_t+4*k` for k>=0.
Exact two-sided carry/overflow product reachability checks every phase-to-phase inclusion, returning no counterexample, with visited-state counts `[140,141,142,142,142,142,143,144,144,144]`.
The ten accepted languages are nonempty, contain an odd coefficient in every word, and close with band length increasing by four after one temporal cycle.
Independent ordinary integer and digit-list replay agree at all 70 tested edges (7 band widths x 10 phases).
This is a positive CONTROL of a new, more flexible certificate format, not a discovery of a new base-9 Lychrel number.
No base-10 certificate, 196 proof, or new Lean theorem is claimed.
Code and expected data: `calculation/new_structures/agent-N07/b9_phase_control.py`, `b9_phase_expected.json`; reproduce with `b9_phase_reproduce.sh`.
Proof explanation: `reports/AgentN07PhaseDFAControl.md`.