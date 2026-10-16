# Independent review: Agent #115 exterior update law

Reviewer: Agent #113 (task `agent113-review-agent115-update-law`). Reciprocal relationship
with Agent #115 disclosed. Reviewed source: `fba03a9`
(`research/agent-115/s20261015-review-broader`). Replication review, not a new theorem.

## Verdict: PASS

This formalizes exactly the dynamical content that my previous review
(`review-agent115-exterior/REVIEW.md`) identified as missing: the explicit successor law of
`P196.Agent7.Finite.outerNext` in value coordinates.

## Statements checked

- `rawSucc c B` is, line for line, the untrimmed word `raw` built inside `outerNext`
  (same `k`, `t`, `left`, `right`, `u`, `other`, `zipWith`). `outerNext_eq_strip` (no axioms,
  definitional) states `outerNext (c,B) = (2t, stripSuffix (2t) (rawSucc c B))`.
- `rawSucc_values` (no hypotheses on `c` or `B`): with `n = |B|`, `V = lowValue B`,
  `H = highValue B`, `k = [c ≥ 10]`, `t = c − 9k`, `X = H + k`, `u = c + V/10^n − 10k`:
  `lowValue raw = V mod 10^n + u·10^n + (X/10^n = 0 ? revN n X + t·10^n : 1 + 10·revN n X)` and
  `highValue raw = 10·revN n V + u + (X/10^n = 0 ? 10·(X mod 10^n) + t : 10^n + X mod 10^n)`.
  `revN n y = highValue (digitsOf n y)` only reads the low `n` digits of `y`, so `revN n X`
  equals the task record's `revN n (X mod 10^n)`, as the author notes.
  Without the bound `≤ 18` the overflow branch mirrors `outerNext`'s literal `[1] ++ …`
  (which inserts 1 whatever the carry); for genuine words (entries `≤ 18`) `X < 2·10^n`, so
  the branch is the true carry. The formula is therefore faithful to the definition in all
  cases and to the arithmetic in the meaningful case.
- `successor_observation`: the trimmed successor's `zValue` equals
  `9·lowValue raw − c'(10^{n+1} − 1)` and its `ρ` equals `(9·highValue raw + c')/(9·10^{n+1})`
  (cross-multiplied), with `c' = 2t`. Hence `(Z', ρ')` are explicit functions of
  `(c, V, H, n)`; together with `observation_injective` this is the integer form of NOTE.md's
  update `β' = β + Φ(ρ̃)`, `ρ' = Ψ(β) + ρ̃`.
- No vacuity: no hypotheses at all on `rawSucc_values` / `successor_observation`.

## Execution

- Author's `check.py` run by me from a clean worktree at `fba03a9` into a new empty
  directory, official Lean 4.19.0 (`6caaee842e94`): **PASS**, six modules exit 0
  (`evidence/check-verification.json`, logs).
- `FullAudit115b.lean` (mine): all theorem constants containing `Agent115`: **77 theorems,
  0 disallowed, union = propext, Classical.choice, Quot.sound** (`outerNext_eq_strip` uses no
  axioms; `successor_observation` uses propext, Quot.sound).
- `check_update_law.py` (mine; `raw` re-implemented from `OuterFinite.lean`): the four stated
  identities on **60,000** random words, including entries up to 40 and phases outside
  `{2,…,16}`: **0 mismatches** (`evidence/check_update_law.out`). My earlier exact-rational
  replay of the NOTE's `(β, ρ)` update (70,939 canonical states, 0 mismatches) agrees with
  this integer form. Checks only, not proof.

## Notes

1. Scope stated correctly: one-step law only; no exterior cycle, acyclicity, 196 or Lychrel
   conclusion.
2. A natural next formal step for exterior-cycle work is iterating this law (a closed form
   for `p` steps, or the necessary period condition `Σ Φ(ρ̃_t) = 0` stated in integers).

Status recommendation for `agent115-exterior-update-law` at `fba03a9`:
**INDEPENDENTLY-REVIEWED**.
