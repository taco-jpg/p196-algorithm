# Agent N10: finite 136-state decimal quotient guard-speed law
- **Label: PAPER PROOF** of a constructive uniform outer-shell bound (phase arithmetic checked COMPUTED).
- Source: known base-10 p8/m20 rec0 exterior `B_t,W_t`. A matching palindromic outer prefix of length `h>=39+20` survives one step to length at least `h-d`, where `d=1` unless its last coefficient is 9, in which case `d=2`, independent of the central word.
- The eight 20-column phase words have NO adjacent 9s. The cut-residue automaton `(t mod 8,(h-40) mod 20)` from the natural start `(0,19)` has exact period 136 and total loss 140.
- Hence `D(H)=140*floor(H/136)+prefixloss[H mod 136]` is a proven guard loss bound. At H=20,000: `D=20,588`.
- `k=1+ceil(D(H)/20)` complete initial W copies guarantee at least one full W at every step through H and thus no palindrome; H20,000 needs k=1,031, initial 41,318 decimal digits.
- Independent ordinary-digit C++ replay of that 41,318-digit seed passes 20,000 steps, retaining 803 full lattice bands (far better than the conservative one-band proof).
- Reproducer: `sh calculation/new_structures/agent-N10/run_guard.sh` (4,800 formal-symbol cut tests, 3,840 actual big-integer controls, 20,000-step C++ replay).
- Proof and exact limitations: `reports/AgentN10SharpGuardSpeed.md`.
- **Not claimed:** an infinite single-number Lychrel orbit or a self-renewing centre.
