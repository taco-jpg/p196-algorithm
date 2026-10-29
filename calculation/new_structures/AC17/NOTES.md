# AC17 research log

- Registered CLAIM in issue #476, building on T12 all-width insertion (a), the even-centre correction (r), and the unsound strict-W9 endpoint pruner (t). Reviewed current cell ledger, T12, phase-8 lattice source, AB17 partial report and S08 physical controls.
- Pure 160-coefficient B8/W8 carry cone loses 92 coefficients in 120 phases and retains only 68: insufficient for the observed W9 interface faults around 135..149.
- Built the centre-adversarial exact 280-coefficient two-ended carry cone. Every high-side carry inlet lies in {0,1}; at coefficient 9 it persists, at every other coefficient it is reset. The exact safe prefix recurrence is L'=L-1-trailing9+gamma, accounting for gamma=1's high-digit offset.
- Complete unpruned search of 30 U ranks, 137,180 junctions each: 4,115,400 cases, no W9 returns, no unresolved cones, clock (1000)^30 throughout, minimum guaranteed final prefix 149. Both even and odd centres, and arbitrary centre lengths, are covered by the proof of centre independence.
- Independent Python bigint/schoolbook decimal replay: 40 trajectories at (q,k)=(14,100),(20,100),(40,160),(80,320),(160,640), 4,800 exact ordinary decimal transitions, all passed. No finite replay is promoted as a certificate.
- Phase-8 B/W cone loses 92 (not phase-0's 91), still leaving a 16-cell guard beyond W-cut cW=52. Rotated T12 paired-insertion proof with U-side 152/122 radius lifts fixed-J reference-width exclusion to q>=14,k>=100.
- The phase-8 short fixed seam cell is exhausted. Moving/growing J, q-changing returns, other phases and all-time decimal existence remain unresolved.
