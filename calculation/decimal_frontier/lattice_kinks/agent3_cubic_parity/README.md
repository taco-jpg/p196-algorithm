# Agent3CubicParityNoGo: self-contained cubic GF(2) classification

All code/data are in this directory; Python 3 standard library only. From repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/generate.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/independent_check.py

generate.py independently regenerates and compares two small committed certificates, without modifying them (use --write to regenerate): rank_witness.json gives 232 concrete rec2 reference/one-site/adjacent-pair perturbation tags (t,j,s,u); graph_certificate.json gives 13 independent GF(2) coefficient masks, a binary potential on 76 directed carry states for each mask, and a constant bit kappa. lat2.txt is the exact 1,952-byte decimal rec2 lattice snapshot. Every file is <5 MB.

Expected output:

    PASS: regenerated 13 coboundaries, 76-state graph, 232 independent rec2 tags
    PASS: 76-vertex/1444-edge exact cyclic carry graph; 13 independent coboundaries
    PASS: 232 independent rec2 witness rows; all 2252 covariance rows rank 232 of 336
    PASS: 104 independent universal zero functions = complete 104-dimensional kernel
    CONTROL: 10,000 random cyclic words, 8,000 covariance checks
    PAPER PROOF: degree<=3 cyclic local GF(2) observables are universally zero
    INDEPENDENT PASS: 232/2252 digit-normalized covariance rank, 13 independent graph identities
    INDEPENDENT PASS: all 1444 directed carry edges and 10,000 random digit-normalization controls

The verify.py graph certificate checks every one of 1,444 local edges and both rank bounds, making the all-eligible-cyclic-row conclusion a finite proof rather than a sample extrapolation. independent_check.py uses ordinary decimal digit normalization rather than the pair-word bulk recurrence, independently recomputes the rank and graph identities, and checks the carry-run control. This is not an all-width centre exclusion, a decimal Lychrel certificate, or a Lean proof. The covariance condition is exactly the mod-2 reduction of the base-10 charge multiplier: C_(t+1)(F_g(P))=(11 if g=1 else 2)*C_t(P).
