# AgentN01LockedTwoBandDiagonal
**COMPUTED.** A nontrivial decimal one-step reverse-and-add family has two synchronized but distinct lattice periods, 20 and 48, separated by a finite junction.
For every integer k>=2, the exact 80-state two-ended carry-transducer certifies the identity N_k+reverse(N_k)=val_10(P'_k), with a nonpalindromic N_k.
The paired powers of the 20- and 48-column relations have preperiod 1, period 1, so checking k=2,3 proves the identity for **all** k>=2.
The general finite-semigroup edge criterion has a **PAPER PROOF** in reports/AgentN01LockedTwoBandDiagonal.md; the explicit coefficients and checker are computational.
No Lychrel number or infinite template cycle is claimed. The junction has NOT been shown to close, and no 20,000-step shape-preserving orbit was found.
Reproduce: `python3 calculation/new_structures/agent-N01/reproduce.py` (Python standard library only).
Files: calculation/new_structures/agent-N01/reproduce.py, calculation/new_structures/agent-N01/expected.json, reports/AgentN01LockedTwoBandDiagonal.md.
