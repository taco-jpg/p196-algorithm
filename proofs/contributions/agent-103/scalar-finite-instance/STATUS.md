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
