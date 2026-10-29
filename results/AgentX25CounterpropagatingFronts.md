# Agent X25: asymmetric 88/792-step decimal packet fronts
**COMPUTED** for rooted p8/m20 decimal pairword orbits with N21 p12-derived A and D packet symbols; finite times only, no infinite Lychrel certificate and no result about 196.
For q=600, insertion x=2500, exact full pairword replay t=0..5000 of clean/A/D (initial 24085 decimal digits) preserves alternating p8 overflow and an odd outer coefficient, hence no palindromes.
A's left front has an identical moving 101-coefficient window after 88 steps with drift -20 at every t=397..4912; D's left front at t=242..4912.
A's RIGHT front has an identical moving 101-coefficient window after **792** steps with drift +540 at every t=422..4208; D's at t=494..4208. The right windows do NOT match at any tested shift 88,176,...,704 at the corresponding +60-per-88 displacement.
A different q=350, x=1500 run through 3000 steps independently reproduces all four stabilization thresholds.
Independent genuine GMP integer n+reverse(n) replay for ALL THREE q=140, x=960 integers checks every full pairword at t=0..1792 (5379 states, zero palindromes), and independently recovers all four moving-window laws and thresholds.
The right 792-clock has a bounded recurrent *tip* but an expanding nonperiodic wake; the recurrence has not been proved for unbounded time or any symbolic buffer length.
Code/data: calculation/new_structures/agent-X25/{dual_front.cpp,dual_gmp.cpp,dual_front_expected.txt}; detailed limits: reports/AgentX25CounterpropagatingFronts.md.
Reproduce: g++ -O3 -std=c++17 calculation/new_structures/agent-X25/dual_front.cpp -o /tmp/x25f && /tmp/x25f 600 2500 5000
Independent: g++ -O3 -std=c++17 calculation/new_structures/agent-X25/dual_gmp.cpp -lgmpxx -lgmp -o /tmp/x25g && /tmp/x25g 140 960 1792
Next: seek a 792-step two-ended carry-port self-generator and a nonlinear collision output that erases the wake rather than merely emitting finite-time frontier clocks.
