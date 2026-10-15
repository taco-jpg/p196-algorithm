# Agent 114: kernel cap-four exterior verification and actual exit bridge

Task: `agent114-cap4-kernel-actual-exit` on `p196/coordination`.
Contribution branch: `research/agent-114/s20261015T1535`.
Pinned upstream source: `eec3d5f3646cab50abad6e610ea19626cd249070`.
Toolchain: official Lean 4.19.0, commit `6caaee842e94`, core + Std only.

## Incremental status

**LEAN-CHECKED supporting interfaces; full cap-four theorem remains WIP.**

`lean/CapCore.lean` adapts a finite escape checker to the unchanged
`P196.Agent7.Finite.outerNext` and `outerIterate`. `ExitBound` is an inductive
proof certificate: its constructors require a checked successor equality at
each transition and an actual exterior-length inequality at the terminal
state. `ExitBound.sound` proves the ordinary finite-iterate interpretation.
`AllRange` and its composition theorem support exhaustive interval coverage.
These are verification infrastructure, not a new dynamical discovery.

`lean/ActualExit.lean`, theorem `Agent114.Exterior.actual_exit_of_check`, proves:
for bounded template blocks, an admissible phase, both initial band lengths at
least twice the checked time bound, and a successful finite exterior check,
the **ordinary integer orbit** has the indicated template representation at an
exit time within the bound. This reuses Agent109's actual-orbit theorem and
retains the explicit finite-certificate premise.

The intended unconditional instance is cap 4 / bound 15. The number 15 and a
sharp exterior `(2,[4,0,1])` already occur in earlier computational work. This
package claims a trust upgrade and actual-map extension, not rediscovery.
The canonical state coverage and the complete finite proof are not yet here.
No accepted return certificate, infinite safe orbit, or result for 196 follows.

## Verification and trust boundary

All nine upstream dependency modules were rebuilt from the pinned text sources
in a fresh local build directory. The current CapCore and ActualExit modules
then compiled successfully with their displayed axiom audits. Allowed axioms
reported by the interfaces are `propext`, `Classical.choice`, and `Quot.sound`;
not every declaration uses all three. This is an author build, not independent
review. The final package clean rebuild and review remain pending.

Two direct Boolean-enumeration strategies exhausted the local memory limit;
their failures do not invalidate the mathematics and are not accepted proof
instances. A proof-producing approach is under development. Candidate
execution may discover values, but only kernel-checked equality proofs may
certify transitions. Native evaluation as a proof oracle is excluded.

Reproduction: stage the pinned upstream `OuterFinite`, `OuterBounds`,
`TemplateStep`, `LychrelDigitSums`, `PeriodObstructions`, `Compat`,
`ReturnCertificate`, and `OuterBridge` modules as in Agent109's
`outer-projection-bridge/build.sh`. Add CapCore and ActualExit from this folder;
compile them in that order with `LEAN_PATH` pointing only to the fresh staging
directory and the official pinned Lean installation. A standalone automatic
rebuild script and complete finite instances will be added incrementally.

## Ownership boundaries

Agent116 owns certificate partial-trim projection and cap-three verification.
Agent110 owns global exterior cycles and certificate return budgets. This task
owns only cap-four kernel verification and its ordinary-orbit extension. Main
integration is not claimed. Independent review is still required.
