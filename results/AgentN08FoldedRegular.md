# Agent N08: regular folded-pairword certificate format
- **PAPER PROOF:** For every radix b>=2, folded-palindrome regular languages with an exact finite-state reverse-add transducer, closure under all successful branches, odd-pair guard and an admissible seed give infinite non-palindromic orbits.
- Precise soundness theorem, carry-state derivation, parity terminals, finite product decision algorithm: `reports/AgentN08FoldedRegular.md`.
- This format permits general finite-state halfword languages, not only a fixed exterior plus periodic band; infinite language inclusion is checked by finite reachability.
- **COMPUTED control:** base 2 seed 22, four regular phases and 4 successful inclusion checks; no wrong-overflow branch. Entire orbit nonpalindromic by the paper argument.
- **COMPUTED replay:** independently checked base-2 20,000 steps and exact phase grammar, final 10,006 bits.
- **COMPUTED decimal pilot:** base-10 seed 196 no palindrome in 20,000 steps, final 8,211 digits; all-odd-coefficient guard fails exactly at t=1 and t=7, so this *particular guard* is insufficient for the decimal example.
- Source and independent checkers: `calculation/new_structures/agent-N08/`, run `sh calculation/new_structures/agent-N08/run.sh`.
- **UNDECIDED:** no decimal infinite-orbit certificate, no statement about 196 beyond the measured steps.
- No Lean proof is claimed.
