# PR #118 — Independent evidence reuse assessment

**Decision: the existing independent execution and review evidence is reusable for the complete frozen mathematical contribution at H = 90c639b8a782a9a832bc19f6a6978196e91a3d78. I found no evidence gap requiring a mathematical source repair or another Lean build of that unchanged source closure.**

This assessment covers source identity, import closure, execution receipts and raw logs, actual audit implementation, transitive axiom coverage, reviewer independence, and preservation of failed attempts. It does not replace the integration owner's mathematical diff review, current-main combination check, or merge decision.

**Signed:** /root/pr118_evidence, Agent #28 evidence reviewer  
**Task:** agent28-session72ab-pr118-integration-20261016  
**Repository:** taco-jpg/p196-algorithm  
**PR:** [#118](https://github.com/taco-jpg/p196-algorithm/pull/118)  
**Reviewed exact head:** 90c639b8a782a9a832bc19f6a6978196e91a3d78  
**Review method:** read-only retrieval of exact-H files through the GitHub connector; independent in-memory SHA-256, Git-blob, import-closure, and raw-log comparisons. I authored none of the contribution's mathematical sources, modified no repository files, performed no publication, and initiated no Lean build.  
**New Lean execution by this evidence reviewer:** NOT_RUN. This report assesses retained original execution evidence.  
**New Python literal-table execution by this evidence reviewer:** NOT_RUN. The retained checker, result, and exact input identities were inspected.

In the paths below:

- P denotes proofs/contributions/agent-107/folded-transducer-20261016/.
- S denotes P/semantic-review/clean-rebuild-20261016T214242.588596Z/.
- C denotes P/canonical-verification-be8e612c/.

## 1. Exact source identity and closure

I fetched and independently hashed all 12 registered source modules at H. For every module, the computed SHA-256 matches both the registry and the strict reviewer manifest; the computed Git blob matches both the registry and the remote response. All canonical build snapshots are byte-for-byte equal to the corresponding H source.

| Repository source | Exact Git blob | Exact SHA-256 |
|---|---|---|
| proofs/Lychrel196Research__c696e0ea3db39d92.lean | c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506 | f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c |
| proofs/Agent107TransducerDefs.lean | 03b290b828321dc9144a8741990f7089f07ece53 | 5df72daaa1a29f7df4d9b967215b735b7e39ebbd9245d1135d1073473178a530 |
| proofs/Agent107TransducerPath.lean | 990a8c083bdb44955b434e25ba6fff4dc73ea124 | 718a0a82b010f75949e02ed7665e61f1b5014c38c4661726cebd00ac0f6db21c |
| proofs/Agent107TransducerInput.lean | 55a811ec593ba8f0ccea5290e8ef8b6f53c46bb3 | 91fbfa4d00f3c8ef8229c571f26847246b72502a24f4a7bd7de7692f898c873b |
| proofs/Agent107TransducerBoundary.lean | 7c46227bc4fd31517ee016ba35bbca2385a0f2fe | cbdc094ba800bf4198bc5a1f2ece8b971aaea91ed2ceb2f1b36a24a978baa89c |
| proofs/Agent107TransducerTablesData.lean | afc8b382cfe84b2660ef0e559901b8baf136885d | 70bc2285605fb1b581bc0bc14adef8593ee451b312adb5f79fcf19cce83988ef |
| proofs/Agent107TransducerTablesChecks.lean | 0461201189bdd1ddd78a1e44a284abce4c1e5c66 | 3b87f981d86ed80d8870ea627c7459f7b3b0bffa987fe13378b2f29966b3a60b |
| proofs/Agent107TransducerTables.lean | 4eeb388160245c1057debc70c49d24f586832a2b | 418febdd3cfcf513b2727543532b00e8add1881c1c826dc8112f96365523c67f |
| proofs/Agent107TransducerOutput.lean | f4cda74629b74db4ed8e4d9f98825e5eb70cb217 | 5e71e9bd7a693e19fed7716e71a951d4c06708f42cffc8b1afde4f65aa6e2d67 |
| proofs/Agent107TransducerNumeric.lean | f27fb02b4b422af06e55ee288cc9f8ecd50a8552 | 67d88fb4dea6639a0230c5d0f93d8ed778e6393c073679233ab0e792160e086a |
| proofs/Agent107TransducerReachable.lean | 7ecaee195da124b420a91590fcfdd274bcf39a87 | 7e4dc0b05d441f27bc56f96d3c1cdc7fafa59393b5456fc1ad7feaa93180681b |
| proofs/Agent107TransducerGraph.lean | f7925c5afa2983d95942cf98f6100221a659417a | b24422cb928ab6d9abc796478ab6c0c2631106f5c196385646c631a6f310b02a |

The actual source imports match every registered import list. Traversing the two roots, Agent107TransducerGraph and Agent107TransducerBoundary, reaches all 12 modules with no missing or surplus project module. The only external source import at that boundary is the official toolchain's Std.

I also independently masked nested comments, line comments, and strings and scanned the actual 12 sources. I found no sorry, admit, sorryAx, mathematical axiom, native_decide, unsafe, ofReduceBool, ofReduceNat, skipKernelTC, trustCompiler, implemented_by, or extern code token. The mathematical sources contain no run_cmd, #eval, or custom elaborator/macro execution.

Registry identity:

- Path: proofs/Agent107Transducer.registry.json
- Git blob: 167426452d3b05319c74b5ea29a09e1b25442d63
- SHA-256: 2a897d49fe54eba72f48e68e7888b3fe9d21aa2cc58f1abb2d48a0a68bd4b238

Canonical verifier identity:

- Path: proofs/verify_project__214bf7673efe116b.py
- Git blob: 21131b03dfa516eb19a0a7a4df4f2a41020d4db1
- SHA-256: c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a

Both are byte-identical to their preserved invocation snapshots.

The connector comparison from be8e612ca0694d5d9d8473c784ab1956f93405b6 to H reports one subsequent commit and exactly 43 changed entries: the contribution README and canonical evidence files. No mathematical module or registry changed in that final step.

## 2. Original strict independent execution

I inspected rebuild_review.py, extend_review.py, reaudit_review.py, the complete manifest, all 34 referenced stdout/stderr files, the failed and successful audit sources, and the final raw axiom log.

The strict chain records:

- Reviewer: /root/semantic_review.
- Start: 20261016T214242.588596Z.
- Finish: 2026-10-16T21:50:20.477394+00:00.
- Compiler: official Lean 4.19.0, release commit 6caaee842e94.
- Build directory: /workspace/scratch/94808c4aecb2/agent107-runtime/reviewer-empty-_z2f9ejb.
- build_dir_initially_empty: true.
- LEAN_PATH containing only that project build directory.
- Worktree baseline: 98d59927ad89c42f438ea857ec5750a0df3b91db; the then-uncommitted new source identities are fixed by the matching individual SHA-256 values above.

Each recorded module compilation uses this actual argv pattern, substituting the recorded module name:

    /workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean
    --trust=0 -j1 -DElab.async=false
    -o /workspace/scratch/94808c4aecb2/agent107-runtime/reviewer-empty-_z2f9ejb/<Module>.olean
    /workspace/scratch/94808c4aecb2/agent107-runtime/reviewer-empty-_z2f9ejb/<Module>.lean

The successful source-build order is:

    Lychrel196Research
    Agent107TransducerDefs
    Agent107TransducerPath
    Agent107TransducerInput
    Agent107TransducerBoundary
    Agent107TransducerTablesData
    Agent107TransducerTablesChecks
    Agent107TransducerTables
    Agent107TransducerOutput
    Agent107TransducerNumeric
    Agent107TransducerReachable
    Agent107TransducerGraph

This is one empty-directory build chain extended as further frozen modules became available. The extension checker validates original/copy source hashes, requires prior successful build records, requires corresponding objects to exist, and refuses silently to overwrite a previously reviewed module. The final source hashes still match H.

There are **17 recorded executions: 12 successful module builds and five audit attempts, four successful and one explicitly failed**. All 12 source-build commands exited 0. No successful build or final audit log contains an error or unsupported-axiom finding. All stderr logs are empty.

The final audit command is the same official Lean binary with:

    --trust=0 -j1 -DElab.async=false
    /workspace/scratch/94808c4aecb2/agent107-runtime/reviewer-empty-_z2f9ejb/IndependentAxiomAudit_extension_3.lean

It exited 0. Its checker uses env.getModuleIdxFor?, selects actual Agent107Transducer source modules, iterates every .thmInfo, prints its axioms, calls collectAxioms, and rejects every axiom outside the explicit permitted set. This covers private and generated theorem constants, rather than merely matching public names or enumerating registry endpoints.

The raw log contains exactly **551 distinct new-module theorem names**. I parsed the complete log and compared it by name, origin, and axiom set with independent-audit-summary.json: no mismatch.

## 3. Separate independent Boundary review

The semantic reviewer authored Boundary, so its Boundary self-check is not counted as independent author review.

The separate reviewer /root/lean_runtime supplied:

- P/boundary-independent-review/REVIEW.md
- P/boundary-independent-review/manifest.json
- P/boundary-independent-review/review_boundary.py
- P/boundary-independent-review/BoundaryModuleOriginAudit.lean
- All six recorded stdout/stderr logs.

That checker creates a new empty directory, copies and rebuilds Defs and Boundary, and uses:

    --trust=0 -j1 -DElab.async=false

Both source builds and the module-origin audit exit 0. The only reused project object is this reviewer's earlier independently rebuilt baseline object, pinned in the manifest by source commit, source blob, source SHA-256, and object SHA-256:

    baseline object SHA-256:
    9b0cc1f8650e0d57c1f64e5d353fb5ada6f69b0fe1082a3ee0196a3ebeb54b8a

The checker explicitly verifies that baseline object and source against its earlier manifest before use. It does not reuse the Boundary author's object.

The audit selects exactly Agent107TransducerBoundary by module origin, rejects introduced .axiomInfo, and applies the same transitive axiom allowlist to every theorem. Its raw output and manifest agree on **30 theorem constants**. All **15 actual public Boundary theorem declarations** are present in that audited set.

The separate review explains the actual 15 theorem statements, including the signed -1 sentinel, empty and one-digit cases, center restrictions, overflow output shape, and the counterexample to whole-function path uniqueness. Its reviewed Boundary hash matches H exactly.

## 4. Canonical verifier is a distinct execution

I inspected the original verifier implementation and the preserved invocation wrapper. The canonical run used the exact published checkpoint:

    be8e612ca0694d5d9d8473c784ab1956f93405b6

The actual recorded argv was:

    python3 proofs/verify_project__214bf7673efe116b.py
    --lean /workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean
    --registry proofs/Agent107Transducer.registry.json
    --project agent107-folded-transducer
    --output /workspace/scratch/94808c4aecb2/p196-agent107/proofs/contributions/agent-107/folded-transducer-20261016/canonical-verification-be8e612c

Recorded cwd:

    /workspace/scratch/94808c4aecb2/agent107-canonical-be8e612c

Recorded execution interval: 2026-10-16T22:02:47.437707+00:00 through 2026-10-16T22:05:39.720553+00:00; exit 0; elapsed 172.28276 seconds.

The wrapper requires the exact HEAD, a clean worktree, a new output path, and verifier/registry bytes equal to git show HEAD:<path>. The original verifier copies and hashes every source, verifies imports and exact root closure, builds all 12 modules, then runs its complete module-origin audit. All **13 Lean commands exit 0**.

**These canonical Lean commands do not include --trust=0.** The canonical result must continue to be described separately from the explicit trust-zero independent build above.

The report's original agent: Agent #1 is unchanged. The outer receipt identifies the actual caller as Agent #107 with the lean_runtime invocation role. The report states repository_wide_pass: false; it remains a scoped project result.

I independently verified:

- All **27** C/FILES.json entries: byte counts, SHA-256 values, and retrieved Git blobs.
- All **41** C/INVOCATION_FILES.json entries: the same checks.
- All 12 preserved canonical source snapshots against H.
- The registry and verifier invocation snapshots against H.

There were **zero mismatches**.

## 5. Complete axiom results and count reconciliation

The canonical checker uses actual module origin for all 12 closure modules and Lean.collectAxioms for every theorem. Its raw log contains exactly **1,338 distinct theorem constants: 787 baseline and 551 new-module constants**.

The allowed transitive axiom union is exactly:

    propext
    Classical.choice
    Quot.sound

Raw canonical distribution:

| Transitive axiom set | Theorem constants |
|---|---:|
| Empty | 324 |
| propext | 240 |
| propext, Quot.sound | 700 |
| propext, Classical.choice, Quot.sound | 74 |

For the 551 new-module constants, the strict audit distribution is:

| Transitive axiom set | Theorem constants |
|---|---:|
| Empty | 206 |
| propext | 204 |
| propext, Quot.sound | 139 |
| propext, Classical.choice, Quot.sound | 2 |

Those two choice-dependent new theorems are precisely:

    Agent107.FoldedTransducer.accepting_indexed_exists
    Agent107.FoldedTransducer.admissible_unique_history

The original canonical audit separately lists **18 unsafe implementation placeholders**, distributed as baseline 13, Defs 2, TablesData 3. I checked the full theorem-dependency lists: **none of those 18 names occurs in any audited theorem's axiom dependencies**. Their separate inventory is therefore compatible with the permitted-axiom policy; they are not additional accepted mathematical assumptions.

### Apparent Boundary count differences are fully accounted for

I compared the strict and canonical raw audits by theorem name. Their new-module name sets are identical, and every corresponding transitive axiom set is identical.

Exactly three axiom-free generated equation constants have different reported origins:

| Constant | Strict full audit | Canonical full audit |
|---|---|---|
| Agent107.FoldedTransducer.terminalCenter.eq_1 | Boundary | Output |
| Agent107.FoldedTransducer.terminalCenter.eq_2 | Boundary | Output |
| Agent107.FoldedTransducer.terminalExtra.eq_1 | Boundary | Output |

This accounts exactly for strict Boundary/Output counts **24/47** versus canonical **21/50**.

The Boundary-only audit additionally assigns these six axiom-free equation constants to Boundary; the full audits assign them to Path:

    Agent107.FoldedTransducer.initial.eq_1
    Agent107.FoldedTransducer.Terminal.eq_1
    Agent107.FoldedTransducer.Terminal.eq_2
    Agent107.FoldedTransducer.actualState.eq_1
    Agent107.FoldedTransducer.nextState.eq_1
    Agent107.FoldedTransducer.inputCenter.eq_1

Thus its count is 30. All 30 names are present in the complete audits. The observed difference is generated-equation origin attribution across different import environments, with no missing theorem or axiom discrepancy.

## 6. Reviewer independence map

| Mathematical source group | Actual author | Independent reviewer whose evidence is reused |
|---|---|---|
| Defs, Output, Graph | Agent #107 root | /root/semantic_review |
| Path, Input, Numeric | scope_scout | /root/semantic_review |
| TablesData, TablesChecks, Tables, Reachable | lean_runtime | /root/semantic_review |
| Boundary | semantic_review | /root/lean_runtime |

The formal [COMMENT review](https://github.com/taco-jpg/p196-algorithm/pull/118#pullrequestreview-5554276338) explicitly attributes those real same-team reviewers and the shared authenticated account. It does not claim external peer approval or a separate GitHub identity.

The canonical execution by lean_runtime does not independently review that reviewer's own Tables/Reachable authorship. Their independent coverage comes from semantic_review. Conversely, Boundary independence comes from lean_runtime, not from its author.

No extra review is needed merely because Agent #28 now takes over integration.

## 7. Source correspondence and preserved failures

The independent literal-table checker reads the original Python AST nodes and the actual Lean literals. It does not import the author's generator or extracted-table JSON. Its result records exact ordered agreement for **46 states, 872 edges, and 251 terminals**. I inspected that checker and independently verified its pinned Python-source SHA-256 values against H:

| Original source | Verified SHA-256 |
|---|---|
| proofs/creative_regular_invariant__ea923cdb26a39825.py | c162a35227715b5c102fff8fa038603df0bb30d7f35f2a694eade81c7a83f312 |
| proofs/creative_regular_direct__8988fd8c6a0aad92.py | 93514df6e6041ccf4c962008f1613bb468dd476f93e8388e6315e8e1d548d294 |
| proofs/persist_spacetime_weighted__d53dd1c09dcfc34a.py | 9b75a34916e85ea4dd0024a5ac5d10499287e8df3114da996f3a3d2b1de292f7 |

I did not rerun this Python comparison. Its saved result and reviewed implementation are auxiliary source-correspondence evidence; the general mathematical claims remain supported by the Lean executions.

The failed strict audit is genuinely retained. Its original error is a name-printing type mismatch; the subsequent "sorry axiom" diagnostic is the failed audit elaboration's error recovery. That execution exited 1 and is not counted as accepted proof evidence. The retry changes the audit's name typing/printing, succeeds, and is followed by the successful complete final audit. No mathematical-source repair is hidden in that recovery.

I also checked the two disclosed reconstructed historical failures:

- Table attempt: original exit -9; reconstructed source SHA-256 5119a7e3b109bea4404805350eb4913fbb561411e27fffe65f1804b4dc22440c, exactly matching the retained original execution record.
- Baseline dependency-audit attempt: original exit 1 due to reserved identifier prefix; reconstructed source SHA-256 ea06f27608a402d7b0bb9cb9a0333f720754e80d9a7ff53b7525ee31d0ae0f4b, exactly matching its original execution record.

Both are explicitly labeled post hoc reconstructions, not contemporaneous source snapshots.

## 8. Evidence identities and retained limitations

Key records inspected:

| Path relative to P | Git blob | SHA-256 |
|---|---|---|
| semantic-review/clean-rebuild-20261016T214242.588596Z/manifest.json | 882abd81890c2b049afd45099eef1c635010edd1 | 42a7582db4df75f7b7c62bcfaafd27885ed1ac6b028dde553f09fe45d49fef68 |
| semantic-review/clean-rebuild-20261016T214242.588596Z/IndependentAxiomAudit_extension_3.lean | a87ed80c10d4746b94120874e736e765d1d37772 | ed80f734ab195e99258d5380936d003f79b81a71bb9d158bb507208467c73436 |
| semantic-review/clean-rebuild-20261016T214242.588596Z/all-exported-axioms-extension-3.stdout.log | ab2bf9507501de9768472fec0eec130344fe17f0 | 76ef7e726d5288c7a0749dbf7c6247e258c7547ebf90720b67fc1925be988a75 |
| boundary-independent-review/manifest.json | 756baae643ff4f19e6bf5881d90e1f1be663e3a4 | 9329251161b18449a3dd229ff727f60609d30c22b9c476b3e857b20def0cf813 |
| boundary-independent-review/BoundaryModuleOriginAudit.lean | 9c7c6f96544a9c2b09c637008b9a233b24e182b9 | d7f600574b6d6493758cdff3d5e22ad0125ee8c92d05a18743d804df3cabbff5 |
| boundary-independent-review/module-origin-audit.stdout.log | 23bece5d4bbe8630808e45da9e4bed4c44cd9471 | f97da1e02875099bb9f4e74e13e3be71090e4cff543d1d965f8173a1cd879ce9 |
| canonical-verification-be8e612c/verification.json | 0bd26252bdb0e255c2fae4aeda6ea3717f7afb5a | 2c8eea6aa04699978823ccacd299b3039a519218b9ded11c39ddd5166e44647d |
| canonical-verification-be8e612c/agent107-folded-transducer/source/ProjectAudit.lean | 0b94abe30edae3d30ea7440db4eb05dd8a9f3e80 | 8be4ff116bc49ca60c1268c7b28a7e1d4fbbc743f42efe40d29f0353dcaff53e |
| canonical-verification-be8e612c/agent107-folded-transducer/logs/ProjectAudit.log | 0b7480381d39b81cf96cb07a9058e6e4d251f82a | 77f2b9660f7f042d983fe1b52aecf41fee90276e9d6a6d2591a09dfc3219a861 |

The original FILES.json SHA-256 is 5d0892a8eb1be94ae10467735bb8d3ab419c06fc73cec48a7ab2a66b5d591405. The complete supplementary INVOCATION_FILES.json SHA-256 is 73a086b0287d8812aaf57f23055075a2a0a2524dd3a8a5f8a841ca628e0d87ce.

Retained limitations:

1. This assessment authenticates and reconciles published evidence; it does not claim that I personally witnessed the historical executions.
2. .olean files, compiler installations, and temporary build directories are deliberately not published. The full strict chain's source identities, commands, statuses, and all referenced logs are published.
3. The earlier baseline/manifest.json references baseline-build.stdout.log, baseline-build.stderr.log, baseline-audit.stdout.log, and baseline-audit.stderr.log; those four named files are not among the contribution's published additions. Seven-interface output is preserved separately in baseline/axioms-and-proof-terms.log. I do not represent those earlier four log names as published artifacts. This does not leave the accepted closure without a baseline build: the later complete strict chain includes its baseline rebuild and both logs, and the canonical chain includes its baseline build and complete 787-theorem audit.
4. The source-correspondence JSON has no separate original argv/timestamp/exit receipt; I treat it as saved auxiliary comparison output, with checked implementation and exact input identities.
5. The theorem scope remains finite transducer semantics and ordinary integer one-step correspondence. It does not establish an infinite safe trajectory, a safe invariant instance, full Python interpreter equivalence, whole-function tail uniqueness, or resolution of P196.
6. Reuse is conditional on the exact source closure above remaining unchanged. Current-main compatibility and any combined-tree changes remain the integration owner's responsibility. A substantive source repair would require appropriately renewed independent review.

**No blocking evidence conflict remains. No additional exact-H Lean execution is recommended solely for evidence reuse or the change of integration owner.**
