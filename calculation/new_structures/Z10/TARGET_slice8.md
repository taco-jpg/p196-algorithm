# Z10 target: phase-0 J5 slice 8/12

Exact target: rooted base-10 p12/m9 phase 0, pairword B34 ++ W9^q ++ J ++ U^k ++ C ++ reverse(U)^k ++ reverse(J) ++ reverse(W9)^q ++ reverse(B34), |J|=5, all J_i in 0..18. Test the uniform return P_120(q,k;J,U,C)=P(q,k+5;J,U,C) for all q>=14,k>=100.

Canonical lexicographic ordering of the 30 distinct charge-zero U3 rotations:
1 (0,9,18); 2 (0,18,9); 3 (2,9,16); 4 (2,16,9); 5 (4,9,14); 6 (4,14,9); 7 (6,9,12); 8 (6,12,9); 9 (8,9,10); 10 (8,10,9); 11 (9,0,18); 12 (9,2,16); 13 (9,4,14); 14 (9,6,12); 15 (9,8,10); 16 (9,10,8); 17 (9,12,6); 18 (9,14,4); 19 (9,16,2); 20 (9,18,0); 21 (10,8,9); 22 (10,9,8); 23 (12,6,9); 24 (12,9,6); 25 (14,4,9); 26 (14,9,4); 27 (16,2,9); 28 (16,9,2); 29 (18,0,9); 30 (18,9,0).

Slice 8/12 is one-based rank r congruent to 8 modulo 12, so ranks 8 and 20: U=(6,12,9),(9,18,0). Each U has 19^5=2,476,099 J words, combined domain 4,952,198. Reference (q,k)=(14,100), representative centre C=[2].

The existing T12Rooted120CutPumping theorem reduces a fixed-J/C/U uniform return to (14,100). Its reset-cone bounds leave 300-152-122=26 protected coefficients in U^100, so the tested B34 W9^14 prefix is independent of every admissible finite palindromic centre. This is a scoped fixed-seam exclusion, not a global Lychrel nonexistence proof.
