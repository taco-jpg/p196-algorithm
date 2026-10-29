# W42 cell report

**Status: EXHAUSTED-NONE for this exact cell. Label: COMPUTED.** This is a scoped obstruction, not a proof that a decimal Lychrel number exists or does not exist.

**Missing lemma supplied:** no phase-0 rooted p12/m9 template with U=(10,8,9), odd palindromic C of length 3, 5, 7, 9, 11, or 13, and |J|=3 or 4 can preserve the required B34 W9^q prefix through 120 ordinary reverse-and-add steps for any independent q,k >= 512.

**REDIRECT:** This closes only the U=(10,8,9), odd-centre, |J|=3–4 phase-0 shard; continue with other unclaimed U/parity cells.

## Exact scope and result

Use the canonical phase-0 B (34 coefficients), W (9 coefficients), and overflow clock g=(100010001000)^10 from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt. The template is P=H ++ C ++ reverse(H), H=B ++ W^q ++ J ++ U^k, with U=(10,8,9). The seam J has length 3 or 4 and coefficients in 0..18. C is a coefficient palindrome of odd length 3..13, with an even midpoint coefficient.

For every admissible J and every allowed odd C, the exact 120-step image disagrees with the required B34 W9^q prefix. The first mismatch is at coefficient index 9q+r, where r belongs to {9,10,11,12,13,14,15,16,18,19}. Equivalently, relative to the W9|J cut at 34+9q, the first-mismatch offsets are -25,-24,-23,-22,-21,-20,-19,-18,-16,-15. Therefore the required endpoint P(q,k+5) is impossible in this cell; no epoch-map fixed point or cycle can start here.

## Complete search-space accounting

Let A(X)=sum_i (-1)^i X_i, with coefficients listed least-significant first. For odd palindromic C, the parity-correct mod-11 gates are A(U)=A(C) mod 11 and 2A(J)+(-1)^|J| A(C)=0 mod 11. Here A(U)=10-8+9=11=0 mod 11, so A(C)=0 and A(J)=0 are necessary. No odd-centre branch was pruned by the even-centre identity.

Raw seam words:
- Length 3: 19^3 = 6,859.
- Length 4: 19^4 = 130,321.
- Total raw J words: 137,180.
- J words satisfying A(J)=0 mod 11: 623 at length 3 and 11,859 at length 4, total 12,482.

Raw realizable odd palindromic centres use 19 choices at each non-middle mirrored pair and 10 even choices for the midpoint. The exact raw and A(C)=0 counts are:

| Length | Raw C words | C words with A(C)=0 mod 11 |
|---:|---:|---:|
| 3 | 190 | 18 |
| 5 | 3,610 | 327 |
| 7 | 68,590 | 6,239 |
| 9 | 1,303,210 | 118,465 |
| 11 | 24,760,990 | 2,251,022 |
| 13 | 470,458,810 | 42,768,923 |
| Total | 496,595,400 | 45,144,994 |

Thus the raw J-by-C space has 68,122,956,972,000 tuples, and the odd-centre mod-11 gates leave 563,499,815,108 tuples. R02's MDD was not used as a pruning source: direct enumeration of all 12,482 gate-admissible J words is tractable, so this result does not depend on the MDD's completeness or soundness.

The search does not enumerate those centre values individually: it uses the exact carry-reset quotient below, reducing the complete cell to the 12,482 admissible J words.

## Why one centre representative suffices

The exact 120-phase symbolic trace has two U-dependent run atoms at every phase, each with count k+c_t and -228 <= c_t <= 0. For k>=512, at least 284 copies remain in each run throughout the trace. The phase words encountered are exactly the 30 charge-zero complement-nine U3 words; each has a coefficient different from 9 in position 0 or 1. Under decimal normalization, a coefficient below 9 maps both incoming carries to 0, and a coefficient above 9 maps both incoming carries to 1. Thus the incoming carry from C is reset within at most two coefficients of the reflected U run before it can reach the W9 boundary. The W9-prefix image is independent of C values and of its odd length. This agrees with the independently reported R09 emitter gate in issue #474, comment 6489204502.

Accordingly, it is complete to run the symbolic 120-step endpoint check on the representative C=(0,0,0) for each J satisfying A(J)=0. The symbolic engine uses independent affine parameters q and k with q,k>=512; it does not infer all-width behavior from samples.

## Symbolic result

The C++ affine-run checker is a standalone port of the R30 symbolic pairword algorithm. It was run over all 12,482 admissible J words in six reproducible chunks. All 12,482 cases completed, with zero symbolic errors, zero overflow-clock failures, and zero cases whose first mismatch was at or beyond the W9|J cut.

| Offset from cut | Number of J words |
|---:|---:|
| -25 | 150 |
| -24 | 317 |
| -23 | 5,807 |
| -22 | 4,945 |
| -21 | 580 |
| -20 | 576 |
| -19 | 37 |
| -18 | 48 |
| -16 | 13 |
| -15 | 9 |
| Total | 12,482 |

The first-mismatch histogram matches the independent true-decimal exhaustive controls exactly.

## Independent validation

- A separate C++ digit-vector schoolbook implementation replayed all 12,482 admissible J words at each of q=k=20, 40, 80, and 160. All four widths had zero W9-prefix passes, zero clock failures, and the same mismatch histogram.
- A separate Python unbounded-integer implementation exhaustively replayed all 12,482 J words at q=k=20. It reproduced the same histogram and zero prefix passes.
- The Python unbounded-integer implementation also ran 192 controls: four representative J words, all six odd centre lengths, two centre representatives per length (all-zero and nonzero, both with A(C)=0), and q=k in {20,40,80,160}. Every control retained the exact 30-overflow clock and reproduced its J-specific mismatch offset.
- The original Python R30-style symbolic checker was cross-checked on one example from each of the ten mismatch-offset classes. All ten affine first-mismatch expressions matched the computed histogram classes.

## Limits

This result covers only phase 0, U=(10,8,9), odd centres of lengths 3..13, seam lengths 3 and 4, and independent q,k>=512. It does not classify even centres, other U words, longer seams, moving seams, or other phases. It is not Lean-verified and makes no global no-Lychrel claim.
