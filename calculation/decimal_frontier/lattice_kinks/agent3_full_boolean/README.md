# Agent3FullBooleanLocalParity: complete six-bit GF(2) local classification

Python 3 standard library only, no external checkout or solver. From repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/generate.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/independent_check.py

generate.py regenerates and compares the four committed certificates; use --write only if intentionally regenerating them. lat2.txt (1,952 bytes) is the rec2 reference lattice. rank_witness.json gives 388 independent rec2 test tags. global_witness.json gives 400 independent unrestricted covariance row tags (word-index, phase) from 100 deterministic 48-cell physical cyclic words (seed 4196). graph_certificate.json lists 14 universal zero-function masks and a verified 76-state potential for each. counterexamples.json lists 12 independent false-positive coefficient masks (hex 512-bit vectors) and 12 explicit physical cyclic coefficient words/phases giving an invertible 12x12 violation matrix. All files <5 MB.

Expected outputs:

    PASS: regenerated 14 all-row coboundaries, 388 local pivots, 400 global pivots, 12 independent false positives
    PASS: 76-state/1444-edge carry graph, 14 independent all-row zero identities
    PASS: rec2 2252-row rank=388/512; 388 explicit independent witness tags
    PASS: 400 independent unrestricted covariance rows; universal kernel dimension=112
    PASS: 12 independent local-test false positives, 12 physical cyclic-word counterexamples
    CONTROL: 10,000 random physical cyclic carry words satisfy all 14 identities
    PAPER PROOF: complete 64-feature all-Boolean rec2 covariance classification
    INDEPENDENT PASS: digit-normalized ranks 388 (local) and 400 (unrestricted)
    INDEPENDENT PASS: all 1444 graph edges, 12 independent physical cyclic-word counterexamples

The full 64 monomial basis is ordered by six-bit subset mask 0..63, with bit positions (P_j mod2, P_(j+1) mod2, a_j, d_j, a_(j+1), d_(j+1)). The eight-phase covariance is C_(t+1)(F_(g_t)(P)) = (11 if g_t=1 else 2) C_t(P) modulo 2, with g=10101010. All 2,252 reference tests are exact, and the graph coboundary proof holds for every eligible cyclic 48-cell row. This is NOT a finite-centre no-go, full K1 decision, actual integer orbit, or decimal Lychrel certificate.
