# Agent #103 — broader two-column (4,4) return: Lean formalization

Task `agent103-broader-return-formal` (`p196/coordination`).

## Stage 1 (LEAN-CHECKED; independent review pending)

Written source: `2026-10-14-component-specific-bound/COMPONENT_SPECIFIC_BOUND.md`,
eq. (2), and `2026-10-14-broader-return/BROADER_RETURN_BOUND.md`.

`BroaderClock.lean` (new; core Lean + project base modules only):

| Declaration | Content |
|---|---|
| `nextPair x y v` | Exact update of the first two pair coefficients given the actual deeper carry `v`. |
| `two_column_step` | For every `Admissible L q` with `L >= 2` (overlapping widths 2 and 3 included): `(nextColumns q L 0, nextColumns q L 1) = nextPair (q 0) (q 1) (carry q (L-2))`, with `carry q (L-2) <= 1`. Proved from `ActualScalar.actual_scalar_step` and `PrefixExtension.actual_extension_formula`. |
| `returnOK_root` | Kernel `decide` (no axioms): every 7-step path of `nextPair` from (4,4) back to (4,4) has outside values 4,8,16,7,15,6,13. |
| `returnOK_sound` | The Boolean classification is sound for every path. |
| `return_forces_clock` (**L1**) | If the actual pair word has prefix (4,4) at times `a` and `a+7`, its outside coefficient equals `ScalarClock.phase i` for all `i <= 7`. |
| `returns_clock_segment` | `R` consecutive seven-step (4,4) returns give `ScalarOrbit.ClockSegment q L a 0 (7R)`. |

`BroaderScalarBound.lean` combines this with the kernel-checked scalar endpoints
(`../scalar-finite-instance/`):

| Theorem | Statement |
|---|---|
| `returns_le_94_plus_warmup` | `Admissible L q`, `2 <= L`, prefix (4,4) at `7k` for `k <= R` ⟹ `R <= 94 + warmup L`. |
| `returns_le_98` | Same from any start time `a`: `R <= 98`. |
| `wide_returns_le_94` | If the width at time `a` is at least 14: `R <= 94`. |
| `no_99_returns` | No 99 consecutive seven-step returns to (4,4). |

These are weaker than the written bound `R <= 90 + warmup L <= 94`; stage 2
(broader 15-job finite instance) is needed for that. All three return
branches and arbitrary branch switching are covered, because L1 is proved for
every return path of the exact local relation, not for named branches.

Build: `verify_broader.py` (= `../scalar-finite-instance/v2/verify_v2.py` plus
the two new modules), `--stage final --resume` in a **copy** of the verified
scalar build directory: 53 modules reused only after the unchanged
source/object/log/dependency fingerprint check, `BroaderClock`,
`BroaderScalarBound` and `AllAxioms` compiled. Result `verification.json`:
PASS, 56 modules, 2,824 theorems, axiom union
`{propext, Quot.sound, Classical.choice}`; the 11 new theorems use
`[propext, Quot.sound]` (`returnOK_root`: none), the four bounds additionally
`Classical.choice` via the scalar endpoints. No `ofReduceBool`/`sorryAx` in
`AllAxioms.log`. Official Lean 4.19.0 `6caaee842e94`.

Scope: finite-horizon obstruction to one return mechanism. Leaving the pattern
does not imply a palindrome; nothing about 196 or Lychrel existence.
