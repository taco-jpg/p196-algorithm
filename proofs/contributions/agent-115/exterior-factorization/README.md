# Agent #115: the exterior map factors through (c, Z, ρ)

**Status: LEAN-CHECKED (author build), independent review pending.**
Task `agent115-exterior-factorization-lean` on `p196/coordination`.

## Formal result

`ExteriorFactorizationProof.lean` proves, against the unchanged exact exterior map
`P196.Agent7.Finite.outerNext` (dependency
`proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean`,
SHA-256 `3376873d…c5f3f6`):

- `Agent115.ExteriorFactorization.target : Target` — for every phase
  `c ∈ {2,4,…,16}` and canonical words `B₁, B₂` (`validOuter`), equal `zValue`
  (Agent #110's centered value `9ΣB_i10^i − c(10^n−1)`) and equal real value
  `ρ = rhoNum c B / (9·10^|B|)` (compared by cross-multiplication) imply
  `outerNext (c,B₁) = outerNext (c,B₂)`. The statement `Target` in `TARGET.lean`
  is unchanged from the earlier WIP commit.
- `factorization_general` — the same with only the coefficient bound `≤ 18`.
- Supporting: `normalize_eq` (a scan is determined by length and value),
  `outerNext_append_band` (appending one band coefficient does not change the
  successor), `outerNext_of_values`, padding invariance of `zValue` and `ρ`.

Axioms: `target`, `factorization_general`, `outerNext_append_band` use
`propext`, `Classical.choice`, `Quot.sound`; `outerNext_of_values` and
`normalize_eq` use `propext`, `Quot.sound`. No `sorry`, `native_decide` or new
axiom. Clean from-source build of all four modules with official Lean 4.19.0
(`6caaee842e94`, binary SHA-256 `92c3d35b…e023`): `evidence/clean-01/verification.json`
(PASS). Reproduce from the repository root:

```sh
python3 proofs/contributions/agent-115/exterior-factorization/check.py /abs/path/to/lean /new/empty/dir
```

## Written parts (not Lean)

`NOTE.md` also gives the explicit successor formula (10-adic digits of
`(Z−c)/9` plus decimal digits of `ρ`, or `ρ/10` on overflow), the rational
system `β' = β + Φ(ρ̃)`, `ρ' = Ψ(β) + ρ̃`, and injectivity of `(c,Z,ρ)` for
`|B| ≤ 30`. These remain written proofs with exact controls
(`controls_ext.py`, `controls_result.json`: 73,513 states, 0 mismatches).

## Scope

One-step structural interface only. No exterior cycle, global acyclicity,
196 or Lychrel-existence conclusion.
