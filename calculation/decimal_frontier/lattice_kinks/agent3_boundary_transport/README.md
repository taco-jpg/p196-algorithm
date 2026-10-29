# Agent3ThreeCellBoundaryTransport: self-contained exact controls

From repository root (Python 3.10+ standard library only):

    python3 calculation/decimal_frontier/lattice_kinks/agent3_boundary_transport/primary.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_boundary_transport/independent_check.py

The primary checker enumerates 19^3*2^2=27,436 actual three-column coefficient/carry assignments, 288 distinct nine-bit patterns, and the connected 64-vertex endpoint quotient. It explicitly constructs 224 pointwise-zero indicator polynomials, 63 endpoint-gradient polynomials and one length-parity polynomial, then verifies rank 288 of their 512-bit monomial masks. The upper-bound witness is exact rank 224 of 229 seeded 48-cell physical cyclic words (seed 9396). All rec2 phases, 48 cuts, 11 interval lengths and the 192-step/48-paired-cell phase return are checked.

The independent checker does NOT import the primary checker. It constructs the 76-state/1,444-edge physical carry graph and 27,436 consecutive-edge pairs. Its rank-224 witness uses a different pivot order and ordinary 384-digit integer reverse-and-add carries, not cyclic carry recurrences. In all eight rec2 phases, it builds genuine 406-digit positive integers from the 11-cell outer prefix plus four 48-cell bulk copies, verifies the actual overflow bit and 96 bulk output pairword coefficients per phase, and checks that the WRONG overflow shift fails. It independently checks all 64 endpoint signatures and interval telescopes.

The included rec2_w0.txt and rec2_prefix.txt are the exact 48-cell initial lattice row and eight 11-cell root rows from the repository's lat2.txt. Seven later bulk rows are generated and checked by both arithmetic engines. Both data files are <5 MB. No network, external solver, Lean, or nondeterministic input is needed.

Expected primary output:

    PASS: 27,436 exact physical triples collapse to 288 allowed 9-bit patterns
    PASS: 64 connected 6-bit endpoints, 6 self-loops, rank 224 local zeros + 63 gradients + 1 length parity = 288
    PASS: 229 seeded cyclic physical words rank 224/512, hence universal zero kernel exactly 288
    PASS: all 8 rec2 phases and 48 cuts; endpoint counts 35,29,27,35,35,29,27,35; union all 64
    PASS: 8*48*11 finite-interval tests, 192-step / 48-paired-cell rec2 return
    PAPER PROOF: finite-interval universal 3-cell transport has exactly 64 independent boundary/length observables

Expected independent output:

    INDEPENDENT PASS: 76-state / 1444-edge physical carry graph, 27436 triples, 288 9-bit patterns
    INDEPENDENT PASS: 229 genuine schoolbook integer reverse-add samples rank224
    INDEPENDENT PASS: 8 rec2 prefix-controlled genuine integer overflows and 768 bulk pairword checks
    INDEPENDENT PASS: all 64 6-bit endpoint signatures; 8*48*11 interval telescope controls

Author's local runs: <2 seconds and <100 MB RSS per checker. Repository-wide tools/verify.py --changed was unavailable due blocked shell GitHub DNS / absent checkout; no success claim. This is non-Lean PAPER PROOF.
