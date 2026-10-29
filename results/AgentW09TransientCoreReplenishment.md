# W09 transient decimal-core replenishment
- **COMPUTED** base-10 candidate N_k = A ++ 4^(2k) ++ B, k=22000, A=46854264879199823016951, B=05961021898086746235863, length 44046.
- Two independent integer engines check 20000 actual reverse-and-add steps: zero palindromes, exact six-phase 8,16,14,10,2,4 homogeneous central pairword block in all 20001 states.
- Central width 44000 initially, 44008 after four/six steps, 44001 at step24, 30723 at step20000; final number has 52261 digits.
- Final LSD-first FNV64 checksum c8ea7c7e51e14bd9; independent base-1000 limb and decimal digit array engines match all checkpoints.
- **PAPER PROOF** of centre insertion pump and conditional nonnegative-budget emitter-cycle criterion, with finite 24-edge control: for all k>=28 the first 24 steps have k-independent caps and centre width 2k+beta_t, beta24=+1, and odd cap guard.
- Scope, proof, obstacle: reports/AgentW09TransientCoreReplenishment.md.
- Code, exact checkpoints, controls: calculation/new_structures/agent-W09/.
- Reproduce: sh calculation/new_structures/agent-W09/reproduce.sh.
- **UNDECIDED** cap recurrence and infinite Lychrel; no Lean verification, no 196 claim.
