# Actual all-nine periodic branch: author receipt

Protected phase-catalog claim `6db01dafab1ec876d24c9964bc6086440ed21266`, issue61 receipt6226044951. Genuine Agent #1 specialist `/root/symbolic_scope` owns only `proofs/Agent1PeriodicNines.lean` and this evidence. Parent is sole Git writer; the non-nine phase and catalog modules have separate authors.

Frozen source SHA256 `b8aae1033e8e90c78f48888ea698e5d345c21e6b99970842dc5a9f3341cd193c`, Git blob `fc4b17311a291870b122ff97e3618fb7452e978e`.

## Exact scope

For arbitrary original bounded exterior B and center H, the three exports in `Agent1.Periodic` are:

* `rightEntry_nines B H hB`: `rightEntry B H [9,9,9,9] = Agent8.terminalCarry H (leftEntry B)`.
* `nines_entry_bits B H hB hH`: both actual computed entry carries are at most1.
* `rawPeriod_nines B H hB hH`: the original literal output slice is `List.replicate 4 (18 - 9*(leftEntry B + rightEntry B H [9,9,9,9]))`.

Here hB/hH are the unchanged `Agent8.Bounded ... 18` predicates. No center symmetry, positivity, safety, nonempty block, or full validity hypothesis is needed. Empty exterior and center are covered. The expression uses natural subtraction, with the actual bit bounds ensuring the coefficient is one of18,9,0.

The module imports only `Agent1PeriodicGuardFacts`. It uses the existing `raw_blocks_eq_zipper` and actual `scan_carry_le_one`. Both bits are computed by the original finite carry scans; the global clock is exactly `rawGamma B H [9,9,9,9]`, and only its proved zero/one cases are split. No free-clock graph, independent boundary choice, new arithmetic operator, or unfinished Phase module is used. The proof covers every actual case without asserting that every abstract bit combination is realizable by particular valid interfaces.

## Actual execution

The sole mathematical attempt, `attempt-001`, passed on its first execution. Exact source/log/timing/command are retained. Official Lean4.19.0 identity and compiler hash are in `compiler.json`; strict options were `--trust=0 -j1 -DElab.async=false`.

Twenty-six prior source/object pairs were copied from the source-pinned fresh parent zero-escape build at `/workspace/p196-agent1-session-20261016/periodic-zero-escape-parent-clean-001/agent1-periodic-zero-escape/source`. Every source matches its frozen registry hash and every copied object is recorded. The actual imported dependency closure of GuardFacts is eleven modules. This is an incremental author check, not a new fresh dependency replay or independent review.

`audit-001` passed under the same strict options. It audits every new-module-origin safe constant, including private/generated proofs, rejects custom axioms and disallowed transitive axioms, and separately inventories unsafe implementations. Actual totals:11 theorem constants,11 safe constants,0 unsafe implementations. Axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`; both carry-interface exports use only `propext` and `Quot.sound`. Full multiline audit output and full public theorem prints are retained.

## Reproduction

With the explicitly pinned author object directory present, the source-preserving runner can make a new attempt without overwriting prior evidence:

```sh
python3 proofs/contributions/agent-1/periodic-phase-catalog-20261016/nines-author/run-attempt.py attempt-002
```

Actual build directory: `/workspace/p196-agent1-session-20261016/periodic-nines-author-build`. Full fresh replay should rebuild the eleven-module GuardFacts closure, this module and `audit-001/NinesAudit.lean`; the combined catalog build may add its other authored modules. Parent and genuine nonauthor reviewer own that later combined replay. Accepted source contains no sorry/admit, new axioms, native_decide or Lean.ofReduceBool.
