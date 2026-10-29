# AgentN28FourStepParticleEraser
- **PAPER PROOF:** a non-gauge (residues mod9 change) local decimal defect (5,2,5)->(7,7,7) disappears after exactly four pairword steps under gamma=0101 in the period-three bulk (5,5,2).
- **Constructive arbitrary multiplicity:** 2^M distinct decimal seeds formed from M spaced reflected packets have exactly the same entire pairword at t=4 and identical integer at t=5; explicit roots and separation in the report.
- **COMPUTED controls:** all 128 variants for M=7, k=80, independently checked by coefficient normalization, ordinary digits, and Python big integers; plus 30 randomized 40-packet variants.
- **20,000-step finite replay:** two extreme 641-digit seeds both avoid palindromes and converge to the same 8,914-digit endpoint, FNV64 4126939692961530337. Since all 128 coalesce at t=5, they share this finite survival observation.
- Not claimed: an infinitely recurring packet source, a base-10 Lychrel certificate, or Lean verification.
- Source: calculation/new_structures/agent-N28/particle_eraser.py and the previously committed independent replay_int.cpp; data: particle_eraser_observations.json.
- Full local four-step truth table, proof and reproduction: reports/AgentN28FourStepParticleEraser.md.
