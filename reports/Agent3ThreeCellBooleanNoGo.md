# Complete three-cell Boolean parity/carry covariance classification on decimal rec2

**PAPER PROOF.** For base 10, overflow period 8 g=10101010, spatial period 48 rec2, and all 512 GF(2) Boolean monomials in nine adjacent physical coefficient-parity/carry bits, the eight-phase covariance kernel of universally zero functions has dimension **2304 of 4096**. The 2,252 reference/one-site/adjacent-pair perturbation tests have rank **814**, leaving a 3282-dimensional finite-test kernel and **978 independent false-positive dimensions**. A concrete degree-five monomial is zero on every reference test but fails on an explicitly given valid cyclic physical-carry word. This is not a finite-centre all-width no-go or a decimal Lychrel certificate.

## Exact model

For each 48-cell coefficient word P_j in {0,...,18}, excluding the all-nine word, unique cyclic ascending and descending carry streams satisfy a_(j+1)=[P_j+a_j>=10] and d_(j-1)=[P_j+d_j>=10]. At position j define nine bits in this order:

    (P_j mod2, P_(j+1) mod2, P_(j+2) mod2,
     a_j, a_(j+1), a_(j+2), d_j, d_(j+1), d_(j+2)).

All 512 square-free monomials indexed by subset mask 0..511 form a basis of the full Boolean function space on these bits. Sum each monomial over all 48 cyclic positions modulo 2. Eight temporal phases have independent 512-bit coefficient vectors (4096 total). The exact cyclic pair-word update is g=0: P'_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1)) and g=1: P'_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2)). Covariance requires C_(t+1)(F_(g_t)(P))=(11 if g_t=1 else 2) C_t(P) modulo 2. The independent checker instead uses ordinary decimal digit normalization and never imports the primary recurrence.

## Finite reference tests: exact rank 814

Enumerate the eight rec2 lattice rows W_t, all valid W_t +/- e_j, and all valid W_t +/- e_j +/- e_(j+1): exactly 2,252 tests. Exact 4096-bit GF(2) elimination produces rank **814**. The verifier deterministically selects and optionally exports 814 independent concrete tags (t,j,s,u). Their JSON encoding has SHA-256 bd95d2e5f2110458960aa3820ff2d4775abc711bc6f28a16c2c82ce8fbab3a29, independently recomputed in the same commit. This is a complete finite rank, not a statistical estimate.

## Universal graph-coboundary lower bound: 288 per phase

The physical carry graph has 76 vertices (p,a,d) and 1,444 edges (p,a,d)->(q,A,D) iff A=[p+a>=10] and d=[q+D>=10]. Form its second-order de Bruijn lift H: vertices are the 1,444 original directed edges, and directed edges are compatible consecutive original edges. H has exactly **27,436** directed edges. Each lifted edge is a valid three-cell local configuration and carries a 512-bit monomial vector f.

A deterministic sequence of 229 cyclic physical words (Python Random seed 9396, 48 coefficients uniform 0..18) has 512-feature rank **224**. Exact nullspace extraction gives **288 independent masks**. For each mask m, the verifier constructs a binary vertex potential phi on all 1,444 vertices of H and a constant kappa in {0,1} and checks, on every one of the 27,436 lifted edges,

    parity(m & f(edge)) = kappa XOR phi(source) XOR phi(target).

For any closed 48-edge walk, potentials telescope and 48*kappa=0 mod2. Thus each mask is an identically zero cyclic feature function on every eligible P, not merely the seeded words. The eight phase placements of 288 masks are independent, giving **2304** universal zero-function covariance coefficient vectors. The generated 876,744-byte graph certificate has SHA-256 56d0b9838a68df2e6729e06c4bccd2045511d2b04bfccd8145761a3bfbfce35f; the verifier reproduces the entire object, checks all 288 potentials and compares this digest to committed manifest data.

## Matching global upper bound: exact rank 1792

Using the first 229 deterministic physical cyclic words and all eight phases, the exact covariance rows have rank **1792** (1,792 selected independent rows among 1,832 tested). The independent tag list has SHA-256 dddc94e9f57d58a03fd69d0e8a437c65b0c4cf19af8fae25f39b49578d8996cc. Any universally zero covariance observable must satisfy these explicit finite equations, so its coefficient kernel has dimension at most 4096-1792=2304. Together with the 2304 graph-coboundary vectors this proves equality, and every universal solution is the zero function. The deterministic seeded rows are an exact finite rank witness; the conclusion does not rely on random extrapolation.

## Explicit physical false positive and exact scope

counterexample.json gives the single-monomial coefficient at temporal phase 0, nine-bit subset mask **345** (degree five, bits 0,3,4,6,8), and an explicit 48-cell P with valid unique cyclic carries. This monomial coordinate is zero on all 2,252 reference covariance rows, but the physical covariance equation at test phase 0 evaluates to **1**. Both checkers reproduce the counterexample by independent arithmetic. Consequently the finite rec2 reference tests alone cannot classify this full three-cell ansatz. The difference between the finite-test kernel dimension 3282 and universal dimension 2304 is exactly **978**.

Reproduce from repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_threecell_boolean/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_threecell_boolean/independent_check.py

Append --export to the primary verifier to materialize all three digest-checked exact certificates locally (each <5 MB). Everything needed, including raw lattice, source, independent checker, literal counterexample, digest manifest and controls, is committed under calculation. No degree beyond nine bits, longer neighborhood, nonuniform spatial weighting, centre existence, base-10 Lychrel number or claim about 196 is established. **PAPER PROOF**, not LEAN-VERIFIED.
