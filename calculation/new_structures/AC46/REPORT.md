# AC46: universal fixed-short-centre obstruction, phase 0

**Label: COMPUTED**, with a PAPER PROOF of two-carry soundness and 331,470 finite centre checks; **NOT Lean-verified**. The full marked-fold CEGAR/SAT emptiness is UNDECIDED. No decimal Lychrel certificate was found.

## Missing-lemma contribution

For the canonical rooted p12/m9 phase-0 exterior B0/W0, fixed-J/C U3 regeneration is impossible for **every finite junction J** and every canonically realizable palindromic coefficient centre of lengths 1..6, all 30 charge-zero U3 rotations, uniformly q>=14 and k>=100. This closes the short-centre sublanguage of PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH without any junction-length bound. In particular this includes both parities and C=(c,c) for all c in 0..18, not just C=(4,4). It does not decide arbitrary-length C, changing C, growing/moving J, q-changing returns, other phases or all-time decimal existence.

## Sound physical-root and central-cone argument

All words are LSD-first symmetric pair coefficients x_i in 0..18, not decimal digits. Normalize with carry c_0=0, digit d_i=(x_i+c_i)%10, carry c_(i+1)=floor((x_i+c_i)/10), gamma=c_L. The next symmetric pair coefficients are d_i+d_(L-1-i) if gamma=0, or x'_0=d_0+1 and x'_i=d_i+d_(L-i) for i>0 if gamma=1. This is ordinary decimal reverse-and-add.

The published rooted phase-0 prefix B0++W0^14 (length 160) and mirrored suffix are present for every q>=14 and arbitrary J,U,C. The low-side prefix normalizes with inlet 0. The high suffix has an unknown incoming carry e in {0,1}: normalize both and require the final overflow gamma to agree. With that gamma, form both possible successor prefixes using the shifted high-digit expression and retain the longest common prefix. By induction, this is guaranteed for every unknown interior, with NO strict-W9 phase condition. The 120-fold computation forces gamma=(1000)^30, retains 69 prefix coefficients, and has an odd coefficient in the guaranteed prefix at every intermediate state (including t0/t120); hence every actual step has this clock and no palindrome.

For the central side, take only the innermost 100 copies of U on each side of C: S0=U^100++C++reverse(U^100). The entire outer remainder (including arbitrary J and extra U copies) is unknown. For any symmetric protected centre S of length M, normalize with both possible incoming carry bits e=0,1 to digit words d_e. With the already physically forced overflow gamma, the true successor includes the centred candidate word whose j-th coefficient is d_e[gamma+j]+d_e[M-1-j] for j=0..M-gamma-1. Because both branches use the identical actual centre, retain the longest common symmetric central substring and discard differing symmetric ends. This is a sound over-approximation by induction for every outer context, not a radius-3 locality assumption. After 120 stages at least 327 protected central coefficients remain. In a literal same-J/C/U return, the central radius-r window must equal that of U^(k+5)++C++reverse(U^(k+5)), independent of J,q,k. Every allowed U/C fails at some radius r<=3.

## Exhaustive certificate

| C length | Palindromic C per U | Total U/C | First mismatch radius 0 / 1 / 2 / 3 |
|---:|---:|---:|---|
| 1 | 10 | 300 | 262 / 32 / 4 / 2 |
| 2 | 19 | 570 | 546 / 24 / 0 / 0 |
| 3 | 190 | 5,700 | 5,658 / 36 / 6 / 0 |
| 4 | 361 | 10,830 | 10,816 / 12 / 2 / 0 |
| 5 | 3,610 | 108,300 | 108,268 / 28 / 4 / 0 |
| 6 | 6,859 | 205,770 | 205,754 / 16 / 0 / 0 |
| **Total** | | **331,470** | **331,304 / 148 / 16 / 2** |

Odd centres have an even midpoint; all remaining coefficients are drawn from 0..18. The C++ engine directly enumerates all listed words and every U rotation, with 122.66s elapsed and 1664 KiB max RSS in the test container. No unbounded SAT/CEGAR decision for arbitrary C is claimed.

## Reproduction and independent decimal check

From repo root:

~~~sh
g++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/new_structures/AC46/centre_census.cpp -o /tmp/ac46_centres
/tmp/ac46_centres 6
python3 calculation/new_structures/AC46/cone.py --clock
python3 calculation/new_structures/AC46/independent.py
~~~

The independent Python checker realizes every chosen symmetric coefficient word as a canonical nonzero-leading integer, compares actual unbounded-integer n+reverse(n) with a separately written schoolbook digit-array implementation at all 120 steps, checks exact overflow, nonpalindrome guard and the protected centre at every intermediate step, then the failed return. Deterministic tests: 294 complete 120-step orbits = 35,280 genuine decimal steps; width pairs (q,k)=(14,100),(20,120),(40,200),(80,400),(160,800), centres of each length1..6, arbitrary junction lengths 0..311 and all 30 U. A planted positive one-step toy target is the true 196->887 output, with deliberately false target rejected. The tests are controls; the ALL-J/ALL-q,k proof is the carry induction.

**Remaining single missing global lemma:** decide the free-length marked J/C folded 120-track physical return language by a valid two-port carry/lag automaton. Strict-W9 per-phase MDD filtering is an under-approximation and cannot decide endpoint-only return; an arbitrary radius-3 locality assumption is unsound because of 9-carry chains. No all-time decimal proof; no ALERT.
