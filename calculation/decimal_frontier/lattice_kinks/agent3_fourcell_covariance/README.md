# Agent3FourCellPhaseCovariance: exact reproduction

From repository root (Python 3.10+ standard library only):

    python3 calculation/decimal_frontier/lattice_kinks/agent3_fourcell_covariance/primary.py
    python3 calculation/decimal_frontier/lattice_kinks/agent3_fourcell_covariance/independent_check.py

Primary: 1312 allowed four-cell patterns / 288 connected nine-bit endpoints, per-phase zero kernel3072; 1471 seed9397 physical 48-cycles rank1024; 1628 seed9410 physical output words each for g0 and g1 rank1024, first full at samples1025 and1628; all 13024 eight-phase covariance rows have exact rank8192/32768. The exact 3256 output words have SHA256 11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9.

Independent: no import from primary. Builds the physical 76-state/1444-edge carry graph, independently obtains 1312 four-cell patterns; uses ordinary schoolbook 384-column reverse-and-add to extract cyclic bulk carries and a genuine 386-digit positive integer with prefix coefficient 1 (g0) or 18 (g1) to normalize every tested output. Independently asserts both image ranks, the full eight-phase rank and the exact 3256-word digest with opposite GF2 pivot order. Eight genuine 406-digit rec2 prefix+bulk controls validate actual overflow and a wrong-overflow negative control.

Compact rec2_w0.txt and rec2_prefix.txt are exact initial 48-cell row and eight 11-cell outer prefixes of the repository rec2 lat2.txt. No download, solver, Lean or external package needed. Every source/data file <5 MB.

Expected primary output:

    PASS: 1312 allowed 4-cell patterns, 288 connected endpoints; per-phase zero kernel 3072
    PASS: 1471 physical 48-cycles rank1024/4096 (seed9397)
    PASS: g=0 image rank1024 at sample1025; g=1 image rank1024 at sample1628 (seed9410)
    PASS: 3256 exact output words SHA256 11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9
    PASS: direct 8-phase 32768-feature covariance rank8192 from 8*1628 exact rows
    PAPER PROOF: all 24576 universal 8-phase covariance solutions are independent per-phase local-zero functions
    PASS: rec2 g=10101010 eight-phase physical cyclic bulk control

Expected independent output:

    INDEPENDENT PASS: physical 76-state carry graph gives 1312 four-cell patterns
    INDEPENDENT PASS: schoolbook 384-column seed9397 rank1024 at sample1471
    INDEPENDENT PASS: actual 386-digit forced-overflow outputs g0/g1 ranks1024 at samples1025/1628
    INDEPENDENT PASS: 3256 output words SHA256 11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9
    INDEPENDENT PASS: 32768-feature 8-phase covariance rank8192 with lowest-bit elimination
    INDEPENDENT PASS: eight 406-digit rec2 root controls and wrong-overflow negative checks

Local checks passed: primary <5 sec, independent <17 sec, each <125 MB RSS. Full repository tools/verify.py --changed unavailable due blocked shell GitHub DNS / absent checkout. Non-Lean PAPER PROOF, not a repository-wide verification claim.
