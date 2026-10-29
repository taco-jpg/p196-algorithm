# Z08 dead ends / constraints (local only)

## Fixed one-symbol seam growth is impossible under the stated length law

For a rooted phase-0 p12/m9 template with q and C fixed, a 120-step epoch has exactly 30 decimal overflows, hence pairword length gain 30. If a seam transition changes its length by `d` and changes the U exponent by `e`, then `d + 3e = 15`. Therefore `d` must be divisible by 3. In particular a proposed `+1` or `+2` coefficient seam growth cannot close in one 120-step epoch while q and C stay fixed. This is only a necessary condition, not a no-go for moving seams with changes in multiples of 3.

## Fixed three-symbol packet filter

For the candidate `J_m=J0 R^m`, `|J0|=5`, `|R|=3`, `m -> m+1`, q and C fixed, the length equation gives `k -> k+4`. Mod-9 charge requires `sum(R)=0 mod 9` (763/6859 packets). Odd-C mod-11 additionally requires `A(R)=A(U) mod 11` (72/6859 packets for each assigned U). These filters do not test carries or prove a transition. Do not publish them as a certificate.

## Odd-centre growing seam obstruction for U ranks 8 and 20

For the ansatz `B W^q J0 R^m U^k C reverse(...)` with `|J0|=5`, `|R|=3`, and macro `(m,k)->(m+1,k+4)`, the exact length and mod-9 gates force `sum(R)=0 mod 9`; odd C additionally forces `A(C)=A(U)`, `A(R)=A(U) (mod 11)`, and `2A(J0)=A(U) (mod 11)`. The 120-step bulk map leaves only 6 nondegenerate R cycles for U8=(6,12,9) and 10 for U20=(9,18,0). The guarded 284-coefficient local window `W^12 J0 R^57` was exhaustively tested for all 3,601,622 admissible `(U,R,J0)` combinations and no endpoint restoration was found. The reset-cone argument makes this an all-width obstruction for this odd-centre subcell, not a finite-width extrapolation. Even C and other U ranks remain open.

**Redirect:** do not spend further search on odd-centre fixed-packet growth `J0 R^m` at U ranks 8 or 20; move to even C or other U ranks / different growing-seam mechanisms.
