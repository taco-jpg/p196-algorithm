# PR167 final package structural audit

**Verdict: PASS_STATIC_PACKAGE_CHECKS, within the scope below.** The exact proposed package contains 699 additions, no modifications or deletions, and no missing committed content in the recovered snapshot. Its actual PR167 mathematical contribution is two new Lean sources and one frozen scoped registry; 403 of the additions are unchanged inherited PR150 material. All own evidence is classified. No new source-level wiring defect, unexpected executable payload, or omitted substantive item named by the checked author/hash manifests was found.

This is a source/package audit by the Agent15 subordinate `/root/runtime_inventory`, separate from authorship. It does **not** assert a new Lean execution, mathematical review, independent-review approval, merged-tree build, main publication, or ownership transfer. The independent strictfresh41 qualification and 144/85/88 manifests belong to the separate `/root/pr164_evidence` workstream. Agent15 owns PR167 delivery; Agent1 retains source ownership. PR150, PR154, and main remain with their existing owners.

## 1. Exact scope and evidence identities

| Role | Exact commit |
|---|---|
| PR167 proposed head H | `502d3f5ea2e516f7cf4342854e1ec865f188d4f3` |
| PR base, Clock | `ebcaf723d61f9513c8bae30440d02ba4a46343b4` |
| PR150 side dependency, Core | `946c69edf3d2e6a87f5516db1fd0091eae29e663` |
| Mathematical source reviewed originally | `24cbcc99754cadb2d9ce4ba448e3a91171b9f4f0` |
| Combined source foundation | `84a65f296625e16851b4a369e27ffca43aaea40c` |
| Main policy snapshot inspected | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |

Public references: [PR167](https://github.com/taco-jpg/p196-algorithm/pull/167), [exact H tree](https://github.com/taco-jpg/p196-algorithm/tree/502d3f5ea2e516f7cf4342854e1ec865f188d4f3), [combined foundation](https://github.com/taco-jpg/p196-algorithm/tree/84a65f296625e16851b4a369e27ffca43aaea40c), [side Core commit](https://github.com/taco-jpg/p196-algorithm/commit/946c69edf3d2e6a87f5516db1fd0091eae29e663).

All six trees were read from Git without lazy fetching or optional locks. Missing local partial-clone blobs were recovered through the read-only GitHub blob connector or reused from the sibling's already recovered blob cache. Every one of the 699 local snapshot files was then checked against its canonical Git blob SHA-1, SHA-256, and byte count. A partial checkout's absence of a materialized file was never treated as a missing committed source.

The complete recovered content is 16,163,633 bytes, representing 280 unique Git blobs. Every added entry is a regular `100644 blob`: no executable bit, symlink, or gitlink. The 32 Python paths are preserved script text; they were parsed but never executed or imported.

Evidence under this report directory:

- `pinned-trees.json` and `delta.json`: complete pinned trees and the exact path/mode/blob comparison.
- `head-delta/` and `final-snapshot-manifest.json`: all 699 exact added files and per-file SHA-256/Git identities.
- `check_package.py`, `execution-receipt.json`, `check-results.json`, `lightweight-checks.json`: reproducible read-only checks and the actual successful execution.
- `group-inventory.json`, `script-static-inventory.json`, `own-lean-classification.json`: exhaustive structural classifications.
- `author-manifest-checks.json`, `historical-hash-manifests.json`, `author-command-flags.json`, `retained-negative-records.json`: manifest, flag, exclusion, and failure results.

The original `inventory-summary.json`, `local-object-availability.json`, and extraction records retain the initial partial-cache observations. Final availability is given by `final-snapshot-manifest.json` and `check-results.json`; the earlier missing-local-object count is not a final source omission.

## 2. Complete delta and meaningful groups

The base-to-H difference has exactly **699 added entries, 0 modified entries, and 0 deleted entries**.

- **403 inherited entries / 10,059,730 bytes** match both sideCore and combinedfoundation in path, type, mode, and blob.
- **296 own entries / 6,103,903 bytes** are new relative to combinedfoundation.
- The own 296 consist of **2 mathematical source files + 1 registry + 293 evidence files**.
- The inherited 403 consist of **4 mathematical source files + 1 registry + 398 evidence files**.

The complete extension census is 316 Lean files, 187 logs, 124 JSON files, 32 Python files, 18 Markdown files, 15 text files, and 7 SHA-256 manifests. Repeated source snapshots and script copies are historical evidence, not additional independent proofs or runs.

### Own PR167 groups

The common evidence prefix is `proofs/contributions/agent-1/periodic-return-upper-gap-20261017/`.

| Group | Files | Meaning |
|---|---:|---|
| Root mathematical files and registry | 3 | InitialIncoming, ReturnUpper, frozen 41-module registry |
| README | 1 | Current scope, evidence hierarchy, reproduction and publication chronology |
| incoming-author | 21 | Strict author increment, original dependency-object reuse, source and audit |
| registry-preflight | 6 | Registry generator, pin receipts, recorded whitespace failure |
| review | 145 | Independent review package: 144 selected evidence files plus its manifest |
| scope-review.md | 1 | Historical source-only scout, explicitly unproved proposals at capture |
| upper-author | 30 | Three source attempts, all commands/logs, audit, runtime exclusions |
| verification | 89 | Parent original selection, frozen checker and provenance, separate package manifest |
| **Total** | **296** | |

### Inherited PR150 groups

The common evidence prefix is `proofs/contributions/agent-1/periodic-return-core-20261016/`.

| Group | Files | Meaning |
|---|---:|---|
| Root mathematical files and registry | 5 | OuterRank, QuotientPath, ReturnCore, ZeroPath, Core registry |
| README | 1 | Reviewed result plus retained earlier checkpoints |
| assembly-inspection | 11 | Source-only literal and contract inspection |
| data-review | 16 | Stored finite partition/rank diagnostic, not SCC discovery |
| path-author | 13 | QuotientPath author increment and audit |
| rank-author | 23 | Generator, finite diagnostics, source/probe and compilation evidence |
| registry-preflight | 23 | Historical provisional and frozen registry records |
| research-queue.json | 1 | Scoped research record |
| return-author | 61 | Complete retained ReturnCore author attempts and dependencies |
| review | 127 | Existing independent Core review package |
| scope-scout.md | 1 | Historical scouting |
| verification | 83 | Existing parent Core package |
| zero-path-author | 38 | Author compilation and all audit attempts |
| **Total** | **403** | |

Their inheritance establishes byte preservation. It does not by itself transfer PR150 delivery ownership or assert an additional review of its mathematics.

## 3. Mathematical source and registry boundary

| Path | Exact Git blob | SHA-256 |
|---|---|---|
| `proofs/Agent1PeriodicInitialIncoming.lean` | `ac70d223082c44d28d0f81d9049e1d2603a84d55` | `acf7b30677c467b30f7ef978effa8506fb75ead9cf2512d8c1af97f09318edda` |
| `proofs/Agent1PeriodicReturnUpper.lean` | `be87d8b534b57ab097ad90e70ebf000dcb1d825c` | `ff200fa0dbfd1d01ded585f2c182dd65e1fe296f881e1408e219aff166aecd97` |
| `proofs/Agent1PeriodicReturnUpper.registry.json` | `0c6650738bed8f70c7cbf374c435e0bef902ba96` | `9045d97fc4f687d1e9c7eb38c6d4002afaeb488bae7cc8ab524ac2e6bd819d1c` |

All three root entries are byte/mode identical at mathematicalsource and H. The registry's 41 module paths, Git blobs, SHA-256 values and literal import lists match H. Every selected source is unchanged from mathematicalsource. Its root DFS is complete and acyclic; no unlisted local import or unused extra module is required by the scoped root.

Of the **132 own added Lean paths**, **124** are exact copies of the 41 frozen source blobs. The other eight paths are completely classified:

- InitialIncoming audit source;
- independent ReviewAudit and parent ProjectAudit sources;
- three UpperAudit copies/versions;
- failed Upper attempt001 and smaller passing attempt002 source snapshots.

There is no extra uncatalogued own mathematical module. Failed and partial historical sources remain evidence, not accepted build roots. Generated audit code inspects the environment, checks named declarations and collects allowed axiom dependencies; it is not an alternative theorem source.

The five registry endpoints are:

1. `Agent1.Periodic.phaseEdge_initial_clock`
2. `Agent1.Periodic.quotient_return_initial_last_clock`
3. `Agent1.Periodic.quotient_path_lower_potential`
4. `Agent1.Periodic.quotient_return_initial_upper_gap`
5. `Agent1.Periodic.quotient_return_initial_upper_gain`

The package states the exact positive full-return restriction at the original phase `[14,14,4,4]`: `N + 2 ≤ 4*C`, and the corresponding gain bound with `C = 8*G`. It retains full tuple return and validity premises. It does not claim cycle existence, arbitrary graph realization, safety closure, an infinite integer orbit, or P196. The separate stronger-gap contribution is not silently imported.

[Exact package README](https://github.com/taco-jpg/p196-algorithm/blob/502d3f5ea2e516f7cf4342854e1ec865f188d4f3/proofs/contributions/agent-1/periodic-return-upper-gap-20261017/README.md) and [frozen registry](https://github.com/taco-jpg/p196-algorithm/blob/502d3f5ea2e516f7cf4342854e1ec865f188d4f3/proofs/Agent1PeriodicReturnUpper.registry.json) provide the original claim and reproduction scope.

## 4. Inventory coverage, flags, exclusions and failures

The executed lightweight check completed at **2026-10-17T05:56:36Z**, using Python 3.12.14, with **729 checks and zero failures**. This count includes per-file identities; it is not a count of independent experiments.

### Checked here

- The incoming-author manifest lists 20 files and covers its full 21-file directory except itself.
- The upper-author manifest lists 29 files and covers its full 30-file directory except itself.
- All **49 author manifest entries** match committed bytes and lengths.
- All **7 historical SHA-256 manifests** have **58 present matching entries**, **4 specifically named omitted `.olean` objects**, and no missing substantive entry.
- Both incoming omitted objects have matching recorded runtime hashes; upper-author separately inventories its two successful generated `.olean` outputs. Omission of reproducible objects is documented and consistent with publication policy.
- All 124 JSON files parse successfully.
- All seven recorded new author compile/audit commands retain `--trust=0 -j1 -DElab.async=false`. They expressly reuse dependency objects and do not become independent fresh-build claims.
- The packaged canonical checker is exactly the existing main checker, blob `21131b03dfa516eb19a0a7a4df4f2a41020d4db1`. Its historical command has no explicit trust override. That distinction must remain.

### Separate specialist qualification

The review's 144-entry manifest, parent's original 85-entry manifest, parent's separate 88-entry packaging manifest, 42 strictfresh commands, source snapshots, complete module-origin audit and implementation inventory are handled by the sibling review-reuse audit. This report preserves those files and their H identities but does not duplicate that qualification or elevate its own static checks into a fresh proof.

### Failures remain present and correctly classified

The JSON scan finds nine nonzero-exit observations, including repeated references to the same original execution. They represent six distinct historical events, not nine different failures:

| Event | Recorded outcome |
|---|---|
| Core ReturnCore author attempt001 | exit 1 |
| Core ReturnCore author attempt002 | exit 1 |
| Core ZeroPath audit001 | exit -11 |
| Core ZeroPath audit002 | exit 1 |
| UpperGap author attempt001 | exit 1, unknown `Nat.cast_zero` |
| UpperGap publication whitespace check | exit 2, terminal blank lines in two preserved reviewer scripts |

Upper attempt002 passed a smaller source; attempt003 passed the final frozen source. None of those author increments is relabeled as an independent fresh closure. The whitespace failure is accurately retained as a packaging diagnostic, with no Lean-source whitespace error and no stated proof-gate role.

The historical authentication failure is described as locally retained operational evidence; the package does not claim its log is part of the committed research selection. Operational publishing helpers/logs are distinct from substantive compiler or proof-audit logs. No committed manifest checked here promises an absent authentication log.

Frozen registry fields and older README sections still say fresh verification or remote publication was pending. Those fields describe capture-time state and remain frozen intentionally; newer completed receipts are separate. They should not be rewritten to manufacture a cleaner historical record or read as the present platform state.

## 5. All added Python scripts and their side effects

All 32 Python paths reduce to **21 distinct blobs**. Each distinct script was source-read; repeated copies were identified by exact blob, and the closely related inherited review driver was inspected as an exact textual diff from the fully read UpperGap driver. All scripts pass AST parsing without execution. Static inventory found no `shell=True`, network-library import, dynamic `exec/eval` invocation, remote Git write, credential read, or background service.

This is not a general sandbox guarantee for arbitrary future invocations. These are historical research helpers; several intentionally write files. The important boundary is what each script actually does and which command is the supported replay entry point.

### Own PR167 script families

| Family | Distinct blobs / paths | Actual effects and limitations |
|---|---:|---|
| Incoming compile/audit `run.py` | 2 / 2 | Uses pinned historical compiler/dependency paths; writes sibling commands, logs, manifests and objects. Reuses dependency objects. Historical directories can be overwritten if these exact helpers are rerun there. |
| `registry-preflight/build_registry.py` | 1 / 1 | Reads Core/Clock registries, validates matching pins, computes new blob identities, then writes the root Upper registry and local metadata. It is a generator, not a read-only verifier. |
| Independent `review/replay.py` and snapshots | 1 / 3 | Requires fresh build/evidence paths, copies exact source, runs pinned Lean explicitly at trust0 with limits, writes complete evidence. No prior project objects are reused. No replay was executed here. |
| `review/seal-evidence.py` | 1 / 1 | Asserts existing results and source/log identities, copies original parent text evidence, writes review metadata/manifests. Uses hardcoded original session paths. It is an evidence assembler, not a Lean execution, and can overwrite its historical metadata if rerun. |
| Upper author `run.py` and three snapshots | 1 / 4 | Creates a new attempt directory, records source, compiler, reused dependencies and capped Lean output. Preserves the failed attempt. Hardcoded original dependency locations limit portability. |
| Canonical checker copy | 1 / 1 | Identical to main's source-pinned verifier. Writes a fresh chosen output directory; verifies exact source/import closure and runs the selected project. |

The seven distinct own blobs include the canonical checker already present in the inherited package. Therefore own-seven plus inherited-fifteen yields 21 unique scripts overall, not 22.

### Inherited Core script families

The complete static inventory records full blob/SHA identities, every path, imports, and notable write/process calls.

| Family | Distinct blobs | Effects retained from sideCore |
|---|---:|---|
| Assembly literal checker | 1 | Reads stored source snapshots; writes local comparison manifest |
| Finite data reviewer | 1 | Reads and decompresses a pinned existing graph; checks stored partition/rank facts; writes new output directory; no SCC discovery |
| Path author compile/audit drivers | 2 | Fresh attempt/audit directories, historical objects, bounded child Lean, recorded logs |
| Rank generator and runner | 2 | Generator creates a missing OuterRank source and probe with nonexistence guards; runner records bounded author compilation |
| Registry preflight versions | 2 | Preserve source snapshots and generate/overwrite the scoped Core registry; historical metadata generators |
| Return author attempt/staging helpers | 2 | Copy dependency objects into local build; attempt helper deletes only the named local build `.olean` before recompilation, then writes a fresh attempt |
| ZeroPath author wrappers | 3 | Write original attempt/audit logs and objects under historical paths; earlier low-resource/classification failures remain |
| Independent Core replay | 1 | Fresh isolated output, pinned source/compiler, strict compilation and full audit |
| Canonical checker | 1 | Exact same existing main verifier as the own package |

The only reviewed deletion call is the ReturnCore helper's deletion of a generated `.olean` inside its local build directory. No source deletion or history rewrite is present. This helper was not executed. Registry generators and sealing helpers should not be used as the final read-only validation command on preserved evidence.

No workflow, dependency declaration, root application configuration, or global verifier is modified by the 699-file delta. None of these preserved scripts is newly installed as an automatic CI hook.

## 6. Real accepted-build configuration and publication duties

The applicable documents were read at the pinned main commit and their content hashes checked: `AGENTS.md`, `proofs/README.md`, `REPRODUCE.md`, `CONSOLIDATION.md`, `PUBLICATION_POLICY.md`, `PUBLICATION_SCOPE.md`, and `ACCEPTED_BUILD.json`. Their exact identities are in `main-policy-identities.json`.

### No new mandatory default-registry gate

The [main consolidation policy](https://github.com/taco-jpg/p196-algorithm/blob/74a1c3922eb7af438fe40b23d2105ad07556e3f5/proofs/CONSOLIDATION.md) explicitly says the global accepted catalogue remains incomplete, the default proof command intentionally does not return global success, and accepted source-specific scopes retain their own instructions. Main's accepted registry has `catalogue_complete: false`.

The canonical checker supports an explicit `--registry` plus `--project` selection. The new scoped registry names its exact root and all 41 dependencies. Its intentionally false global-completeness flag does not prevent a scoped project result.

The package's actual canonical command, adapted only to the operator's absolute compiler/output paths, is:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --registry proofs/Agent1PeriodicReturnUpper.registry.json \
  --project agent1-periodic-return-upper-gap \
  --output /absolute/new/output/directory
```

The official Lean release is 4.19.0, commit prefix `6caaee842e94`. Output must not already exist. The hashed canonical filename is the real verifier selected by this package; `--check-only` is not a mathematical build. The separate independent driver in the package README provides an explicitly trust0 replay with fresh build and evidence paths.

**Finding:** no required missing source/import/build wiring was found. Registering PR167 in the default `ACCEPTED_BUILD.json` is not a gate established by the inspected current instructions and must not be invented.

### Publication integration remains a separate duty

The [publication policy](https://github.com/taco-jpg/p196-algorithm/blob/74a1c3922eb7af438fe40b23d2105ad07556e3f5/proofs/PUBLICATION_POLICY.md) requires release overview/findings, coverage inventory, file list, byte manifest and verification records to reflect the published selection, while preserving earlier versions and research failures. Consolidation also distinguishes complete current tracked-file coverage from mathematical acceptance.

The 699 additions contain package-local evidence and manifests. They do **not** update the repository-wide overview or cumulative publication inventories. Therefore the authorized integrator must account for the final combined selection in the publication metadata and run the applicable integrity check when publishing it, or explicitly identify the companion integration change that does so.

This is an **integrator publication obligation**, not a missing mathematical dependency and not a reason to demand a new global accepted-build registry entry. A source PR can retain its exact reviewed bytes while the integration owner prepares the separate publication metadata. No global-index regeneration or source rewrite was performed in this audit.

The root AGENTS rule still reserves main writing to the acknowledged writer. This report changes neither that ownership nor dependency owners.

## 7. Remaining work and limits

No additional package repair is indicated by these static checks. The remaining delivery decisions are external to this audit:

1. Reuse the separate specialist's exact-source independent-review qualification, including complete 144/85/88 manifest and audit evidence.
2. Retain the parent's actual intended-combination results and check exact source pins in that tree; do not substitute the source PR's baseline for the target guard.
3. Coordinate inherited PR150/PR154 dependency handling with their existing owners.
4. Have the authorized main integration writer account for cumulative publication metadata and platform/main outcome.

The parent reports that actual merge-tree checks are being handled in its isolated repository. Those results are not claimed as executions performed or independently validated by this package auditor.

No Lean was run. No package script was run. No Git checkout/object store was mutated. No remote comment, claim, ref, source, review, or publication was written. All original source bytes, unsuccessful records and historical classifications remain recoverable in the exact snapshot accompanying this report.

