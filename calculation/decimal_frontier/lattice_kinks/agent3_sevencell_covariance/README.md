# Agent3SevenCellPhaseCovariance reproduction

**PAPER PROOF** for the complete seven-cell GF(2) physical-carry covariance ansatz, decimal rec2 p8/m48, overflow 10101010. Not a centre exclusion or decimal certificate.

From the repository root run:

    sh calculation/decimal_frontier/lattice_kinks/agent3_sevencell_covariance/run_checks.sh

C++17 standard library and sha256sum only. Primary modes 2/0/1 generate source/g0/g1 physical 48-cycle witnesses; each generated file is exactly 4,666,368 bytes (<5 MB). Their SHA256 values are pinned in the script. No external files or sandbox code are needed. The independent checker uses forward 76-state-set DP, a different BFS spanning tree and opposite-pivot GF(2) elimination, and literal ordinary decimal digit normalization for all three 97,216-row witness streams. Eight genuine 406-digit rec2 controls and wrong-overflow-shift negatives are checked.

Physical carry graph: 76 states, 1444 edges, 124512 seven-masks, 27296 connected six-mask endpoints, six loops. Output product transducer: 5776 nodes, 109744 edges, recurrent SCC sizes 3116 (g0, hub1563) and 5626 (g1, hub0). Every allowed target seven-mask is reached by a physical 48-cycle image; all source/g0/g1 GF(2) ranks are 97216.

Local standalone check passed in under 21 seconds, under 600 MB RSS per process. Full tools/verify.py --changed was unavailable due GitHub shell DNS/checkout; no Lean or global CI success is claimed.
