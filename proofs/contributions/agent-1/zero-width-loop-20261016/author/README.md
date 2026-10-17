# Explicit zero-phase width loop

Author: Agent1 specialist `/root/research_status/numeric_bridge_review`.
Claim accepted at coordination commit
`8a8e6b9d748cbd25892e4836ff1a25fc55a78ca2`.
Worktree baseline: ReturnCore `946c69e` with the existing WidthLift sources.

Frozen mathematical source: `proofs/Agent1PeriodicZeroWidthLoop.lean`.
SHA256: `e00095f228fc552a3c870d84abdaa68dbaf720778ddcebd529d999c31fd5d2bd`.
Git blob: `46ca7616fb83d2cb28fc7240492a47d57136be03`.

## Exact mathematical scope

The module imports only `Agent1PeriodicWidthLift` and
`Agent1PeriodicZeroPath`. Their literal dependency union has 36 existing
modules, hence 37 including the new source. OuterRank, ReturnCore,
CondensationBound, ordinary WidthNumeric, and ReturnClock are not imported.

The two definitions expose the complete finite witness:

* `zeroWidthNode t` has zero phase, outside 9 at even indices and 18 at
  odd indices, and residue `(2 + t / 2) % 8`.
* `zeroWidthEdge t` lifts the corresponding literal clock-zero edge from
  outside 9 to 18 or clock-one edge from outside 18 to 9.

Eleven public theorems check edge membership; all sixteen exact sources,
targets, clocks, and `none` carry labels; vertex membership; endpoint
closure; clock sum eight; original validity of `([9],[],[0,0,0,0])`;
its exact initial projection; and its positive canonical decimal realization
with all original in-range column sums at copy count three.

`zeroWidthLoop_certificate` bundles the complete labelled walk.
`zeroWidthLoop_no_full_return` applies the existing ZeroPath theorem to
every positive exact quotient path whose full initial tuple is that
original-valid tuple. `zeroWidthLoop_projection_not_sufficient` places
finite closure and canonical initial realization alongside this universal
full-return impossibility at the same initial projection.

The chosen graph edges are not asserted to be the actual quotient orbit.
The original catalog also has a different clock-one edge from zero phase,
outside 9, to outside 10. Listed membership alone cannot select the actual
incoming carry. No source here claims safety, nonpalindromicity, an infinite
ordinary orbit, SCC information, or an affirmative finite-interface return.

## Actual author checks

Official Lean 4.19.0, commit `6caaee842e94`, was run with
`--trust=0 -j1 -DElab.async=false`. Each invocation has a 600-second bound
and a 1500 MiB RSS watchdog sampled every 10 ms; no virtual-address cap is
used. Exact commands, compiler hash, source snapshots, dependency source
and object pins, and actual results are retained for every attempt.

| Invocation | Result | Seconds | Kernel peak RSS, KiB |
| --- | --- | ---: | ---: |
| attempt-001 | FAIL | 0.56 | 445132 |
| attempt-002 | PASS | 0.52 | 452948 |
| audit-001 | PASS | 1.49 | 768288 |

The first attempt lacked `Decidable` instances for three existing `Bounded`
goals in the original-validity constructor. Its log accurately retains
Lean's error-recovery `sorryAx` propagation. The successful source supplies
those three fields directly with `simp [Bounded]`; no theorem statement,
original predicate, or imported source changed. No watchdog fired.

These are author increments, not fresh dependency rebuilds. All 36 reused
objects came from the successful fresh parent ReturnCore and Width builds.
The driver checks each registry source hash, Git blob identity, literal
imports, working source, retained fresh-build source, successful build
report, compiler identity, and object hash, both before and after checking.
The private `dependencies/` directory is only a local object/source cache
and is ignored for publication. Its complete identities are in every
`source-and-dependencies.json`.

The audit prints exact types and axiom lists for all 13 public declarations
(two definitions and eleven theorems). It independently enumerates every
constant originating in the new module and traverses the logical axiom
chains of all 13 theorem constants, all four safe definitions, and zero
safe opaques. The actual union is exactly the standard three:
`propext`, `Classical.choice`, and `Quot.sound`. Generated unsafe compiler
implementations are inventoried separately; none is a theorem or an
additional logical axiom. `audit-001/origin-summary.json` records exact
inventory counts and export coverage.

`SOURCE_SCOPE.md` is the unchanged preclaim source-only scout, SHA256
`c66c28545ac6c67d7b1423e26261f8944b23791af1360785d92ccccb5197393a`.
No source or Git writes outside the assigned module and author evidence
directory were performed. Parent publication and the independent full
37-module fresh check remain separate gates.
