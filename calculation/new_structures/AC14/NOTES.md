# AC14 notes
- Registered phase-5 CLAIM in issue #476, building on (a) T12, (r) parity correction, (t) endpoint healing.
- BREAK: earlier AB26/AB38 coefficient-7/8 failures contradict valid root; first 70 coefficients are unchanged at q=14 after 120 steps.
- Carry-aware suffix-inlet absorption removes only output digits that depend on unknown deeper carry; no strict-phase W9 pruning.
- Reproduced 20,000 randomized one-step cases, 20 120-step Python-bigint vs independent schoolbook digit-array controls at q=14,20,40,80,160, and 11 centre lengths for one J/U.
- All 4,115,400 J/U cases have W9 endpoint mismatches in [134,151], independent of arbitrary palindromic C and k>=48.
