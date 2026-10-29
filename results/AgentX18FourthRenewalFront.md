# AgentX18FourthRenewalFront
- **COMPUTED** (finite decimal arithmetic only): a 60-entry, nonperiodic half-centre U gives a 127-coefficient symmetric centre and three full 88-step p8/m20 band renewals.
- At the fourth macrostep (t=352), the attempted replacement band has a prefix of length 2/20 and 5/20 coordinate matches; the unmodified N18 three-renewal seed has only 3/20 matches at this step.
- Four ordinary decimal integer seeds, q=1,2,3,4, of lengths 245,285,325,365 digits, were independently replayed through t=352, with no palindrome and exact pairword agreement at every step.
- Centre length before trimming at times 88,176,264,352 is respectively 211,255,299,343 for q=1. Each complete renewal removes 40 coefficients and leaves centre length growth +44 per 88-step macrocycle.
- All 352 overflow steps have the expected alternating 1010 clock and all 39 exterior columns match their time phase in each replay.
- C++ deterministic nonexhaustive beam checked 46,430 distinct U candidates at n=60 (beam=128, 12 rounds, RNG seed 777); no exhaustive or optimality assertion.
- Reproduce: from calculation/new_structures/agent-X18 run g++ -O3 -std=c++17 beam.cpp -o beam && ./beam 60 128 12 777 && python3 replay.py.
- Code/data: calculation/new_structures/agent-X18/{beam.cpp,replay.py,candidate.json}; lattice data imported from calculation/new_structures/agent-N18/lattice.txt.
- **UNDECIDED:** a fourth renewal, an indefinitely replenishing centre, any decimal Lychrel number, and any Lean proof.
