# V16 phase-3 cell report

**Status: EXHAUSTED-NONE** for the requested phase-3 rooted p12/m9 cell with |J|=3..4, all 30 charge-zero U3 words, and every canonical palindromic C of any finite length, under q>=14,k>=100. The requested centre range 2–13 is included. No fixed point or finite epoch cycle in this cell can exist, because no candidate satisfies the necessary one-epoch W9 endpoint restoration. This does not settle other phases or longer J.

## Exact endpoint result

The 120-step endpoint-only search enumerated all

30 * (19^3 + 19^4) = 4,115,400

(U,J) pairs at (q,k)=(14,100), using the exact rooted phase-3 clock gamma[(3+t) mod 12]. It did not reject a candidate when W9 was temporarily damaged; every candidate was evolved through all 120 steps and tested only for restoration of the complete B3 W3^14 prefix at step 120.

- Endpoint restorations: **0 / 4,115,400**.
- Same-cell seam/U-port candidates: **0**.
- Rooted-clock failures: **0**.
- Every candidate has an intermediate W9 mismatch, with first mismatch by step 53; none restores the W9 prefix at t=120. Exact histogram and range-coverage checks: endpoint_w9_cell_summary.txt.
- The strict-per-phase lane is also empty, but that is a weaker corollary and is not used to reject endpoint-only candidates.

## Centre independence and admissible domain

For the requested lengths 2–13, the canonical centre count is 546,254,940 (odd-length centres have an even midpoint coefficient), so the raw U x J x C Cartesian domain is 2,248,057,580,076,000. The result extends to every finite centre length because C was eliminated by a reset-cone argument, not by sampling or mod-11 pruning: every phase of every U3 row has a non-9 coefficient within at most three cells, so the upper carry entering the W9|J collar is reset before it can depend on C. The centre is at least 303 coefficients from the cut for k>=100, while the 120-step U-side cone advances at most 151 columns.

The local engine tracks 170 coefficients beyond the W9 cut. For phase 3 the exact 120-step cone losses are W=90 and U junction/centre pairs {(149,120),(150,119),(151,121)}. Thus the collar leaves 19 cells beyond the maximum U-junction cone; the T12 U insertion cut after 55 copies retains at least 14 reset-guard cells on each side, and the W insertion cut after two copies retains 18 cells at q=14. The phase-3 clock is a cyclic shift of the T12 clock; the phase-rotated reset-cone/insertion proof therefore makes the endpoint-W9 property invariant under every W or U insertion, extending the finite result to all q>=14,k>=100.

## Independent validation and reproduction

verify_local.py compares the local collar with full pairword transitions for 100 random J/U/C cases through all 120 steps, checks all 12 W9 row transitions and rooted overflow gates, verifies all 30 U3 rows return after 120 steps from all 12 clock phases, checks the phase-3 cone bounds, and independently checks true Python-bigint plus digit-array reverse-add at q/k=20,40,80,160 with both centre parities.

From repository root:

    python3 calculation/new_structures/V16/verify_local.py
    g++ -O3 -std=c++17 -o /tmp/v16-w9 calculation/new_structures/V16/strict_w9_cell_local.cpp
    /tmp/v16-w9 --endpoint-only --phase 3 --q 14 --k 100 --steps 120 --collar 170

The committed summary was aggregated from 42 contiguous chunks and checked for gaps/overlaps. A single full-domain run is reproduced by the command above; it prints the same candidate count, endpoint count, and first-mismatch histogram. No MDD or mod-11 pruning is used. The result excludes the whole requested cell by a necessary endpoint condition; it is not a base-10 Lychrel existence proof.
