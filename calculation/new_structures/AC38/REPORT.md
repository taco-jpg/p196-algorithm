# AC38 phase-5 exterior audit

**COMPUTED**, exact carry-set overapproximation with independent integer controls. **No decimal Lychrel certificate or complete J6 exclusion.**

## Quantified necessary guard

For the published B5 (34 coefficients), W5 (9 coefficients), (q,k)=(14,100), |J|=6 and centre length 2 or 3, set ALL 2*(6+3k)+|C| unknown inner coefficients independently to {0,...,18}. This is a superset of all J/U/C choices, including nonphysical ones. Under 120 exact two-ended decimal carry-set steps, every phase's length/overflow bit is forced, giving the clock (0001)^30, and the endpoint's first 115 coefficient sets are singleton and equal to the original exterior B5 W5^14. In particular P120[8]=B5[8]=11. The formerly asserted phase-5 index-8 mismatch is false, and must not be used to reject endpoint-only candidates.

A carry-set step independently unions the possible normalized digits and carries, then unions the sums of mirrored digit sets. By induction this encloses each genuine trajectory, even where correlations are lost; a singleton output is exact. The result covers **all interior assignments at these fixed structural lengths**, not a sample. Symbolic rechecks at q/k=20/80,40/160,80/320,160/640, for both centre lengths, force prefixes of 169,349,709,1429 respectively, each 45 sites before the W9 cut. These are separately checked finite widths; no all-q pumping theorem is claimed.

## Honest endpoint-only partial cell

J=(0,j1,j2,0,0,0), j1,j2 in 0..18, all 30 charge-zero U3 rotations, both fixed centres [4,4]/[4,14,4]: 361*30*2=**21,660 distinct cases** at q14/k100, 120 physical decimal coefficient-carry steps each, no intermediate W9 pruning. All had exact +30 length and (0001)^30 clock; no identical-template return and no complete B5 W5^14 endpoint restoration. The first mismatch is at coefficient 134 in 8,430 cases and 135 in 13,230. **Status PARTIAL(21,660/2,822,752,860)** for all 30 U and these two fixed centres only. Arbitrary centres and remaining J are not excluded.

An independent canonical-source Python arbitrary-precision n+reverse(n) oracle agrees with a separate schoolbook pairword engine at each of 120 actual steps on 50 controls across q/k=14/100,20/80,40/160,80/320,160/640, with even and odd palindromic centres. It independently confirms P120[8]=11 and boundary mismatches at W9 cut-26 or cut-25.

Commands from repository root:

    python3 calculation/new_structures/AC38/guard.py --q 14 --k 100 --centre-len 2
    g++ -O3 -std=c++17 calculation/new_structures/AC38/scan.cpp -o /tmp/ac38scan
    /tmp/ac38scan calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt 0 361
    python3 calculation/new_structures/AC38/oracle.py calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt

**Proof-function sentence:** this supplies an exact, all-interiors, 120-step rooted exterior constraint while removing an unsound early-index exclusion, so the remaining search can target the true W9/J repair boundary. It does not supply a stationary seam fixed point or an all-time proof.
