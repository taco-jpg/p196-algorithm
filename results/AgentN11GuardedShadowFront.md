# AgentN11GuardedShadowFront
**COMPUTED** finite-time front timing for explicit decimal N_L; elementary guarded-prefix one-step soundness lemma in report, not Lean.
Three stripe lengths L=2000,4000,8000 compared to N_45000 (and N_16000 control): outermost pair-coefficient first divergence at 13,505 / 26,346 / 52,270; outer-64 first divergence at 13,120 / 26,006 / 51,936.
First differing overflow decision at steps 13,512 / 26,352 / 52,274; the initial zero domain had already vanished at steps 3,334 / 6,648 / 13,274 respectively.
All 11 first-arrival times for coefficient prefix widths K=1..1024 are exact, independently checked at K=1,64,1024 and overflow by MSB-first decimal-string arithmetic with every iterate nonpalindromic through each divergence.
New constructive mechanism: the pairword defect front is delayed around 6.5L steps before reaching the exterior, despite the zero-domain front disappearing at around 1.66L steps. No universal velocity or infinite certificate claimed.
A guarded one-step prefix-transfer lemma works for arbitrary-length integers whenever the common coefficient at the inner cut is !=9 (12,000 independent bigint random controls).
Source/checker/controls/runner: calculation/new_structures/agent-N11/sync_front.cpp, sync_independent.cpp, guarded_prefix.py, shadow_expected.json, shadow_reproduce.sh.
Detailed proof, caveats and route to regenerative cuts: reports/AgentN11GuardedShadowFront.md.
