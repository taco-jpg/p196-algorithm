# AgentN21P12TransducedPacketTrain

**COMPUTED (base 10, steps 0..820).** On the p=12/m=9 decimal lattice, four congruent symmetric defect packets separated by 504 columns yield an exact translated, additive, growing-kink train at every step 0..819. The first nonlinear three-column interactions occur at step 820, at lower-half positions 648..650, 1152..1154 and 1656..1658.

All six independently realized canonical 5,000-digit seeds (background, four singles, combined) undergo 820 ordinary Python-bigint reverse-and-add steps with exact full pairword agreement against a distinct coefficient-normalization engine and no palindrome at any of the 821 states. The common length at step 820 is 5,205 digits. Individual deviation packet supports first overlap at step 816, but the additive law persists through 819.

**PAPER PROOF (conditional sufficient format).** The report proves an exact multi-packet carry-firewall composition lemma and specifies a finite-state, pumpable packet-train cycle criterion sufficient for an infinite nonpalindromic orbit if every symbolic edge, palindrome guard and nonshrinking-gap condition can be checked. No such decimal cycle has been found; no Lean theorem or conclusion about 196.

Reproduce: `sh calculation/new_structures/agent-N21/run.sh`; code and sample data under `calculation/new_structures/agent-N21/`; full proof, shape and limitations in `reports/AgentN21P12TransducedPacketTrain.md`.
