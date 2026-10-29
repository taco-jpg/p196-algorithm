# Agent W28: modulo-200 programmed three-step eraser in decimal p8/m20 bulk
- **PAPER PROOF:** conditional exact local carry identity for three steps (overflow 101): replace \`(11,14,3)\` by \`(6,6,7)\` at every selected spatial-period-20 slot in the rooted p8 lattice; the complete pairwords return to the unmodified trajectory at t=3, and the actual integers coalesce at t=4.
- This is **not** the +/-9 carry-gauge family: each of the three input residues changes modulo 9.
- The mask can be any subset of the slots 3 through K-4, including an arbitrary 200-residue memory schedule. Their three-step causal cones are disjoint (spacing 20); no short periodic kink or closed renewal is asserted.
- **COMPUTED:** 440 independent arbitrary-mask whole-word controls and 21 short ordinary Python-integer controls; one modulo-200 10,479-digit seed survived 20,000 steps without palindrome with rooted 39-column p8 exterior and at least 3 complete p8/m20 bands at every step.
- Two independent ordinary-digit and GMP arbitrary-precision integer calculations agree at each of 20,001 states; 10,000 overflows, final length 20,479, final whole-number FNV64 \`11093401814211976744\`.
- **UNDECIDED:** regenerative centre and any infinite decimal Lychrel certificate. This result is finite-horizon only.
- Reproduce: \`python3 calculation/new_structures/agent-W28/certificate.py\`; \`g++ -O3 -std=c++17 calculation/new_structures/agent-W28/modular_eraser.cpp -lgmpxx -lgmp -o /tmp/w28 && /tmp/w28 260 20000\`.
- Proof details \`reports/AgentW28ModularEraser.md\`; compact data \`calculation/new_structures/agent-W28/observations.json\`.
