# Agent3FourCellBoundaryTransport: complete self-contained reproduction

Run from repository root (Python 3.10+ standard library only):

    python3 calculation/decimal_frontier/lattice_kinks/agent3_fourcell_transport/primary.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_fourcell_transport/independent_check.py

The primary enumerates 19^4*4=521284 physical four-cell assignments and deduplicates to 1312 twelve-bit patterns; the nine-bit endpoint graph has 288 vertices, six self-loops and is connected. It constructs the 288 independent 1312-bit edge evaluations of 287 endpoint indicator gradients plus constant length parity, and verifies that 1471 deterministic seeded cyclic words (Python Random(9397)) have 4096-monomial rank1024. This gives the sharp 2784+287+1=3072-dimensional universal zero-sum kernel.

The independent checker never imports the primary checker. It glues three edges of a separately enumerated 76-state/1444-edge physical carry graph, reproducing 521284 physical four-cell paths and 1312 allowed 12-bit patterns. It independently verifies rank1024 using ordinary 384-digit reverse-and-add carry normalization and a lowest-bit rather than highest-bit GF(2) pivot. Eight genuine positive 406-digit decimal integers from rec2 prefixes plus four bulk copies reproduce actual overflow bits and 768 interior next-pairword coefficients; a wrong-overflow negative control must fail. It checks 178 distinct rec2 nine-bit boundary signatures and finite-interval telescopes.

Included rec2_w0.txt (48 coefficients) and rec2_prefix.txt (8 rows x 11 coefficients) are exact snapshots from rec2 lat2.txt. All source/data are in this folder, each file <5 MB. No network, external solver or Lean required.

Expected primary output:

    PASS: 521284 physical four-column assignments -> 1312 allowed 12-bit patterns; 2784 forbidden
    PASS: 288 connected 9-bit endpoints, 6 loops; 287 gradients + 1 length parity independent
    PASS: 1471 seeded 48-cell physical cyclic words attain rank1024/4096
    PAPER PROOF: exact 3072-dimensional cyclic-zero kernel = 2784 local zeros + 287 gradients + 1 length parity
    PASS: rec2 8 phases x 48 cuts; endpoint counts 45,42,35,45,45,42,35,45; union 178
    PASS: 8*48*11 finite-interval telescopes, 192-step return adds 48 paired cells

Expected independent output:

    INDEPENDENT PASS: 76-state 1444-edge graph, 521284 4-cell paths, 1312 physical 12-bit patterns
    INDEPENDENT PASS: 1471 genuine 384-digit integer samples attain rank1024/4096
    INDEPENDENT PASS: eight 406-digit rec2 controls, actual overflow, wrong-shift negative control, 768 bulk outputs
    INDEPENDENT PASS: 288 endpoint graph connected, six loops; 178 rec2 endpoint signatures; interval telescopes

Local runs: primary <5 seconds/<100 MB; independent <2 seconds/<100 MB. Full tools/verify.py --changed unavailable due blocked shell GitHub DNS / absent checkout. Non-Lean PAPER PROOF, not a repository-wide verification claim.
