# AgentX12TwoClockCentrePulse
**COMPUTED** (exact finite arithmetic, not a decimal Lychrel certificate).
Define palindromic least-significant-first pairwords P(q,r)=B0 ++ W0^q ++ C(r) ++ rev(W0)^q ++ rev(B0), where B0/W0 are the known p8/m20 rooted exterior, U=1^40 except U[13]=7,U[20]=7,U[30]=6, and C(r)=[8,0,0]++U++1^r++[16]++1^r++rev(U)++[0,0,8].
For q=7,r=850, P(q,r+1) is a **whole-word symmetric one-symbol insertion** of P(q,r) at all 1001 states t=0..1000 of two genuine decimal reverse-add orbits; inserted symbol at t>=1 cycles [2,4,8,16,14,10].
In all 989 twelve-step comparisons the cut moves -5 positions relative to the changing midpoint; all 737 264-step comparisons move -44 absolute positions. The 264-step beat combines a 12-step inner clock with the rooted 88-step exterior.
For q=1,r=850, the same entire-word insertion persists 1000 steps even though its 12-step drift first fails for the interval starting t=613 and alternating overflow first fails at t=622: a carry-dependent envelope mode change, not insertion death.
For q=1, each r=1..100 has a measured first insertion-death time L(5k+s)=6k+(13,15,16,16,17)[s-1] for s=1..5; these are 100 finite instances, NOT an all-r theorem.
An independent Python built-in-integer calculation replays all four base-10 orbits through 1000 additions (4004 whole-number/pairword comparisons; zero palindromes), separately from the coefficient engine.
Reproduce: `python3 calculation/new_structures/agent-X12/beat.py` (Python 3.11+); compact output `calculation/new_structures/agent-X12/observations.json`.
Details and proposed adaptive macro-certificate format: `reports/AgentX12TwoClockCentrePulse.md`.
**Not claimed:** a fixed integer with infinite survival, an all-r glider theorem, a Lean proof, a complete closed macro-edge, or any assertion about 196.
