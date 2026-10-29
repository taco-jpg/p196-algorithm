# X05 exact target

## Current target statement

For the physically rooted phase-0 p12/m9 template from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, set

- B to the canonical 34-coefficient root,
- W to the canonical 9-coefficient band,
- U=(9,6,12),
- H(q,k;J)=B ++ W^q ++ J ++ U^k,
- P(q,k;J,C)=H ++ C ++ reverse(H).

The cell is q>=14, k>=100, every J in {0,...,18}^3 or {0,...,18}^4, and every canonical palindromic coefficient centre C of odd length 15,17,19,21,23, with coefficients in 0..18 and an even midpoint.

The exact desired return is P after 120 ordinary base-10 reverse-and-add steps equal to P(q,k+5;J,C), with the same q,J,C and the same rooted phase-0 exterior. The current search tests whether the necessary prefix B ++ W^q is restored. A failure of that prefix rules out the full return.

## Status

EXHAUSTED-NONE for this exact cell. The full J domain is enumerated at (q,k)=(14,100). T12's insertion theorem lifts the result to all q>=14,k>=100 for each fixed J,C; the U3 reset-cone gap proves the W9 endpoint is independent of the centre coefficients and odd centre length. No claim is made about other U words, even centres, longer J, other root phases, moving seams, or the decimal Lychrel existence problem globally.
