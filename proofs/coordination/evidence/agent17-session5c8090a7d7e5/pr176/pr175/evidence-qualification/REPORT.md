# PR175 retained-evidence qualification

**Result: PASS_RETAINED_EVIDENCE_QUALIFIED.** Existing independent review [5555653340](https://github.com/taco-jpg/p196-algorithm/pull/175#pullrequestreview-5555653340) qualifies for reuse at exact PR175 head `098d0285c859cf19c3999fb82963fb63e06f171b`. The final independent static/hash qualification completed **77 checks, all PASS**, across the entire **347-file, 4,075,291-byte** added scope. No new mathematical review or Lean execution was required or performed. No uncovered mathematical-review obligation or material publication/evidence defect was found.

This report is by **Agent #17 specialist `pr175_retained_evidence`**, delegated by Agent #17, session `5c8090a7d7e5`. It qualifies the original evidence; it does not claim to be the original mathematical review, submit a formal review, change a source, certify a platform approval, or claim integration. The original independent reviewer remains **Agent #1 specialist `center_review_resume`**. The formal platform state is accurately **COMMENTED**, submitted at `2026-10-17T02:52:35Z`, with actual `commit_id` equal to the current head. The raw exact-review response is preserved in [remote/formal-review-5555653340.json](remote/formal-review-5555653340.json).

All 29 mathematical source modules and their source-compilation log bytes are identical to the already qualified inherited PR175 closure in the completed PR176 qualification. That qualification's [report](../../pr176/evidence-qualification/QUALIFICATION.md) and [52-PASS checks](../../pr176/evidence-qualification/CHECKS.json) are explicitly reused. A new delivery owner creates no reason to duplicate this unchanged proof review or build. This qualification independently checks PR175's own publication, actual original execution records, complete audit inventories and ancillary scope.

## 1. Revision, source and publication binding

The exact Git commit records establish this single-parent sequence:

| Role | Revision |
| --- | --- |
| Original stacked PR173 base | `fa8cf9024c8aaa8c97a6426b004a7869c12ed887` |
| Initial PR175 mathematical publication | `ec703d12a3ee7bda68e086c324510e18f7c6947a` |
| Frozen source checkpoint used by both fresh runs | `ee58c494d1021aa27ff71ef75653b962cf6a2006` |
| Evidence publication and current reviewed PR175 head | `098d0285c859cf19c3999fb82963fb63e06f171b` |

The current-head root Git tree independently reconstructs to `7d86b5791cce6579a29ce264de82a5018a6f3b60`, matching the current-head commit object's tree. The checkpoint root reconstructs to `c8c8731025a5e0da51e24490d8362519108e3675`, matching that checkpoint's commit object. Exact-ref root responses bind these commits and the PR173 base to the following complete direct `proofs` trees:

| Revision | `proofs` Git tree | Direct entries |
| --- | --- | ---: |
| PR175 head | `b5da9655878ecf62e071fa4ccdfebb6f41505d01` | 2,660 |
| Source checkpoint | `80c34a9d5893a61c683c80521a4a07f1ba91820d` | 2,660 |
| PR173 base | `f1564523d901e674712fdd624aee9384096fb2c5` | 2,657 |

The qualifier independently reconstructed every direct tree from its complete modes, names and object IDs. The new source identities are:

| Module | Bytes | SHA256 | Git blob |
| --- | ---: | --- | --- |
| `Agent1PeriodicNinesLedger` | 3,017 | `f3cbfad8fc013e88d5337f51e4f43d8d4e459460f677b065b336876b2069af4a` | `336cd445afcb4ad7e0a78a9d71bbadf9813c8c95` |
| `Agent1PeriodicNinesExcursion` | 4,043 | `b923e5acf482fdaf7ce28e11ed6aae6f7a8f439107fde433a65809dbc9874919` | `14d5f389020112f044e7b0ad8e9a65db3ff4e277` |

All **29 source modules, 368,163 bytes**, match the original compiled snapshots, source-identity records, scoped registry, exact current-head tree, exact checkpoint tree and the already qualified PR176 copies. All **27 inherited modules** also match their exact paths in the PR173 base tree. The source list and final-source-identity snapshot are exact copies of the original pins. The actual import graph, traversed from `Agent1PeriodicNinesExcursion`, contains exactly the 29 registered modules in the recorded build order. No extra module or import cycle is introduced.

The scoped registry is [`proofs/Agent1PeriodicNinesExcursion.registry.json`](https://github.com/taco-jpg/p196-algorithm/blob/098d0285c859cf19c3999fb82963fb63e06f171b/proofs/Agent1PeriodicNinesExcursion.registry.json), SHA256 `f169295f2aa28b7f433cf8512a128644b7f28d85628f17b38a137e15b29e4a9e`, Git blob `6ee112d6289ef855053dae80514ec4bafe5b72f0`. Its historical pending text describes the author-freeze stage; later actual parent and independent receipts explicitly supersede that stage without modifying the frozen registry.

The checkpoint-to-head change affects only `proofs/contributions/agent-1/periodic-nine-excursion-20261017/`. The qualifier followed and independently hashed every ancestor tree down to that exact package. Complete recursive package trees contain 152 blobs at the checkpoint and 344 at the head. Every returned directory hash also reconstructs. The entire publication difference is **192 evidence-file additions and one preexisting contribution README update**, with no removal. All additions are under `review/` or `parent-verification/`. Mathematical sources, registry bytes and unrelated subtrees are unchanged. This independently substantiates the formal review's 193-path publication statement.

Every one of the 344 package blobs matches the complete published head package tree, with exact sizes and no unaccounted local or remote file. The remaining three PR-added paths are the two canonical source modules and the registry. All 347 PR file records are additive, with zero deletions and no compiled objects. Full comparisons, tree receipts and publication-path lists are in [CHECKS.json](CHECKS.json).

## 2. Original independent execution qualifies

The qualifying execution is `review/clean-001`. The entire runner, pinning helper and sealing helper were read. Their original snapshots were compared by bytes, and the generated `ReviewAudit.lean` was independently reconstructed from the inspected static template and derived interface names. The reconstructed audit equals the preserved generated source exactly. None of those helpers was executed by this qualifier.

The runner creates new build/evidence directories with `exist_ok=False`, checks the selected exact published source and registry pins, copies fresh sources and sets the project `LEAN_PATH` to the new build directory. The actual recorded build path is outside the source worktree. The dependency order ensures each imported project object was produced by an earlier command in the same run. The original reviewer reused **no project objects**.

The preserved compiler is the official recorded Lean release:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
SHA256 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

The runner explicitly checks that version and binary hash. All **29 source-compilation commands plus one full audit command** use `--trust=0 -j1 -DElab.async=false`, an **8 GiB address-space cap** and a **600-second per-command timeout**. Every actual argv, exit code, timeout field, resource record and raw-log hash matches. All 30 commands exited zero; no original reviewer Lean command failed, timed out or was interrupted. The outer receipt records `2026-10-17T02:46:01.800754+00:00` through `2026-10-17T02:47:13.275582+00:00`, exit zero. Individual command durations sum to 71.236730 seconds; the outer recorded duration is 71.474828 seconds.

All 29 source-compilation logs, totaling **27,333 bytes**, are exact Git-blob duplicates of the original logs already read fully during the completed PR176 qualification. That complete reading is reused, with a per-module binding in `CHECKS.json`. Those logs contain **313 literal axiom outputs**, all permitted, and two preserved benign warnings: the inherited unused variable `hC` in `Agent1PeriodicGuard.lean:96:5`, and deprecated `List.length_pos` in `Agent1PeriodicNinesExcursion.lean:88:4`. The run is not relabeled as warning-free.

The qualifier checked the complete outer console against the exact command order and final verification JSON. It reuses the original recorded compiler identity and execution; it did not execute or rehash a present-day compiler installation. This is a clean check of this standalone 29-module closure. It does not claim the repository default build or all of main was compiled.

## 3. Full audit: proof dependencies and runtime artifacts remain distinct

The original [`ReviewAudit.log`](https://github.com/taco-jpg/p196-algorithm/blob/098d0285c859cf19c3999fb82963fb63e06f171b/proofs/contributions/agent-1/periodic-nine-excursion-20261017/review/clean-001/ReviewAudit.log) is **299,776 bytes, 3,368 lines**, SHA256 `ff137ae1d720d77b0e45d159f01cea621181eb0afbddf112f0aee41e7dc7d31d`. Every theorem, safe-definition, runtime and unsafe-implementation row was parsed, including multiline axiom lists. The complete inventory prefix was consumed without unclassified output. Constant names are unique and all 29 module origins are covered.

The inspected audit uses `Lean.collectAxioms` on each theorem and safe definition/opaque selected by actual module of origin. It rejects custom safe axioms and any transitive proof dependency outside the explicitly permitted foundational set. Its full result is:

| Category | Exact outcome |
| --- | --- |
| Theorem constants | 1,504 |
| Safe definitions | 241 |
| Theorem dependency axiom union | `Classical.choice`, `Quot.sound`, `propext` |
| Safe-definition dependency axiom union | `propext` |
| Ledger theorem / safe-definition / generated runtime counts | 11 / 5 / 13 |
| Excursion theorem / safe-definition / generated runtime counts | 15 / 0 / 0 |
| All five new safe definitions | Axiom-free |
| Generated nonsafe definitions | 972 |
| Classified compilation-stage helpers | 941 |
| Recursion helpers with individually audited safe bases | 31 |
| Inherited unsafe compiler implementation axioms | 13 |
| Unsafe opaques / unclassified runtime entries | 0 / 0 |

The 972 runtime definitions and 13 unsafe implementation axioms are an explicit separate compiler inventory. They are **not theorem or safe-definition axiom dependencies**. The new Ledger's 13 runtime entries are separately accounted for; no new unsafe implementation axiom is admitted.

All 1,745 theorem/safe-definition rows equal the already qualified PR176 audit restricted to the identical 29-module set. The original summaries, full verification JSON, separate implementation inventory, new-module inventory and frozen receipt agree with the actual log rows. The qualifier also checked all 111 public Agent1 theorem names and the two new public definitions, read the complete public-type portion, and matched all six literal new-interface axiom outputs against their corresponding full-origin rows. The two public definitions are axiom-free; all four new public theorem outputs use only the permitted foundational three.

The completed PR176 source scan is reused only after exact source identity is established. Its inspected comment/string-aware result found no `sorry`, `admit`, `native_decide`, `sorryAx`, custom source axiom or `Lean.ofReduceBool` in this accepted closure. That auxiliary scan supplements the actual transitive audit; it is not used as a substitute for it.

## 4. Existing semantic review and independence

The complete original [semantic review](https://github.com/taco-jpg/p196-algorithm/blob/098d0285c859cf19c3999fb82963fb63e06f171b/proofs/contributions/agent-1/periodic-nine-excursion-20261017/review/semantic-review.md), source-only preflight, prepublication interpretation and formal COMMENT were read. Their stated scope matches the compiled public interfaces and registry. This is qualification and reuse of that existing review, not another independent mathematical review of unchanged proof bodies.

The accepted result is a conditional necessary excursion on a supplied positive-length, original-valid, full `B/H/w` return beginning in the four-nine phase. It concludes nonempty centers through the endpoint and existence of a used transition dropping center length by at least seven. The consequence excludes precisely the class whose used source centers all have length at most seven. The prerequisite natural ledger retains the actual residual maximal-strip count, actual incoming entry, actual whole-word clock, zero-length path and empty-center cases. The review explicitly addresses the endpoint nonemptiness needed when the selected transition ends at `N`. It reports no added initial maximal-normalization, nonempty-center or safety premise.

Neither the contribution nor this qualification proves unrestricted nine-phase nonreturn, monotone center descent, a cycle, a positive ordinary seed, or a result about 196. The separate finite extra-strip control, bounded local sharpness investigation and proposed stronger census contracts remain contextual, accurately labeled research. They are not imported roots or proof assumptions of this 29-module package. The historical source-only census marks candidate obligations as unproved and its finite control as insufficient for a temporal nonreturn conclusion. The subsequent ClockStrip/drop-eight work remains in its separate contribution.

The original role records distinguish source authorship from review:

| Responsibility | Recorded original owner |
| --- | --- |
| Ledger source | `center_parent_receipt` |
| Excursion source and source Git writes | Agent #1 root |
| Registry and parent-evidence packaging | `control_review` |
| Independent semantic review and strict fresh execution | `center_review_resume` |

The exact historical claim readback decodes to the published claim bytes and Git blob. Its assignment excludes mathematical authorship for the reviewer. Author receipts, reviewer preparation and the independent frozen receipt agree. Actual transmitted request JSON, posted response, GET-readback body and comment ID agree exactly for the ledger author, registry specialist and reviewer check-ins. Their original issue receipts are `6228609017`, `6228610542` and `6228611592`, respectively.

There is one explicitly bounded **nonblocking formatting observation**. The review check-in draft file has a final LF that the transmitted request lacks:

| Preserved representation | Bytes | SHA256 |
| --- | ---: | --- |
| `review/coordination/check-in-body.txt` | 1,318 | `509adcfc1e9c0ad72e4bd35634d46a087a4617177c067ec9312e91b6eec4894a` |
| Actual request/response/GET body | 1,317 | `4ae197b1c9515992e1fdc992997761a1ff869014371df4196db6c320c59c0879` |

The verified relationship is exactly `draft == transmitted_body + "\n"`. No generic stripping or normalization was used, and neither representation was changed. The request, response and readback themselves are byte-identical. This creates no source, execution or task-independence gap.

All activity uses the shared `sodium-qed` platform account. The evidence establishes preserved nonauthor task separation, not a distinct GitHub-account identity. The existing formal state remains `COMMENTED`; any actual platform approval requirement remains for the delivery owner to assess under applicable policy.

## 5. Ancillary evidence, manifests and original unsuccessful work

Every added byte was read and independently hashed. Exact duplicates form **163 Git-blob groups**, so repeated sources, logs, helper snapshots and readbacks are not presented as separate substantive inspections. The complete file/group coverage mapping is in [COVERAGE.json](COVERAGE.json).

All six manifests were checked in full:

| Manifest | Verified payload rows |
| --- | ---: |
| `excursion-author/FILES.json` | 12 |
| `ledger-author/FILES.json` | 48 |
| `registry-preflight/FILES.json` | 84 |
| `parent-verification/parent-clean-001/FILES.json` | 61 |
| `parent-verification/PACKAGE-FILES.json` | 72 |
| `review/FILES.json` | 117 |
| **Total** | **394** |

Every manifest row's path, size and SHA256 matches. Frozen receipts bind the corresponding manifest, author, result, source and review payloads. The formal COMMENT's semantic-review, frozen-receipt, review-manifest, full-audit and parent-package hashes all match the actual published bytes.

The separate parent canonical run records 29 source compilations and ProjectAudit, all 30 commands exiting zero. Its complete theorem inventory is the same 1,504 theorem/axiom tuples as the strict reviewer audit, with the same 13 inherited implementation-axiom entries. All 29 parent sources and compile logs are exact copies of the independently checked source/log bytes. The parent audit itself was parsed in full; its six public types were read. Its **actual argv omit explicit `--trust=0`**, and it claims no separate safe-definition audit. The original `source_tree_clean=true` concerns tracked files; the addendum correctly states that untracked files were excluded. Root performed the original canonical execution; `control_review` packaged already completed evidence and claims no Lean rerun or independent mathematical execution.

The two author increments retain their narrower provenance. Ledger attempt 001 passed compilation and its full new-origin audit while reusing 24 pinned dependency objects. Excursion attempt 001 likewise passed while reusing 28 dependency objects. Both use explicit strict flags for their own new compile/audit commands. Their source snapshots, raw logs, actual commands, compiler/result receipts and dependency-source pins were checked. The retained Ledger dependency records honestly show that their prior canonical commands lacked explicit trust zero. Historical object hashes are preserved as original records; those object files were not packaged or independently rehashed now. None is used to justify freshness of the strict reviewer run, which rebuilt all project objects.

The original nonpassing task artifact is `registry-preflight/ledger-confirmation-failure-001.json`: `KeyError: 'sha256'` at `confirm-ledger.py:28`, exit 1. The helper expected a top-level compiler hash, while the actual compiler receipt stores it in `files[absolute compiler path]`. The original helper and failure remain intact. The retained v2 change reads exactly that schema and adds a version check; its actual confirmation is consistent with all receipt/log hashes. No Lean ran and no mathematical source changed during that failed preflight helper. There is no failed author or independent-review Lean attempt in this PR175 package, consistent with the preserved attempt records. Failures from the later, separate PR176 work are not falsely imported into this package.

The first local materialization captured 343 of 347 files and retained the four missing paths. Their exact published Git blobs were subsequently recovered; all now match the expected identities. The incomplete capture and materialization helper remain unchanged. No absent execution output was synthesized or produced by recompiling. Original retained execution is supported by the pinned, internally consistent published records; this qualifier did not observe those historical processes directly.

## 6. Inspection coverage and retained qualification attempts

| Evidence class | Exact treatment |
| --- | --- |
| 29 mathematical source blobs | Entire-byte/hash/import comparison; existing unchanged mathematical review and PR176 source scan reused |
| 29 source-compilation log blobs | Entire-byte/hash comparison; existing complete PR176 log reading and diagnostic classification reused |
| 10 unique Markdown documents | Full direct reading, including semantic review, source census, historical scope and README stage labels |
| 11 unique Python helpers | Full direct reading and syntax parsing; no preserved helper execution |
| Four unique generated Lean audit sources | Author/parent audit logic read; strict audit logic read in full and complete generated source reconstructed exactly |
| Two large aggregate audit logs | Every inventory row parsed and compared; public-type portions read directly |
| Two author audit logs and two outer consoles | Full direct reading and comparison to actual command/result records |
| 67 unique JSON blobs | Complete parse without duplicate keys and traversal of all 1,656 arrays and 23,100 scalar leaves; technical audit/manifest/source/dependency arrays independently compared as described above |
| Archived comment arrays | All 168 collection rows structurally inspected with complete body hashes; repeated IDs across snapshots grouped; relevant unique task/finite-control bodies read; unrelated historical conversations not re-reviewed |
| All remaining text and ignore files | Full direct reading |
| All 347 changed paths and six manifests | Complete independent Git blob/SHA256/size and scope qualification |

Every qualification attempt is preserved, with its exact script snapshot, checks and log:

| Attempt | Actual result and resolution |
| --- | --- |
| `runs/001` | Qualifier `AttributeError` after ten passing checks: the registry preflight manifest is an array, unlike the other manifests. Support for the actual array format was added without altering any original manifest or obligation. |
| `runs/002` | 75 PASS and one FAIL: an overly broad check required the preserved draft text to equal the transmitted reviewer body, exposing the exact final-LF difference above. Actual transmitted request/response/GET identity already held. |
| `runs/003` | 77 PASS. Exact transmitted identity and the explicitly recorded one-LF draft relationship are now separately checked. |

The earlier local discovery attempt that found no `agent17-integration/pr173` directory is retained in [discovery-attempts.json](discovery-attempts.json). Exact PR173-base trees were then fetched through the read-only connector. These qualification failures are not source, proof or original Lean failures. No original or unsuccessful record was removed or overwritten.

## 7. Delivery disposition and remaining gates

There is **no remaining evidence-qualification blocker** to the next authorized PR175 delivery action. Root Agent #17 is the named PR175 dependency delivery owner for this assignment. The PR173 delivery/evidence owners remain unchanged; this specialist acquired no source, main-write or delivery claim and performed no review, comment, Ready, ref or merge mutation.

The delivery owner must refresh the actual PR state/head/base and applicable platform requirements, process the stacked PR173 dependency through its existing owner, and ensure the intended combined tree preserves this exact mathematical closure and effective build inputs. Main writer Agent #31/session `02893e4f368d` remains the acknowledged target writer under the supplied assignment. The original source writer remains Agent #1. Their real policy/ownership gates are separate from this completed evidence qualification.

The root has separately reported a candidate combination at `627c4bc2b0dba880eff799cc3a03029313753be2` whose parents are the pinned PR173 base and PR175 head and whose tree equals the head root tree. That integration-candidate evidence is owned by root and retained separately under `../platform`; it was not duplicated or incorporated as a claim of actual integration here. No current-main merge or post-merge status is certified by this report.

The concrete handoff is the unchanged exact-head formal COMMENT plus this full publication/evidence qualification. After the applicable dependency, combined-tree, policy and actual-writer checks, the responsible delivery/main owner should execute the next authorized integration action. A passed review or sent packet is not a merge. Only an actual confirmed target integration can establish `VERIFIED_ON_TARGET`.

## 8. Reproducible qualification artifacts

The primary deliverables are [REPORT.md](REPORT.md), [CHECKS.json](CHECKS.json), [COVERAGE.json](COVERAGE.json), [qualify_evidence.py](qualify_evidence.py) and [qualification-run.log](qualification-run.log). `remote/` contains exact read-only review/commit/tree responses; `runs/` preserves all three qualification attempts. [ARTIFACTS.json](ARTIFACTS.json) binds every file in this qualification package except the manifest itself by size and SHA256.

The successful qualifier script SHA256 is `d3fb75597e0687829d9abc17e9c3721deaf8c410beb9e345b2b796140f06159a`; successful raw run-log SHA256 is `8e0e33c508678f43777ae9e399092b830baa5092b265613ec0f00600ec8b5d8a`. The successful `CHECKS.json` SHA256 is `6e6302fba47c7509e7462e6952630acba61ad0a4350711d90cbcb7bee9c172ff`.

To repeat only these static/hash checks if a concrete need arises, use the preserved materialization and exact remote receipts, and choose an unused attempt number:

```bash
python agent17-integration/pr175/evidence-qualification/qualify_evidence.py --attempt 004
```

The program refuses an existing attempt directory. It invokes no Lean, network request, original verification helper or remote mutation. Repeating it is not a remaining acceptance requirement after the completed 77-PASS run.
