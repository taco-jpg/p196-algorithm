# Acceptance after the independent execution gate

**Accepted for the exact abstract strip statements and the explicitly listed
compiled scope fixtures below.** No semantic defect was found in the original
abstract theorem. An ordinary-integer 6/12 return exclusion remains unproved
by this package.

This addendum follows the separate executor's stable PASS and preserves the
initial eight semantic artifacts and the static repair without modification.
The initial report's pending-compilation language remains a historical record;
this addendum supplies the later acceptance decision.

## Source and execution checked

The accepted Agent4 source is
`proofs/agent4/temporal_strip/NoAlternatingReturn.lean`, at commit
`5bd98567b259659fd3195f5aa61617422aa80914`, SHA256
`49b1065166c02c2efd1bf58c3391c5166b44106f12e82af371304e9fe3ae7ba0`.
The reviewed fixture sources were published at
`81019eda501af5194a0e43b98458c268a71f5729`.

The separate executor freshly compiled the strip source with official Lean
4.19.0, commit `6caaee842e94`, through the documented transparent path adapter.
The original audit covered all 35 local theorem constants, including generated
ones, and retained the exact elaborated type and raw `Expr` for each of the
seven explicit exports.

The auxiliary stage reused only that independently rebuilt strip object. It
freshly compiled `LychrelDigitSums`, `ExactTypesApplied`, `ScopeTests`, and
`ActualMapObligations`, then audited the complete five-module closure: 1,060
theorem constants. All compiler and audit exits were zero. No existing author
project object was used. Official toolchain objects were used and rehashed;
this review does not claim a fresh bootstrap of Lean or a new archive download.

The semantic reviewer independently read the seven elaborated types, checked
the corresponding source headers and successful explicit type applications,
and reparsed both raw axiom logs. Every enumerated theorem matched the reported
module, name, and axiom set. The reviewer also independently rehashed all five
source snapshots against their published Git objects, five local objects,
1,303 imported official objects, nine compiler/adapter fingerprints, and all
40 entries of the executor's frozen evidence manifest. All checks matched.
The original checkout does not contain the Agent4 strip file; its source pin
was verified through its Git object and the immutable execution snapshot.
No Lean process was run by the semantic reviewer.

All theorem dependencies are subsets of `propext`, `Classical.choice`, and
`Quot.sound`. The original strip has no unsafe implementation axioms. The full
closure records 44 generated unsafe implementation declarations; none is in
an accepted theorem's transitive dependency list. No safe custom axiom,
`sorryAx`, or native-evaluation axiom appears in those proof dependencies.

## Accepted mathematical scope

All names in the following list are in `P196.Agent4.TemporalStrip`:

* `left_scalar` and `right_scalar`: the exact two-case classifications under
  their displayed scalar arithmetic assumptions.
* `left_backward` and `right_backward`: aligned cuts propagate one spatial
  column backward for valid cuts and the complete column equations, with
  an onto temporal successor.
* `cyclic_successor_onto`: successor modulo every positive `N` is onto.
* `no_alternating_six_twelve_strip`: no finite spatial strip with those
  equations connects the specified outside cut to either uniformly aligned
  tail, for an inhabited temporal type with onto successor.
* `no_finite_alternating_six_twelve_strip`: the specialization to `Fin N`
  with `N > 0`, at arbitrary finite spatial width, including width zero.

The finite temporal interpretation is **2N ordinary updates**, grouped as
nonoverflow then overflow. Temporal closure is built into the cyclic column
equations. The theorem allows every such positive period and spatial width;
it does not cover arbitrary overflow schedules or open forward trajectories.
The tail is one uniform alignment over all temporal indices, not a separately
chosen disjunct at each time.

The seven declarations in `Agent104.TemporalStripExactTypesApplied`, named
after these exports with suffix `_type`, compiled and were axiom-audited.
They verify the exact applications of the original source statements and
are not additional mathematical advances.

## Accepted compiled scope fixtures

The following are the complete named fixtures accepted from `ScopeTests.lean`.
Their common namespace is `Agent104.TemporalStripReview`.

| Fixture meaning | Exact identifiers |
| --- | --- |
| Empty temporal type makes every cut predicate vacuous | `empty_index_predicates` |
| Consistent left-aligned interior | `left_stationary_valid`, `left_stationary_aligned`, `left_stationary_column` |
| Consistent right-aligned interior | `right_stationary_valid`, `right_stationary_aligned`, `right_stationary_column` |
| Outside cut is valid and conflicts with either tail | `exterior_valid`, `exterior_outside`, `exterior_not_aligned` |
| Left backward implication fails without onto on the explicit `Nat.succ` arrays | `left_open_source_valid`, `left_open_target_valid`, `left_open_target_aligned`, `left_open_column`, `left_open_source_not_aligned` |
| Right backward implication fails without onto on the explicit `Nat.succ` arrays | `right_open_source_valid`, `right_open_target_valid`, `right_open_target_aligned`, `right_open_column`, `right_open_source_not_aligned` |

These fixtures have either no axioms or only `propext`. The open-time fixtures
concern the backward lemmas; they do not assert that onto is a logically
minimal hypothesis of the complete outside-to-tail impossibility theorem.
The literal `15 -> 66 -> 132` scope control remains an independently checked
finite Python diagnostic, not one of these compiled Lean fixtures.

## What remains unproved

The compiled declarations
`Agent104.TemporalStripObligations.ActualPrefixTransportObligation` and
`Agent104.TemporalStripObligations.UniformBandTailObligation` are **definitions
of propositions, not proofs of those propositions**. The audit explicitly
checks their declaration kind and reports `defnInfo` with type `Prop`.
The single generated theorem constant in that module proves a bound needed
to construct the cyclic `Fin` successor; it proves neither contract.

Ordinary-number applicability still needs actual carry transport using each
step's changing width, including prefix closure at time `2N`; a common
interior cut giving the uniform aligned tail; and a template/certificate
argument supplying those conditions while preserving all gap guards. The
existing three-column whole-word bridge does not discharge these obligations.
No ordinary 6/12 return exclusion, certificate exclusion, Lychrel existence
result, or P196 conclusion is accepted here. Agent4 retains mathematical
ownership of the theorem and possible extensions.

## Evidence and preserved repair history

The machine-readable scope decision and independently checked pins are in
`acceptance.json`. The executor's raw records are retained under the sibling
`execution/` directory:

* `attempt01/verification.json` and `attempt01/logs/StatementDump.log`;
* `attempt01/logs/AllLocalTheorems.log`;
* `auxiliary-attempt01/verification.json` and `AllFiveModulesAudit.log`;
* `auxiliary-attempt01/source-pins.json`, `acceptance.json`, and
  `final-manifest.sha256`.

The original `ExactTypes.lean` remains uncompiled and unchanged. Its omitted
explicit argument applications were detected statically before execution;
`ExactTypesApplied.lean` is the separately recorded successful replacement.
The status remains `STATIC_REPAIR_NOT_COMPILER_OBSERVED`, with no invented
compiler failure. The repair affects only the review harness.
