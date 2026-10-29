# Complete five-cell physical-carry covariance classification

**PAPER PROOF.** In decimal rec2 (p=8, m=48, overflow `10101010`), the universal eight-phase GF(2) covariance system on all 32,768 square-free Boolean monomials of five consecutive coefficient parities, five ascending carries and five descending carries has exact rank **37,376/262,144** and kernel **224,768**. Every solution is a direct sum of per-phase pointwise-zero functions, endpoint gradients and length parity. This is NOT a moving-centre no-go or a decimal Lychrel certificate.

## Exact equations

For cyclic pairword coefficients P_j in 0..18 and *physical* correlated carries a_j,d_j,

    a_(j+1)=floor((P_j+a_j)/10), d_(j-1)=floor((P_j+d_j)/10).
    g=0: P'_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1)).
    g=1: P'_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2)).

Let F(P) be the 32,768-vector of cyclic mod-2 sums of every 15-bit square-free monomial. Phase coefficients c_t obey universal covariance precisely when for every physical cyclic P and t,

    c_(t+1)·F(step_g(P))=(2 if g=0 else 11)*c_t·F(P) (mod 2),
    g=1 for even t, g=0 for odd t.

## Complete one-phase kernel

The 76 physical one-column states (P,a,d) have exactly 1,444 directed edges (P,a,d)->(Q,A,D), where A=floor((P+a)/10) and d=floor((Q+D)/10). All **9,904,396** four-edge walks yield exactly **5,984** distinct admissible 15-bit five-cell masks. Their source/target four-cell masks form a connected 1,312-vertex directed de Bruijn graph with six self-loops. The independent checker instead enumerates 521,284 physical four-column assignments and glues two compatible four-cell masks, independently obtaining exactly the same 5,984 masks, vertices, connectivity and loops.

Of the 32,768 Boolean functions, **26,784** vanish pointwise on all admissible masks. Every function psi on the 1,312 boundary vertices induces a gradient f(u->v)=psi(u)+psi(v), which telescopes on cycles; connectedness gives gradient rank **1,311**. The constant-one edge function vanishes on 48-cycles because 48 is even; a self-loop proves it is independent of gradients. Thus at least **26,784+1,311+1=28,096** independent functions have zero sum on every physical 48-cycle. For a finite interval [L,R] their non-pointwise-zero contribution is exactly `psi(s_L)+psi(s_(R+1))+kappa*(R-L+1)` modulo 2.

Both standalone engines construct 56,576 deterministic physical 48-cycles from SplitMix64 seed `0x6a09e667f3bcc909` and obtain exact GF(2) rank **4,672** of the 5,984-bit cyclic mask histograms, first at sample **32,700**. Histogram-to-square-free-monomial transformation is the invertible Boolean zeta transform, so the monomial feature rank is also 4,672. Therefore the cyclic-zero dimension is at most 32,768-4,672=**28,096**, saturating the constructed lower bound and proving the complete one-phase classification.

## Eight-phase rank and physical arithmetic controls

Both engines obtain exact g=0 and g=1 output-image feature ranks **4,672**, first at sample **8,523** and **56,576** respectively. The primary applies the physical cyclic carry recurrence. The independent checker builds actual 386-digit positive decimal integers with forced overflow g=0 or g=1, performs ordinary schoolbook digit normalization, and extracts all 48 interior output coefficients. All **113,152** output words agree under FNV64 `567a7f76b4b8de3f`. Independent source features come from genuine 384-digit normalizations; the two rank engines use opposite pivot orders.

At odd phases g=0, covariance reads `c_(t+1)·F(step_0(P))=0`. Full image rank forces each even-phase coefficient into the 28,096-dimensional local-zero subspace. At even phases g=1, the source coefficient is already local-zero; full g=1 image rank forces every odd-phase coefficient into that subspace too. Conversely every independent choice of eight local-zero coefficients satisfies covariance. Hence the exact eight-phase kernel is **8×28,096=224,768**, rank **8×4,672=37,376** out of 262,144. No phase-coupled universal five-cell invariant survives.

The independent checker additionally normalizes eight genuine **406-digit** rec2 integers built from included eleven-cell prefixes and the 48-cell seed, checks all overflow bits and 96 interior coefficients per phase, and rejects deliberately wrong overflow shifts. The primary independently checks the rec2 eight-step cyclic return. This theorem excludes only this GF(2) ansatz, not spatially varying, longer-window or finite-centre invariants, and says nothing about 196.

## Reproduction (C++17 standard library only)

    c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance/primary.cpp -o /tmp/agent3_five_primary
    /tmp/agent3_five_primary calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance
    c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance/independent_check.cpp -o /tmp/agent3_five_independent
    /tmp/agent3_five_independent calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance

Both passed locally (<17 seconds and <14 MB RSS each). Full `tools/verify.py --changed` was unavailable because GitHub shell DNS prevents checkout; no Lean verification or repository-wide check is claimed.
