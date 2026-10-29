# AC20 working notes

- Claimed phase-11 endpoint-only J3/J4 in #476 after checking docs/CELL_LEDGER.md; AB20 was only 600 sampled cases.
- Phase11 rows are W11=(2,9,2,4,0,17,11,9,12), B11 starts (5,2,3,3,3,16,...). Do not mistake the intervening binary carry-port 9-vectors for W.
- Used exact schoolbook decimal pairword normalization; the 120-step full sweep imposes NO strict-phase W9 pruning. Exhaustive 8,230,800 candidates: no restored W9, clock-count errors 0, length errors 0.
- Bigint audit: 160 controls x120 actual integer steps across five widths; eight different centres x30 U x2 J =480 further actual-number tests gave the same earliest mismatch per fixed J/U.
- Phase11 carry-port bulk: 10 of each U cone pair (150,119), (149,120), (151,121); U returns after 120. W retreat=90, W insertion guard18, U minimum clean gap28.
- All-width and centre-independent implication invokes phase-rotated T12 paired-insertion/reset-cone proof; the finite replay alone does not quantify q,k,C.
