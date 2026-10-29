# Q01: T* phase-specific carry symmetry

**PAPER PROOF.** The rooted p12/m9 W9/U3 family has a forced *complement-reflection* law in every long U3 bulk. This is an exact one-step normalization statement for all band widths and all 30 published charge-zero U3 rows; it does not rely on the p16 neutral-exterior census.

## Statement

For a coefficient x in {0,...,18}, define the decimal carry map

    f_x(c) = floor((x+c)/10),  c in {0,1}.

Thus f_x is the constant-0 map for x <= 8, the identity for x = 9, and the constant-1 map for x >= 10. A T* bulk word U is a cyclic rotation of (9,a,18-a) for even a in {0,2,...,18}. It therefore contains exactly one low coefficient l <= 8, one 9, and one high coefficient h >= 10, with l+h=18.

Let tau_U = f_(u2) o f_(u1) o f_(u0), with composition read in LSD-first word order. Then tau_U is constant. Reversing U swaps the order of l and h, so

    tau_rev(U)(c) = 1 - tau_U(c)     for every c in {0,1}.

The same maps hold for U^k and rev(U)^k for every k >= 1.

Define steady carry paths s0,...,s3 and r0,...,r3 by starting each word at its fixed carry (s0=s3=tau_U, r0=r3=tau_rev(U)) and applying its three carry maps. For every U3 row,

    s_j + r_(3-j) = 1     for j=0,1,2,3.

This is **complement-reflection, not equal-carry reflection**.

## Exact phase table

Here l <= 8 and h >= 10, with l+h=18. The six rows cover all rotations from both orientations of the published U3 family.

| U order | Steady carry cuts s0s1s2s3 | Reverse order | Steady carry cuts r0r1r2r3 |
|---|---|---|---|
| (9,l,h) | 1101 | (h,l,9) | 0100 |
| (l,h,9) | 1011 | (9,h,l) | 0010 |
| (h,9,l) | 0110 | (l,9,h) | 1001 |
| (9,h,l) | 0010 | (l,h,9) | 1011 |
| (h,l,9) | 0100 | (9,l,h) | 1101 |
| (l,9,h) | 1001 | (h,9,l) | 0110 |

The table is a six-case proof: a low coefficient resets carry to 0, a high coefficient resets it to 1, and a 9 preserves it. The last of the low/high coefficients therefore fixes the block output; reversal swaps which one occurs last. The listed steady cuts satisfy s_j = 1-r_(3-j) entry by entry.

## Consequence for a physical T* pairword

Take any canonical symmetric coefficient pairword P = H C rev(H), with H = B W^q J U^k, where U is any of the 30 T* rows, C is any legal palindromic centre, and J,B,W are arbitrary finite words with a legal positive leading coefficient. Carries are the actual low-to-high normalization carries of P.

The first U copy can enter with an arbitrary carry from J, but its outgoing carry is forced to tau_U. Likewise the first reverse-U copy can enter with an arbitrary carry from C, but its outgoing carry is forced to 1-tau_U. Hence every copy after those two finite boundary collars follows the steady paths s and r. For every k >= 3, every cut i in a lower U copy numbered j=1,...,k-2 from the outer end satisfies

    c_i + c_(|P|-i) = 1.

This is uniform in q,k,J,C and applies separately at every temporal phase because all 30 U rows are covered.

**Search consequence:** a T* checker must retain both physical carry ports. Any proposed invariant that identifies the two reflected interior carries as equal is impossible on the U3 bulk; the valid interior state is anti-diagonal. This is a local all-width obstruction only: asymmetric carry paths remain allowed, and no complete centre/seam return or decimal Lychrel number is proved.

## Independent ordinary-integer controls

Reproduce from the repository root by running python3 calculation/new_structures/Q01/tstar_carry_symmetry.py.

The checker reads the published lat_p12m9.txt, constructs canonical integer sources with the actual phase-0 B,W, J=[5], each U3 row, and centres C=[12] (odd length) and C=[8,8] (even length). For every q,k in {20,40,80,160}, it compares N+rev10(N) from ordinary Python big integers with full coefficient normalization, then checks every mirrored interior carry cut. The symbolic theorem, not the sample, establishes all widths.

**Executed control:** reproduced in an isolated local mirror with the published fixture; all 960 canonical integer sources and 280,320 mirrored-cut checks passed. These finite controls validate the implementation only; no 120-step survival or return is claimed.
