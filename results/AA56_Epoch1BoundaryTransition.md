# AA56: Four universal epoch-map edges with an expanding seam

**Label: COMPUTED. Exact scope: four individually symbolically checked 360-step transitions, each for all independent integers q,k >= 2048, using the R30 symbolic pairword checker in `calculation/new_structures/R30/parametric.py`. This is not an all-time Lychrel certificate.**

## Missing lemma supplied

The result gives exact symbolic epoch-map edges for a concrete rooted decimal p12/m9 family, including finite boundary aprons and changing palindromic centres. It does not extrapolate from finite-width integer replays.

Let B and W be the canonical phase-zero rows from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, with |B|=34 and |W|=9. The initial family is

`T0(q,k) = B ++ W^q ++ [5] ++ (9,14,4)^k ++ [10] ++ reverse(...)`.

For each epoch n=1,2,3,4, the checker discovers fixed finite words J_n and C_n from a concrete seed, then symbolically verifies the entire 360-step orbit against

`T_n(q,k) = B ++ W^(q-8) ++ J_n ++ (4,9,14)^(k-(89+n)) ++ C_n ++ reverse(...)`

where the source seam/centre are the previous epoch's J_(n-1), C_(n-1). The output sizes are:

| Edge | Input U exponent loss | Output seam length | Output centre length |
|---:|---:|---:|---:|
| 1 | 90 | 252 | 273 |
| 2 | 91 | 504 | 549 |
| 3 | 92 | 756 | 831 |
| 4 | 93 | 1008 | 1119 |

Every edge has the exact 360-step overflow clock `(1000)^90`, total overflow 90, and an odd pair-coefficient witness at every intermediate phase. The target pairword length is exactly 90 coefficients longer than the source. Each edge is checked for all independent q,k >= 2048; the concrete seed is used only to discover the fixed finite J_n/C_n words, after which the symbolic checker verifies universal equality.

## Reproduction

Run from repository root:

```bash
python3 calculation/new_structures/AA56/check_epoch_chain_symbolic.py
```

The script uses the existing R30 symbolic engine, checks the canonical decimal/pairword guards, extracts the finite seam/centre words from a concrete orbit, and then checks each of the four symbolic transitions and all 360 odd-coefficient guards.

## Limitation

This chain is not self-reproducing: q decreases by 8 per epoch and k decreases by 90, 91, 92, then 93. The seam and centre expand, but no transition has been proved that restores the consumed W9 budget. Four exact edges do not prove the pattern for all epochs, and no cycle or repair lemma has been established. Do not label this as a decimal Lychrel number or an all-time certificate.
