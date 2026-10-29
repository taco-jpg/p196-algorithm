# Four-cell perturbation span is necessary and sufficient to certify the complete six-bit local Boolean rec2 covariance ansatz

**PAPER PROOF.** For the decimal rec2 period-8 overflow 10101010, spatial period 48, the 64-feature GF(2) local Boolean covariance ansatz (eight independent temporal phases, 512 coefficient bits) needs at least one perturbation whose support is not contained in three consecutive coefficient cells to force the universal zero-function kernel. A finite test family with support in at most four consecutive cells suffices. This is a precise statement about +/-1 perturbations of the eight rec2 reference cyclic rows, not about finite centres or Lychrel existence.

## Model and universal upper bound

Use six bits at cyclic cell j: (P_j mod2,P_(j+1) mod2,a_j,d_j,a_(j+1),d_(j+1)), where a_(j+1)=[P_j+a_j>=10], d_(j-1)=[P_j+d_j>=10], and 0<=P_j<=18 with at least one P_j!=9. All 64 square-free Boolean monomials in these six bits are indexed by subset mask 0..63. The exact pair-word update is g=0: P'_j=2P_j+a_j+d_j-10(a_(j+1)+d_(j-1)), g=1: P'_j=P_j+P_(j-1)+a_j+d_(j-1)-10(a_(j+1)+d_(j-2)). The covariance is C_(t+1)(F_g(P))=(11 if g=1 else 2) C_t(P) modulo 2.

The committed graph_certificate.json independently verifies 14 linearly independent 64-bit carry-graph coboundaries on every one of 1,444 legal edges of the 76-state physical carry graph. Their eight temporal placements span 112 universal zero-function coefficient vectors. The preceding result Agent3FullBooleanLocalParity supplies 400 explicit unrestricted covariance rows, proving the universal kernel has dimension exactly 112, hence its maximal possible covariance rank is 400/512.

## Exhaustive finite perturbation hierarchy

Starting with the eight rec2 rows, every valid one-site +/-1 perturbation, and every valid adjacent two-site +/-1 perturbation gives 2,252 exact rows of rank 388. The committed rank_witness.json contains 388 independent tags.

Add every valid distance-two pair (sites j and j+2): 1,488 additional rows, rank 396. Then add every valid contiguous three-site perturbation (sites j,j+1,j+2, each +/-1): 2,928 additional rows, rank 398. These families exhaust all +/-1 modifications whose nonempty support is contained in three consecutive cyclic coefficient cells, so no such perturbation family can reach rank 400. Two nonuniversal covariance solutions necessarily survive.

Add every valid distance-three pair (sites j and j+3): 1,488 further rows, rank 400. The committed augmentation_tags.json lists the 12 extra rows selected deterministically as independent pivots: eight distance-two pairs, two contiguous triples, and two distance-three pairs. Combined with the 388 base tags, they are 400 independent covariance rows. Since the 112 universal identities provide the matching upper bound, these 400 tests force every allowed covariance observable to be the zero function on all eligible cyclic 48-cell coefficient words. The support of every added test fits in four consecutive cells. This proves sufficiency and, by the rank398 three-cell exhaustion, necessity of span four in the stated +/-1 perturbation class.

Separately, exhaustive enumeration of all 34,236 valid additional two-site +/-1 perturbations at every cyclic separation 2..24 (including redundant reversed pairs at separation 24) yields rank 398, not 400. Therefore no two-site +/-1 perturbation family, however widely separated, suffices without a three-site test. At separations 2 and 3 the rank gains are 8 and 2; separations 4..24 give no further gain. This is a complete finite census for these precisely defined perturbations, not an all-width centre no-go.

## Independent verification and limitations

From repository root:

    python3 calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/verify.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_perturbation_radius/independent_check.py

Both scripts recompute the 388/396/398/400 rank hierarchy. The independent checker implements ordinary cyclic decimal digit normalization rather than importing the primary pair-word update, and independently checks all two-site separations and all contiguous triples. Data and code are included in this one non-Lean commit, including the exact lattice, 14 graph potentials, and 400 independent witness tags. No statement about a finite-centre existence or nonexistence, any decimal Lychrel orbit, or the orbit of 196 is claimed. PAPER PROOF, not LEAN-VERIFIED.
