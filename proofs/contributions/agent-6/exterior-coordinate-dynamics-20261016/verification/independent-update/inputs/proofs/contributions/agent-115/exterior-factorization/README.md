# Agent #115: (c, Z, ρ) is an exact coordinate system for the exterior map

**Status: INDEPENDENTLY-REVIEWED** by Agent #113 (task
`agent113-review-agent115-exterior`, verdict PASS, reviewed source `740c045`,
record `proofs/contributions/agent-113/review-agent115-exterior/REVIEW.md` on
`research/agent-113/s20261015`): fresh `check.py` run, full-environment audit of
all 61 Agent115 theorems (standard axioms only), and an independent exact-rational
replay of the written `(β, ρ)` update on 70,939 states (0 mismatches).

Reviewer's interpretive note, adopted here: `target` and `factorization_general`
follow from faithfulness of `(c, Z, ρ)` modulo band padding
(`observation_injective`, `eq_of_values`, `outerNext_append_band`); they are not an
update law in `(Z, ρ)` coordinates. The explicit update rule remains a written
proof. The header comment of `TARGET.lean` ("UNPROVED TARGET") is historical: it
predates the proof and the file is kept byte-identical to the reviewed source.
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
- `ExteriorUpdateLaw.lean` (task `agent115-exterior-update-law`, **LEAN-CHECKED,
  not yet independently reviewed**): the explicit update law in value coordinates.
  For any `c` and any word `B` of length `n`, with `V = lowValue B`,
  `H = highValue B`, `k = [10 ≤ c]`, `t = c − 9k`, `X = H + k`,
  `u = c + V/10^n − 10k` and `revN n y` the value of the reversed `n`-digit
  representation of `y`, `rawSucc_values` gives
  `lowValue(raw) = V % 10^n + u·10^n + (X < 10^n ? revN n X + t·10^n : 1 + 10·revN n X)` and
  `highValue(raw) = 10·revN n V + u + (X < 10^n ? 10·(X % 10^n) + t : 10^n + X % 10^n)`
  for the untrimmed successor `raw = rawSucc c B` (length `n+1`), and
  `successor_observation` turns these into the successor's `zValue` and `ρ`.
  Together with `observation_injective` this is an explicit, kernel-checked
  dynamical system on `(c, Z, ρ)` conjugate to the exterior map; digit reversal
  `revN` is its only nonlinear ingredient. No hypothesis on `c` or `B` is needed
  for these identities.
- Supporting: `normalize_eq` (a scan is determined by length and value),
  `outerNext_append_band` (appending one band coefficient does not change the
  successor), `outerNext_of_values`, padding invariance of `zValue` and `ρ`.

Axioms: `target`, `factorization_general`, `outerNext_append_band`,
`observation_injective`, `eq_of_values` use
`propext`, `Classical.choice`, `Quot.sound`; `outerNext_of_values` and
`normalize_eq` use `propext`, `Quot.sound`. No `sorry`, `native_decide` or new
axiom. Clean from-source build of all four modules with official Lean 4.19.0
(`6caaee842e94`, binary SHA-256 `92c3d35b…e023`): `evidence/clean-02/verification.json`
(PASS, five modules, seven audited theorems; `clean-01` is the earlier four-module run).
`evidence/clean-03/verification.json`: PASS with the update-law module (six modules,
nine audited theorems; `rawSucc_values` uses `propext, Classical.choice, Quot.sound`,
`successor_observation` uses `propext, Quot.sound`). Reproduce from the repository root:

```sh
python3 proofs/contributions/agent-115/exterior-factorization/check.py /abs/path/to/lean /new/empty/dir
```

## Written parts (not Lean)

`NOTE.md` also phrases the law as digit sequences (10-adic digits of `(Z−c)/9`
plus decimal digits of `ρ`, or `ρ/10` on overflow) and as the rational system
`β' = β + Φ(ρ̃)`, `ρ' = Ψ(β) + ρ̃`. Those 10-adic/real phrasings remain written;
their integer content is the Lean law above. Exact controls 
(`controls_ext.py`, `controls_result.json`: 73,513 states, 0 mismatches).

## Scope

One-step structural interface only. No exterior cycle, global acyclicity,
196 or Lychrel-existence conclusion.
