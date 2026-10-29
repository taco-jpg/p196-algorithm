# X24 running notes

- Read the mission and the current #475/#474 coordination history. Phase-0 |J|=3..4 is held by several overlapping broad claims, so registered the neighboring phase-1 cell instead. Claim comment: #6491766836.
- Reused the published T12 exact pairword/carry-reset semantics and phase-rotated insertion theorem; retained even centres (odd-centre mod-11 filters are not applied to even C).
- Local C++ search uses exact two-ended carry/overflow transitions on the W9|J collar; `k=100` gives 300 U coefficients, beyond the 170-column collar. The U3 phase-1 cone bound is left <=152 and right <=122; collar 170 leaves a guard.
- Independent U3 controls: full pairword carry engine, fresh-buffer digit-array reverse-add, Python arbitrary-precision integer reverse-add, and local-collar prefix all agree for 120 steps at q=20,40,80,160 with k=100,160,320,640 and both centre parities represented. All 30 U3 rows return after 120 steps under the phase-1 clock.
- U3 exhaustive run covers `[0,4,115,400)` in 42 contiguous chunks with no gaps or overlaps: 4,115,400 tested, zero clock failures, zero root-B mismatches, 4,115,400 W9 endpoint failures, and zero endpoint restorations. The phase-1 U3 endpoint graph is empty, so the SCC bound is vacuous.
- Follow-on claim #6492724994: phase-1 U6 row `(17,14,17,1,4,1)`, `|J|=3..4`, 240 steps, target `k->k+10`, reference `(q,k)=(24,100)`. Exact cone `(299,239)`, W9 loss 181, insertion guards W=17 and U6=31.
- U6 sweep complete: 14 chunks cover `[0,137180)` without gaps/overlaps; 137,180 tested, zero clock failures, zero root-B mismatches, zero W9 restorations. Bigint/digit-array/pairword controls pass at q=40,80,160, and W/U insertion identities pass through 240 steps.
- Next target after this cell: a distinct U6 orbit/phase or unresolved moving/growing seam; do not repeat either exhausted cell.
