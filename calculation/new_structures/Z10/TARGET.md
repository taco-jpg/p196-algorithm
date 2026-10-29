# Z10 target: rooted p12/m9 phase-0 J5 slice 10/12

**Target:** decide whether any fixed-seam member of the canonical rooted phase-0 family

P(q,k;J,U,C) = H ++ C ++ reverse(H), H = B34 ++ W9^q ++ J ++ U^k,

can satisfy the exact 120-step return P_120(q,k;J,U,C) = P(q,k+5;J,U,C) for every independent q >= 14, k >= 100, where J has length 5 and every coefficient lies in 0..18.

The fixed lexicographic ordering of the 30 distinct charge-zero rotations is:

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

Slice 10/12 means one-based ranks 10 and 22, hence U=(8,10,9) and U=(10,9,8). For each U, the full seam domain is all 19^5 = 2,476,099 words; combined domain is 4,952,198 (U,J) pairs.

The finite reference is (q,k)=(14,100). The scan uses representative centre C=[2], a valid palindromic coefficient centre with an even midpoint coefficient. This is enough for the outer-prefix test because the existing T12 reset-cone bounds put at most 152 changed coefficients from the junction and at most 122 from the centre into the U band in 120 steps. Since |U^100|=300, at least 300-152-122=26 coefficients separate those cones, so the post-step B34 W9^q prefix is independent of every admissible finite palindromic C.

The existing results/T12Rooted120CutPumping.md theorem states that, for each fixed J,C,U, a uniform return for all independent admissible widths holds iff the return holds at the single finite width (14,100). Therefore, if the exact reference scan finds a W9-prefix mismatch for every J, no fixed-J/C member in this U slice can be an all-width 120-step return. This target is only a scoped exclusion of fixed-seam T* certificates, not a global nonexistence theorem for decimal Lychrel numbers.
