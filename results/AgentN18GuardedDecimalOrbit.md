# AgentN18GuardedDecimalOrbit
**COMPUTED**: decimal seed family with a finite, long-lived lattice exterior; **not** a base-10 Lychrel certificate.
Define the least-significant-first symmetric pair word `P(q) = B ++ W0^q ++ [0] ++ reverse(W0^q) ++ reverse(B)`, where `B` is the first 39 path columns of the first `p8_scc.txt` SCC at time 0 and `Wt` is time row `t` from `lattice.txt` (period 20).
Split each symmetric pair coefficient `p_i` into source decimal digits `d_i=min(9,p_i)`, `d_{n-1-i}=p_i-d_i`, and `d_mid=0` (canonical leading digit 8).
For `q=256`, initial seed has 10,319 digits, SHA256 of its conventional decimal spelling `59f306f54f7295f0b77181c76840b12d5d264b3512e078925345a614cf98afa0`.
Ordinary GMP integer replay checks all `N_0..N_20000`: no palindrome; every *whole* pair word agrees with the temporal 39-column exterior and contains at least 28 complete period-20 `W_t` copies on each reflected side.
At `t=20000`: 20,319 digits, 10,000 overflows, >=28 complete intact bands; coefficient-list arithmetic independently agrees (the implementations use different number representations).
First exterior-column mismatch is at `t=88q+4` for `q=1,2,3,4,8,16,32,64,128,256` (bounded observations; not an all-q formula), initially at spatial index 38; thus `q=256` fails to close at `t=22532`.
Run from `calculation/new_structures/agent-N18`: `g++ -std=c++17 -O3 forward_guard.cpp -o forward_guard && ./forward_guard 256 20000`.
Independent numeric check: `g++ -std=c++17 -O3 check_gmp.cpp -lgmpxx -lgmp -o check_gmp && ./check_gmp 256 20000` (requires GMP; no template normalization is used by this checker).
Controls: `./forward_guard 1 92` reports first break 92; `./forward_guard 2 180` reports 180; `./forward_guard 4 356` reports 356; `./forward_guard 256 22532` reports first break 22532.
Scope: finite-step arithmetic only; the moving central front ultimately destroys the exterior. Proposed new direction: an inverse-preimage renewal step that injects one period-20 block before approximately 88 further steps, without altering the exterior carry phase.
