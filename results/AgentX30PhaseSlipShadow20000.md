# X30: noncoalescing phase-slip shadow in decimal period-four bulk
- **COMPUTED**: exact decimal seed N0=("5346")^4000 ++ "3465" ++ ("5346")^7999 (48,000 digits). Among all 20,001 reverse-add states t=0..20000: zero palindromes; final 56,323 digits; 8,323 overflows.
- The overflow bit at EACH step matches that of the unmodified ("5346")^12000 reference. Yet the two orbits never coalesce: initial/final Hamming distance 4/21,586, maximum 21,744.
- In every modified orbit state the symmetric pair-coefficient word contains >=3,941 consecutive period-4 positions, exact global minimum at t=20000.
- Every state has a mirrored digit mismatch at index <=18 in unchanged outer digits; common outer guard >=14,129 digits on both sides.
- Independent radix-1e9 bigint and decimal schoolbook arithmetic agree on EVERY state, with FNV64 MSB-first decimal final checksum d4ed11ed5dc47a65.
- Additional 20k-step shadows: a 80-block patch 3465, a 1/80-block patch 4653, and a one-block 6534; smaller Q=10000 one-block case passes two engines with minimum pair-period-4 run 1,273.
- Reproduction: g++ -O3 -std=c++17 calculation/new_structures/agent-X30/phase_shadow.cpp -o /tmp/x30s && /tmp/x30s 12000 4000 1 1 20000; same command for independent_limb.cpp (executable /tmp/x30i). CSV and source in that directory; proof-scheme discussion in reports/AgentX30PhaseSlipShadow20000.md.
- **NOT** a base-10 Lychrel certificate, an infinite-time result, or a Lean proof. Both the periodic region and guard decrease; no self-renewing cycle is found.
