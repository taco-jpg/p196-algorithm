# Agent #103 — broader two-column (4,4) return: Lean formalization

Task `agent103-broader-return-formal` (`p196/coordination`).

## Result summary

**Stage 2 (LEAN-CHECKED; independent review pending): the written bound is now
an unconditional Lean theorem.**

| Theorem (`stage2/BroaderBound.lean`) | Statement |
|---|---|
| `BroaderBound.returns_le_90_plus_warmup` | `Admissible L q`, `2 <= L`, `pairAt q L (7k) = (4,4)` for all `k <= R` ⟹ `R <= 90 + warmup L`, where `warmup L = (14-L+2)/3 = max(0, ceil((14-L)/3))`. This is eq. (2) of `COMPONENT_SPECIFIC_BOUND.md` exactly. |
| `BroaderBound.returns_le_94` | From any start time `a`: `R <= 94`. |
| `BroaderBound.wide_returns_le_90` | If the actual width at time `a` is at least 14: `R <= 90`. |
| `BroaderBound.no_95_returns` | No 95 consecutive seven-step returns to (4,4). |

`pairAt q L t` is the first two coefficients (least significant first) of the
actual pair-word orbit `iterPairs`; `Admissible` is the repository's exact
admissible mirrored-word predicate (every positive integer's pair word is one).
All three return branches and arbitrary switching are covered. Scope:
finite-horizon obstruction to this return mechanism only; leaving the pattern
does not imply a palindrome; nothing about 196 or Lychrel existence.

## Stage 2 construction

* `stage2/gen_broader.py`: the 15 broader jobs (source ids 16-30) of the pinned
  certificate `component_certificates.json.gz` (SHA-256 `ff7a70ee...b47e`),
  renumbered 0-14, emitted with the v2 chunked table representation as
  `BJobCatalog`, `BJobData0-14`, `BJobChecks0-14` (namespace `BroaderJobData`),
  and `BroaderHierarchyData`/`BroaderHierarchy`. Data model, row-check and
  hierarchy templates follow the original scalar generators verbatim except for
  names, certificate-read job links and the width-2 root (bound 636).
* `stage2/BroaderRoot.lean`: the root bridge. `root2` is the bit-bounded
  restriction of `lift ScalarRoot.root` to the fifteen return states;
  `root2_realization` (kernel `decide`) embeds it into `BroaderJobData.data0`
  (same fields; the induced lift edges are exactly the 23 stored edges);
  `returnIn_root` (kernel `decide`) shows every state on a return path is one of
  the fifteen; `actual_broader_root_path` turns `R` returns into an actual path
  of `7R+1` vertices in that graph at spatial width 2, via stage 1 and the
  existing `ScalarRoot.actual_two_column_path`, `actual_path_select`,
  `BoundedPrefixLift.actual_path_encode`.
* `BroaderHierarchy.finite_root_bound` (row checks + `ActualJobFamily`) gives
  `7R+1 <= 636` at width at least 14; `BroaderBound` adds the warm-up.

Build (`stage2/verify_stage2.py` = stage-1 driver + these modules), in a copy of
the verified stage-1 build directory:
`--stage checks --resume` CHECKS_PASS (79 modules; all 32 broader data/check
modules compiled fresh; BJobChecks7/8 about 1550 s each) and `--stage final
--resume` PASS: **92 modules, 5,511 theorems**, axiom union
`{propext, Quot.sound, Classical.choice}`; no `ofReduceBool`/`sorryAx` in either
audit log. Report `stage2/verification.json`, logs `stage2/compile.log`,
`stage2/evidence/`.

Audit-file note (recorded failure, not a proof issue): the single combined
5,511-statement `AllAxioms` file aborted with "Stack overflow detected" twice
(also with `ulimit -s unlimited`; the frontend thread stack is separate).
Each half passes alone (`evidence/diagnostic_split_*.log`). The driver therefore
splits the identical audit by namespace into `AllAxiomsScalar` and
`AllAxiomsBroader` (same imports and flags) and requires the union of parsed
records to equal the expected theorem list. The failed attempt's file, log and
driver output are retained in `stage2/evidence/`. A theorem named
`fields_checked'` was renamed `fields_table_checked` (and likewise for edges)
because the driver's audit-name regex does not accept primes.

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
