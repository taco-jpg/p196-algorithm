### Seam defect sets D_R(V) (letters that can precede a maximal band V^inf)
| V | word | D_1 (rigid2/cadical) | D_12 rigid2/cadical195 | D_12 indep enc2/cadical195 | D_12 rigid2/kissat404 |
|---|------|------|------|------|------|
| U0 | (9, 0, 18) | empty | empty | empty | empty |
| U1 | (0, 18, 9) | empty | empty | empty | empty |
| U2 | (18, 9, 0) | {5, 14} | empty | empty | empty |
| U3 | (9, 2, 16) | empty | empty | empty | empty |
| U4 | (2, 16, 9) | empty | empty | empty | empty |
| U5 | (16, 9, 2) | {6, 7, 15, 16} | empty | empty | empty |
| U6 | (9, 4, 14) | {15, 16} | empty | empty | empty |
| U7 | (4, 14, 9) | empty | empty | empty | empty |
| U8 | (14, 9, 4) | {7, 8} | empty | empty | empty |
| U9 | (9, 6, 12) | empty | empty | empty | empty |
| U10 | (6, 12, 9) | empty | empty | empty | empty |
| U11 | (12, 9, 6) | empty | empty | empty | empty |
| U12 | (9, 8, 10) | empty | empty | empty | empty |
| U13 | (8, 10, 9) | empty | empty | empty | empty |
| U14 | (10, 9, 8) | {17} | empty | empty | empty |
| U15 | (9, 10, 8) | empty | empty | empty | empty |
| U16 | (10, 8, 9) | empty | empty | empty | empty |
| U17 | (8, 9, 10) | {1} | empty | empty | empty |
| U18 | (9, 12, 6) | empty | empty | empty | empty |
| U19 | (12, 6, 9) | empty | empty | empty | empty |
| U20 | (6, 9, 12) | empty | empty | empty | empty |
| U21 | (9, 14, 4) | {2, 3} | empty | empty | empty |
| U22 | (14, 4, 9) | empty | empty | empty | empty |
| U23 | (4, 9, 14) | {10, 11} | empty | empty | empty |
| U24 | (9, 16, 2) | empty | empty | empty | empty |
| U25 | (16, 2, 9) | empty | empty | empty | empty |
| U26 | (2, 9, 16) | {2, 3, 11, 12} | empty | empty | empty |
| U27 | (9, 18, 0) | empty | empty | empty | empty |
| U28 | (18, 0, 9) | empty | empty | empty | empty |
| U29 | (0, 9, 18) | {4, 13} | empty | empty | empty |

D_12 solve times 20-106 s over 90 runs.

### Centre comoving defect sets E_R(V) (letters that can follow a maximal band, comoving return)
| V | word | E_4 (rigid2/cadical) | R used | E_R rigid2/cadical195 | E_R indep enc2/cadical195 | E_R rigid2/kissat404 |
|---|------|------|---|------|------|------|
| U0 | (9, 0, 18) | empty | 4 | empty | empty | empty |
| U1 | (0, 18, 9) | empty | 4 | empty | empty | empty |
| U2 | (18, 9, 0) | empty | 4 | empty | empty | empty |
| U3 | (9, 2, 16) | empty | 4 | empty | empty | empty |
| U4 | (2, 16, 9) | empty | 4 | empty | empty | empty |
| U5 | (16, 9, 2) | {3, 12} | 6 | empty | empty | empty |
| U6 | (9, 4, 14) | empty | 4 | empty | empty | empty |
| U7 | (4, 14, 9) | empty | 4 | empty | empty | empty |
| U8 | (14, 9, 4) | {2, 11} | 6 | empty | empty | empty |
| U9 | (9, 6, 12) | empty | 4 | empty | empty | empty |
| U10 | (6, 12, 9) | empty | 4 | empty | empty | empty |
| U11 | (12, 9, 6) | empty | 4 | empty | empty | empty |
| U12 | (9, 8, 10) | empty | 4 | empty | empty | empty |
| U13 | (8, 10, 9) | empty | 4 | empty | empty | empty |
| U14 | (10, 9, 8) | empty | 4 | empty | empty | empty |
| U15 | (9, 10, 8) | empty | 4 | empty | empty | empty |
| U16 | (10, 8, 9) | empty | 4 | empty | empty | empty |
| U17 | (8, 9, 10) | empty | 4 | empty | empty | empty |
| U18 | (9, 12, 6) | empty | 4 | empty | empty | empty |
| U19 | (12, 6, 9) | empty | 4 | empty | empty | empty |
| U20 | (6, 9, 12) | empty | 4 | empty | empty | empty |
| U21 | (9, 14, 4) | empty | 4 | empty | empty | empty |
| U22 | (14, 4, 9) | empty | 4 | empty | empty | empty |
| U23 | (4, 9, 14) | {7, 16} | 6 | empty | empty | empty |
| U24 | (9, 16, 2) | empty | 4 | empty | empty | empty |
| U25 | (16, 2, 9) | empty | 4 | empty | empty | empty |
| U26 | (2, 9, 16) | {6, 15} | 6 | empty | empty | empty |
| U27 | (9, 18, 0) | empty | 4 | empty | empty | empty |
| U28 | (18, 0, 9) | empty | 4 | empty | empty | empty |
| U29 | (0, 9, 18) | empty | 4 | empty | empty | empty |

Also E_8 (rigid2/cadical): U5 empty, U8 empty, U23 empty, U26 empty.

### Task 1: seam SAT (seamsat.py), all 30 U
| length | UNSAT | SAT | other/missing | solve time min-max (s) |
|---|---|---|---|---|
| 10 | 30 | 0 | 0 | 171-2791 |
| 11 | 30 | 0 | 0 | 123-916 |
| 12 | 30 | 0 | 0 | 206-1365 |
max RSS 8.5 GB

### Task 2: centre SAT (satc.py), all 30 U
| length | UNSAT | SAT | other/missing | solve time min-max (s) |
|---|---|---|---|---|
| 13 | 30 | 0 | 0 | 68-149 |
| 14 | 30 | 0 | 0 | 61-160 |
| 15 | 30 | 0 | 0 | 72-224 |
max RSS 7.2 GB
