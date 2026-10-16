# Agent 104 independent review of real safe incoming weights

Status: **INDEPENDENTLY-REVIEWED**. The independent hosted build and the
separate semantic review passed. This review accepts exactly the 15 original
`Agent13SafeWeights` exports in `Weights.lean` and `SqrtBound.lean`, with
their stated hypotheses. Agent 13 retains ownership of those results and
ongoing product/buffer extensions.

For the ordinary decimal reverse-and-add map, the accepted incoming sum
contains every actual safe predecessor. Here `Safe n` means that `n` is
positive and both `n` and its next iterate are nonpalindromic. For real
weights strictly positive and nonincreasing only on this safe set, the
theorems give growing incoming-weight ratios at explicit safe targets, a
strict square-root lower bound, and a counterexample to every proposed
uniform real multiplier. The actual target safety and the positivity needed
for division are proved. This excludes the specified weight method; it
does not prove an infinite safe orbit or settle 196.

The exact source is `122367d4935f0b4cd9e0bee19e4121ec66b3164b`. The independent
type harness was first published at `ab6768ef000358b5f81c6807db674dc7515819c9`.
Review runner `39d9f3eb196aae5071b5c48e8a5166dad388ce9d` executed in
[GitHub Actions run 38700059129](https://github.com/taco-jpg/p196-algorithm/actions/runs/38700059129),
attempt 1. All six original modules and the harness were built in an empty
project, and all 19 recorded commands exited zero. The full audit covers
1,129 compiled original-closure theorem constants plus 15 exact-type
applications, including generated and private declarations. These are audit
coverage counts, not additional mathematical results. All accepted transitive
dependencies use only `propext`, `Classical.choice`, and `Quot.sound`.

Lean is pinned to official 4.19.0 (`6caaee842e94`), and Mathlib to
`c44e0c8ee63ca166450922a373c7409c5d26b00b` with its exact manifest and package
commits. **The official compiled Mathlib dependency cache was reused; no
Mathlib source rebuild is claimed.** The hosted checker verified all actual
imported object paths, hashes, and corresponding committed cache sources.
The downloaded artifact contains all seven fresh local objects but not the
external cache objects; post-download local rehashes are limited accordingly.

The execution reviewer verified the actual artifact and raw audit. A
separate semantic reviewer checked all 15 elaborated and raw theorem types,
all 1,144 axiom records, source identities, local object bytes, and artifact
inventories. The semantic reviewer did not execute Lean. The artifact ZIP
and all 56 member bytes were checked; substantive logs are preserved without
modification. The original author's run `38688269514`, recorded in
`prior-author-evidence.json`, remains separate prior evidence.

The frozen acceptance and replay material is:

- [Execution acceptance](execution/acceptance.md) and
  [machine-readable record](execution/acceptance.json).
- [Independent semantic acceptance](semantic/ACCEPTANCE_ADDENDUM.md) and
  [exact accepted names and scope](semantic/acceptance.json).
- [Complete publication inventory](execution/publication-manifest.json),
  [original artifact exclusions and recovery](execution/artifact-selection.json),
  and [recovery script](execution/recover_hosted.py).
- [Actual run provenance](hosted-run-provenance.json) and
  [integration handoff](INTEGRATION.md).

The original 16-file execution preflight and eight-file semantic checkpoint
remain unchanged; their pending labels describe those historical checkpoints
and are superseded by the acceptance addenda. Finite diagnostics and prose
examples are not additional accepted Lean theorems. The remote task is
`agent104-review-agent13-real-weights`, originally claimed at coordination
commit `ac825edf3e77ce40aa6cf9d4b45913feb66cff9d`.

This is a review contribution. The original source is proposed in PR #29
and is absent from main `02aa80d7939c2cbdb6290a026a00a9142b236c28`; integration
requires that source package and the explicit Mathlib dependency registration
described in `INTEGRATION.md`. This review does not reserve integration
ownership or change shared indexes.
