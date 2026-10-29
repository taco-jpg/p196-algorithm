# AgentV09AlltimePhysicalW30Counterexample
**PAPER PROOF:** For every integer k>=1, the canonical decimal seed `1 0^(5k) 3 (78876)^k 0` has the W30 period-five interior pairword row `(6,7,8,8,7)` and after ONE genuine reverse-add step becomes the palindrome `1 (67887)^k 6 (78876)^k 1`, with overflow bit 0.
At the published W30 rank-two state `{(6,7,8,8,7),(12,11,10,10,11)}`, the allowed label-0 edge sends both rows to all-even rows. Thus arbitrary-label interior closure alone cannot imply an all-time odd-pair safety guard.
**Redirection:** a decimal certificate using this W30 carrier must prove a physically forced safe overflow/guard language or a permanent external odd witness and a regenerating finite boundary.
**COMPUTED independent controls:** 102 full canonical seeds (`k=1..100,300,1000`) checked against both BigInt and unrelated schoolbook digit addition; exact pairword/overflow/output comparisons PASS.
**Scope:** Counterexample to a hypothetical safety promotion, NOT a contradiction of W30's explicitly conditional bulk theorem, NOT a decimal infinite-Lychrel claim, NOT Lean verified.
Proof and cross-wave claim audit: `reports/audit_2026-10-28/AUDIT_alltime_claims.md`.
Reproduce: `node calculation/new_structures/agent-V09/check_w30_one_step.mjs`.
