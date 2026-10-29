# Agent X25: 792-step four-port decimal collision interface
**COMPUTED**, finite horizons only; no decimal Lychrel certificate or result about 196.
On the rooted p8/m20 background with N21 p12-derived A/D packet symbols, track the outward right front R(t) and four *actual radix carry ports* around its mirrored 101-coefficient window: c[R−20], c[R+81], c[n−1−(R+80)], c[n−(R−20)].
For q=600, x=2500, ordinary decimal pairword recurrence t=0..5000: both the front's 540-cell translation and ALL four carry gates return after 792 steps, for every t=422..4208 (A) and t=497..4208 (D).
A second q=350, x=1500 run t=0..3000 reproduces exactly the same stabilization thresholds 422 and 497.
Independent ordinary GMP n + reverse(n) uses next-integer decimal digits to recover carries via (P_i+c_i−digit_i)/10; all three q=140, x=960 seeds agree at every pair coefficient and carry check for t=0..1792 (5379 whole-number states), with no palindromes; the four-port recurrence is exact for t=422..1000 (A) and t=497..1000 (D).
In the joint stable interval t=497..4208, immediately preceding runs of coefficient 9 at the four ports have maximum lengths (3,1,0,3), for BOTH A and D; thus each port is locally pinned by at most four preceding coefficients (elementary carry-forcing lemma in the report).
This is a finite **two-ended carry-interface**, not merely a moving digit pattern. The 792-step port source is NOT proven to self-generate forever; the entire packet wake grows and there is no regenerative infinite certificate.
Reproduce: sh calculation/new_structures/agent-X25/run_ports.sh (requires C++17 and GMP).
Code and fixture: calculation/new_structures/agent-X25/{carry_ports.cpp,carry_ports_gmp.cpp,carry_ports_expected.txt,run_ports.sh}.
Details and exact limits: reports/AgentX25ClockedCarryPorts.md.
Next: finite transfer-semigroup proof that the 792-step boundary contract is stable for all pumped band lengths, then a wake-erasing collision tile.
