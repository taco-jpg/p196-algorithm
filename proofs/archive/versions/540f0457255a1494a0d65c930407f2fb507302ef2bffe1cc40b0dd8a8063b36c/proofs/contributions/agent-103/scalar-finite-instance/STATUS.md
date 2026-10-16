# Agent #103 — scalar finite-certificate Lean instance (WIP)

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
