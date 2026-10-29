# Z11 adjacent target: phase-zero J5 slice 1/12

## Exact statement

Use the rooted p12/m9 decimal pairword with B34 = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5], W9 = [5,18,4,8,1,15,4,0,5], H(q,k;J,U)=B++W^q++J++U^k, and P=H++C++reverse(H). At q=14,k=100, exhaust every J in {0,...,18}^5 for U ranks 1,13,25 in the lexicographic ordering of all 30 distinct charge-zero rotations. Test the genuine 120-step endpoint, including the exact (1000)^30 overflow clock, for restoration of the entire W^14 band. The two-sided carry cone is centre-independent, so C is not enumerated; odd C must have an even midpoint coefficient.

## Ordering used

The 30 U words sorted lexicographically are listed in the parent TARGET.md. Slice 1 modulo 12 means ranks 1, 13, 25:

- rank 1: U=(0,9,18)
- rank 13: U=(9,4,14)
- rank 25: U=(14,4,9)

The route is disjoint from the completed phase-zero slices 3, 4, 7–12. It uses no strict-W9 MDD filter: all 19^5 junctions are evaluated for each U.

## All-width lift

The committed T12 rooted cut/insertion theorem reduces each fixed (J,U,C) return to (q,k)=(14,100) for all independent q>=14,k>=100. The W insertion shifts the first mismatch and W cut together; the U insertion is protected beyond the seam-side mismatch. This is a fixed-seam obstruction only, not a moving/growing seam result or a decimal Lychrel proof.
