# AgentW02P12BallisticFront
**COMPUTED**, base 10 p12/m9 phase-2, ordinary reverse-and-add times t=0..5000 from three 20,000-digit seeds.
The rightmost defect position satisfies R_A(t+76)=R_A(t)+33 for every 337<=t<=4924; R_B does so for every 155<=t<=4924.
Three independent ordinary decimal digit-vector replays cover 15,003 nonpalindromic states; every full lower-half delta FNV64 hash, support endpoint and edge coefficient matches the separate local carry engine.
The bulk pairword and carry arrays have exact (76,33) space-time covariance by a finite 12x9 table check.
**COMPUTED** collision-clock renormalization: for all 41 gaps g=189,198,...,549, T(g+378)=T(g)+608; it fails at g=180 (605) and g=558 (607). Five actual integer collision events are independently checked.
The second frontier coefficient mismatches as late as t=4592 (A) and t=4644 (B); the full wake does NOT return with the front, so this is not a periodic soliton or an infinite Lychrel certificate.
Source, independent decimal checkers, expected data, corruption control and reproduction: calculation/new_structures/agent-W02/, `sh calculation/new_structures/agent-W02/run.sh`.
Interpretation and exact caveats: reports/AgentW02P12BallisticFront.md. No Lean theorem or result about 196 is claimed.
