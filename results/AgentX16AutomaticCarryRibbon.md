# AgentX16AutomaticCarryRibbon
**PAPER PROOF:** a sound synchronized binary-indexed automatic carry-ribbon certificate format for any base b>=2, with phase-indexed pairword and carry DFAOs over (cycle k, digit position i), exact local normalization, overflow and reflection, and a finite universal automata-test specification. An accepted cycle would prove an infinite palindrome-free orbit. No decimal cycle is claimed.
**COMPUTED control:** an all-k nonperiodic Thue-Morse carry latch is proved algebraically to survive three states and then reach a palindrome; redirects to a regenerating carry interface.
**COMPUTED finite survivor:** base10 Thue-Morse pairword coefficients (17,14), k=63, 134->8396 digits over 20,000 genuine steps, zero palindromes and an odd pair coefficient at every one of 20,001 states; 1,601 independent Python-int edges. No infinity claim.
**COMPUTED controls:** exact base9 published B61/W4 10-edge return for 50 lengths (500 edges); 196 20,000-step replay (8296 digits). No fixed p8 exterior inferred (matching prefix <=5).
Detailed derivation: `reports/AgentX16AutomaticCarryRibbon.md`.
Code and data: `calculation/new_structures/agent-X16/`.
Reproduce using `automatic_ribbon.py`, `second_probe.py`, `base9_control.py`, `search_tm.py` as in report.
Not LEAN-VERIFIED; general DFAO product checker is specified but not implemented; full repo verify unavailable in isolated sandbox.