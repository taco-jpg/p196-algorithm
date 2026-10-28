# Agent10F2G01LinearDecision
**PAPER PROOF.** For every integer base b>=2, the canonical-root neutral
exterior position automaton for the period-two overflow word g=01 can be
decided by an exact affine-column BFS with at most 8b+1 reachable states
and at most four candidate edges per state (O(b) arithmetic operations).
Proof: reports/Agent10F2G01LinearDecision.md.
Code: calculation/decimal_frontier/lattice_formats/code/agent10_g01_even_fast.cpp.
Reproduce: c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_formats/code/agent10_g01_even_fast.cpp -o /tmp/a10g01;
/tmp/a10g01 2 10000 /tmp/a10g01.csv (append-only output; fresh file).
Generic-engine cross-check: b=2..300 identical visited counts/first accepts.
Finite controls: 1710/5000 even bases b<=10000 accepted; b26 depth 8.
Scope: exterior acceptance only; no centre closing, infinite-base
certificate family, base-10 result, or 196 Lychrel conclusion.