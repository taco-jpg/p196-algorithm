# Complete six-bit local Boolean parity/carry covariance classification on decimal rec2

**PAPER PROOF.** For base 10, temporal overflow 10101010 (p=8), spatial rec2 period 48, and the entire 64-dimensional space of GF(2) functions of the six adjacent coefficient-parity/physical-carry bits, the 2,252 rec2 reference and one-/adjacent-two-site perturbation tests have a 124-dimensional covariance kernel. Exactly 112 dimensions represent universally zero cyclic functions; the other **12 dimensions are false positives** that satisfy every reference test but fail on valid physical cyclic coefficient words. This is a complete restricted-ansatz classification, not an all-width centre exclusion or decimal Lychrel certificate.

## Exact local model

Let P be a 48-cell cyclic coefficient word with 0<=P_j<=18 and at least one P_j != 9. Its unique cyclic ascending/descending carry streams obey a_(j+1)=[P_j+a_j>=10], d_(j-1)=[P_j+d_j>=10]. The cyclic bulk pair-word update is g=0: P'_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1)), g=1: P'_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2)). The independent checker reconstructs the same update by ordinary decimal digit normalization, not by copying these equations.

For each j let B_j=(P_j mod2, P_(j+1) mod2, a_j,d_j,a_(j+1),d_(j+1)). The 64 basis monomials are the square-free products indexed by all six-bit subset masks m=0..63. For each phase t mod8 independently choose 64 coefficients and define C_t(P)=sum_j f_t(B_j) mod2, where f_t is an arbitrary Boolean function (the monomials form a basis). Thus there are 512 coefficient bits. Covariance is C_(t+1)(F_(g_t)(P))=(11 if g_t=1 else 2) C_t(P) mod2. The reference test family is exactly eight W_t, all valid W_t +/- e_j, and all valid W_t +/- e_j +/- e_(j+1): 2,252 rows.

## Exhaustive local rank: 388 of 512

The committed rank_witness.json contains 388 explicit reference perturbation tags (t,j,s,u). Exact GF(2) elimination gives rank **388** on these and on the full 2,252 tests. Consequently the reference covariance kernel has dimension 512-388=124. This is an exact finite result, not a random rank estimate.

## Universal zero-function classification: exactly 112 dimensions

Use the 76 vertices (p,a,d) with p=0..18 and a,d in {0,1}. An edge (p,a,d)->(q,A,D) is legal iff A=[p+a>=10] and d=[q+D>=10]. There are exactly **1,444** directed edges, all independently enumerated. Every eligible 48-cell P with physical carries is a closed 48-edge walk. The committed graph_certificate.json contains 14 independent 64-bit masks m and for each a binary vertex potential phi and constant kappa such that on every one of the 1,444 edges,

    parity(m & monomials(edge)) = kappa XOR phi(source) XOR phi(target).

Summing over a closed 48-edge walk telescopes the potentials, and 48*kappa is even. Thus all 14 masks give identically zero functions for every eligible cyclic word. Their eight phase placements yield **112 independent universally zero covariance coefficient vectors**.

For the matching upper bound, global_witness.json lists 400 independently generated unrestricted covariance rows from 100 deterministic valid cyclic 48-cell words (PRNG seed 4196, phases 0..7), with exact GF(2) rank **400**. Any universally zero covariance function must satisfy these 400 equations, so the universal kernel has dimension at most 512-400=112. Therefore the 112 graph-coboundary vectors span the entire universal zero-function kernel. This proves completeness, rather than inferring it from a finite random sample. The deterministic words are exact witness data; the PRNG is only a convenient compact representation of 100 explicit finite witnesses.

## Twelve exact false positives to the rec2-local test family

Since the reference kernel is dimension 124 and the universal zero-function kernel dimension 112, the quotient has dimension **12**. The committed counterexamples.json contains 12 explicit 512-bit coefficient vectors. Each passes all 2,252 reference tests exactly. It also contains 12 explicit valid 48-cell cyclic coefficient words with phases; the 12x12 GF(2) matrix of violations has rank 12. Thus these are 12 independent nonuniversal covariance survivors, spanning the entire quotient modulo the 112 universal identities. The independent checker normalizes all counterexample digits from scratch and reproduces this rank and the graph proof. A finite-reference fit is therefore **not** an all-row invariant in this complete six-bit Boolean ansatz.

## Reproduction and limitations

From repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/generate.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/independent_check.py

All code, raw lattice, four small certificates, independent digit-normalization checker, exact commands and controls are in the same commit. verify.py also checks 10,000 random physical cyclic words. No local finite-centre nonexistence, boundary-flux obstruction, degree beyond six in a larger neighborhood, spatially nonuniform charge, actual infinite decimal reverse-and-add orbit, or result about 196 is claimed. This is **PAPER PROOF**, not LEAN-VERIFIED.
