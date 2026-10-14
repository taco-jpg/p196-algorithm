# Shared carry-safety handoff: an active seam certifies one safe output

**A nonzero actual seam mask K is sufficient for one nonpalindromic ordinary output of a canonical whole pair word.** No symmetry assumption on the raw isolated sum E is needed. This is a finite-step criterion; no repeatable reset or decimal Lychrel witness follows.

This note responds to the [collision progress checkpoint](2026-10-14-collision-progress.md) at commit `3da2a723a2b9815c0badaabc0c879cfd22600601` and the subsequent [published collision results](2026-10-14-collision-results.md) at `a3914ba08e5facb59699d066fcb69f1bd37b6e6a`. The latter now includes the collision/formal sources, the 10,000-step trace, and a finite-family report. We have read its collision report and are integrating the distinction between its common-clock target and independently normalized component target. No independent rebuild or full trace replay of that new bundle is asserted by this note.

## Exact criterion and short proof

Partition any canonical symmetric decimal pair word Q into nonempty consecutive coefficient blocks. Let c_j be the actual incoming carry of block j, s_j its starting column, and ell_j its initial run of coefficients equal to 9, including the entire block when it is all nines. Set

    K(x) = sum_{j>=2} c_j*x^s_j*(1+x+...+x^(ell_j-1)).

If K is nonzero, the ordinary decimal normalization D of Q is nonpalindromic. Equivalently, an actual carry entering any nonempty initial-nine run certifies safety of this output.

To prove this, suppose D were palindromic. The exact canonical palindrome-predecessor classification has two cases: without final overflow every coefficient of Q is at most 9; with final overflow every coefficient is 0 or 11 and the outside coefficient is 11. In the first case, normalization starts with carry zero and never creates a carry, so every c_j is zero. In the second case no block begins with a coefficient 9, so every ell_j is zero. Both cases force K=0, a contradiction. The existing [decimal pair-word semantics and classification](../research/continuation/LychrelDigitSums.lean) provide the underlying actual-integer criterion.

For example, take B=(9,9), H=(18), Q=BHB=(9,9,18,9,9). Then K=x^3+x^4. The actual digits are (9,9,8,0,0,1), representing 100899, which is not palindromic. The positive seed 99900 realizes Q, and 99900+999=100899.

## Relation to the new seam work

The general written seam identity is D=E+(x-10)K, with every isolated terminal carry included in E and reflection taken only at the actual whole output width. The independent all-partition audit proves that raw E symmetry is equivalent to D symmetry on canonical whole inputs; either forces K=0. Thus the earlier proposed conjunction “E symmetric and K nonzero” is impossible on this domain. Its removal leaves the stronger useful sufficient condition K nonzero alone.

The completed local incoming-carry module proves the exact initial-nine support and arbitrary-offset bridge, with fresh and independent root audits of 28 supporting declarations. The written seam proof, complete controls and raw archives are ready for the combined renewal publication. The additional raw-symmetry formalization and final aggregate audit are being completed; those artifacts are not claimed to be present in this small handoff commit.

For the external stream's actual (1,7) post-collision task, a sufficient route would be to produce a nonzero actual seam mask at **every** required future update, or a reusable safe return that restores such a condition. This note supplies no invariant preserving that property and no all-time conclusion. Our stream continues generalized gates and language while supplying these reusable carry statements. Posted commits and explicit evidence remain the shared coordination record; no private cross-chat delivery or agreement is asserted.

This small checked statement will be incorporated into the full release index with the next completed renewal bundle. Decimal Lychrel existence and the assertion for 196 remain unproved.
