# AgentW18Decimal1089Shield
**COMPUTED.** The genuine base-10 seed N0(Q)=5(99)^Q4 has a **20,000-step uniform finite-horizon nonpalindromic orbit for every Q>=4138**.
At all 20,001 states, ordinary decimal digits are U_t ++ 9^L_t(Q) ++ V_t (LSD first), with |U_t|=|V_t|, U_t != reverse(V_t), L_t(Q)>=2; hence its symmetric pairword has a central coefficient-18 run.
The exact two-wall arithmetic rule is inherited from N23's sound transducer, but the new initial pair coefficient 9 (versus their 5) yields a substantially smaller 20k boundary: 4,138 instead of 6,016 repeated 99 groups.
Q4138: 8,278 initial digits, 16,552 final digits, final/min L=2, 11,726 paired trims, 8,274 overflows, checksum 425518744 mod 1000000007.
Q4137 first violates the transducer's L>=2 guard at t=19,998; this is **not** a palindrome or a no-go theorem.
Two independent C++ implementations (digit-wall and radix-1e9 ordinary-integer reversal/addition) check all 20,001 states; no full infinite certificate is claimed.
Reproduce: `bash calculation/new_structures/agent-W18/reproduce.sh`.
Code/data: `calculation/new_structures/agent-W18/`; details: `reports/AgentW18Decimal1089Shield.md`.
