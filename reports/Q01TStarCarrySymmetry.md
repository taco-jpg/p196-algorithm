# Q01: T* phase-specific carry symmetry

**PAPER PROOF.** The p12/m9 rooted W9/U3 family has a forced *complement-reflection* law in every long U3 bulk. This is an exact one-step normalization statement for all band widths and all 30 published charge-zero U3 rows; it does not rely on the p16 neutral-exterior census.

## Statement

For a coefficient (x\in\{0,\ldots,18\}), define the decimal carry map
\[
f_x(c)=\left\lfloor\frac{x+c}{10}\right\rfloor,\qquad c\in\{0,1\}.
\]
Thus (f_x) is the constant 0 map for (x\le8), the identity for (x=9), and the constant 1 map for (x\ge10). A T* bulk word (U) is a cyclic rotation of ((9,a,18-a)) for even (a\in\{0,2,\ldots,18\}). It therefore contains exactly one low coefficient \(\ell\le8\), one 9, and one high coefficient (h\ge10).

Let (\tau_U=f_{u_2}\circ f_{u_1}\circ f_{u_0}), with the composition read in LSD-first word order. Then (\tau_U) is a constant map. Reversing (U) swaps the order of \(\ell\) and (h), so
\[
\boxed{\tau_{\operatorname{rev}(U)}(c)=1-\tau_U(c)\quad\text{for every }c\in\{0,1\}.}
\]
The same maps hold for (U^k) and (\operatorname{rev}(U)^k) for every (k\ge1).

Define the steady carry paths (s_0,\ldots,s_3) and (r_0,\ldots,r_3) by starting each word at its fixed carry (respectively (s_0=s_3=\tau_U), (r_0=r_3=\tau_{\operatorname{rev}(U)})) and applying its three (f_x) maps. For every U3 row,
\[
\boxed{s_j+r_{3-j}=1\quad(j=0,1,2,3).}
\]
This is **complement-reflection, not equal-carry reflection**.

## Exact phase table

Here \(\ell\le8\) and (h\ge10), with \(\ell+h=18\). The six rows cover all rotations from both orientations of the published U3 family.

| U order | Steady carry cuts (s_0s_1s_2s_3) | Reverse order | Steady carry cuts (r_0r_1r_2r_3) |
|---|---|---|---|
| ((9,\ell,h)) | 1101 | ((h,\ell,9)) | 0100 |
| ((\ell,h,9)) | 1011 | ((9,h,\ell)) | 0010 |
| ((h,9,\ell)) | 0110 | ((\ell,9,h)) | 1001 |
| ((9,h,\ell)) | 0010 | ((\ell,h,9)) | 1011 |
| ((h,\ell,9)) | 0100 | ((9,\ell,h)) | 1101 |
| ((\ell,9,h)) | 1001 | ((h,9,\ell)) | 0110 |

The table is a six-case proof: a low coefficient resets carry to 0, a high coefficient resets it to 1, and a 9 preserves it. The last of the low/high coefficients therefore fixes the block output; reversal swaps which one occurs last. The listed steady cuts then satisfy (s_j=1-r_{3-j}) entry by entry.

## Consequence for a physical T* pairword

Take any canonical symmetric coefficient pairword
\[
P=H\,C\,\operatorname{rev}(H),\quad
H=B\,W^q\,J\,U^k,
\]
where (U) is any of the 30 T* rows, (C) is any legal palindromic centre, and (J,B,W) are arbitrary finite words with a legal positive leading coefficient. Carries are the *actual* low-to-high normalization carries of (P).

The first U copy can enter with an arbitrary carry from (J), but its outgoing carry is forced to \(\tau_U\). Likewise the first reverse-U copy can enter with an arbitrary carry from (C), but its outgoing carry is forced to \(1-\tau_U\). Hence every copy after those two finite boundary collars follows the steady paths (s) and (r). For every (k\ge3), every cut (i) in a lower U copy numbered (j=1,\ldots,k-2) from the outer end satisfies
\[
\boxed{c_i+c_{|P|-i}=1.}
\]
This is uniform in (q,k,J,C) and applies separately at every temporal phase because all 30 U rows are covered.

**Search consequence:** a T* checker must retain both physical carry ports. Any proposed invariant that identifies the two reflected interior carries as equal is impossible on the U3 bulk; the valid interior state is anti-diagonal. This is a local all-width obstruction only: asymmetric carry paths remain allowed, and no complete centre/seam return or decimal Lychrel number is proved.

## Independent ordinary-integer controls

Reproduce from the repository root:

`python3 calculation/new_structures/Q01/tstar_carry_symmetry.py`

The checker reads the published `lat_p12m9.txt`, constructs canonical integer sources with the actual phase-0 (B,W), (J=[5]), each U3 row, and centres (C=[12]) (odd length) and (C=[8,8]) (even length). For every (q,k\in\{20,40,80,160\}), it compares (N+\operatorname{rev}_{10}(N)) from ordinary Python big integers with full coefficient normalization, then checks every mirrored interior carry cut. The symbolic theorem, not the sample, establishes all widths. Execution: reproduced in an isolated local mirror with the published fixture; all 960 canonical integer sources and 280,320 mirrored-cut checks passed. These finite controls validate the implementation only; no 120-step survival or return is claimed.
