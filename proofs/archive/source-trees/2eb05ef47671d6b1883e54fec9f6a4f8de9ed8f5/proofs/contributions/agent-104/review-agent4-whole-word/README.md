# Agent 104: independent review of the actual three-column bridge

**INDEPENDENTLY-REVIEWED.** The six `P196.Agent4.WholeWord` exports at
`4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7` passed separate semantic review,
a fresh five-module dependency build, and a complete transitive axiom audit.
All six exports use exactly `propext` and `Quot.sound`. The full 1,092-constant
dependency audit permits only those axioms plus `Classical.choice`.

The reviewed result applies to an actual return of the first three symmetric
digit sums under the explicit saturated-width-growth equation. It concludes
that the return time is divisible by eight. Its ordinary-number specialization
uses the actual canonical endpoint. It supplies no such return or growth
condition for 196 and gives no infinite-orbit existence result.

The kernel-checked review illustrations are
`P196.Agent104.Agent4Review.saturated_return_89870` and
`P196.Agent104.Agent4Review.nonsaturated_return_770`. The first gives an actual
eight-step return with the required growth. The second gives a seven-step
return without that growth, demonstrating why the growth hypothesis cannot
be dropped. Their exact canonical digits, widths, orbit values, and prefix
equalities are in `semantic/ReviewScopeWitnesses.lean`; all 24 compiled theorem
constants in that module passed the audit. These are scope illustrations,
not claims of novelty or major new theorem counts.

See [completed acceptance](execution/acceptance.md),
[machine-readable acceptance](execution/acceptance.json), and
[semantic review](semantic/SEMANTIC_REVIEW.md). The earlier pending/preflight
records are preserved unchanged and are superseded by the completed acceptance
for these exact pins. Python diagnostic enumerations remain diagnostics.

Reproduction commands and source/toolchain pins are in the execution reports
and runners. Use official Lean 4.19.0, fresh build directories, and one compiler
process for the five-module replay. The scope check explicitly reuses that
freshly built dependency set. Toolchain archive provenance is inherited and
disclosed; every imported official object was rehashed during this review.

Task `agent104-review-agent4-whole-word` was published through the shared
coordination branch before investigation. Original authors' proof files and
shared indexes were not modified. This review's evidence is published on the
Agent 104 contribution branch and awaits default-branch integration.
