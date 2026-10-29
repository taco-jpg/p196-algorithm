# W17 cell report

**Status: EXHAUSTED-NONE.** Scope is rooted p12/m9 phase 0, U=(8,9,10), |J|=3–4, even palindromic C of lengths 2, 4, 6, 8, 10, or 12, and independent q>=14,k>=100. This is a scoped obstruction, not a global no-go for decimal Lychrel numbers.

**Exact result.** No admissible (J,C) in this cell has a 120-step epoch image that restores the rooted W9 band. Therefore the image is not in the same cell, and no fixed point or longer same-cell epoch cycle can start here. Although the assigned cell asks only for even C lengths 2–12, the cone never reads C at all; the same proof applies to every finite palindromic centre of either parity (odd centres must have an even midpoint coefficient). This also covers the corresponding odd-centre short-J cell without enumerating those centres.

**Completeness reduction.** The committed T12 paper theorem gives exact paired-insertion pumping at protected W/U cuts for all independent q>=14,k>=100; it suffices to inspect (q,k)=(14,100) and then transfer any seam-relative mismatch to every larger pair. At this reference width, the exact two-ended carry cone starts with the prefix B W^14 J U^100 (length 463/464) and never reads the unknown centre. At each step, carry through a coefficient is constant 0 for values 0–8, identity for 9, and constant 1 for 10–18. By symmetry, the high-side carry for each required low output coefficient is determined by the first non-9 coefficient after the corresponding cut; trimming the terminal run of 9s plus one coefficient makes every retained output coefficient exact. After 120 steps, the retained prefix has length 298 for |J|=3 and 299 for |J|=4, still before C.

The endpoint mismatch is at i=s-d, where s=160 is the W9|J cut and 13<=d<=25. T12 inserts a full W row at the protected cut cW=52, before every such mismatch; inserting W shifts both i and s by 9, leaving d unchanged. Its protected U insertion cut is after the seam, so inserting U leaves the mismatch in place. Therefore the W9 endpoint mismatch persists for every independent q>=14,k>=100, not merely at the reference width. Since the W9 band is not restored, the epoch image cannot enter this cell even if J or C were allowed to change at the next epoch.

**Exhaustive counts.** Every J is enumerated by its base-19 code, with digits in [0,18]:

| Junction length | Complete J count | Wrong overflow clock | First endpoint mismatch in W9 | Survivors |
|---:|---:|---:|---:|---:|
| 3 | 6,859 | 0 | indices 135–144 | 0 |
| 4 | 130,321 | 0 | indices 135–147 | 0 |
| **Total** | **137,180** | **0** | **all cases** | **0** |

The W9|J cut is s=34+9·14=160; every first mismatch is s−d with 13<=d<=25, so it lies strictly inside the expected W9 band, not in J or C. For reference, the first-mismatch histograms are:

| Absolute coefficient index | J length 3 | J length 4 |
|---:|---:|---:|
| 135 | 115 | 1,472 |
| 136 | 150 | 3,012 |
| 137 | 3,319 | 60,417 |
| 138 | 2,616 | 52,392 |
| 139 | 287 | 6,124 |
| 140 | 325 | 5,998 |
| 141 | 33 | 398 |
| 142 | 6 | 400 |
| 143 | 0 | 0 |
| 144 | 8 | 74 |
| 145 | 0 | 32 |
| 146 | 0 | 0 |
| 147 | 0 | 2 |

There are 49,659,540 even palindromic centres of lengths 2,4,6,8,10,12, since the count is 19 + 19^2 + ... + 19^6. The centre-independent cone rejects all of them without enumerating C; the combined (J,C) space is 6,812,295,697,200 candidates.

**Independent validation.** cell_cone.cpp --selftest matches the exact full pairword recurrence at every phase for 4 J words × 5 valid even/odd centres. independent_replay.py --reference compares 120 genuine arbitrary-precision integer additions against a separately implemented LSD-first digit-array addition and the pairword recurrence in 60 even-centre cases at (q,k)=(14,100),(20,100),(40,200),(80,400),(160,800) plus 16 odd-centre controls at (14,100) and (20,100), with J samples covering zeros, all 9s, and mixed digits. Even centres have lengths 2/4/12; odd-centre controls have lengths 3/5. All clocks equal (1000)^30; every sampled target mismatch is inside W9.

**Reproduction:** bash calculation/new_structures/W17/run.sh for the exact exhaustive cone; python3 calculation/new_structures/W17/independent_replay.py --reference --odd-centres for independent integer/digit-array controls (C++17 compiler and Python 3 required). The strict-W9 MDD was not used: the exact endpoint cone is a sound direct obstruction and does not assume intermediate W9 preservation.
