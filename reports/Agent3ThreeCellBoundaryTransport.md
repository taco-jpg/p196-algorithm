# Complete finite-interval transport of three-cell Boolean carry coboundaries

**PAPER PROOF.** In base 10, the 288-dimensional space of nine-bit Boolean three-cell observables whose sum vanishes on every physical 48-cell cyclic pairword is exactly the direct sum of **224 pointwise-zero functions, 63 six-bit boundary-potential gradients, and one interval-length-parity function**. Thus the finite-interval quotient has dimension exactly 64. On the rec2 p8/m48 lattice all 64 endpoint signatures occur. This is a classification of this restricted observable family, NOT an all-width centre exclusion, decimal certificate, or result about 196.

## Model and exact finite-interval identity

Let P_j be pairword coefficients in {0,...,18}, with physically correlated ascending/descending carries a_(j+1)=[P_j+a_j>=10], d_(j-1)=[P_j+d_j>=10]. Exclude the all-nine cyclic word (nonunique cyclic carries). Define the nine bits x_j=(P_j mod2,P_(j+1) mod2,P_(j+2) mod2,a_j,a_(j+1),a_(j+2),d_j,d_(j+1),d_(j+2)), and the six-bit boundary state s_j=(P_j mod2,P_(j+1) mod2,a_j,a_(j+1),d_j,d_(j+1)). The 512 square-free Boolean monomials form a basis of all nine-bit functions.

For EVERY universal cyclic-zero function f there are a bit kappa and a six-bit function psi such that, on every physically admissible triple,

    f(x_j) = kappa + psi(s_j) + psi(s_(j+1))  (mod 2).

For ANY finite interval [L,R] of physical coefficients, even without cyclic closure,

    sum_(j=L)^R f(x_j) = kappa*(R-L+1) + psi(s_L) + psi(s_(R+1))  (mod 2).

This is an exact physical-carry endpoint flux, not an assumption of independent carries. Psi is unique up to an additive constant after restricting f to admissible patterns; changing f on forbidden patterns has no physical effect.

## Complete classification by finite exact witnesses

For p,q,r in {0,...,18} and independent bits a,F, physical consistency forces A=[p+a>=10], B=[q+A>=10], D=[r+F>=10], d=[q+D>=10]. Exhaustively enumerate 19^3*4=27,436 triples. Their nine-bit projections comprise exactly 288 distinct allowed patterns and 224 forbidden patterns. Their source/target six-bit boundary states form a 64-vertex, 288-edge directed quotient graph, with all 64 states present, a connected underlying undirected graph, and exactly six self-loops. Both independent implementations enumerate and check these finite facts.

Invertible Boolean Möbius inversion implies that functions supported on the 224 forbidden patterns give 224 independent pointwise-zero masks. For any function psi on the 64 boundary states, the gradient psi(source)+psi(target) telescopes. Connectedness gives gradient rank 63 (only constant psi is killed); a self-loop proves the constant-one edge function is independent of all gradients. On 48-cycles the constant contributes 48=0 mod2. Hence there are 224+63+1=288 independent universal zero-sum masks.

Conversely, the primary checker constructs 229 deterministic length-48 physical cyclic words using Python Random(9396). Their 512-dimensional monomial-sum vectors have exact GF(2) rank **224**, so the universal zero-function space has dimension at most 512-224=288. The 288 independent constructed masks saturate this upper bound. This proves COMPLETE classification. The independent checker reproduces rank 224 using genuine 384-digit ordinary integer reverse-and-add carries and the opposite Gaussian pivot order, without importing the primary recurrence.

The new content beyond the previously established 288-mask cyclic classification is the sharp 224+63+1 decomposition and complete 64-dimensional finite-interval boundary transport. In particular the 224 local-zero dimensions cannot create any hidden finite-interval centre flux. This does NOT address nonlinear observables involving more than three cells, spatially nonuniform masks, or exact centre transfer.

## Rec2 phase and moving-centre return

The accompanying compact data are the 48-cell initial rec2 bulk row W0 and eight 11-cell root prefixes. The primary checker regenerates all eight phases and their exact eight-step return with g=10101010. The independent checker instead builds genuine 406-digit positive decimal integers with half-pairword prefix_t+W_t repeated four times, performs ordinary digit-by-digit reverse-and-add, and checks each actual overflow bit, 96 interior output pairword coefficients per phase (768 total), and a deliberately wrong-overflow negative control.

The numbers of distinct six-bit endpoint states per phase are **35,29,27,35,35,29,27,35**. Their union is all **64** possible states. All 48 cuts, eight phases and eleven interval lengths 1,2,3,4,7,11,24,47,48,49,96 satisfy the endpoint formula for all 63 indicator gradients and the constant. The 192-step rec2 time return has 96 overflows, growing the half-length by 48 paired cells; both the spatial residue modulo 48 and interval-length parity return. Therefore, IF a finite moving centre has a physical six-bit endpoint return after 192k steps, every one of the 288 universal three-cell flux identities closes automatically. This does not construct a returned centre or exclude any centre width.

Reproduce from repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_boundary_transport/primary.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_boundary_transport/independent_check.py

See calculation/decimal_frontier/lattice_kinks/agent3_boundary_transport/README.md for exact outputs, data and controls. Both local checkers passed in <2 seconds and <100 MB RSS each. The GitHub shell DNS is blocked, so repository-wide tools/verify.py --changed was NOT run. **PAPER PROOF**, not LEAN-VERIFIED.
