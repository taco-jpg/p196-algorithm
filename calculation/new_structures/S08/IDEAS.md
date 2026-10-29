# S08 IDEAS: scoped negative result

Label: COMPUTED, with the exact scope below. No base-10 Lychrel existence claim is made.

For the fixed R18 phase-4 seam J24 and U=(18,0,9), every one of the 17 odd palindromic length-3 centres C=[a,b,a] satisfying the necessary odd-centre mod-11 condition 2a-b = 5 (mod 11) fails the two-epoch return. The affine run-length checker gives, for every independent q,k >= 512, a first full-template mismatch at 120 steps at 9q+35 (actual 9, expected 5) and at 240 steps at 9q+12 (actual 6, expected 5). The latter is 22 coefficients before the W9/J boundary x=34+9q.

The first second-epoch W-prefix fault is at state 136, phase 8, index 9q+33: actual 14, expected 15. At state 135, phase 7, the low coefficient and its upper mirror are both 17, with carry-ins 0 and 0, so normalization gives 7+7=14. The required phase-8 coefficient 15 needs upper carry-in 1 while the lower carry remains 0.

Redirect for S09/S14: changing only C cannot repair this seam; the junction/inner carry history must change so the upper mirrored W carry is 1 at phase 7. This does not exclude other J/U/phase/centre-length or moving-seam families.
