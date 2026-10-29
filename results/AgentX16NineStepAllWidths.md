# AgentX16NineStepAllWidths
**PAPER PROOF:** for EVERY k>=0 the decimal Thue-Morse 17/14 pairword seed (2k+8 digits) has 9-step overflow `101010101`, all ten states nonpalindromic, and exact phase-nine 9-port locations: k=0 {2,10}; k=1 {2,4,6,8,10,12}; k>=2 boundary {2,2k+10}, with centre {k+5,k+7} exactly if u(k-2)..u(k+3) is 001101 or 101100.
**PAPER PROOF:** a sound finite case split into 100-digit prefix, all 326 length-100 Thue-Morse factors, all 128 length-41 centre factors, and direct widths k=0..95. Exhaustive true carry-port choices collapse after cropping two cells per side at each phase. Completeness of factor sets established by substitution closure, not simulation length.
**PAPER PROOF:** exact natural density of two-port-only width parameters = 11/12 (16-factor primitive substitution matrix).
**COMPUTED controls:** 96 small widths, 864 ordinary big-int edges; exact finite factor check 326+128 states; positive matrix power M^5.
Scope is **nine steps only**, no phase-nine return cycle, no infinite decimal Lychrel proof, and NOT Lean-verified.
Code `calculation/new_structures/agent-X16/prove_nine_step.py`; compact data `calculation/new_structures/agent-X16/nine_step_universal_proof_data.json`.
Proof and geometry: `reports/AgentX16NineStepAllWidths.md`.
Reproduce: `python3 calculation/new_structures/agent-X16/prove_nine_step.py`.