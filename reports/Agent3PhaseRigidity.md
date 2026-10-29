# Exact all-width two-phase rec2 intermediate rigidity

**PAPER PROOF (finite-state certificate).** This proves an unbounded-spatial-width necessary condition on the physical g=1 then g=0 rec2 exterior. It is not an exclusion of any finite centre width or a base-10 Lychrel certificate.

## Physical transfer, not independent formal carries

For base-10 cyclic pairword coefficients P_j in 0..18, a physical state is s_j=(P_j,a_j,d_j) with ascending and descending schoolbook carries a_j,d_j in {0,1}. The exact edge relation s_(j-1)=(p,a,d) -> s_j=(q,A,D) is A=floor((p+a)/10) and d=floor((q+D)/10). It has 76 states and 1444 edges. The two ordinary-digit output functions, calculated as sums of literal digit residues, are

    f0(q,A,D) = ((q+A) mod 10) + ((q+D) mod 10)
    f1((p,a,d),(q,A,D)) = ((q+A) mod 10) + ((p+d) mod 10).

Let X be the source, Y=F1(X) the intermediate, and Z=F0(Y) the target. At each spatial column j, the product-graph vertex is (j mod 48, s_j, t_j), where s_j is the physical state of X, t_j that of Y, and f0(t_j)=Z_j. A product edge to column j+1 exists precisely when both s_j->s_(j+1) and t_j->t_(j+1) are physical edges and t_(j+1).P=f1(s_j,s_(j+1)). This is **exactly** the two-step schoolbook arithmetic, including correlated carries. No independent-carry relaxation is used.

## Finite graph proof for every spatial period

The eight rec2 phase rows W_t and the eight 11-cell physical rooted prefixes are pinned in controls.txt. For t=0,2,4,6, use target Z=W_(t+2) with phase indices modulo 8. Exhaustive graph construction and strongly connected decomposition give:

| first phase t | graph vertices | graph edges | cyclic SCCs | vertices in sole cyclic SCC | distinct intermediate physical states at each spatial position |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 14,592 | 14,360 | 1 | 282 | 1 |
| 2 | 15,276 | 16,190 | 1 | 310 | 1 |
| 4 | 14,592 | 14,360 | 1 | 282 | 1 |
| 6 | 15,276 | 16,190 | 1 | 310 | 1 |

The sole cyclic SCC's singleton projected t_j is exactly the state (W_(t+1)[j], a_(t+1)[j], d_(t+1)[j]) of the genuine rec2 intermediate, verified independently at every j=0..47. Any cyclic physical source of spatial period 48k, **arbitrary k>=1**, induces a closed walk of length 48k in this finite phase-expanded graph. Every vertex of a closed walk belongs to a cyclic SCC; the unique SCC has the singleton t_j projection. Therefore the intermediate Y must be W_(t+1)^k, with exactly its physical carry states. This proof is **not** extrapolation from bounded k or a finite-horizon orbit.

More generally, any finite path in the fixed-target product graph whose two endpoints lie in the sole recurrent SCC cannot leave that SCC: leaving and returning would place every visited vertex in the same SCC. Hence, when a two-phase source and target are eventually exactly the rec2 bulk at both spatial tails and the entire target is the fixed rec2 row, the intermediate cannot contain a finite defect. This is a precise obstruction to a two-step *hidden intermediate* bulk repair. It does **not** forbid a centre defect in the final target, a moving seam, a longer regenerative clock, or a spatial path with non-recurrent boundary ports.

## Reproduction and independent controls

Run from repository root:

    sh calculation/decimal_frontier/lattice_kinks/agent3_phase_rigidity/run_checks.sh

The C++17 primary enumerates all 76 physical states, 1444 edges, constructs each exact product graph, performs iterative Kosaraju SCC, verifies the unique cyclic SCC and singleton 48-position intermediate projection, and checks the rec2 eight-phase cyclic return. The independent Python checker uses a separately constructed 76x76 physical graph, literal decimal digit residues, a separate Kosaraju implementation, and the same exact graph counts. It validates all eight rooted 406-/407-digit rec2 ordinary reverse-add controls, then **400 randomized 406->407->407-digit genuine two-step schoolbook calculations** with modified bulk words, confirming the phase-coupled equations independently. All controls passed locally. Standard-library Python and C++17 only; compact input data controls.txt is included in the same commit.

**Exact limitation:** This theorem constrains the *intermediate physical exterior* conditional on an exactly restored two-step exterior. It neither proves that any decimal centre returns nor excludes every possible centre; the missing lemma is a **nonconsuming, carry-closed, positive-growth centre seam through the 192-step rooted clock**. The source preimage is not unique. No Lean verification or tools/verify.py --changed success is claimed because the local GitHub shell checkout/toolchain is unavailable.
