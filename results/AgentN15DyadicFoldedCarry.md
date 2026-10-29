# AgentN15DyadicFoldedCarry
**PAPER PROOF** (exactly scoped): for every dyadic level h>=2, the base-10 palindromic pairword `P_h=(4 ++ sigma^h(A)) ++ reverse(4 ++ sigma^h(A))`, `sigma(A)=AB`, `sigma(B)=BA`, `A=14`, `B=16`, has **two exact successive morphic reverse-and-add pairword images**, given by explicit one-letter and adjacent-letter formulas in the report.
The first edge is independently certified for ALL h by a four-state Boolean carry-relation monoid: just two reachable substitution-matrix triples (preperiod 1, period 1). The overflow-1 next edge uses an exact delayed high-digit relation.
**COMPUTED**, separate finite claim: canonical decimal seeds at h=5..12 survive 20,000 ordinary digit-list steps with full pairword/digit-sum cross-check and no palindrome; h=9: 1026 -> 9362 digits, 8336 overflows. Independent Python bigint replay checks h=9 for 1,000 steps.
By temporal step 3 the interior no longer follows a one-letter morphism; measured finite-prefix coding radius rises from 0 at t=1 to 20 at t=32 (h=11). Thus no all-time morphic closure has been found.
This is **NOT** a decimal Lychrel certificate, not a proof of an infinite palindrome-free orbit, and says nothing specifically about 196.
Proof/limits: `reports/AgentN15DyadicFoldedCarry.md`.
Reproduce: `sh calculation/new_structures/agent-N15/run.sh`.
Sources/data/checkers: `calculation/new_structures/agent-N15/`.
