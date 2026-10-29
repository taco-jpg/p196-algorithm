# AgentW27Grafted196NineBand
**COMPUTED.** For every integer Q >= 6005, the actual base-10 reverse-and-add orbit of the explicit seed `196 ++ 9^(2Q) ++ 196` is nonpalindromic at every time t=0..20000.
Every such state has a central 9 band and hence a palindromic pairword of shape `B_t ++ 18^(g_t+2(Q-6005)) ++ reverse(B_t)` for the baseline maximal central pairword 18 band, with g_t >= 5.
The finite computation at Q=6005 compares **all decimal digits at every step** between two independent arithmetic engines and also checks the exact Q=6006 two-9 insertion identity at every step.
**PAPER PROOF ingredient:** central-9 insertion commutes with reverse-and-add while both successive states retain >=5 central 9 digits; inductively transfers the entire Q=6005 verified prefix to every Q>=6005.
Q=6005: start length 12016, last length 20317, 8301 length overflows, minimum central 9 and pairword 18 runs both 5; no palindrome among all 20001 states.
Independent Python arbitrary-precision integer replay through t=160 and 19566 exhaustive short-outer-word lemma tests.
Code: `calculation/new_structures/agent-W27/{hybrid.cpp,lemma_check.py,expected.json}`. Reproduce: `c++ -O3 -std=c++17 calculation/new_structures/agent-W27/hybrid.cpp -o /tmp/w27 && /tmp/w27 6005 20000 && python3 calculation/new_structures/agent-W27/lemma_check.py`.
Details: `reports/AgentW27Grafted196NineBand.md`. This is a **finite-horizon parameterized family**, not a base-10 Lychrel certificate, not the true 196 orbit, and not an infinite-time assertion.
