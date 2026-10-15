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
- JobData5 onward: running
