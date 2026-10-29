# Z11 target and fixed ordering

## Exact statement under test

For the rooted decimal p12/m9 lattice in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, use

- B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5];
- W = [5,18,4,8,1,15,4,0,5];
- H(q,k;J,U) = B ++ W^q ++ J ++ U^k and P = H ++ C ++ reverse(H).

The route is phase zero, |J|=5, q=14, k=100, with every J in {0,...,18}^5. The exact claim being tested is whether the 120-step genuine decimal reverse-and-add map can restore the entire rooted W^14 band for the same fixed J,U,C, with the required (1000)^30 overflow clock and endpoint H(14,105;J,U). The endpoint mismatch search is centre-independent: the two-sided carry cone computes an exact known prefix without enumerating C.

## Fixed U ordering and assigned slice

My ordering is the 30 distinct charge-zero cyclic rotations, sorted lexicographically as integer triples. One-based ranks are:

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

Slice 11 modulo 12 consists of ranks 11 and 23: U=(9,0,18) and U=(12,6,9). These are disjoint from the reported rank-3/15/27 census.

## Reduction and scope

The committed T12 rooted cut/insertion theorem says that for fixed J,C,U, the all-width 120-step return question for independent q>=14,k>=100 reduces exactly to (q,k)=(14,100), with the protected W insertion shifting the mismatch and W cut together. This computation uses no strict-W9 MDD pruning: every one of the 19^5=2,476,099 J words is evaluated, so no temporary-W9-damage assumption is made. The conclusion is only about fixed seams in these two U rows; it does not rule out moving/growing seams or prove a decimal Lychrel number.


## Adjacent follow-on target

The next route is phase-zero slice 1/12: U ranks 1, 13, and 25, namely (0,9,18), (9,4,14), and (14,4,9), again exhausting all 19^5 length-five J words at (q,k)=(14,100). Its exact statement and ordering subset are in slice01/TARGET.md; its complete census is in slice01/REPORT.md.


## Adjacent follow-on target: slice 2/12

Phase-zero J5 slice 2/12 uses lexicographic U ranks 2, 14, and 26: (0,18,9), (9,6,12), and (14,9,4), exhausting every 19^5 J word per U at (q,k)=(14,100). The scoped report and reproduction files are under slice02/.


## Adjacent follow-on target: slice 5/12

Phase-zero J5 slice 5/12 uses lexicographic U ranks 5, 17, and 29: (4,9,14), (9,12,6), and (18,0,9), exhausting every 19^5 J word per U at (q,k)=(14,100). Its scoped report and reproduction files are under slice05/.
