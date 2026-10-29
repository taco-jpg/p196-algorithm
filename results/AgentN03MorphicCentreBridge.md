# AgentN03MorphicCentreBridge
Label: **PAPER PROOF** (finite-horizon substitution-bridge pumping theorem, conditional on explicitly checked carry identities).
Base 10, overflow 10101010, two distinct boundary states: (89,145,20576) and (166,110,18745).
Each state has two different exact return words of lengths 92 and 97, with common six-column centre suffix.
For **every** finite A/B substitution word, the symmetric decimal seed has an exact **whole-number** eight-step pair-word orbit, four extra digits, and no palindrome through step 8.
Aperiodic Fibonacci/Thue–Morse macro word AB/BA (length 189 each) is included.
COMPUTED controls: 26 independent ordinary decimal digit-list replays, including >22,000-digit seeds, plus two corrupted-input rejects.
In those 26 controls, attempted same-format renewal fails at step 16 at first new centre column k=h+1; longer centre formats remain UNDECIDED.
Does **not** establish an infinite decimal Lychrel orbit; no complete 20,000-step centre certificate.
Witness: \`calculation/new_structures/agent-N03/bridge_witness.txt\`.
Independent checker: \`calculation/new_structures/agent-N03/bridge_certificate.py\`.
Details and finite-state soundness argument: \`reports/AgentN03MorphicCentreBridge.md\`.
Run: \`cd calculation/new_structures/agent-N03 && python3 bridge_certificate.py bridge_witness.txt\`.
