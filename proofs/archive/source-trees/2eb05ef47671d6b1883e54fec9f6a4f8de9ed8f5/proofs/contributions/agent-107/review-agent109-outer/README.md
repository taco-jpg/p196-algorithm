# Agent #107 — independent review of the actual outer projection bridge

**Status: INDEPENDENTLY-REVIEWED — PASS for the exact mathematical statements.** Two nonblocking documentation qualifications are recorded below. This is replication and review of Agent109’s result, not a new theorem claim.

Reviewed source: `b2374410d427beb78fc601ee81cf15e34a1ac934`. Published review claim: `241d17f64de0495ecad32d2cc2aa68b467748b63`. [SCOPE.json](SCOPE.json) pins the nine-module source closure.

The endpoint `Agent109.OuterCompat.lychrel_cap2_exit` connects Agent7’s finite exterior certificate to the repository’s ordinary `Lychrel196.orbit`. With the exact bounded-block, even-phase, valid initial exterior and actual template-representation hypotheses, initial exterior length at most two and both bands at least 14 imply that the computed exterior coordinate has length greater than two at some time at most seven. This is a statement about the specified template coordinate, not escape from every possible template representation.

## Independent evidence

- [Semantic review](SEMANTIC_REVIEW.md): actual integer/width correspondence, real carries, phase and validity conditions, seven-step band budget, noncircular hypotheses and representation scope. This specialist did not execute Lean.
- [Signed execution review](execution/EXECUTION_REVIEW.md) and [fresh execution manifest](execution/agent107-outer109-clean-syq1jnqb/manifest.json): a separate specialist compiled all nine modules sequentially from an empty directory using official Lean 4.19.0 `6caaee842e94`; no project object was reused. Complete compiler logs and an independently implemented harness are retained under `execution/`.
- [Complete target axiom audit](execution/agent107-outer109-clean-syq1jnqb/audit-all-exported.stdout.log): all 23 exported theorems in OuterBridge, OuterCompat, OuterFinite and OuterBounds pass. The transitive union is only `propext`, `Classical.choice`, `Quot.sound`; the finite cap-two certificate uses kernel reduction and has no axioms. These are audit counts, not counts of new independent results.
- [Exact-integer controls](controls/README.md): 10,944 realized trajectories, 76,608 literal reverse-and-add updates, zero failures. Complete deterministic trajectories are losslessly retained. These finite controls supplement the Lean evidence and establish no additional accepted theorem.

Both vendored Agent7 modules are byte-identical to upstream `da4a1799b74b98b4199cdb224ea7a694b2657651`. The nine reviewed sources match the pinned commit, and the source checkout remained clean before and after execution. Standard logical axioms are explicitly accepted; no incomplete proof, new mathematical axiom, native_decide or compiler-evaluation oracle occurs in the checked dependency chain.

## Documentation qualifications and handoff

`OuterBridge.lean` has stale comments saying band length 16; its formal endpoint and README correctly use 14. The generic `actual_outer_orbit` description also needs to distinguish an arbitrary initial exterior from the maximally trimmed positive-time exteriors. Initial validity already supplies this distinction in the cap-two endpoint. [PROPOSED_DOC_FIX.patch](PROPOSED_DOC_FIX.patch) is an unapplied, comment-only suggestion for the owner; no author source has been changed. The exact theorems need no correction identified by this review.

The optional return-certificate cycle corollary in Agent109’s task remains unfinished and outside this review. Larger exterior caps remain separate computational work. No cycle, infinite palindrome-avoiding orbit, decimal Lychrel existence or claim about 196 follows here.

The integration owner may cite this package when reviewing the pinned outer extension of PR #23. This contribution does not modify Agent109’s task record, the default branch or shared accepted-build indexes. See [REPRODUCE.md](REPRODUCE.md) for commands, runtime limitations and retained evidence.
