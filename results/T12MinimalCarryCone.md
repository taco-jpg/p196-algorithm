# T12MinimalCarryCone

**Label: PAPER PROOF**, with exact finite phase enumeration and independent arbitrary-precision controls.

## Statement

For the rooted decimal p12/m9 clock and its prescribed 120-step phase, the exact minimal *carry-port* causal radii are:
- W9 seam-facing side: 91 pair coefficients.
- U3 junction-facing side: at most 152 coefficients, attained by ten of the thirty allowed U words.
- U3 centre-facing side: at most 122 coefficients, attained by ten other U words.

The latter two maxima occur at different rotations. For any fixed finite junction J, the seam-local transition therefore depends on at most **243+|J|** pair coefficients, independently of q and k. This is a sharp radius for arbitrary entering 0/1 carry differences, not a claim that all extremal differences are physically reachable from canonical decimal seams.

## Proof

For a pair coefficient x in 0..18, the normalization carry map is T_x(c)=floor((x+c)/10), c in {0,1}. If x is not 9, T_x(0)=T_x(1); if x=9, T_x(0)=0 and T_x(1)=1. Thus a carry difference resets at every non-9 coefficient and propagates exactly across a 9. Since the published W rows have no adjacent 9s, a boundary displacement per step is 1+r-gamma on the right side, where r is the run of 9s (0 or 1) and gamma is the rooted overflow bit. The exact 120-phase recurrence gives W retreat 91: 89 increments of 1, 30 overflow-phase increments of 0, and one non-overflow increment of 2. The recurrence depends on q only through (34+9q-35) mod 9 = 8, so the result is uniform for all q>=14.

For U3, compute the periodic carry-loop successor F_gamma for each coefficient row using both low- and high-side carry loops, with the gamma=1 upper-index shift included. Each of the thirty words (9,a,18-a) and its rotations returns after 120 phases, with exactly one isolated 9 in each row. If l_t and r_t are the two moving fronts, their exact recurrences are
l_(t+1)=l_t+1+1[V_t[l_t mod 3]=9],
r_(t+1)=r_t+1+1[V_t[(-r_t-1) mod 3]=9]-gamma_t.
Summing all 120 transitions gives (left,right)=(152,121),(151,122),(150,120), ten words per pair. Because these are the exact carry-difference recurrences, no smaller uniform radius suffices in the arbitrary carry-port model.

The U band has length 3k. At k>=100, its 300-coefficient minimum length exceeds 152+122 by 26, so the seam and centre influence cones remain separated. For q>=14, the W prefix at q=14 has 160 coefficients and loses 91, leaving 69; the W insertion cut at coefficient 52 still has 17 protected coefficients beyond it. The seam window is consequently finite for each fixed J, of width at most 91+|J|+152.

## Independent reproduction

Run from repository root:

```bash
g++ -O3 -std=c++17 calculation/new_structures/T12/verify.cpp -o /tmp/t12-verify
/tmp/t12-verify calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt
```

The compiled checker validates all thirty U words, all 120 bulk phases, 240 exact paired-insertion cases at q=20,40,80,160 with k=q+80, the overflow clock and an odd-pair nonpalindrome guard at every phase. Eight case configurations additionally compare every step with boost::multiprecision::cpp_int. Exact output is preserved in calculation/new_structures/T12/verify.log.

**Limit:** This proves the local finite-window reduction, not the existence of a returning seam. No 240-step restored template or decimal Lychrel number is claimed.
