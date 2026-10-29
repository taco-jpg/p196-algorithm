# Cubic local parity/carry observables are universally zero on decimal rec2 cyclic bulk

**PAPER PROOF.** This extends the 22-feature degree<=2 classification of Agent3QuadraticParityNoGo to the entire 42-feature degree<=3 square-free local GF(2) basis, with all eight temporal phases independently weighted. Every coefficient vector satisfying the stated rec2 covariance tests represents the zero function on every eligible cyclic pair word, not merely on the tested 2,252 rows. No all-width finite-centre exclusion or decimal Lychrel certificate is implied.

## Model and exact scope

Base 10, spatial period 48, overflow word g=10101010, eight temporal phases t mod 8. For any 48-cell coefficient word P_j in {0,...,18} with at least one P_j != 9, the unique cyclic ascending and descending carry bits satisfy

    a_(j+1) = [P_j+a_j >= 10],       d_(j-1) = [P_j+d_j >= 10].

The cyclic bulk map is

    g=0: P'_j = 2P_j+a_j+d_j-10(a_(j+1)+d_(j-1)),
    g=1: P'_j = P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2)).

At each cell let x=P_j mod2, y=P_(j+1) mod2, a=a_j, d=d_j, A=a_(j+1), D=d_(j+1). Take all 42 square-free Boolean monomials of degrees 0, 1, 2 and 3 in (x,y,a,d,A,D) in lexicographic combination order, sum each monomial over all 48 cells modulo 2, and weight by an arbitrary independent 42-bit vector at each of eight phases: 336 coefficient bits. The covariance equation is C_(t+1)(F_(g_t)(P)) = (11 if g_t=1 else 2) C_t(P) (mod 2). The tested family is precisely the eight rec2 reference rows, all valid W_t +/- e_j, and all valid adjacent W_t +/- e_j +/- e_(j+1), 2,252 cases. The theorem applies to every coefficient vector satisfying these tests, not to arbitrary degree>=4 or longer-range features.

## 13 universal zero-function masks via a 76-vertex graph

Define graph vertices (p,a,d) with 0<=p<=18, a,d in {0,1} (76 vertices). A directed edge from u=(p,a,d) to v=(q,A,D) is legal exactly when A=[p+a>=10] and d=[q+D>=10]. There are exactly 1,444 edges. Every eligible cyclic 48-cell coefficient word with its physical unique carry streams traces a closed walk on this graph. The edge has six bits (p mod2,q mod2,a,d,A,D) and corresponding 42-bit monomial vector f(u,v).

The committed graph_certificate.json lists 13 independent 42-bit masks m, and for each a 76-bit potential phi and constant kappa in {0,1}. verify.py and the independent digit-normalization checker verify, for every edge,

    parity(m & f(u,v)) = kappa XOR phi(u) XOR phi(v).

On a closed 48-edge walk, potentials telescope and the constant contributes 48*kappa=0 (mod2). Thus each mask represents an identically zero cyclic feature function for every eligible P, with no sampling assumption. The 13 masks are linearly independent (exact GF(2) rank 13). Eight independent temporal placements give 104 independent coefficient vectors of universal zero functions. The masks include the previous degree<=2 identities but add four independent degree-3 directions per phase.

## Exact finite-rank upper bound, hence completeness

rank_witness.json contains 232 distinct tags (t,j,s,u) selected deterministically from the 2,252 rec2 tests. Recomputing the exact pair-word and carry transitions gives 232 linearly independent 336-bit covariance rows. The independent checker instead normalizes decimal digits in both directions and obtains the same rank, and verifies the full 2,252-row rank is exactly 232. Therefore the covariance kernel has dimension at most 336-232=104. Since the 104 universally vanishing vectors above lie in it, the kernel is exactly their span. Every solution is the zero function on all eligible cyclic words. This is a complete algebraic proof for the stated 42-feature ansatz, not an extrapolation from finite samples.

## Reproduction and limitations

From repository root run, in order:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/generate.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_cubic_parity/independent_check.py

The primary verifier additionally tests 10,000 random 48-cell cyclic words and 8,000 covariance equations; the independent checker performs 10,000 separate digit-normalization/carry-run controls. These random tests are supplementary; the 232-row rank certificate and 1,444-edge coboundary certificate are exhaustive and sufficient. No arbitrary finite centre, boundary source, nonlocal charge, degree>=4 polynomial, nonlinear centre transfer, actual integer orbit or base-10 Lychrel number is decided. This is PAPER PROOF, not LEAN-VERIFIED.
