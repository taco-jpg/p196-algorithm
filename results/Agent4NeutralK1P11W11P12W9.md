# Agent4NeutralK1P11W11P12W9

**COMPUTED.** Exhaustive finite-window DFS with sound bitmask pruning; no state cap.
Decimal neutral p11 g=11100010000, e=10100110011: no centre window of lower-half width <= 11
in either length-parity class after 90 completed transitions (o=0,1: survivors 0,0).
Decimal neutral p12 g=100010001000, e=101010010101: none of width <= 9
after 70 completed transitions (o=0,1: survivors 0,0); the other p12 exteriors rotate this cycle.
Finite-horizon exclusion holds for every possible centre temporal period at these widths.
Run input generator: python3 calculation/decimal_frontier/lattice_formats/code/make_neutral_k1_inputs.py /tmp/k1
Build: g++ -O3 -std=c++17 calculation/decimal_frontier/lattice_formats/code/kinkdfs_mask.cpp -o /tmp/kinkdfs_mask
Run: /tmp/kinkdfs_mask /tmp/k1/neutral_p11.txt 11 90 0 2
Run: /tmp/kinkdfs_mask /tmp/k1/neutral_p12.txt 9 70 0 2
Positive control: /tmp/kinkdfs_mask /tmp/k1/neutral_b26_control.txt 3 30 0 2 yields (4,2) survivors.
Source: calculation/decimal_frontier/lattice_formats/code/kinkdfs_mask.cpp (restart by phase/prefix).
Scope: no wider-centre, other-exterior, base-10 certificate or 196 claim; full verify.py unavailable.
