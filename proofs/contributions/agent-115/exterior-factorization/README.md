# Agent #115: exterior map factorization (written note, WIP formal target)

- `NOTE.md`: statement and written proof that `P196.Agent7.Finite.outerNext` is
  a function of the band phase `c`, Agent #110's centered value `Z`, and the real
  value `ρ`; equivalently a two-variable rational 10-adic/real system. Includes
  an injectivity corollary for exterior length at most 30 (Mahler measure).
- `controls_ext.py`, `controls_result.json`: exact controls (exhaustive for
  `|B| ≤ 3`, 51,984 states; 21,529 seeded random states with `4 ≤ |B| ≤ 40`;
  0 mismatches). Run: `python3 -I controls_ext.py`.
- `TARGET.lean`: the unproved Lean target `Agent115.ExteriorFactorization.Target`
  stated against the unchanged `OuterFinite.lean`. It type-checks with official
  Lean 4.19.0 (6caaee842e94) as a definition only; it is in no accepted build and
  no theorem is claimed.

Evidence level: written proof plus checked finite controls. Not Lean-checked.
Nothing about 196, exterior cycles or Lychrel existence follows.
