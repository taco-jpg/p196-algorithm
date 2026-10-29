# Z07 target: phase-0 rooted p12/m9, five-site junction, U-rotation slice 7/12

## Exact question

Use the canonical phase-0 rooted pair-coefficient template

P(q,k;J,U,C) = H ++ C ++ reverse(H),

H = B ++ W^q ++ J ++ U^k,

with B and W from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, |J|=5, every coefficient of J in 0..18, and exact 120-step overflow clock g=(100010001000)^10. Decide whether any assigned (J,U) preserves the required rooted B ++ W^q prefix after 120 genuine decimal reverse-and-add steps at the T12 reference width (q,k)=(14,100). A restored prefix is necessary for P(q,k) -> P(q,k+5), so any exact mismatch excludes the full return for that fixed seam.

The computational representative is the legal odd centre C=[0,0,0]. The all-centre lift is only through T12's published two-sided cut/insertion result: the W9 endpoint cut is outside both U/centre disturbance cones at k=100, and the fixed (J,C,U) all-width return reduces to the reference width (14,100). No odd-centre-only mod-11 pruning is used; even centres remain included by the centre-independence argument.

## Fixed U ordering

Order the 30 distinct cyclic rotations of (9,a,18-a) for even a=0,2,...,18 lexicographically by coefficient tuple, with the tuple in LSD-first order:

1. (0,9,18)
2. (0,18,9)
3. (2,9,16)
4. (2,16,9)
5. (4,9,14)
6. (4,14,9)
7. (6,9,12)
8. (6,12,9)
9. (8,9,10)
10. (8,10,9)
11. (9,0,18)
12. (9,2,16)
13. (9,4,14)
14. (9,6,12)
15. (9,8,10)
16. (9,10,8)
17. (9,12,6)
18. (9,14,4)
19. (9,16,2)
20. (9,18,0)
21. (10,8,9)
22. (10,9,8)
23. (12,6,9)
24. (12,9,6)
25. (14,4,9)
26. (14,9,4)
27. (16,2,9)
28. (16,9,2)
29. (18,0,9)
30. (18,9,0)

Slice 7 of 12 means ranks 7+12j in 1-based rank notation. This shard therefore has U-ranks 7 and 19: U=(6,9,12) and U=(9,16,2).

## Exhaustive domain and controls

There are 19^5 = 2,476,099 junction words per U and 4,952,198 (J,U) pairs in this shard. The C++ screen enumerates every base-19 code in [0,19^5) for each U with no junction pruning and performs all 120 exact pair-coefficient transitions on the full finite representative. It checks every overflow against the required clock and tests exact W9-prefix restoration. Because endpoint-only restoration can in principle recover from temporary damage, the strict-W9 MDD is not used as a pruning rule; this preserves completeness for the endpoint question.

Independent true-decimal controls use Python arbitrary-precision integers, a fresh-buffer decimal digit-array schoolbook adder, and the pair-coefficient recurrence, at (q,k)=(20,100),(40,160),(80,320),(160,640), for both U values and five fixed length-5 junctions. All 120 phases are cross-checked.

This target is only the assigned finite seam cell. It does not address longer/moving junctions, other phases, unassigned U rotations, or the global decimal Lychrel existence question.
