# Z10 target: phase-0 J5 slice 11/12

**Exact target:** rooted base-10 p12/m9, phase 0, pairword
P(q,k;J,U,C) = B34 ++ W9^q ++ J ++ U^k ++ C ++ reverse(U)^k ++ reverse(J) ++ reverse(W9)^q ++ reverse(B34),
with |J|=5, each J_i in {0,...,18}, and a charge-zero U3 rotation. Decide whether any fixed J,C,U in this slice has the required uniform 120-step return P_120(q,k;J,U,C)=P(q,k+5;J,U,C) for all independent q>=14,k>=100.

The canonical lexicographic ordering of the 30 distinct charge-zero rotations is:
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

Slice is defined by one-based rank r congruent to 11 modulo 12. It therefore contains ranks 11 and 23, U=(9,0,18) and U=(12,6,9). Each U has 19^5=2,476,099 junction words; combined domain is 4,952,198 cases.

Reference width: (q,k)=(14,100), with representative centre C=[2]. The existing T12Rooted120CutPumping theorem states that for fixed J,C,U, a uniform return over all admissible widths is equivalent to a return at (14,100). Its reset-cone bounds allow at most 152 coefficients of U^100 to be affected from the J side and 122 from the centre side in 120 steps. As U^100 has 300 coefficients, at least 26 coefficients remain between these cones, so the tested outer B34 W9^14 prefix is independent of every admissible finite palindromic C.

The result excludes only this fixed-seam U slice. It is not a global nonexistence proof for decimal Lychrel numbers.
