# Z08 target: phase-0 rooted p12/m9 growing-seam return

**Status:** PARTIAL overall; the odd-centre subcell for U ranks 8 and 20 is EXHAUSTED-NONE. Even centres and other U ranks remain open.

## Exact family

Take the canonical phase-0 rooted words `B` (length 34), `W` (length 9, sum 60), and overflow clock `g=(100010001000)^10` from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`. Coefficients are LSD-first in `[0,18]`. Let `U` be either rank 8 or rank 20 in the lexicographically sorted set of the 30 distinct rotations of `(9,a,18-a)`, for even `a=0,2,...,18`:

1. `(0,9,18)`
2. `(0,18,9)`
3. `(2,9,16)`
4. `(2,16,9)`
5. `(4,9,14)`
6. `(4,14,9)`
7. `(6,9,12)`
8. `(6,12,9)`  **U8**
9. `(8,9,10)`
10. `(8,10,9)`
11. `(9,0,18)`
12. `(9,2,16)`
13. `(9,4,14)`
14. `(9,6,12)`
15. `(9,8,10)`
16. `(9,10,8)`
17. `(9,12,6)`
18. `(9,14,4)`
19. `(9,16,2)`
20. `(9,18,0)` **U20**
21. `(10,8,9)`
22. `(10,9,8)`
23. `(12,6,9)`
24. `(12,9,6)`
25. `(14,4,9)`
26. `(14,9,4)`
27. `(16,2,9)`
28. `(16,9,2)`
29. `(18,0,9)`
30. `(18,9,0)`

For a finite initial junction `J0` of length 5, a three-coefficient packet `R`, and a fixed palindromic coefficient centre `C`, define

`H(q,m,k) = B ++ W^q ++ J0 ++ R^m ++ U^k`

`P(q,m,k) = H(q,m,k) ++ C ++ reverse(H(q,m,k))`.

The target transition is one exact 120-step ordinary decimal reverse-and-add macro

`P(q,m,k) -> P(q,m+1,k+4)`

for every independent `q >= q0`, `m >= m0`, `k >= k0`, with the same physical seam phase, both carry ports and all 30 overflow bits correct, a canonical positive decimal source, and a proved non-palindrome guard at every intermediate step. If an exact uniform edge is found, its iterates would grow the new `R` band and the existing `U` band indefinitely. A finite-width replay alone is not sufficient.

## Why this is a distinct neighboring route

The phase-0 fixed-seam cells `|J|=5..6` with centres through length 32 have broad existing claims. This target instead makes the seam a second growing band `R^m`; it is not a fixed-J epoch-map census. It builds on (a) T12 cut/insertion only where its protected-cut hypotheses are proved, (e) the epoch seam as a dynamical system, and (m) short-seam phase-0 exhaustion only as scope context. No p8 facts are transferred to the p12 clock.

## Exact necessary gates for this ansatz

The rooted clock has 30 overflows per 120 steps, so the pairword length increases by 30. Since `|R|=3`, `m -> m+1`, `k -> k+4`, and `q,C` are fixed, the template length change is

`2 * (|R| + 3*4) = 30`.

The digit-sum residue modulo 9 is invariant after 120 steps because `2^120 = 1 (mod 9)`. Since `sum(U)=27` and `sum(W)=60`, this requires `sum(R)=0 (mod 9)` for a repeated fixed packet. There are exactly 763 such packets among the `19^3 = 6859` words in `[0,18]^3`. The all-9 packet is a previously excluded neutral-band route; `R=U` is retained as a control but is degenerate because `R^m U^k=U^(m+k)`, reducing to the stationary-seam T* target. Thus the genuinely distinct packet candidates number at most 761 per U for even C.

For an odd-length palindromic `C` only, the parity-correct mod-11 gate additionally requires `A(U)=A(C)` and `2A(J_m)-A(C)=0` when `|J_m|` is odd, where `A(X)=sum_i (-1)^i X_i`. Since `|J0|=5` and `|R|=3`, `A(J_m)` alternates between `A(J0)` and `A(J0)-A(R)`, while `|J_m|` alternates parity. Requiring both parities of `m` forces `A(R)=A(U) (mod 11)` and `2A(J0)=A(U) (mod 11)`. This leaves 72 packets `R` for each of U8 and U20; after removing the degenerate `R=U` control, 71 distinct packets remain per U. **Do not apply these mod-11 conditions to even-length C**, where the folded pairword alternating sum vanishes identically.

These are necessary algebraic filters only. They do not establish a physical 120-step edge, a seam repair, or an all-time certificate.

## Scoped obstruction discovered (odd-length C only)

The growing-seam target is now being tested against a necessary local endpoint condition. For odd-length palindromic C, the mod-11 gates reduce the exact candidate set to R words that satisfy sum(R)=0 mod 9 and A(R)=A(U) mod 11, and junctions J0 satisfying 2A(J0)=A(U) mod 11. The exact 120-phase period-three bulk map further requires R to return to itself. Exhaustive enumeration gives seven such R cycles for U8 and eleven for U20, including the degenerate R=U control in each case; excluding R=U leaves six and ten packets.

The local window is W^12 ++ J0 ++ R^57 (108 W coefficients, all five J0 coefficients, and 171 R coefficients). The exact reset cones leave 17 W cells and 19 R cells as guards. The R-side boundary is 189 coefficients from the U seam when m=120, exceeding the 152-column cone. Hence for q>=14, m>=120, k>=100 the 120-step window map is independent of q,m,k,C and a true template return must restore this entire window. The exhaustive compiled scan checks every mod-11-admissible J0 for all 16 nondegenerate R cycles.

The scope does not include even-length C or the other ten U rotation ranks. The independent Python-bigint verifier checks the local transition against genuine decimal N+reverse(N) at q=20,40,80,160, with m=120 and k=100.
