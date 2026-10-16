# Periodic pointwise realizability: author receipt

Claim: `d5786f691f77c606f7343b1182cc67643f058a8f`, task `agent1-periodic-realizability-20261016`. Author is the genuine Agent #1 specialist `/root/symbolic_scope`. Parent is the sole Git writer. This evidence does not claim independent review or a fresh dependency build.

Frozen source: `proofs/Agent1PeriodicRealizability.lean`, SHA256 `cfa1fb0e7562976600e8f56e15d5ee9970979757eacb77c00c80df3de3625953`, Git blob `68a7b98e7d7ea9078c27a5df85061bcad994ce99`.

The two public endpoints are `Agent1.Periodic.periodicWord_admissible B H w k hv hk` and `Agent1.Periodic.periodicWord_realizable B H w k hv hk`, for the unchanged `ValidPeriodic B H w` and `0 < k`. The second returns positive `n`, original `DecimalDigits.Canonical n d` at the exact periodic-word length, and every in-range original `DecimalDigits.columnSum`. It directly invokes the already proved `FoldedDecimal.valid_word_realizable`. The first reuses `periodicWord_canonical` and `middle_append_eq`; no generic realizer, decoder, or symmetric-list decomposition was recreated.

This is pointwise in `k`. There is no exponent-independent seed, initial nonpalindromicity, safe successor closure, orbit-cycle obstruction, or infinite-orbit result in this module.

## Actual execution

Official Lean 4.19.0, compiler identity in `compiler.json`. Seventeen existing dependency source/object pairs were checked against the exact Validity registry and copied into the isolated author build. Their source and reused-object hashes are all in `reused-dependencies.json`; this is explicitly an incremental author check. No new dependency compilation is claimed.

* `attempt-001`: actual failed source and complete compiler log retained. A rewrite could not see the indexed list expression beneath a beta-redex. The compiler's error-recovery `sorryAx` output belongs only to this rejected attempt; it is not accepted evidence.
* `attempt-002`: source unchanged after this success; exit 0 with `--trust=0 -j1 -DElab.async=false`. Both exported axiom reports contain only `propext` and `Quot.sound`.
* `audit-001`: exit 0 with the same strict compiler options. Every safe constant originating in the new module was transitively audited, including generated proof helpers: 5 theorem constants, 5 safe constants total, 0 unsafe implementation constants. Axiom union is exactly `propext` and `Quot.sound`. Unknown axioms and new axiom declarations are rejected by the audit program. Full theorem prints follow the audit in its log.

## Reproduction

The actual preserved command for each source attempt is in its `result.json`; `run-attempt.py` copies the exact source into a new attempt directory before compilation and refuses to overwrite that directory. It uses the explicitly recorded isolated author build `/workspace/p196-agent1-session-20261016/periodic-realizability-author-build` and its 17 pinned prior objects. For another incremental run from this worktree:

```sh
python3 proofs/contributions/agent-1/periodic-realizability-20261016/author/run-attempt.py attempt-003
```

For a fresh closure replay, the parent should use the existing 17-module Validity registry plus this module, copy sources under their import filenames, and compile dependencies in import order before the new module and the preserved audit. The later combined package registry/review will supply that full replay; it is not asserted by this author receipt.

All accepted source remains free of `sorry`, `admit`, new axioms, `native_decide`, and `Lean.ofReduceBool`. Original arithmetic and validity definitions are unchanged.
