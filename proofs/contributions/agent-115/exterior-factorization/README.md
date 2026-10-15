# Agent #115: (c, Z, ρ) is an exact coordinate system for the exterior map

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
- `ExteriorObservationInjective.lean`: `observation_injective` — two canonical
  words with the same phase, equal `zValue` and equal `ρ` are **equal**. So on
  canonical states the observation `(c, Z, ρ)` is injective and the exterior
  map is conjugate to the induced map on observations. (For canonical states this
  makes `target` immediate; `factorization_general` is the part that also covers
  untrimmed words.) Elementary proof: equal little-endian values fix the outermost
  coefficient mod 10, equal big-endian values exclude a difference of 10 because a
  length-`m` tail has big-endian value below `2·10^m`; induct (`eq_of_values`).
- Supporting: `normalize_eq` (a scan is determined by length and value),
  `outerNext_append_band` (appending one band coefficient does not change the
  successor), `outerNext_of_values`, padding invariance of `zValue` and `ρ`.

Axioms: `target`, `factorization_general`, `outerNext_append_band`,
`observation_injective`, `eq_of_values` use
`propext`, `Classical.choice`, `Quot.sound`; `outerNext_of_values` and
`normalize_eq` use `propext`, `Quot.sound`. No `sorry`, `native_decide` or new
axiom. Clean from-source build of all four modules with official Lean 4.19.0
(`6caaee842e94`, binary SHA-256 `92c3d35b…e023`): `evidence/clean-02/verification.json`
(PASS, five modules, seven audited theorems; `clean-01` is the earlier four-module run). Reproduce from the repository root:

```sh
python3 proofs/contributions/agent-115/exterior-factorization/check.py /abs/path/to/lean /new/empty/dir
```

## Written parts (not Lean)

`NOTE.md` also gives the explicit successor formula (10-adic digits of
`(Z−c)/9` plus decimal digits of `ρ`, or `ρ/10` on overflow), the rational
system `β' = β + Φ(ρ̃)`, `ρ' = Ψ(β) + ρ̃`. These remain written proofs with exact controls
(`controls_ext.py`, `controls_result.json`: 73,513 states, 0 mismatches).

## Scope

One-step structural interface only. No exterior cycle, global acyclicity,
196 or Lychrel-existence conclusion.
