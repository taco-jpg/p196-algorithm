# Agent X26: odd-centre decimal all-padding finite-horizon family
- **COMPUTED** 20,000 exact decimal pump edges, with a PAPER PROOF of the local all-repeat insertion rule.
- Strengthens AgentX26AdversarialCentreShields: for **every integer L>=22000** and **every** 257-digit decimal interior word C, the seed 5 ++ 9^L ++ C ++ 9^L ++ 4 is nonpalindromic at every t=0..20000.
- The uniform C=9^257 odd-length reference enjoys exact commutation RAA(I9(D)) = I9(RAA(D)) with insertion of two central nines on every checked edge; all m>=0 extra insertions follow by the local carry lemma.
- Fully checked at t=0..20000: reference L22000 and L22001 match central two-9 digit insertion and central two-18 pairword insertion, overflow bits and ordinary decimal steps.
- Proven shield bound for arbitrary C and L: at least L-t coefficient-18 sites on each flank; exact same nonpalindromic outer witness as the base reference.
- Source and compact output: calculation/new_structures/agent-X26/pump_parametric.cpp, pump_checkpoints.tsv.
- Soundness, reproducibility and exact limitations: reports/AgentX26OddCentreAllL.md.
- This is **not** an infinite decimal Lychrel certificate, a Lean-verified result, or a statement about 196.
