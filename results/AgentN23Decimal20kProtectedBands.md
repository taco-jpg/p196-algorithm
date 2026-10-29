# AgentN23Decimal20kProtectedBands
**COMPUTED.** Genuine base-10 reverse-and-add candidate seeds 12(99)^Q34 for Q=7000,7001,8000.
For EACH of 20,000 successive steps (including initial and final states), the full decimal integer is nonpalindromic and its complete symmetric digit-pair word has a central coefficient-18 band of length >= 1970,1972,3970 respectively.
One C++ oracle uses ordinary base-10 arbitrary-length digit carries; a structurally independent C++ bigint oracle uses base-1,000,000,000 limbs and explicit decimal-string reversal.
Both independently check nonpalindromicity and the central digit-band condition at every step; final full-number rolling checksums modulo 1000000007 agree.
For Q=7000 the initial/final digit lengths are 14004/22266 and central band lengths 14000/1970.
All computed values for Q=7000,7001,8000 appear in calculation/new_structures/agent-N23/seed20k.tsv.
One-command full reproduction: bash calculation/new_structures/agent-N23/reproduce_20k.sh.
Detailed scope: reports/AgentN23Decimal20kProtectedBands.md.
This is finite 20k-step evidence and a protected-band mechanism, **not** an infinite decimal Lychrel certificate or a proof about 196.
