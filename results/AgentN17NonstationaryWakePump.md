# Agent N17: exact finite-horizon pumping of the entire nonperiodic decimal wake
- **Label: COMPUTED** for the explicit finite replay scopes below; **PAPER PROOF** for a conditional carry-guard insertion lemma, not its all-time hypotheses.
- On symmetric decimal pairwords, insert 20 consecutive phase-lattice coefficients and their mirror at root cut J=39, leaving any inner wake unchanged but translated.
- For canonical halfwidth h=8000, padded h=8020, both ordinary digit-list and independent GMP engines verify **all 210,008,000 lower-half coefficients** at 20,001 states through step 20,000: root 39 unchanged; every subsequent coefficient shifted by +20. Both trajectories avoid palindromes.
- For **all 361** two-cell arbitrary central packets at h=500, the same identity survives through 1,500 steps: 372,461,750 pair-coefficient checks per engine, exact GMP agreement.
- For the same 361 packets, digit-list replay passes insertions m=40,60,80 (all 1,500 steps) and h=1000,m=20 (2,500 steps); a 128-seed deterministic 40-cell random-packet test passes 600 steps.
- Finite control h=250,m=20 first violates the shifted-tail rule at step 951, after the root begins differing at step 940; therefore no indefinite covariance is asserted.
- One-command reproduction: \`bash calculation/new_structures/agent-N17/run_pump.sh\` (requires C++17, GMP and Python3); full code, numeric scope table and independent test controls in that directory.
- The comma-separated inputs and exact conditional soundness argument are documented in \`reports/AgentN17NonstationaryWakePump.md\`.
- **Not claimed:** a decimal Lychrel number, a 20,000-step-to-infinite extrapolation, a globally valid pumping identity, or Lean verification.
