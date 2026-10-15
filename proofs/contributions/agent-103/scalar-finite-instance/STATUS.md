# Agent #103 — scalar finite-certificate Lean instance

**Status: LEAN-CHECKED (fresh build, full transitive axiom audit PASS).
Independent review pending (Agent #9 replay, issue #13). Not yet INTEGRATED.**

## Result

With the v2 table representation (same values as the original package's
tables; see below), the complete scalar finite-certificate chain compiles from
an empty build directory, and every one of the 2,813 theorems declared in the
54 project modules has transitive axioms within `{propext, Quot.sound,
Classical.choice}`. No `sorryAx`, `Lean.ofReduceBool`/`native_decide`, or
custom axiom appears anywhere in the audit log, including transitively from
the base file.

Newly unconditional Lean theorems (all `[propext, Classical.choice, Quot.sound]`):

| Declaration | Statement (informal; exact Lean in the cited files) |
|---|---|
| `ScalarHierarchy.finite_root_bound` | For `Admissible L q`, `14 <= L`: an `ActualPath` of the finite root graph `data0` at width 1 has `n <= 659` vertices. |
| `ScalarBound.root_vertex_certificate` | Discharges `ScalarPeriods.RootVertexCertificate` (the explicit premise of the accepted conditional wrappers). |
| `ScalarBound.wide_periods_le_94` | If the actual pair orbit has width `>= 14` at time `a` and its outermost coefficient follows the seven-phase scalar clock for `7R` steps from there, then `R <= 94`. |
| `ScalarBound.initial_width_dependent_bound` | From time 0: `R <= 94 + warmup L`, `warmup L = (14-L+2)/3`. |
| `ScalarBound.periods_le_98` | Any admissible word, any start time and phase: `R <= 98`. |
| `ScalarBound.canonical_periods_le_98` | Same for the pair word of any canonical decimal integer. |
| `ScalarBound.no_99_period_clock`, `wide_no_95_period_clock` | No `ClockSegment` of `7*99` steps (resp. `7*95` at width `>= 14`). |

Meaning and scope: `ClockSegment q L a s n` says the outermost pair
coefficient of the actual reverse-and-add pair-word orbit (`iterPairs`)
equals `ScalarClock.phase (s+i)` for `i = 0..n`. These are finite-horizon
obstructions to one specific recurrent mechanism. They do **not** prove that
any orbit reaches a palindrome, that 196 is or is not Lychrel, or that a
decimal Lychrel number exists.

Build: `v2/verify_v2.py --stage checks` (fresh, empty directory, 47 modules,
0 reused) then `--stage final --resume` in the same directory (7 new modules
+ `AllAxioms`; the 47 resumed objects are this build's own, admitted only
after the unchanged source/object/log/dependency fingerprint check). Report:
`v2/verification.json` (status PASS, checker SHA-256
`3bac9996...09225`), full concatenated logs `v2/compile.log`, raw
`v2/AllAxioms.log`, manifests, driver stdout, `v2/SHA256SUMS`. Compiler:
official Lean 4.19.0 `6caaee842e94`, executable SHA-256 `92c3d35b...e023`,
flags `-j1 -DElab.async=false`. Wall time: checks stage about 82 min on two
workers, final stage about 4 min.

Reproduce (from a checkout of this branch):

```sh
python3 proofs/contributions/agent-103/scalar-finite-instance/v2/check_v2_equivalence.py
python3 proofs/contributions/agent-103/scalar-finite-instance/v2/verify_v2.py \
  --lean /path/to/lean-4.19.0/bin/lean --build-dir /empty/dir --stage checks
python3 proofs/contributions/agent-103/scalar-finite-instance/v2/verify_v2.py \
  --lean /path/to/lean-4.19.0/bin/lean --build-dir /empty/dir --stage final --resume
```

(`check_v2_equivalence.py` needs `sys.setrecursionlimit` raised, e.g. run via
`python3 -c "import sys,runpy;sys.setrecursionlimit(100000);runpy.run_path('...',run_name='__main__')"`.)

---

# History

Task: `agent103-scalar-finite-instance` on `p196/coordination`.

Status: **WIP. No new theorem is claimed.**

Goal: finish the frozen package
`proofs/contributions/2026-10-15-scalar-finite-certificate-formal/` with a
**fresh** build (empty build directory, no reused objects) of every data and
production row-check module, then the `final` stage (hierarchy composition,
`RootBridge`, `ScalarBound`, transitive `#print axioms` audit).

If it passes, `ScalarHierarchy.finite_root_bound` (actual scalar-root path has
at most 659 vertices when the starting width is at least 14) discharges the
explicit `ScalarPeriods.RootVertexCertificate` premise, giving unconditional
Lean statements `ScalarBound.periods_le_98`, `no_99_period_clock`,
`wide_periods_le_94`. These are finite-horizon structural bounds on the
outermost pair coefficient following the prescribed seven-phase scalar clock.
They do not prove that 196 or any seed is Lychrel.

Environment: official Lean 4.19.0 release tarball
(`lean-4.19.0-linux.tar.zst`, SHA-256
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`, matching
the hash other agents report for the Actions artifact), `lean --version`
commit `6caaee842e94`. Unmodified package driver `verify.py`, flags
`-j1 -DElab.async=false`, `--stage checks` first.

Progress log (fresh build, seconds):
- LychrelDigitSums 83.6, ScalarClock, ActualScalar, ScalarOrbit,
  PrefixExtension, ActualPrefixLift, FiniteGraph, RankRows, JobCatalog: PASS
- JobData0–JobData4: PASS (0.3, 1.7, 8.0, 3.2, 5.8)
- JobData5 21.4, JobData6 333.2, JobData7 1033.3: PASS
- JobData8 onward: running. Elaboration time is roughly quadratic in table
  size (each table is one nested `if` term of up to ~190 KB per line); the
  1.7 MB modules are expected to take about an hour each on one core.

Development-only probe (separate directory, NOT production evidence, objects
copied from the production build): `JobChecks0`–`JobChecks5` compile with
exit 0 (0.3, 6.0, 34.1, 17.8, 28.9, 96.4 s), consistent with the original
author's development checks. These do not count as production row checks;
the driver recompiles every `JobChecks` module itself.

### Development shadow with `decide +kernel` (NOT production evidence)

To surface row-check failures early, a second core compiles copies of the
generated `JobChecksN.lean` in which the final tactic `decide` is replaced by
`decide +kernel` (kernel-only reduction; still no `native_decide`, no
compiler-trusted evaluation). On JobChecks6 rows this is about 2x faster
(edge chunk 11.4 s vs 21.2 s). Result so far: every row theorem of
JobChecks0-6 is accepted (JobChecks6 in 722 s). The production acceptance
remains the unmodified generated sources compiled by the unmodified
`verify.py`; the shadow only gives early warning and would be used, after
the shadow finishes, to dry-run the never-compiled final-stage drafts
(`ScalarHierarchy`, `RootBridge`, `ScalarBound`).

## Finding: the original package cannot build JobData8 (v1 attempt FAILED)

The unmodified fresh build (`v1-attempt/`) passed every module through
`JobData7`, then **`JobData8` failed after 3837 s** with
`(deterministic) timeout at isDefEq, maximum number of heartbeats (200000)`
while elaborating `nextCodes8` (one ~600 KB nested `if` term on a single
line), followed by `unknown identifier 'nextCodes8'`. The original author's
run had stopped at JobData6, so this module had never been built. The full
driver output, final manifest and the JobData8 log are retained in
`v1-attempt/`. The original package therefore needs a change before its
endpoints can be accepted; this is not an environment problem.

## v2: same tables, chunked representation (`v2/`)

* `generate_scalar_data_v2.py` imports the original generator's pinned
  `models()` unchanged and only replaces the Lean representation of each
  lookup table: chunks of at most 256 entries, each its own small `def` with
  the same balanced comparison tree on absolute indices, plus a balanced
  dispatch tree on chunk starts. Maximum line length drops from 607,767 to
  7,705 characters.
* `check_v2_equivalence.py` (standalone parser/evaluator, no code shared with
  either generator) confirms that for all 16 jobs every table agrees with the
  original emitted table at every index `0..N+16` (391,915 evaluations), that
  alias definitions are identical, and that every non-table line is
  byte-identical. Result: `v2_equivalence.json`, PASS.
* Soundness does not rely on this equivalence: all local graph, rank and
  lift conditions are re-proved by the kernel from whatever the tables
  contain, and `RootBridge` checks `data0` against the semantic root by
  `decide`. The equivalence only preserves provenance to the reviewed tables.
* Development timings (not production evidence): v2 `JobData6` < 1 min
  (was 333 s), v2 `JobData8` about 3 min (v1 timed out after 64 min); the
  **unmodified** generated `JobChecks6` proofs pass on v2 data in 517 s
  (edge chunk 4.6 s vs 21.2 s on v1 tables).
* `verify_v2.py` is a copy of the original `verify.py` whose only changes are:
  JobData sources from `v2/generated`, reports written under `v2/`, and up to
  two concurrent compilations of modules whose imports are already
  validated. Fingerprinting, reuse predicate, sorry/axiom token scan, final
  revalidation and the transitive axiom audit are unchanged. Row-check,
  hierarchy, bridge and endpoint sources are the original files.

Current: fresh v2 production build (`--stage checks`) running.

### v2 production progress (fresh build, `verify_v2.py --stage checks`)

All 16 v2 `JobData` modules and the previously never-compiled
`ScalarHierarchyData` PASS (seconds): JobData0 0.303; JobData1 1.787; JobData3 3.429; JobData2 6.55; JobData4 4.597; JobData5 11.908; JobData6 60.741; JobData7 105.682; JobData8 184.481; JobData10 21.814; JobData9 183.322; JobData11 75.744; JobData12 72.102; JobData14 9.611; JobData15 6.923; JobChecks0 0.458; JobChecks1 7.835; JobChecks2 34.949; JobChecks3 17.85; JobChecks4 29.741; JobData13 165.791; ScalarHierarchyData 2.564; JobChecks5 75.689.
Row checks JobChecks6-15 running. No endpoint accepted yet.

### Final (00:51 UTC-7)

Checks stage: CHECKS_PASS, 47/47 modules (JobChecks0-15 all PASS; largest
JobChecks13 1301 s, JobChecks8 1583 s, JobChecks9 1579 s). Final stage:
ScalarHierarchy, ScalarRoot, WidthOne, ScalarPeriods, RootBridge, ScalarBound
PASS; AllAxioms PASS in 191 s; overall PASS, 2,813 theorems audited.
