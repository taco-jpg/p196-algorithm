# Agent N08: regular folded-pairword certificate format
- **PAPER PROOF:** For every radix b>=2, folded-palindrome regular languages with an exact finite-state reverse-add transducer, closure under all successful branches, odd-pair guard and an admissible seed give infinite non-palindromic orbits.
- Precise soundness theorem, carry-state derivation, parity terminals (including corrected one-digit overflow), finite product decision algorithm: `reports/AgentN08FoldedRegular.md`.
- This format permits general finite-state halfword languages, not only a fixed exterior plus periodic band; infinite language inclusion is checked by finite reachability.
- **COMPUTED control:** base 2 seed 22, four regular phases and 4 successful inclusion checks; no wrong-overflow branch. Entire orbit nonpalindromic by the paper argument.
- **COMPUTED replay:** independently checked base-2 20,000 steps and exact phase grammar, final 10,006 bits.
- **COMPUTED decimal pilot (corrected Q52):** base-10 seed 196 has no palindrome among 20,000 checked source states; after 20,000 operations length is 8,296 digits with 8,293 overflows. The odd-coefficient guard fails exactly at t=8,13,19 (not t=1,7). This finite replay does not certify an infinite decimal orbit.
- Source and independent checkers: `calculation/new_structures/agent-N08/`, run `sh calculation/new_structures/agent-N08/run.sh`.
- **UNDECIDED:** no decimal infinite-orbit certificate, no statement about 196 beyond the measured steps.
- No Lean proof is claimed.
