# Complete eight-phase four-cell physical covariance classification for rec2

**PAPER PROOF.** For decimal base 10, rec2 overflow g=10101010, spatial period 48 and all 4096 square-free Boolean monomials of four adjacent coefficient parities plus four ascending and four descending physical carries, the exact eight-phase covariance system has **rank 8192/32768** and **kernel dimension 24576**. Every kernel vector is a direct sum of eight independently chosen per-phase cyclic-zero functions (each dimension 3072); there are no nontrivial phase-coupled universal cyclic observables in this entire four-cell ansatz. This is NOT a periodic-centre existence/no-go theorem, a base-10 Lychrel certificate, or a result about 196.

## Exact covariance equations

For each physically admissible 48-cell cyclic pairword P, let F(P) be the 4096-bit vector of cyclic sums (mod 2) of all 12-bit four-cell Boolean monomials. Physical carries obey a_(j+1)=[P_j+a_j>=10], d_(j-1)=[P_j+d_j>=10]. The exact bulk pairword update is

    g=0: P'_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1));
    g=1: P'_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2)).

A phase-labelled coefficient vector c=(c_0,...,c_7), each c_t in GF(2)^4096, obeys universal cyclic covariance iff for every P and t,

    c_(t+1)·F(step_g(P)) = (2 if g=0 else 11)*c_t·F(P) (mod 2),
    g=1 for t even, g=0 for t odd.

The multiplier 2 vanishes modulo 2; 11 reduces to 1. This is a universal cyclic bulk statement, not a finite-centre or arbitrary independent carry assertion.

## Exact lower bound: 8×3072 per-phase local-zero functions

Four-cell physical carry enumeration gives 1312 allowed 12-bit patterns, 2784 forbidden patterns, and a connected 288-state nine-bit boundary graph with six self-loops. Pointwise-zero functions (dimension 2784), boundary gradients (287) and constant length-parity (1) span exactly the 3072-dimensional universal 48-cycle zero-function space. This decomposition is independently reproduced in this commit; the full finite-interval theorem is also in the prior result Agent3FourCellBoundaryTransport. Every per-phase cyclic-zero function evaluates to zero on all P, and therefore satisfies every eight-phase covariance equation. Hence the covariance kernel has dimension at least 8×3072=24576.

## Matching rank witness and complete exclusion of phase coupling

The primary and independent engines construct 1471 deterministic physical 48-cell cyclic words with Python Random(9397). Their 4096-feature vectors have exact GF(2) rank **1024** (first attained at sample 1471), so each phase's cyclic-zero kernel has dimension at most 4096-1024=3072. Next, 1628 deterministic physical 48-cell words (Random(9410)) are sent through each of the g=0 and g=1 physical bulk maps. Their image feature vectors independently attain **rank 1024** in both cases, first at sample **1025** for g=0 and **1628** for g=1.

For odd t, g=0, the covariance equation is c_(t+1)·F(step_0(P))=0. Since the g=0 image spans the entire 1024-dimensional physical cyclic-feature space, all four even-phase coefficients must be per-phase cyclic-zero functions. For even t, g=1, the source even-phase function is already zero; the equation becomes c_(t+1)·F(step_1(P))=0. The g=1 image also spans the entire physical cyclic-feature space, forcing all four odd-phase coefficients to be per-phase cyclic-zero functions. Thus EVERY covariance solution lies in the 8×3072 local-zero subspace. The kernel is exactly **24576** and the rank **32768-24576=8192**.

For an independent direct matrix control, both checkers also build all **8×1628=13024** explicit 32768-bit covariance rows and obtain exact GF(2) rank **8192**, using opposite pivot orders. The primary uses cyclic carry recurrences; the independent checker obtains carries from ordinary 384-column schoolbook integer reverse-and-add. For each g it creates a real positive 386-digit integer with outer pair coefficient 1 (forcing g=0) or 18 (forcing g=1), performs genuine digit normalization and extracts the 48-cell interior output. Both implementations generate all 3256 output coefficient words identically, with SHA-256 **11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9**. Both checkers assert the exact digest; agreement is not inferred merely from equal ranks.

## Rec2 controls, scope and reproduction

Included 48-cell W0 and eight 11-cell root prefixes are copied from the committed rec2 lattice. Both engines validate all eight g=10101010 phases; the independent checker builds eight genuine 406-digit positive decimal integers from prefix plus four bulk copies, checks actual overflow and interior output, and rejects deliberately incorrect overflow shifts.

The theorem rules out additional universal cyclic phase-coupled four-cell Boolean invariants, not spatially varying observables, five-cell or longer neighborhoods, or a periodic moving-centre kink. The already known per-phase boundary gradients still give finite-interval endpoint flux; their closure cannot decide centre existence without extra centre dynamics. No 196 conclusion.

Reproduce from repository root (Python standard library only):

    python3 calculation/decimal_frontier/lattice_kinks/agent3_fourcell_covariance/primary.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_fourcell_covariance/independent_check.py

Exact outputs, independent checker, compact data and controls are in calculation/decimal_frontier/lattice_kinks/agent3_fourcell_covariance/README.md. Local runs passed (<17 seconds, <125 MB each). Repository-wide tools/verify.py --changed was not run due blocked shell GitHub DNS / absent checkout. **PAPER PROOF**, not LEAN-VERIFIED.
