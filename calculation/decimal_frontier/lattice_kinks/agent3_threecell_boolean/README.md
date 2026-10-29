# Agent3ThreeCellBooleanNoGo: complete 512-feature rec2 local classification

Python 3 standard library only. From repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_threecell_boolean/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_threecell_boolean/independent_check.py

Optional: append --export to the primary verifier to generate reference_witness.json (814 exact tags, 9.6 KB), global_witness.json (1,792 tags, 13.5 KB), and graph_certificate.json (288 masks and 1,444-vertex potentials, 876.7 KB). These generated files are not needed for verification; their exact SHA-256 digests are fixed in the committed manifest.json, and the verifier recomputes and checks all three. This is a self-contained deterministic finite certificate, not a random inference. The raw rec2 lattice is committed as lat2.txt (1,952 bytes). counterexample.json is a literal physical cyclic 48-cell word where a degree-five single-monomial covariance mask fails despite passing every rec2-local test. All generated artifacts are <5 MB.

Expected output:

    PASS: 2252 rec2 tests rank814/4096; 814 explicit deterministic independent tags
    PASS: 229 seeded cyclic words give rank1792/4096; 288 independent graph coboundaries per phase
    PASS: 1444 base carry edges, 27436 de Bruijn edges, 288 exact potential checks, all SHA256 digests
    PASS: degree-five single-monomial finite-test false positive has a physical cyclic-word counterexample
    PAPER PROOF: all 3-cell Boolean local covariance zero functions form a 2304-dimensional kernel
    INDEPENDENT PASS: digit-normalized 2252 reference rank814 and 229-word global rank1792
    INDEPENDENT PASS: 288 universal masks on 27436 lifted carry edges; explicit physical false positive

The six-bit two-cell ansatz is replaced by nine bits: coefficient parities at j,j+1,j+2, ascending carries at j,j+1,j+2 and descending carries at j,j+1,j+2. All 512 square-free Boolean monomials (subset masks 0..511) and eight independent phases give 4096 coefficients. The 76-state physical carry graph has 1444 edges; its de Bruijn lift has 1444 vertices and 27436 edges. Every eligible cyclic 48-cell row corresponds to a closed walk in the lift. A graph potential identity proves universal zero functions; independent 1792 covariance rows prove completeness. No periodic centre, decimal Lychrel certificate, or orbit of 196 is claimed.
