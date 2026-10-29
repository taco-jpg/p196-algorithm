# AC07 TARGET (2026-10-29)

Canonical phase-0 p12/m9 B34,W9 (coefficients LSD-first; source data calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt). Fix U in {(9,12,6),(12,6,9),(6,9,12)}, q=14,k=100 and J=[5]. For all palindromic coefficient words C of length 7..14, midpoint even when odd, decide whether 120 G=(1000)^30 physical decimal reverse-add steps return the centre collar U^105 C reverse(U)^105 with *the same C*; every carry port and gamma bit must be physically correct. Scan all 7,8, more lengths if feasible. Centre-only equality does NOT assert W9 restoration or a certificate.

Additional full-template necessary lemma: for arbitrary palindromic C of ANY finite length and J of length <=3 with entries 0..18, test whether P=B W^14 J U^100 C reverse(U^100) reverse(J) reverse(W^14) reverse(B) can map to P'=B W^14 J U^105 C ... after 120 steps under the same clock. A sound outer-prefix abstraction that existentially quantifies *all* high-end carry inputs {0,1,2} can refute this family without searching C.

Missing lemma supplied: endpoint-only all-centre obstruction for the short stationary seams |J|<=3 at the reference width, not merely strict per-phase W9 preservation. It is a no-go for this restricted T* mechanism, NOT a decimal all-time certificate.
