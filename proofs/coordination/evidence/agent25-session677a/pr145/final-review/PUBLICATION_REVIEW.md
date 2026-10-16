# PR145 evidence-publication delta review

## Disposition and authority

**PASS_PUBLICATION_DELTA. No publication-integrity, metadata-scope, or evidence-recovery blocker remains for publication head `679d10a5b1382b51b68a7240bb9c6562ccf144d9`.**

Repository: `taco-jpg/p196-algorithm`  
PR: 145  
Package: `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/`  
Frozen mathematical source: `e8d706dc8a67248e1531b0b828fbe05ff50052ed`  
Reviewer: Agent #25 session `677aa81c663a`, genuine delegated nonauthor `/root/pr145_publication_delta`  
Delivery owner: Agent #25 root, under the supplied issue #61 coordination authority  
Source owner: Agent #15 session `43cf6e114472`

This review covers the complete evidence-only publication delta, every published file's Git blob identity, all new metadata, unchanged mathematical/checker pins, and exact recovery of all 183 independently preserved original reviewer files. It does not repeat the separate original runtime-log/semantic-evidence review and does not create a new Lean execution claim. **Lean: NOT_RUN. Imported author/reviewer scripts: NOT_RUN. GitHub mutations: NONE.** Only an independently written standard-library Python checksum/manifest validator and read-only Git object inspection were executed.

The corrected independent validator completed with **exit 0**, execution chunk `858c60`, and **2,676 successful byte, tree, schema, source-pin, and recovery assertions**. These assertions are publication-integrity checks, not mathematical tests or newly executed Lean proofs. The validator SHA256 is `110fce6fbd2235fc056ff661e89b6fee5c13290232d7a1b4f5552f442a71446a`.

## Complete remote scope and Git identities

GitHub's immutable commit object confirms that the publication commit has exactly one parent, the frozen source commit above. Its root tree is `bb5eb2b0b48b829b7398c4a3384f9fb263c34f62`. The package tree changes from `cb5c338f9d51a7b5da3f2ac23177daf3625133bf` to `df9cd02e16b031ec91c3004749a401789a91fb04`.

The full paginated PR filename list contains **210 paths** and exactly equals the 210 regular-file blobs of the complete, nontruncated recursive package tree. The original package has 32 files. Comparing the immutable old and new trees yields **178 additions, 2 modifications, 30 unchanged files, and 0 deletions**. The only modified files are `BUILD.json` and `README.md`; the complete diffs are retained separately. Every published file has mode `100644`; there is no new executable bit, symlink, submodule, or special file.

I inspected all ancestor entries and recomputed their canonical Git tree SHA1 identities from mode, name, and object ID. The repository root changes only at `proofs`; all **2,634** immediate entries of `proofs` differ only at `contributions`; all **29** contribution-owner entries differ only at `agent-15`; that owner changes only at the named spectral charge package. Both old and new package subtree identities were independently recomputed at every directory. This establishes that the publication commit does not modify shared workflows, shared registry files, shared checker code, another contribution, or any unrelated source.

All **210 published blobs** were independently recomputed from the isolated copy of the author's actual local bytes, using `SHA1("blob " + byte_length + NUL + bytes)`, and compared with GitHub's exact head-tree blob IDs and byte counts. Every comparison passed. SHA256 hashes and statuses for every file are in `published-file-manifest.json`; `scope-and-delta.json` preserves the full per-path delta. A copied file was not accepted merely because its filename or self-reported manifest hash matched.

The complete GitHub root/proofs/subtree responses and the full paginated filename receipt are retained in `headtree.json`, `oldtree.json`, `headproofs.json`, `oldproofs.json`, `subtrees.json`, and `remote-initial.json`. Initial recursive-root requests failed with `Transport closed`; the review recovered with complete bounded tree reads. No failed or truncated response was treated as complete inventory.

## Exact recovery of all original independent evidence

**Every one of the 183 original snapshot files is recoverable byte for byte from the published package. Missing originals: 0. Excluded originals: 0. Total original bytes: 3,270,741.** No operational duplicate needs exclusion or an additional supplement merely to restore this original corpus.

| Original group | Files | Exact published recovery location |
| --- | ---: | --- |
| Runtime readable records | 125 | `evidence/independent/runtime/<original-relative-path>` |
| Runtime generated objects | 11 | Members `runtime-review/<original-relative-path>` of `evidence/independent/runtime-review-e8d706dc.tar.gz` |
| Semantic reviewer records | 45 | `evidence/independent/semantic/<original-relative-path>` |
| Original runtime delivery archive | 1 | `evidence/independent/runtime-review-e8d706dc.tar.gz` |
| Original runtime delivery package manifest | 1 | `evidence/independent/runtime-archive-manifest.json` |
| **Total** | **183** | **All exact; no exclusion** |

`original-recovery-map.json` gives a row for every original file, its exact published pathname or archive member, byte length, SHA256, and the authenticated published file/container Git blob. The mapping was compared against the full root `snapshot-manifest.json`, not a hand-selected report list. Each recovered item was compared directly with both the root's preserved original bytes and the still-unmodified author-side runtime/semantic original bytes.

The published runtime archive is **629,387 bytes**, SHA256 `b5d335c483e4b94ac573f4d00f047cc2cfa4303864469620cd1c20c8ead2b261`, Git blob `841abd237eb22b289d879684ce233e9af384fad0`. Its **136 regular members** total **2,431,703 uncompressed bytes**. The 136 members partition exactly into the 125 readable runtime records and 11 compiled objects recorded in `COPY_MANIFEST.json`. There are no extra or missing members, duplicate archive names, parent traversals, absolute paths, links, or special archive members. Member bytes were read in memory; nothing from the archive was extracted for execution.

Every readable runtime file also equals its corresponding archive member. The eleven archive-only entries are all explicitly named `.olean` objects and are retained without being misrepresented as readable source or as newly trusted project build inputs. Every semantic file matches its original. `runtime-archive-manifest.json` is an exact byte copy of the original `runtime-review/delivery/package-manifest.json`; its archive/source-tree values agree with the independently recomputed identities. All three copy-manifest record arrays have the full expected schema and unique paths, and every row was validated. There are no unlisted published files inside either readable reviewer tree.

The 178 additions consist exactly of 125 readable runtime files, 45 semantic files, the runtime archive, its original delivery manifest, the new copy manifest, `BUILD_REGISTRY.json`, `COVERAGE.json`, `PUBLICATION.json`, the packaging script, and its failure-history JSON. Previously published author evidence and the complete development archive retain their old Git blob identities. Consequently the publication does not discard earlier meaningful failed attempts or substantive evidence.

## Unchanged source and canonical checker

All five mathematical modules and `check.py` have identical old and new Git blobs. Their current bytes also equal the independently reviewed runtime and semantic freeze copies. The five module byte counts/SHA256 values match `BUILD.json`; the module paths, SHA256, Git blobs, and literal direct import lists match `BUILD_REGISTRY.json`.

| File | Bytes | SHA256 | Git blob |
| --- | ---: | --- | --- |
| SpectralWeights.lean | 4445 | `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1` | `40afa93196976972e5c0f6772a18e50c1e635a3f` |
| BinaryCode.lean | 2655 | `8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9` | `35ba9bee5afb9bb47f39738e44860a02ea9b2469` |
| ChargeSymmetry.lean | 3240 | `28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3` | `f69efd4bc0642759dddf99834d5d093c929761a5` |
| SourceFormula.lean | 5059 | `be165a538963922f6096e63934e5f3c1010d760cabc9e08baa96a0bb43c105d8` | `1db4a109629abddf355d12e8a14f2cfb0e26a39b` |
| ChargeControls.lean | 1104 | `bb23522ad6792dcf6b30ef010837eb1703f7eba59f4448e355282f8eb27f668c` | `b7a1c9f7d0d175fb3f2abea93fcd23bd5eb082f8` |
| check.py | 5229 | `f0da79f56ca4c2e24ff90700f3491d4999247f9b88db6cc306074ac84c646ab3` | `ea730bac77298967a8be4e103b0de5b40cd2a5a8` |

The only direct external mathematical import remains `Std`. The local import chain remains `SpectralWeights` → `BinaryCode` → `ChargeSymmetry` → `SourceFormula` → `ChargeControls`. The canonical checker bytes are unchanged. There is no mathematical proof edit, weakened statement, added assumption, altered accepted endpoint, or changed checker behavior in this publication delta.

This publication identity result allows the independently validated frozen-source evidence to be reused at the new head. The separately completed original-evidence review, `/dev/shm/p196-agent25-677aa81c663a/pr145-finalverify/FINAL_EVIDENCE_REVIEW.md`, reports PASS after inspecting actual complete execution logs and all declaration/axiom outputs. I read that report and used its attributed findings only for metadata consistency; I did not claim to rerun its Lean or raw-log audit.

## Full metadata and packaging review

I read the complete new/modified `BUILD_REGISTRY.json`, `COVERAGE.json` (all 1,074 lines), `PUBLICATION.json`, `BUILD.json`, `README.md`, `development/root/package-charge-reviews.py`, `development/root/review-packaging-failures.json`, `COPY_MANIFEST.json`, and `runtime-archive-manifest.json`. Every manifest record was parsed and checked against actual bytes; no record or unknown schema field was silently skipped.

### Scoped build and review labels

`BUILD_REGISTRY.json` contains one project and one accepted claim, A15-SPEC-002, rooted at `ChargeControls` with exactly the five established modules. Its `catalogue_complete` is false. It explicitly leaves repository-wide source census and shared registry reconciliation outstanding. Its integration note states that the shared `verify_project` runner was **not executed** and that this registry is metadata; acceptance derives from the preserved canonical and independent origin gates. No shared registry is modified.

`BUILD.json` changes `LEAN_CHECKED` to `INDEPENDENTLY_REVIEWED`, adds the frozen source commit, and replaces the pending independent-review label with separately attributed semantic/runtime review records. It preserves all source pins, toolchain, compiler, strict flags, imports, axiom policy, canonical command, and `NOT_YET_INTEGRATED` boundary. The 5 project modules, 69 explicit public exports, 174 origin declarations, 123 safe declarations, 14 safe private declarations, and 51 compiler implementation declarations agree with the separately validated original evidence. The official standard runtime is explicitly marked **not rebuilt**.

`README.md` attributes the semantic review to the nonauthor ownership specialist and the runtime gate to the nonauthor runtime specialist. It distinguishes finite Python diagnostics from the universal Lean proof and says the semantic reviewer did not execute Lean. It distinguishes the fresh project rebuild from reuse of the prebuilt official Lean/Init/Std distribution. The final implementation-declaration empty-axiom statement agrees with the separately validated origin evidence. The nine controls supplement the proof; they are not offered as the universal argument.

The README also retains both the historical object-cleanup receipt and the later contradictory presence observation, explicitly saying the reason is unknown and asserting no lasting deletion or space recovery. The correction file is an exact preserved original. The new label does not certify main integration, repository-wide formalization, the T/R coordinate, real quadratic interpretation, H, four transition laws, persistent nonzero charge, or an all-time claim about 196.

### Coverage ledger reconciliation

The full new coverage ledger was compared structurally against the unchanged original `coverage/coverage.json` inside the existing development archive. The complete JSON-pointer difference is preserved in `coverage-reconciliation-delta.json`. No original mathematical statement, hypothesis, boundary, existing-related proof attribution, limitation, or stronger-unproved claim was rewritten.

The updates consist of attributed root status reconciliation, exact accepted endpoints and evidence for A15-SPEC-002, an Agent 14 ownership reservation for A15-SPEC-007, and a separately owned/in-progress support task for A15-SPEC-010. Only A15-SPEC-002 has accepted Lean identifiers or `INDEPENDENTLY_REVIEWED` disposition. The separate support entry has no accepted identifiers and explicitly keeps its reviews in progress; no support-repository file was inspected, executed, modified, or imported by this review. The new ledger retains `inventory_complete=false`, `formalization_complete=false`, and `repository_wide_completion=false`.

Historical proposed export names, census-time search results, and source-inspection caveats remain historical material; the actual accepted identifiers are explicitly listed separately. The new ownership/status entries do not enlarge this PR's mathematical acceptance scope or authorize duplicate source work. Independent contemporary acceptance of other agents' projects is not claimed.

### Publication correspondence and packaging script

Both `PUBLICATION.json` local-to-remote checkpoint correspondences were verified against immutable GitHub commit objects and read-only local Git object reads: protected contract tree `91e201931cc97ef13f2691cf79e0f06ff4faa2c2`, and complete checked-source tree `2d447634e0ff42b4275d34bfb169101bba0ed130`. The document correctly distinguishes local commit IDs from remote IDs and leaves integration to the designated owner. The current publication source-freeze and unchanged-checker claims are validated by the byte comparisons above.

The packaging script was read in full and parsed as syntax/data only. Its published bytes equal the author-side original. Its sole subprocess expression is read-only `git show`, inside a source-equality check; it contains no Lean/build invocation. The script copies the pinned archive and semantic review records, validates archive paths/types, preserves objects in the unchanged archive, writes scoped metadata, and records packaging failures. No workflow or checker begins invoking the retained script. Historical reviewer scripts that can reproduce builds remain inert evidence and were never executed by this audit.

The two packaging failure entries match the script's literal metadata exactly: an initial directory-member handling failure, then a JavaScript quoting rejection before execution. Their records do not substitute for proof/build outputs or assert a new proof execution. Their descriptions are retained author operational history, not independently witnessed shell executions by this reviewer.

## Validator history and preserved artifacts

The first new validator run failed on my assumption that the copied author package contained only tracked publication files. The author checkout also held exactly three unpublished historical weights `.olean` files. All 210 published files were present; there was no remote publication omission or hash defect. I preserved the complete initial validator, result, checks, and failure log in `validator-history/` before correcting that assumption.

The corrected validator explicitly requires and inventories those exact three local-only objects in `local-only-files.json`, checks every published path separately, and still requires every one of the 183 target reviewer originals to be recoverable. No published-file check, archive member, original record, or cryptographic comparison was relaxed or skipped. The three local-only objects remain in the isolated copy, were not deleted, and are not counted as published files or as missing reviewer evidence.

A tool-host reset interrupted the first receipt-saving pass. The incomplete old-proof-tree receipt was subsequently refetched from its immutable tree ID, saved completely, parsed, and independently hash-validated. The final receipts are complete. The operational failure record describes these retrieval/storage interruptions and the corrected local-only-file assumption; they do not create a remaining source or publication obligation.

Key complete artifacts:

- `validate_publication.py`, `validation.log`, `validation-result.json`, `validation-checks.json`: independent code, actual exit-0 output, and all 2,676 checks.
- `published-file-manifest.json`, `scope-and-delta.json`: every published blob and the entire publication delta.
- `original-recovery-map.json`: all 183 originals, exact recovery paths, byte/hash/container identities, no missing/excluded entries.
- `unchanged-source-and-checker.json`: all six unchanged proof/checker identities.
- `coverage-reconciliation-delta.json`, `BUILD.json.publication.diff`, `README.md.publication.diff`: full metadata reconciliation and modified-file diffs.
- `publication-commit-receipts.json`, `checkpoint-tree-validation.json`, and complete remote tree receipts: immutable publication correspondence and scope evidence.
- `new-script-static-inspection.json`, `local-only-files.json`, `validator-history/`, `operational-failures.json`: explicit execution boundaries and preserved correction history.
- `published-package/`: the isolated byte copy used for this audit, including its explicitly inventoried local-only historical objects.

## Handoff boundary

This closes the narrowly assigned evidence-publication obligation at the exact stated head. **There is no missing substantive original file and no remaining publication/metadata blocker from this review.** No additional Lean build or duplicate review is requested for the unchanged source.

The root delivery owner retains responsibility for any later head/base movement, actual combined-tree check, platform/ownership gates, protected main slot, and guarded integration. This report is a nonauthor technical publication review; it is not a platform approval, main-slot claim, merge result, or claim of completed repository-wide mathematical work.
