# Agent15F2FamilyP1724
**COMPUTED.** Exact 192-bit reachable-position automaton census for bases 7,19,22,25 and primitive canonical overflow periods 17..24, with a 3,000,000-state cap per word.
30635 primitive position-zero-feasible words: 30618 exhausted with no eligible lattice cycle of spatial length m ≤ number of overflows S; 17 hit the cap and remain **UNDECIDED**.
No new self-mirror absorbing lattice or base-10 certificate is asserted.
Scope is only the stated bases, periods, first-column necessary filter and caps; no general parametric-family claim.
Data: `calculation/decimal_frontier/lattice_formats/agent15_f2_p17_24.md`.
Reproducer: `calculation/decimal_frontier/lattice_formats/code/agent15_generate_f1.cpp`, `code/agent15_f2_reproduce.py`, and existing `code/bauto5.cpp`.
Controls: base 9 `1100011000` m=4 and base 13 `1010010000` m=1; known base-7 imprimitive `(10)^12` m=6.
Reproduction: build both C++ files with `g++ -O3 -std=c++17`; run `python3 agent15_f2_reproduce.py` in an empty scratch directory containing both binaries.
