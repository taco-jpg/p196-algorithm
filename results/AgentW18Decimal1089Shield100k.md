# AgentW18Decimal1089Shield100k
**COMPUTED.** The constructive base-10 family `N0(Q)=5(99)^Q4`, from `AgentW18Decimal1089Shield.md`, extends to **100,000** palindrome-free reverse-and-add steps uniformly for **every Q>=20,702**.
Its exact two-wall carry recurrence (from N23) keeps `U_t ++ 9^L_t(Q) ++ V_t` (LSD first), equal-size unequal reflected exteriors, and `L_t(Q)>=2` for all t<=100000; every actual symmetric pairword has a central coefficient-18 run.
At boundary Q20702: 41,406 starting digits, 82,808 final digits, min/final central band 2, paired trims 58,598, overflows 41,402, final rolling checksum 132839273 (mod 1000000007).
A new independent full-decimal-digit reverse-add oracle (not using the symbolic two-wall recurrence) verifies all 100,001 actual digit lists, nonpalindromicity, and central band at every state, with matching checkpoints and checksum.
Q20701 loses the *L>=2* guard at t=99,995; no palindrome or infinite-time claim follows from this boundary.
This improves the earlier N23 100k threshold Q30037 by 31.1% but is still a finite-horizon COMPUTED family, not a decimal Lychrel certificate.
Reproduce: `bash calculation/new_structures/agent-W18/reproduce_100k.sh`.
Code/data: `calculation/new_structures/agent-W18/`; details: `reports/AgentW18Decimal1089Shield100k.md`.
