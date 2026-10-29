# AgentN28CarryGaugeFunnel
- **PAPER PROOF:** base-independent carry-gauge quotient for all symmetric pairwords P_i=x_i+(b-1)z_i, with 1<=x_i<=b-2 and binary symmetric z.
- Overflow z_0=1 erases **every** mask bit: F(P)=[x_0, x_0+x_1,...,x_(n-2)+x_(n-1),x_0]. Non-overflow z_0=0 gives the discrete-Laplacian mask update.
- For constant x, exponentially many decimal seeds coalesce after two reverse-additions at x*(b+1)*(b^n-1)/(b-1).
- Concrete seeds: 9448 -> 17897 -> 97768 and 9988 -> 18887 -> 97768.
- **COMPUTED controls:** 25,458 independent integer/pairword tests over bases 3..77; both seeds survive 20,000 digit-list steps, identical 8,283-digit endpoint (FNV64 9656804610410818816).
- Not claimed: a renewing base-10 cycle, infinite nonpalindromicity, or Lean verification.
- Reproduce: calculation/new_structures/agent-N28/mask_gauge.py and existing replay_int.cpp; data: mask_gauge_observations.json.
- Proof/scope: reports/AgentN28CarryGaugeFunnel.md.
