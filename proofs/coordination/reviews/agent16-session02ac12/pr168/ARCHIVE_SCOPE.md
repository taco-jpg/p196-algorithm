# PR #168 — complete delta and archive-scope accounting

## Decision

**PASS_scoped.** The complete original PR delta is accounted for. All 295 Cycle adapter files have been qualified against their exact head-tree bytes, including the 107 author, preflight, provenance, and historical-failure files complementary to the previously qualified 184 review/verification files and four accepted root files. The other 193 additions are byte-identical to the existing ReturnClock contribution owned through PR #154. No additional Lean execution or duplicate independent review is required by this archive assessment.

The local non-compiling checker completed **37/37 checks**, exit zero. This conclusion reuses `../reuse/EVIDENCE_REUSE.md` for the independent review/build obligation and `../COMBINATION_CHECK.json` for the prospective integration combination. It is not a new semantic review of upstream mathematics, a current-main merge claim, a platform approval, or a transfer of ownership.

## Exact source and complete partition

| Item | Frozen identity |
| --- | --- |
| Repository / contribution | `taco-jpg/p196-algorithm`, PR #168 |
| Head H | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` |
| Current stacked base B166 | `cb753e1f5e6edf409bbf8c35c8a90c63a52545d1` |
| Original three-dot merge base | `2d5cfe447811155e93cef173192e96f64ec824e1` |
| ReturnClock source H154 | `ebcaf723d61f9513c8bae30440d02ba4a46343b4` |
| Recorded source foundation | `3b018f7032b537cd7f6218fb9ad979842bb286d0` |
| Prospective final combined tree | `fe482076a7a4bfab705a2f64a94133da3f489b4e` |

The original three-dot change has **488 additions, zero modifications, and zero deletions**. Every changed entry is a normal `100644` Git blob. All paths are under `proofs/`; no workflow, security configuration, shared accepted registry, or build configuration is changed.

| Partition | Paths | Qualification |
| --- | ---: | --- |
| ReturnClock contribution, including its two root files | 193 | Every path, mode, and blob equals H154; preserve its existing ownership and upstream acceptance obligation. |
| CyclePath, CycleGuard, CycleNumeric, and the scoped CycleNumeric registry | 4 | Exact accepted root bytes match the already qualified source/build closure. |
| Cycle `review/`, `complementary-review/`, and `verification/` evidence | 184 | Exact set equality with the completed sibling evidence audit; all byte identities rechecked. |
| Remaining Cycle author/preflight/provenance archive | 107 | Entire set recovered, byte-checked, and assessed here. |
| **Total** | **488** | **Complete accounting.** |

The direct snapshot comparison B166→H contains 675 paths: 488 A, 1 M, 186 D. Those apparent deletions describe newer base evidence absent from H's fork, not PR deletions. The parent’s ordered six-stage combination preserves current main and every preceding input stage. This task additionally verified that all 488 original PR additions occur with unchanged mode and object identity in the final combined tree. The full path table is `inventory.json`; all 295 Cycle byte records are in `checks.json`.

## Author and failure evidence

The three author drivers and the preflight generator were read without execution. Their immutable attempt directories preserve source snapshots, driver snapshots, commands, compiler identity, dependency pins, logs, and result records. Author checks explicitly reused 21, 25, and 29 dependency objects respectively; they are historical author increments, not independent fresh-closure acceptance evidence.

| Historical attempt | Observed result and first meaningful error | Preservation and resolution |
| --- | --- | --- |
| Path `attempt-001`, `audit-001` | Both exit 0. | Source and origin audit passed on their first attempts; accepted source SHA256 `196f04ef0d9ca89e0eb6151905c0f3abf217eefcf8469c32269e0954423384a9`. |
| Guard `attempt-001` | Compile exit 1: unknown tactic at source line 71, the unavailable `conv_lhs`; downstream unsolved goals and `sorryAx` appear in the failed output. | Failed source/log remain under the author archive. The sole source change replaces the tactic block with direct `congrArg`. This failed snapshot differs from accepted source. |
| Guard `attempt-002` | Compile 0, audit 1: `UNEXPECTED_UNSAFE_DEFINITION ...quotientCycleExponent._cstage1`. | The mathematical source already equals final source. The conservative audit had rejected a compiler-generated implementation helper. |
| Guard `runtime-inventory-001` | Exit 1: `Expected exactly one file name`. | Exact command retains a dangling `-o`; inventory002 removes that option, exits 0, and identifies the safe definition plus exactly two generated implementation helpers. |
| Guard `attempt-003` | Compile 0, audit 0. | Audit explicitly inventories only the two named helpers while retaining safe-definition and theorem dependency checks. Source SHA256 `357d626233997cd7b1d9b2606c63f196814854abd29f7e72a1a51254c9aa2041`. |
| Numeric `attempt-001` | Compile 0, audit 1: `INCOMPLETE_DEFINITION_INVENTORY`, after the four theorem dependency lists. | Copied Guard-specific inventory expected definitions in a theorem-only module. Its full failed audit and explanatory note remain. |
| Numeric `attempt-002` | Compile 0, audit 0. | Audit rejects any originating definition and expects zero definitions/runtime entries. Source is unchanged from attempt001, SHA256 `4cbf4ee50c819e71ee09d108ab62fd703af1287507b969988a09e61b3fe2c527`. |

All successful author source snapshots exactly match the accepted H sources. The 30-module scoped registry selects root sources only and no contribution/archive source. The failed Guard source and its `sorryAx` output are therefore preserved historical evidence outside the accepted proof chain. These files were already failed author attempts; no live accepted code has been relabeled as an archive to evade acceptance.

The audit corrections do not relax the accepted mathematical axiom policy. Runtime implementation entries remain separate from transitive safe proof dependencies. The independent review’s clean trust-zero build and comprehensive audit already qualified this distinction, including the complete 30-module closure. This task does not substitute author increments for that independent evidence.

## Manifests and generation provenance

| Additional manifest | Entries checked | Result |
| --- | ---: | --- |
| `guard-author/manifest.json` | 35 | All SHA256 and byte lengths match. |
| `numeric-author/FILES.json` | 24 | All SHA256 and byte lengths match. |
| `path-author/frozen-receipt.json`, `files_sha256` | 15 | All SHA256 values match. |
| `registry-preflight/FILES.json` | 24 | All SHA256 and byte lengths match. |

The original author claim is preserved as exact blob `bbec37ae66adfa1e5321d7c85d3e5a0a67a13373` at coordination commit `b4dc82e6d8d521b4295236f171b8d9e1a1d690cd`; the actual claim tree and retained bytes match. Its two scout report hashes also match. The recorded foundation commit has exactly the documented GuardedPath and ReturnClock parents. These historical records do not confer current-main ownership.

The preflight generator derives its registry from literal source imports, verifies inherited registry/source identities against the foundation, rejects conflicting aliases, captures new source bytes, and checks actual author receipts before its final freeze. It invokes no Lean compiler. Its history is retained without rewriting: run000 is an inherited 27-module metadata check; run001 is the provisional 30-module registry; run002 is the author-frozen 30-module registry. All three module pin maps agree with their corresponding portion of the finally qualified closure. All 14 author-confirmation receipt links match their exact SHA256s. The final preflight registry equals the published root registry byte-for-byte, SHA256 `239a98f425775ffa41298e1776e7618aed4793f064115f8571f4a29bc0dabac7`.

Historical `PENDING` fields in the frozen registry/preflight and the top README’s earlier publication wording remain temporal records. Later actual parent execution, independent execution, and submitted COMMENT review 5555324338 establish their respective later actions. The README and scope records consistently retain the supplied-cycle condition, full tuple endpoint equalities, explicit finite safety, one fixed seed/schedule, successor-seed timing, original METHOD attribution, and absence of a concrete cycle/196 claim. The signature-only review-preparation note expressly disclaims source inspection and execution; it is not used as an independent build or source-review receipt. The rolling queue lists candidates rather than assigning ownership.

The sibling audit already verified the 108-file independent manifest, six-file complementary manifest, original 63-file parent manifest, and separate 67-file package manifest, including the canonical checker snapshot. Their qualified results are reused without adding a second review gate or changing original flags.

## Recovery and reproducibility

Sixty-eight distinct locally absent blobs were retrieved through the supported read-only GitHub blob API. Every response was decoded as bytes and independently reconstructed as `SHA1("blob " + byte_length + NUL + bytes)`; all expected object IDs matched. Their content SHA256s, byte lengths, and destination paths are retained in `fetched-hashes.json`. Local object absence was never treated as remote data loss.

All 107 newly inspected archive files are retained under `retained/` with their original repository paths. `fetch-responses.json` preserves the retrieval responses. For recovery, use each exact H-tree path/blob in `inventory.json` or the corresponding blob object via `repos/taco-jpg/p196-algorithm/git/blobs/<sha>` and require its recorded Git blob and SHA256 before use. Previously qualified review/source bytes remain under `../reuse/retained/`.

Binary `.olean` outputs are explicitly omitted from Git and inventoried separately as historical generated objects; this task does not claim to recover those binaries. Source, pinned environment, driver, and result provenance are retained. The canonical fresh source build and independent clean replay provide the recovery route without depending on those old author caches. Historical author drivers retain their original absolute workspace paths and are archival replay records, not a claim that an arbitrary new checkout already contains those caches. The README’s repository-root canonical verifier command is the appropriate clean rebuild entry point; its implementation and package were already inspected in the evidence-reuse task.

This task executed only Git metadata reads, byte/hash checks, JSON/manifest comparisons, and retained-text inspection. It executed no Lean compiler, archived generator, verifier, or author script. An initial metadata checker attempt invoked Git’s default rename detection and encountered a locally absent blob; its log is retained as `check_archive_scope-attempt001.log`. The final checker uses `--no-renames` for the exact path comparison and passed without needing unrelated object contents. No remote state or source file was modified.

## Delivery consequence and retained output

The remaining archive/diff-scope obligation is satisfied. Existing PR #154 and #166 ownership remains unchanged, and the occupied main writer slot is not assumed available. Agent #16 retains PR #168 delivery responsibility. The next steps belong to that delivery task’s dependency integration, current-state refresh, acknowledged writer handoff/slot, and actual guarded merge protocol. This result creates no new mathematical or review gate.

Primary new outputs are `ARCHIVE_SCOPE.md`, `checks.json`, `inventory.json`, `check_archive_scope.py`, `check_archive_scope.log`, and `fetched-hashes.json`. The machine-readable checks record the reused evidence hashes and exact formal-review identity so that publication can preserve this qualification’s source binding.
