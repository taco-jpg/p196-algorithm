# AC30 reproducibility notes

Reference: calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, phase row 9 (not row 0).

1. Compile: g++ -O3 -std=c++20 calculation/new_structures/AC30/scan.cpp -o /tmp/ac30scan
2. Arithmetic gate: python3 calculation/new_structures/AC30/gate.py
3. Carry cones: python3 calculation/new_structures/AC30/phase9_cones.py
4. Ordinary integer insertion audit: python3 calculation/new_structures/AC30/verify_lift.py 0 30 (240 insertion trajectories, 120 edges each). Code selects published lattice relative to its own path.
5. Exhaustive mod-11 filtered all-width necessary cell: /tmp/ac30scan calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt oddgate 4952198 0 14 100 0
6. Chunk reproduction (preserves identical exhaustive search): offsets 0,500000,...,4500000; count 500000 except final offset 4500000 count 452198. Aggregate all lines first_mismatch=N count=M to obtain the histogram. Each U is indexed over all 19^5 junction words, rejecting only A(J) != 3 mod 11 before actual replay.
7. Independent bigint: python3 calculation/new_structures/AC30/independent.py calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt 0,0,0,0,0 9,0,18 4,14,4. The script prints q/k controls at 14/100,20/80,40/160,80/320,160/640.

Full exact histogram (LSD pair-coefficient index, count): 135:186153, 136:70771, 138:101269, 139:78411, 140:7563, 141:5043, 142:562, 143:395, 144:22, 145:50, 147:3. Sum 450242, zero returns, zero clock/length discrepancies and zero palindromes at t=0..119. All 30 genuine overflows are at times t=3 mod4.

Pruning caveat: odd-centre all-width mod-11 gate is sound because an all-q,k return needs both independent q and k parity classes. This does NOT establish endpoint-only failure for 28 excluded U at the single literal k=100. No strict-W9 phasewise filters are present.
