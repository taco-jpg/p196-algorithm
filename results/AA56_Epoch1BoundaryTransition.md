# AA56: Universal first epoch transition with an expanding seam

**Label: COMPUTED. Exact scope: one 360-step transition for all independent integers q,k >= 2048, under the symbolic pairword checker in `calculation/new_structures/R30/parametric.py`. This is not an all-time Lychrel certificate.**

## Missing lemma supplied

The result gives an exact symbolic epoch-map edge for a concrete rooted decimal p12/m9 family, including the finite boundary apron and the changed centre. It does not merely extrapolate a handful of integer replays.

Let B and W be the canonical phase-zero rows from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, with |B|=34 and |W|=9. The input family is

`T0(q,k) = B ++ W^q ++ [5] ++ (9,14,4)^k ++ [10] ++ reverse(...)`.

The checker constructs a fixed finite output seam J1 of length 252 and a fixed palindromic output centre C1 of length 273 from a concrete discovery replay, then checks the entire 360-step symbolic orbit against

`T1(q,k) = B ++ W^(q-8) ++ J1 ++ (4,9,14)^(k-90) ++ C1 ++ reverse(...)`

for every independent q,k >= 2048. The output's length is `18q + 6k + 161`, exactly 90 coefficient positions longer than the input. The 360-step overflow clock is `(1000)^90`, total overflow 90, and every intermediate folded pairword has an odd coefficient, guarding non-palindromicity throughout this macro.

## Reproduction

Run from repository root:

```bash
python3 calculation/new_structures/AA56/check_epoch1_symbolic.py
```

The script uses the R30 symbolic checker, extracts the candidate finite J1/C1 constants from a concrete seed, checks independent concrete controls at (q,k)=(120,200) and (160,320), then proves the universal symbolic equality with qmin=kmin=2048 and checks all 360 odd-coefficient guards.

## Limitation

This edge is not self-reproducing: q decreases by 8 and k decreases by 90, while the seam and centre expand. The second and third epochs have additional width-loss patterns, so no closed cycle or repair lemma has been established. Do not label this as a decimal Lychrel number or an all-time certificate. Its value is the exact boundary/centre state transition needed to analyze whether a later epoch can refund the consumed W9 defect budget.
