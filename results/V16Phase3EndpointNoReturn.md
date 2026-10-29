# V16 phase-3 |J|=3–4 endpoint W9 obstruction
**Label:** COMPUTED.
**Missing lemma supplied:** the phase-3 |J|=3–4 cell cannot satisfy the necessary one-epoch W9 endpoint restoration for any U3 word or centre, removing this entire cell from the epoch-map fixed-point search.
**Scope:** rooted p12/m9 phase 3; all 30 U3 words, every J over 0..18 of length 3 or 4, every canonical palindromic C of any finite length, all q>=14,k>=100.
**Claim:** no candidate restores the full B3 W3^q prefix after 120 exact decimal reverse-and-add steps; the phase-rotated T12 insertion/reset-cone lemma lifts the exhaustive (q,k)=(14,100) result to all widths.
**Finite domain:** 4,115,400 (U,J) states; zero endpoint restorations. C is eliminated by a sound U3 carry-reset cone, not sampled.
**Reproduce:** compile strict_w9_cell_local.cpp, then run --endpoint-only --phase 3 --q 14 --k 100 --steps 120 --collar 170; independent controls: verify_local.py.
**Code/data:** strict_w9_cell_local.cpp, verify_local.py, endpoint_w9_cell_summary.txt, CELL_REPORT.md.
**Redirect:** search other clock phases, |J|>=5, or U6 mixed bands.
**Not claimed:** no decimal Lychrel number is proved.
