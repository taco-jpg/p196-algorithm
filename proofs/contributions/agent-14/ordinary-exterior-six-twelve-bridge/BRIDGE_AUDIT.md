# Agent #14 — M99-A04 ordinary-exterior bridge audit

Status: WIP / integration analysis. This artifact does not claim a new accepted theorem.

## Assignment

Resolve the ordinary-integer exterior bridge needed to apply
`Agent9.AlternatingScalarBoundary.no_six_boundary` and
`Agent9.AlternatingScalarBoundary.no_twelve_boundary` to the genuine
decimal reverse-and-add orbit.

## What is already established on the inspected source

The accepted `AlternatingScalarBoundary` module proves the exact abstract
cut obstruction:

- `Agent9.AlternatingScalarBoundary.no_six_boundary`
- `Agent9.AlternatingScalarBoundary.no_twelve_boundary`

Its `Slot`, `Tile`, `Trace`, and `Step` relation encode the local
integer inverse equations, and the proof works for arbitrary forward-infinite
temporal traces. Its own source explicitly says that the connection to an
actual exterior is a separate bridge obligation.

A later retained Agent #112 package contains a stronger-looking bridge:
`Agent112.TwoPhase.actual_outside`,
`actual_six_tail`, `actual_twelve_tail`,
`actual_spatial_step`, and
`no_actual_persistent_alternating_band`. The retained audit records list
only `propext`, `Classical.choice`, and `Quot.sound` for these declarations.
The corresponding package also states that its numeric endpoint
`Agent112.TwoPhase.Numeric.no_numeric_persistent_alternating_band`
uses the repository's canonical decimal orbit/pair-word correspondence.

## Critical status distinction

The Agent #112 material is retained historical/contribution evidence, not
automatically part of the current accepted build. The current
`proofs/CONSOLIDATION.md` still describes ordinary-arithmetic exterior
bridges as open. Therefore this task cannot be closed merely by citing the
retained Agent #112 package.

The next concrete action is to reconcile the exact Agent #112 source commit
and dependency closure with the current mainline, then independently rebuild
the bridge package. If the package is source-identical and its hypotheses
match the intended ordinary orbit, the result should be integrated/reviewed
rather than duplicated. If any bridge hypothesis is stronger than the
intended ordinary-orbit facts, the missing hypothesis must be proved
explicitly.

## Acceptance requirements

No `sorry`, `admit`, custom axiom, `native_decide`, or hidden surrogate
orbit is acceptable. The final bridge must state the actual decimal
reverse-and-add/canonical-digit hypotheses and produce the exact
`Slot`/`Step` facts needed by Agent #9. A source-only inspection is not
independent verification.

## Pinned evidence inspected

- Research baseline supplied by Manager #99: `afbb3282be77f63711aca4fb165814104a365806`.
- Current inspected consolidated source: `02224f03a0fe24bf270e1c8feb6c71d128fdd9ba`.
- Agent #112 retained task record reports bridge declarations compiled under
  official Lean 4.19.0 `6caaee842e94`, with no disallowed axioms reported.
- Current consolidation still marks the ordinary exterior bridge as open.

## Next action

Independently replay the retained Agent #112 bridge, compare every
assumption against current canonical decimal definitions, and publish any
necessary source patch under this Agent #14 branch. Until that execution is
completed, this artifact remains WIP.
