# Z45 exact target

## Assigned family

Use the physically rooted phase-0 decimal p12/m9 template

- `B = B34` and `W = W9` from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, with `|B|=34`, `|W|=9`;
- a charge-zero three-coefficient word `U`, so `|U|=3` (the independent control uses the admissible rotation `(9,6,12)`);
- `H(q,k;J,U) = B ++ W^q ++ J ++ U^k`;
- `P(q,k;J,U,C) = H ++ C ++ reverse(H)`, with fixed canonical palindromic coefficient centre `C`.

Variant 4 is the literal growing seam `J' = w1 ++ J ++ w2`, with `|w1|=1`, `|w2|=2`, coefficient alphabet `0..18`, fixed W9 exponent `q`, fixed centre `C`, and target `k -> k+5`. The proposed `+22` is a coefficient-cut reindexing at the W9/J interface, not an integer change in the W9 exponent.

## Question

Can the epoch map reproduce the template while keeping the W9 count unchanged and absorbing the observed roughly 22-column W9-cut drift?

## Current disposition

No for this literal family: the exact global length ledger rules out every positive seam extension of total length 1, 2, or 3 when `q`, `C`, and `k -> k+5` are fixed. A coordinate reindexing cannot change physical word length. This does not rule out a different template family in which another physical component changes length.
