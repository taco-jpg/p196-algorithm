# Independent review: Agent #115 exterior factorization

Reviewer: Agent #113 (task `agent113-review-agent115-exterior`). Reciprocal review, disclosed:
Agent #115 reviewed Agent #113's two-digit-prefix package. Reviewed source: `740c045`
(`research/agent-115/s20261015-review-broader`; identical for this directory to the branch head
`0fcc8a0`). The task record's pin `6d9c42a` is covered: `ExteriorFactorizationProof.lean` and
`TARGET.lean` are byte-identical in both; `740c045` only adds `ExteriorObservationInjective.lean`
and four audit lines. Replication review, not a new theorem.

## Verdict: PASS, with one interpretive note that should travel with the result

## What is proved (checked)

- `target : Target`. For every nonneutral even phase `c` and canonical words `B₁, B₂`
  (`validOuter`), equal `zValue` (Agent #110's `9ΣB_i10^i − c(10^n−1)`) and equal
  `ρ = rhoNum c B / (9·10^|B|)` (cross-multiplied) imply equal `outerNext` successors.
  `outerNext`, `validOuter`, `normalize`, `stripSuffix` are the unchanged
  `P196.Agent7.Finite` definitions (`OuterFinite.lean`, SHA-256 `3376873d…c5f3f6`, checked by
  the author's `check.py`). `zValue`, `rhoNum`, `highValue` match NOTE.md.
- `factorization_general`: the same conclusion for any words with entries `≤ 18` (not
  necessarily trimmed or with positive head).
- `observation_injective`: canonical words with the same `c`, `Z` and `ρ` are equal.
- Supporting: `eq_of_values`, `outerNext_append_band` / `_replicate` (appending band copies
  does not change the successor), `zValue_append_*`, `rhoNum_append_*`, `normalize_eq`.
- No vacuity: all hypotheses are satisfiable (e.g. `B₁ = B₂`, or padded pairs for
  `factorization_general`).

## Interpretive note (important for anyone building on it)

Because `(c, Z, ρ)` is a complete invariant of the exterior state *modulo appending copies of
the band coefficient* (`observation_injective` for canonical words; `eq_of_values` plus padding
invariance in general), `target` and `factorization_general` follow from the faithfulness of
this encoding together with `outerNext_append_band`. They do **not** by themselves give an
update law in `(Z, ρ)` coordinates. The author's README says this for `target`; the NOTE's
phrase "removes the radix obstruction / `(c, Z, ρ)` is autonomous" should be read the same
way: the coordinates are autonomous because they encode the state.

The dynamical content is NOTE.md's explicit update `β' = β + Φ(ρ̃)`, `ρ' = Ψ(β) + ρ̃` (digit
sums of the 10-adic digits of `β` and decimal digits of `ρ̃`). That remains a **written proof**;
it is not formalized. Agents studying exterior cycles (e.g. Agent #110's open proposition) who
want to use `(β, ρ)` dynamics formally would need that update formalized.

## Execution

- Author's `check.py` run by me from a clean worktree at `740c045` into a new empty directory,
  official Lean 4.19.0 (`6caaee842e94`): **PASS**, all five modules exit 0, seven audited
  exports (`evidence/check-verification.json`, logs).
- `FullAudit115.lean` (mine): every theorem constant whose name contains `Agent115` in the
  compiled environment: **61 theorems, 0 disallowed, union = propext, Classical.choice,
  Quot.sound** (`evidence/FullAudit115.log`).
- `check_rational_system.py` (mine; `outerNext` re-implemented from `OuterFinite.lean`, not
  copied from the author's controls): with exact rationals, the NOTE's update
  `β' = β + Φ(ρ̃)`, `ρ' = Ψ(β) + ρ̃` holds on **70,939** canonical states (all with `|B| ≤ 3`,
  plus 20,000 seeded random states with `4 ≤ |B| ≤ 30`): **0 mismatches**. Injectivity modulo
  padding: **0** violations over 12,996 `(c, Z, ρ)` classes of words with `|B| ≤ 3`,
  `c ∈ {4, 12}`. Checks only, not proof.

## Notes

1. `TARGET.lean`'s docstring still says "UNPROVED TARGET (WIP), kept outside every accepted
   build"; it is now compiled in the accepted build and discharged by `target`. Stale wording
   only.
2. The author's audit covers 7 named exports; the full-environment audit above covers all 61.
3. Scope stated correctly: one-step structural interface; no exterior-cycle, acyclicity, 196 or
   Lychrel conclusion.

Status recommendation for `agent115-exterior-factorization-lean` at `740c045` (and its
`6d9c42a` subset): **INDEPENDENTLY-REVIEWED** for the Lean statements above. The explicit
`(β, ρ)` update stays a written proof, now with an independent numerical replay.
