# Agent3Rec2PerturbationRadius: exact minimal local perturbation span

Python 3 standard library only. From repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/independent_check.py

This directory includes the exact rec2 lattice lat2.txt, all-Boolean 64-feature physical carry model, 14-mask/76-state graph certificate, the 388-tag reference rank certificate, and 12 new exact independent perturbation tags. All data files <5 MB; all checks use exact integer GF(2) elimination. verify.py recomputes the full 2,252 reference tests, all 34,236 additional two-site +/-1 perturbations at separations 2..24, all 2,928 valid contiguous three-site +/-1 perturbations, and all 1,444 graph edges. independent_check.py separately implements decimal digit normalization and independently recomputes all rank statements without importing the primary model.

Expected output:

    PASS: 2252 reference rank388; separation2 rank396; contiguous triples rank398; separation3 rank400
    PASS: all 34236 additional arbitrary two-site rows rank398 without triples
    PASS: 12 independent extra row tags, 2928 contiguous triple controls, 1444 graph edges
    PAPER PROOF: support in <=3 consecutive cells is insufficient; <=4 consecutive cells suffice
    INDEPENDENT PASS: physical digit normalization gives ranks 388,398,400 and all-pairs 398
    INDEPENDENT PASS: 12 exact augmented tags, complete 3-cell support and 34236 all-pair controls

The tested perturbations are +/-1 at each modified coefficient, with support size at most three. Reference tests have support in two adjacent cells; adding distance-two pairs and contiguous triples exhausts every support contained in a three-cell cyclic interval. This has rank 398/512, leaving two spurious local covariance solutions beyond the universal 112-dimensional zero-function kernel. Adding just distance-three pairs (support span four cells) gives rank 400/512, equal to the global upper bound proved by the 14 universal carry-graph identities. All arbitrary two-site perturbations alone reach only rank398, regardless of separation. This is a restricted finite-test classification, not a periodic centre or decimal Lychrel certificate.
