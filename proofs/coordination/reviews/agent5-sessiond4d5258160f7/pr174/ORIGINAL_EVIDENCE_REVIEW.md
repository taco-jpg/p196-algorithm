# PR 174: qualification of existing verification and publication evidence

## Disposition

**Existing mathematical review and verification: PASS, reusable at the pinned head.**

**Complete publication accounting: one precise unresolved gap.** The published source-census report refers to original scout evidence, including a failed index-processing attempt, that is not present in the PR package and has no supplied immutable publication mapping. Source-owner recovery or identification of that original package is required before claiming complete compliance with the publication policy. This does not invalidate the mathematical source, strict fresh-closure execution, or independent semantic review.

This is an evidence-qualification assignment for Agent #5 / session `d4d5258160f7`, reporting to the named PR 174 delivery owner. No source authoring, remote mutation, ownership claim, Ready transition, merge, Lean execution, or additional mathematical experiment was performed. No new mathematical obligation requiring duplicate review was found. Combined-tree, dependency-delivery, platform, and target-write decisions remain with the parent delivery owner.

## Immutable inputs and accepted rules

| Input | Exact identity |
| --- | --- |
| Repository | `taco-jpg/p196-algorithm` |
| PR | [174](https://github.com/taco-jpg/p196-algorithm/pull/174) |
| Reviewed final head H | `790ee166caf3c60c7176d53209e3e755e7ed9a9d` |
| Mathematical source checkpoint S | `bfa0247b78845558d087eec08e113e91decaaddb` |
| Direct base, PR 172 head B | `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80` |
| Accepted policy snapshot | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Actual review | [5555595181](https://github.com/taco-jpg/p196-algorithm/pull/174#pullrequestreview-5555595181), `COMMENTED`, commit H |
| Source branch | `research/agent-1/periodic-nine-control-20261017T0219Z` |

The complete supplied campaign and accepted `AGENTS.md` / `proofs/PUBLICATION_POLICY.md` were read. The publication policy requires original source, substantive logs, failed attempts, audit evidence and reproducibility information to remain recoverable. It permits exclusion of reproducible compiler objects, runtimes, caches and operational publishing infrastructure. It also requires truthful separation of finite conclusions, formal theorems, incomplete work and historical records. The campaign explicitly permits reuse of qualifying unchanged independent review and forbids restarting it merely because delivery changes hands.

The local repository index and working tree are intentionally partial. All repository presence, identity and mode checks used immutable Git objects; no working-tree absence or `git status` inference was used.

## Complete changed-file qualification

REST changed-files pages were retained in full, including connector envelopes and the unmodified API payloads. Pagination returned **100 + 57 + 0** entries. The PR snapshot independently reports 157 changed files, 43,601 added lines and zero deletions. All 157 filenames and blob identifiers match the immutable H tree and the direct B-to-H diff.

One `git cat-file --batch` acquisition read the complete selected object bytes. Every object was checked against its Git blob SHA-1, API SHA, byte count, SHA-256 and tree mode. All **157 files / 2,102,067 bytes** are additions, regular `100644` blobs, and valid UTF-8; every JSON payload parses. The complete bytes are preserved under `blobs/`, and `selection-manifest.json` records each filename, blob identity, SHA-256, byte count, mode, API status, additions/deletions and evidence role. API patch truncation does not limit this review because the full authoritative blobs were read separately.

| Published role | Files |
| --- | ---: |
| New formal source | 1 |
| Scoped registry | 1 |
| Exact source snapshots | 56 |
| Generated audit sources | 3 |
| Original verification logs | 35 |
| Source identity, command and result records | 26 |
| Verification or packaging driver snapshots | 9 |
| Scope and review reports | 7 |
| Coordination provenance records | 10 |
| Byte manifests | 5 |
| Manifest seals | 2 |
| Operational exclusion snapshots | 2 |
| **Total** | **157** |

The source-to-H diff contains 116 added evidence/metadata paths. It does not change the mathematical sources or registry. No executable workflow, accepted global build registry, source adapter, compiler installation or binary object is added by this PR.

### Manifest and receipt checks

Every listed file was checked against its actual bytes, and every package directory was compared with the corresponding manifest rather than relying on entry counts. There are no unlisted payload files or nonexistent manifest entries within these five published manifest scopes.

| Manifest | Entries | Exact exclusions |
| --- | ---: | --- |
| `author/FILES.json` | 10 | Itself |
| `registry-preflight/FILES.json` | 26 | Itself |
| `parent-verification/parent-clean-001/FILES.json` | 33 | Itself |
| `parent-verification/PACKAGE-FILES.json` | 44 | Itself and `frozen-receipt.json` |
| `review/FILES.json` | 67 | Itself and `frozen-receipt.json` |

The outer parent package retains the original 33-entry manifest unchanged. Its seal binds the package manifest, original manifest, original verification report, source receipt and result addendum. The review seal binds its complete manifest, semantic review and verification report. All receipt hash links match H. Self-exclusion is accounted for explicitly; no circular self-hash was expected.

Important identities:

- Review manifest SHA-256: `99b85e925da4941e9fae9390ef8f1d25501f3b2763b793f55afadc97dc0b19ee`.
- Review seal SHA-256: `1c27268ba908bdf8224ad1234dd0ddd231c53c1a7eb7314854aadddd3155e779`.
- Parent package manifest SHA-256: `de70dbb9d19f48d23d39e2be2f899ff122dd478c93862c9f028813bb0284d852`.
- Original parent manifest SHA-256: `7f697573c858b2ff3a7eefdc6f5966cf2bc135549885da8a16b2c36b5dad7b11`.
- Parent seal SHA-256: `71926f130b13edb6bb9bbbfec674bb132129d52ee1a053c75d659deb52edff9c`.

These manifests prove completeness of their enumerated package scopes. They do not by themselves prove that every separate research artifact mentioned in the scope report was included; the outstanding scout reference below is the material distinction.

## Source closure and source-to-review binding

The new source is `proofs/Agent1PeriodicNinesExtraStrip.lean`, blob `21dc3897b77499d95aee131ab02d7056ee676ae2`, SHA-256 `e50a7e04b272f8b0d78d380b1ec1e2df80fc4b1647719dd31bdac02109a8107e`.

The scoped registry is `proofs/Agent1PeriodicNinesExtraStrip.registry.json`, SHA-256 `faa3a7717ce7c1385d856c689afbb3d95bd35cacaf04c428dbf5aa41f8f693f3`.

The 15 mathematical source entries were checked against Git tree identities at S and H. For every entry, the published Git blob, registry pin, retained independent compiled-source snapshot, parent compiled-source snapshot and preflight snapshot identify the same bytes. All 14 inherited modules additionally match direct base B. The exact 15-module import graph was derived from the source after masking nested comments and strings, checked for unregistered dependencies and cycles, and compared with the registry. It is the minimal custom closure of `Agent1PeriodicNinesExtraStrip`; built-in `Std` imports are external toolchain dependencies. The center-map and cycle adapters are absent from this closure. **No PR 173 mathematical dependency is introduced.**

The exact closure is `PeriodObstructions`, `ActualWordBridge`, `PrefixSemantics`, `LychrelDigitSums`, `IncomingCarry`, `Agent1RepeatedBlock`, `Agent1RepeatedBlockContext`, `Agent1PeriodicDigits`, `Agent1PeriodicSlices`, `Agent1PeriodicGuard`, `Agent1PeriodicGuardFacts`, `Agent1PeriodicOuterStrip`, `Agent1PeriodicCenterStrip`, `Agent1PeriodicQuotient`, and `Agent1PeriodicNinesExtraStrip`.

The scoped registry's historical pending-review wording is preserved at its freeze point. The later receipts and actual final-head review record completed verification; the historical wording is not evidence that the later run was missing. Similarly, the frozen review receipt's pending-formal-review field predates actual review 5555595181. The actual platform review is the current delivery evidence.

## Existing execution evidence: actual coverage and limitations

The author driver, independent replay driver, source-pinning driver, canonical verifier, preflight script, packaging script, generated audits, semantic report, receipts, command records and substantive logs were inspected. The independent raw audit rows were parsed in full, including multiline axiom lists, instead of relying on summary counts.

| Execution | Retained result | Correct qualification |
| --- | --- | --- |
| Author `attempt-001` | Two successful strict commands, compile plus new-origin audit | Incremental; 14 dependency objects reused from a prior fresh run |
| Root canonical `parent-clean-001` | 15 modules plus ProjectAudit; 16 zero exits | Fresh scoped closure; actual argv has no explicit `--trust=0`; no separate safe-definition audit |
| Independent `review/clean-001` | 15 modules plus ReviewAudit; 16 zero exits | Strict fresh scoped closure, `--trust=0 -j1 -DElab.async=false` |
| Parent evidence packager | Byte identity / preservation checks | Did not run Lean and is not an independent mathematical execution |
| Supporting `semantic_check` | Source-only supporting review | Did not execute Lean or a mathematical Python experiment |
| This Agent #5 evidence specialist | Full byte, manifest, source-binding, raw-log and coverage qualification | No Lean execution and no replacement mathematical review |

The independent execution uses the recorded Lean 4.19.0 release, commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Its driver creates a fresh build directory with `exist_ok=False`, sets `LEAN_PATH` to that fresh directory, copies exact pinned sources and records all commands. Each command has an 8 GiB address-space cap and 600-second timeout. All 16 log hashes match the recorded outputs; all exits are zero, with no timeout. The recorded elapsed sum is 67.85137776000192 seconds.

The full independent audit contains **1,348 unique theorem constants** and **227 unique safe definitions/opaques** from the selected closure. Each row's transitive axiom set is within `{propext, Classical.choice, Quot.sound}`. The theorem union is exactly those three; the safe-definition union is `{propext}`. All selected custom modules appear in the theorem audit. All 68 named public Agent1 theorem exports occur in the retained type-check output.

The new module contributes exactly five theorem constants, no safe definitions, no runtime entries and one public theorem. Its public axiom output is literally `[propext, Quot.sound]`. Source token checks and retained origin audits show no `sorryAx`, `Lean.ofReduceBool`, unsupported custom logical axiom or compiler-trusted finite-computation shortcut in the accepted chain.

The separate inherited implementation inventory contains 944 non-safe definitions: 916 compilation-stage helpers and 28 unsafe-recursion helpers with audited safe bases. Thirteen unsafe implementation axioms are inventoried separately; there are no unsafe opaques or unclassified runtime helpers. These entries are absent from accepted theorem/safe-definition axiom dependencies. The new module has none. Treating these implementation declarations as custom logical assumptions of the finite theorem would misstate the audit.

The canonical parent run independently retains 1,348 theorem rows, all 16 command logs and its original source report. Its actual argv is not retroactively relabeled strict. Its `source_tree_clean` flag concerns tracked files only, and `repository_wide_pass` is false. Neither parent nor independent evidence establishes a fresh build of all main.

### Independence and actual review state

Review 5555595181 is an actual `COMMENTED` review submitted at H. It identifies specialist `control_review`, who authored the scoped registry and review metadata but none of the mathematical sources. The mathematical root author and execution/packaging roles are explicitly separated in the published records. That is the disclosed project-level subagent independence supporting reuse; a different agent number is not treated as evidence of a different GitHub account. The platform review uses the same `sodium-qed` account as the PR author and is not an eligible independent account's formal approval. Platform-specific approval requirements are outside this evidence disposition and must be evaluated separately by the delivery owner.

## Finite semantic boundary retained

The concrete source and existing semantic report were read to qualify what the executed commands actually cover. No second proof-development or semantic-review campaign was initiated.

The public theorem fixes `B=[1]`, `H=[9,9,9,14,18,18,14,9,9,9]`, `w=[9,9,9,9]`. Its eight conjuncts establish original validity, initial maximal center stripping returning `(H,0)`, actual entry sum one, unchanged next raw period, exactly two mirrored period pairs stripped, residual center `[18,18]`, quotient outer `[3]`, and one further actual raw period equal to `w`.

Two mirrored pairs remove two four-entry blocks on each side, sixteen coefficients total. The theorem refutes a blanket one-step bound of at most one stripped pair on this original-valid, initially center-normalized domain, including a nonempty residual and one additional nine-period observation. It supplies no full tuple return, safe infinite continuation, temporal descent/no-return theorem, reachability from 196 or solution of the 196 problem. It does not refute a bound requiring additional temporal hypotheses. The theorem and review consistently retain these limitations.

## Publication gap: original source-census/scout package

The specific immutable report is:

`proofs/contributions/agent-1/periodic-nine-control-20261017/scope/source-census.md`

Its byte-identical copy is `review/scope-report-snapshot.md`. Both are blob `aaf62e85c2a8f9ba272e3fdf79de0350b523cbe4`, 8,579 bytes, SHA-256 `f233d4b20ab3c5010d0fb8e21e59d680e07057fd8ca2ca3bef39aa78d2031bec`.

The report makes three concrete retention references:

1. Line 7 describes 245 task records at coordination commit `4c9e6e7aa08147f3798ffad8657c08512e7774c8`, both branch-list pages covering 162 branches, and issue 61 comments through proposal 6228357838. It says the full exact task records and API readbacks are retained.
2. Line 21 describes a Git-tree search at `c42dd0b6accedd27424a9511f8c06b651d21779e`, 3,334 matching lines across 245 files, a separate literal negative search, and an initial incorrect colon/argv index split followed by a retained corrected index. It says the original raw search output was unchanged.
3. Line 49 identifies `nines-extra-control-scout/source-pins.json` and `source-files/` snapshots for eleven selected source files, with their original bytes, Git blobs and SHA-256 values.

All 157 published files and all package manifests were examined for an alternate mapping. No scout package or manifest mapping is supplied. An immutable full-H pathname search for the named scout and related control-census/search/index paths finds only the published `scope/source-census.md`; no `nines-extra-control-scout` path exists in that tree. The repeated report is not the raw search, failed/corrected index record, eleven-source pin list or original API snapshot collection it describes.

This finding is deliberately bounded: it does not assert that the author's original local files were destroyed, nor that no other branch or later publication contains them. It establishes an unresolved publication reference at H. The report gives a relative scout directory but no authoritative absolute workspace path. The absolute location must be obtained from the author or a specific original workspace record, not guessed.

**Concrete remedy:** the source owner should provide an immutable published location with a complete byte mapping, or append the exact original scout bundle and an additive inventory/receipt. Retain the failed index-processing attempt and corrected output as historical evidence. If the original snapshot already exists elsewhere, bind its exact commit, path, byte count and hashes. A new rerun is not a substitute for retention of the original work. Reconcile the package manifests and final-head review binding after the additive publication. Unchanged mathematical sources, closure and registry preserve the existing proof evidence; no fresh Lean run is justified solely by this documentation/evidence addition.

## Local execution and retained evidence

The first immutable blob read failed because the default public-network proxy was unavailable. Its original partial stdout, stderr and exit are preserved as `raw/objects.*.attempt-001`. The same public Git read then succeeded through the approved escalated read path. It used no credentials, authentication workaround, ref write, checkout or index mutation. The complete successful batch is `raw/objects.batch`; the selected tree rows, full API reads and raw review are retained alongside it.

`scripts/qualify.py` performs local evidence qualification only. It does not invoke Lean, execute the retained drivers or evaluate the candidate mathematically. It extracts only the already-inspected comment-mask function to derive import/token facts, then hashes and parses retained sources/logs. Its first qualification run exited zero. `raw/qualification.stdout`, `raw/qualification.stderr`, `raw/qualification.exit` and `raw/attempt-log.json` preserve actual results. The missing scout's historical failed index attempt is not falsely represented as locally recovered.

Deliverables:

- `EVIDENCE_REVIEW.md`: this scoped disposition and concrete remedy.
- `machine-receipt.json`: source bindings, manifest checks, raw audit coverage, execution distinctions and publication gap.
- `selection-manifest.json`: every selected published byte/blob/mode and evidence role.
- `raw/`: original API responses, immutable tree/diff reads, acquisition outputs, reference search and checker logs.
- `blobs/`: exact full original published file bytes.
- `scripts/`: the acquisition and qualification logic used in this assignment.

**Delivery consequence:** reuse the qualified mathematical review while resolving the precisely identified publication reference. Do not restart unchanged proof verification, infer that a source-branch merge is main integration, or treat this evidence report as a Ready/merge action.
