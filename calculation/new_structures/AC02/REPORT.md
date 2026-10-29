# AC02: rooted p12/m9 U-group a=2 centre census

**Label: COMPUTED.** **Global Lychrel status: UNDECIDED, no all-time certificate.** Exact source: canonical B0 (34), W0 (9), J=[5], q=14, k=100; U=(9,2,16),(2,16,9),(16,9,2), genuine 120 ordinary decimal reverse-and-add steps, expected q unchanged and k→k+5, centre radius R=122+|C|+30. Unlike strict-phase W9 tests, temporary W9 damage was never pruned.

## Exhausted necessary-condition cells

Each centre coefficient is 0..18, C is palindromic, and odd midpoints are even. For **each** of the 3 U words:

| |C| | full distinct C per U | physical t120 centre tests per U | discarded by all-width mod-11 gate per U | central window matches |
|---|---:|---:|---:|---:|
| odd 7 | 68,590 | 68,590 | 0 | 0 |
| even 8 | 130,321 | 130,321 | 0 | 0 |
| odd 9 | 1,303,210 | 1,303,210 | 0 | 0 |
| even 10 | 2,476,099 | 2,476,099 | 0 | 0 |

Therefore **11,934,660 distinct physical reference-width tests**, with zero central-window fixed points, zero fallback/non-rejoined carries. Counts are exactly 19^floor(|C|/2) times 10 for odd |C|, 1 for even. The C7..10 cells are EXHAUSTED-NONE for the stated reference-width centre necessary condition.

For **odd |C|=11**, the result is **EXHAUSTED-NONE only for all-width T* return**, NOT for the unfiltered reference-width centre-only predicate. Each U has 24,760,990 centres. Under the previously established odd-centre gate A(U)=A(C) mod 11 (necessary for independently variable k), the counts are:
- U=(9,2,16): 2,250,982 passed gate and were physically simulated; 22,510,008 rejected by the all-width gate; 0 centre matches.
- U=(2,16,9): same counts, 0 centre matches.
- U=(16,9,2): 2,251,028 passed and were physically simulated; 22,509,962 rejected; 0 centre matches.
Thus 74,282,970 C11 T* alternatives are accounted for by 6,752,992 full physical checks and 67,529,978 sound odd-C modular exclusions. The modularly excluded words have **not** been ruled out as isolated reference-width centre fixed points.

## Partial, not exhausted

For each U and each |C|=12,13,14, the first 10,000 lexicographic distinct palindromic C were tested with no window matches or non-rejoined carries, **PARTIAL** only: per-U denominators are 47,045,881, 470,458,810, and 893,871,739 respectively. Across three U words this is **90,000 / 4,234,129,290** physical tests, and is not an exclusion. No mod-11 pruning was used for these tests.

## Sound computation / audit argument

At every t the differential engine represents the exact coefficient pairword by a baseline P_t plus a changed interval [lo,hi]. Since coefficients below lo equal the baseline, the incoming decimal carry at lo equals the baseline carry. It computes digit normalization from lo through hi and continues across unchanged coefficients **until the outgoing carry equals the baseline carry**. Hence all normalized decimal digits outside [lo,stop] equal baseline digits, with identical overflow. Mirrored pairing confines every changed coefficient at t+1 to the explicitly constructed symmetric interval [min(lo,N'-1-stop), N'-1-min(lo,N'-1-stop)]. This proves the invariant inductively through 120 steps. A carry that does not rejoin takes the full-width exact decimal fallback instead of being excluded. In all exhaustive cells here the fallback count was zero. Every survivor requires the exact centre window equality. Thus zero survivors is a necessary-condition exclusion, NOT an all-time orbit proof.

Intermediate-state audit mode checked 100 centre samples per U and |C|=7..10 against a separately computed full-width digit-array state at all 120 transitions: zero discrepancies. Independent Python arbitrary-precision n+reverse(n) replay checked 45 U/C/width controls, 5,400 genuine decimal transitions, at (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640); every digit normalization, 30 length overflows and (1000)^30 clock agreed. Another 60 exact runs tested five J variants per U/centre control and found identical 311-site centre windows at q14/k100; this **samples** the junction-separation claim rather than proving T12. The full arbitrary-J T12 lift must retain its published reset-cone premises.

## Reproduce

Run from repository root (the C++ embeds the published B0/W0 values):

    g++ -O3 -DNDEBUG -std=c++17 calculation/new_structures/AC02/centre_census.cpp -o /tmp/ac02-centre
    /tmp/ac02-centre 0 2 7 10 0
    /tmp/ac02-centre 0 2 11 11 0 oddallwidth
    /tmp/ac02-centre 0 2 12 14 10000
    /tmp/ac02-centre 0 2 7 10 100 audit
    python3 calculation/new_structures/AC02/independent_check.py

All labels and denominators above are per stated predicates. No all-time decimal certificate, no two-epoch seam restoration, and no results/ entry.