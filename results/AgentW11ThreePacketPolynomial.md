# W11: 20,000 exact decimal three-packet steps
- **COMPUTED:** for each integer q>=12031, `N0=88*10^(2q)+3*10^q+75` has no palindrome among orbit states 0..20000.
- Every step is an exact three-packet polynomial edge with two separated variable gaps; raw symmetric pairwords have three disjoint finite zones.
- **PAPER PROOF (conditional finite induction):** exact packet reflection/merge and integer Cauchy root bound; integer checks bound the 20,001 states.
- At q=12500 independent decimal-digit and GMP integer replays match; 21 number/pairword checksums and exact integer endpoint comparisons pass.
- Max required bounds: packet 12009, pairword 12009, nonpalindrome 12031; final gaps 492 and 491, final length 33256 digits.
- Reproduce with `calculation/new_structures/agent-W11/{triple_replay.cpp,independent_gmp.cpp,checkpoints.tsv}` and commands in `reports/AgentW11ThreePacketPolynomial.md`.
- Deliberate palindromic input `(12,33,21),q=100` is rejected.
- **NOT CLAIMED:** any infinite Lychrel certificate, positive drift, Lean verification, or anything about 196.
