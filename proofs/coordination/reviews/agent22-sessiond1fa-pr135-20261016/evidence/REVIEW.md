# PR135 retained verification and provenance review

**Reviewer:** Agent #22, independent nonauthor specialist `pr135_evidence`  
**Delivery owner:** Agent #22 root; original mathematical authorship remains with Agent #104 and the cited upstream contributors.  
**Decision:** **PASS — the retained complete canonical verification is reusable for the exact repaired source head.**  
**Fresh Lean compilation by this reviewer:** **NOT_RUN.** No Lean invocation, source edit, GitHub publication, ownership mutation, or merge was performed by this specialist.

## Decision and exact source binding

The original reviewed head was `786ea690d8221503ae93dc3f981b1b56749ff40f`. The effective head after the separately published documentation repair is **`32d2b92ec79becfbb4d2aa2cf9bd42f8bbd5597e`**, whose sole parent is that original head. Mathematical sources remain frozen at `dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4`; the thirteen generic dependencies remain pinned to `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`.

All **42** checks in the complete retained-evidence audit passed. The subsequent **seven** checks binding that audit to the repaired head also passed. There is **no outstanding retained-build, source-provenance, axiom-audit, or evidence-label gap** in this specialist's assigned scope. The one identified current-label defect was corrected without changing mathematical sources, verification programs, source snapshots, original reports, or logs.

The machine-readable conclusion is `AUDIT.json`. Its immutable predecessor, `audit-attempt-003.json`, contains the full 42-check result, all 523 selected-source records, historical run findings, and the original README finding. `check_retained_evidence.py` and `check_repaired_head.py` reproduce these read-only checks against already available Git objects. The original two audit attempts and corresponding checker versions are preserved.

This decision is not a claim that all of `main` was rebuilt or that PR135 has merged. Mathematical semantic review, the current-target combined tree, platform checks, integration ownership, and the guarded merge belong to the named delivery owner and the other assigned specialists. They should proceed using the qualifying unchanged evidence; this review does not create an additional Lean rebuild or review-of-review gate.

## Material inspected and governing policy

The full controlling role document, `AGENTS.md`, and [`proofs/PUBLICATION_POLICY.md`](https://github.com/taco-jpg/p196-algorithm/blob/786ea690d8221503ae93dc3f981b1b56749ff40f/proofs/PUBLICATION_POLICY.md) were read. The policy requires accurate evidence labels and retention of substantive sources, failures, logs, and reproducible source snapshots. It permits exclusion of compiled objects, dependency caches, and runtime installations as reproducible infrastructure when the reason is recorded.

In this review, `P/` denotes `proofs/contributions/agent-104/prefix620-kernel-20261016/`. Every original incoming file was read from immutable Git blobs: **2,703 added paths**, **1,314 distinct blobs**, and **19,590,558 bytes counting repeated paths**. There were no original modifications or deletions relative to the original merge base. This includes all current concrete sources, all contribution files, generated historical versions, retained raw logs, manifests, and review records. Reading the entire payload for identity and evidence preservation is distinct from the parallel specialist's mathematical review of the generated contents.

The following executable evidence programs were read in full without executing them:

- `P/generator/build_concrete.py`.
- `P/verification/author-base/build_base.py`.
- `P/verification/independent620/rebuild.py`.
- `proofs/verify_project.py`, `proofs/replay_original_layout.py`, and the selected unchanged backend `proofs/verify_project__214bf7673efe116b.py`.

Both complete frozen semantic reviews and their freeze/pin files were also read. No approval badge or summary was substituted for the actual reports, commands, sources, and logs.

## Source closure and provenance

The source sets in the generation manifest, dependency map, snapshot, standalone registry, original canonical report, and snapshot-linkage record agree exactly:

| Source group | Count | Exact origin |
|---|---:|---|
| Concrete 620 modules | 510 | `dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4` |
| Generic source dependencies | 13 | `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` |
| Selected root import closure | **523** | The union of those two sets |

For **every** source, this review read actual Git bytes and checked the recorded source commit, Git blob ID, SHA256, byte count, imports, original canonical snapshot digest, registry digest, build-source digest, and equality with the source at the current PR head. The complete closure was independently reconstructed from imports. It reaches exactly 523 modules from `Agent104Prefix620`, in the recorded dependency order; none is outside the root closure and no generated manifest member is omitted. There are no source adapters in this selected build. The external source imports are `Std`, with `Lean` additionally imported for the audit; their official objects are pinned below.

For generic sources carrying an original-layout origin, the historical object was also read and compared. The three authoritative upstream inputs—the original certificate, `gen_code.py`, and `scope.py`—match the retained copies and their archived Git objects. The manifest's adapter hash matches the actual `generate_frozen620.py`. This is source identity validation; no new generator or finite mathematical computation was executed here.

Important immutable digests are:

| Artifact | SHA256 |
|---|---|
| Generation manifest | `d2b92c7139f59fe1cb8268addd0d10073780275f06b109bc3cf72933f9170c03` |
| Root `Agent104Prefix620.lean` | `9c4af5ff576c4184c1beb7fded6e1c0a33a815bfb1130793029815e66ab3e653` |
| Original certificate | `e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5` |
| `independent620/build.json` | `f044307147ccd1541aea7b0a537ca05347bf0100f5aafa50433332a7809a5a36` |
| `independent620/REGISTRY.json` | `509310b61aefbef5f4330eb0e8bbbc1f4d71a1728edaeeb5f147d48eb6a603a3` |
| `independent620/source-snapshot.json` | `09e0c610ba247e3e16995cd4ed4c4eddc815735a43a5c2e04cbae56834c75035` |
| Original canonical report | `52992057d5f3051a6db6413ed724375e06f903ef8ea78a145ef23693f2edba30` |
| Complete `ProjectAudit.log` | `8c59855ddc50189307e0da9d08d9b9f917ae30ec7bbf0c7e15db11f8c30b5ca6` |
| Generated `ProjectAudit.lean` | `08db920c5f80724b9bc0b85f9f3fa2c474ac607f0b841b9803dff6672a1c53d5` |

The actual source linkage is documented in [`SOURCE_SNAPSHOT_LINKAGE.json`](https://github.com/taco-jpg/p196-algorithm/blob/786ea690d8221503ae93dc3f981b1b56749ff40f/proofs/contributions/agent-104/prefix620-kernel-20261016/verification/independent620/SOURCE_SNAPSHOT_LINKAGE.json), not inferred merely from a commit label in the outer report.

## Complete canonical execution

The inspected preparation driver creates a previously absent build directory, loads generic sources from their pinned Git objects, checks generated sources against the published mathematical commit and manifest, and constructs the selected original-layout replay. The wrapper and original backend are unchanged. Their exact verified hashes are:

| Component | SHA256 |
|---|---|
| Wrapper | `e314b0656470773e81d14d04bbb548f914cd9e9808c89fdb07166d8ca58ef55b` |
| Replay helper | `744180f651360c1df34d1fad465dc009a304abbafab5277ddfb163a738430c70` |
| Canonical backend | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |

The replay map contains **524** selected paths, including the backend, and **514** additions needed for this selected layout. All mapped source bytes agree with the independently checked source records.

The actual canonical report contains **523 module compilations followed by one complete audit**, all **524 with exit status 0**. Every command and its complete retained log was checked. Their order is exactly the independently reconstructed dependency order followed by `ProjectAudit`. The outer log contains the same 524 successful command receipts. The actual commands use:

```text
lean -j1 -DElab.async=false -o Module.olean Module.lean
lean -j1 -DElab.async=false ProjectAudit.lean
```

**These are default-trust=max commands. They do not contain `--trust=0`.** The evidence is a complete fresh source build in a new directory, with no author `.olean` reused; it must not be relabeled as an explicit-trust-zero execution. The independent compiler stage ran sequentially. The original canonical elapsed time is 1,504.317765 seconds, and the outer elapsed time is 1,510.532073 seconds.

All **527** retained canonical files were checked byte-for-byte against their preservation inventory. The original output inventory contains **1,049** entries: all 524 logs, 523 source snapshots, the generated audit source, and the report. Every entry was resolved to its retained file or its identical pinned source bytes. The publication list contains **547** files, of which **546** have nonself hashes in `PUBLICATION_SHA256.json`; the inventory's self-exclusion is explicit and consistent. The broader attributed publication count of 548 is not the count of this standalone list.

### Original-layout metadata is preserved and correctly interpreted

The raw canonical fields remain:

```text
agent = Agent #1
source_commit = 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5
source_tree_clean = false
repository_wide_pass = false
```

Inspection of the wrapper, replay helper, backend, source maps, and complete source linkage explains these values. The checker has a literal upstream implementation label, and its Git HEAD is the historical replay baseline in a materialized workspace. The actual execution actor is recorded separately as Agent #104 `runtime_scout`; the actual 510+13 inputs are linked to the published mathematical and generic commits. These unchanged metadata fields do not invalidate the selected-project result. Equally, they must not be represented as a clean build directly at the published head or a repository-wide pass.

The reproducible supported entry point is the bundled `rebuild.py --canonical` with its dependency map, generation manifest, published source reference, standard-library manifest, root, and endpoints. The originally contemplated flat `proofs/Agent104Prefix620.registry.json` is not the registry used by this execution.

## Exhaustive theorem and axiom audit

This review read the complete raw audit log and reconstructed the generated `ProjectAudit.lean` exactly. Its reconstructed SHA256 equals the retained audit-source SHA256. The audit iterates the actual Lean environment constants, selects by origin module, rejects every safe custom axiom, traverses every selected theorem with `Lean.collectAxioms`, and rejects theorem dependencies outside the three permitted foundational axioms. It includes compiler-generated theorem helpers.

The log contains **3,047 distinct theorem declarations** from **456** modules. The other **67** selected modules contain no audited theorem declarations but were still compiled. Independently parsed statistics equal the complete published statistics, including all per-module counts, endpoint axiom sets, histogram entries, and unsafe-entry names:

| Exact theorem axiom set | Count |
|---|---:|
| Empty | 1,577 |
| `Classical.choice` | 15 |
| `Classical.choice`, `Quot.sound`, `propext` | 105 |
| `Quot.sound`, `propext` | 922 |
| `propext` | 428 |
| **Total** | **3,047** |

The audit records **zero safe custom axioms** and **70 unsafe implementation axioms**. All 70 names and origin modules match the original report, outer report, and statistics. None appears in the theorem axiom union. Those implementation declarations are not accepted theorem dependencies.

| Exported theorem | Audited axioms |
|---|---|
| `Agent104.Prefix620.palindromeStarts620_iff` | None |
| `Agent104.Prefix620.ancestry_bound12` | `Classical.choice`, `Quot.sound`, `propext` |
| `Agent104.Prefix620.no_196_620_palindrome` | `Classical.choice`, `Quot.sound`, `propext` |

The earlier generic build's **1,453** theorem records are reproduced with the same module, theorem name, and axiom set in the complete final audit. The scope remains the canonical leading-digit-620 palindrome family. The separate depth-12 witness is not part of this registry or a dependency of this build.

## Runtime and standard-library identity

The retained environment is official Lean **4.19.0**, release commit `6caaee842e94`. The compiler SHA256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Every recorded compiler/library pin matches the independently obtained official-member manifest, including the executable, four shared-library paths, and all **1,471** `.olean` entries: **1,476 recorded files** in total.

The standard-library entries total **1,061,238,608 bytes**. Their complete set, byte sizes, and digests agree with the independently checked official archive:

```text
6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe
```

The inspected original build driver checks its input files, source snapshots, compiler/shared-library files, registry, and standard-library objects at completion as well as preparation. This specialist compared the retained pins with the independent 4,617-member official archive manifest; it did not rehash or download the entire runtime again. The origin-manifest hash is `d7485aac2bce75037c914c94f90bbd96d6f5bd272cfe99211730b3b02e02e012`; the comparison-report hash is `a7b95444d5b3578b476a62ea01afd26a0f26ee6ba3e9f65475606b67b686270f`. Their precise local input paths are recorded in the machine-readable audit.

## Author evidence and preserved failures

Author incremental verification and independent complete verification remain separate:

| Retained phase | Actual scope | Trust and concurrency |
|---|---|---|
| Generic base | 13 source compilations, one exhaustive audit, two tool-identification commands; all 16 exit 0 | Default trust=max; sequential |
| Author concrete history | Ten run records, 522 compiler commands, including eight failed commands | Explicit `--trust=0`; early scheduled stages allow two processes |
| Final author stage | 431 newly compiled concrete modules plus 79 reused author successes | Explicit `--trust=0`; one process |
| Independent canonical | 523 freshly compiled sources plus complete audit | Default trust=max; one process; no author object reuse |
| Canonical transport check | Source/import preparation only | Zero mathematical compilations; explicitly labeled accordingly |

The current author's success index contains all 510 concrete modules and matches their final source hashes and actual successful command/log records. All **1,057** recorded import-object hash links match the corresponding recorded objects. Seventy-one early success records have no per-import object-hash field; this is not silently filled in or treated as a clean independent build. Reproducible object bytes were not rehashed by this reviewer. Acceptance relies on the complete separate fresh canonical execution, not a new assertion about retained caches.

All ten historical author records, all command logs, and the exact eight failed source files were read and checked. Failures remain accurately classified:

| Historical attempt | Preserved failure |
|---|---|
| `data-002` | Two exit-1 logs report `unknown namespace 'Agent124.CodeCert'` |
| `pilot-001` | Initial monolith exit -9; concurrent short monolith exit -15, with explicit SIGTERM receipt |
| `finite-pilot-001` | Whole-list initial coverage exit -9; concurrent short coverage exit -15, with explicit SIGTERM receipt |
| `finite-pilot-002` | Both whole-list coverage reductions exit -6 and retain `Stack overflow detected. Aborting.` |

The signal -9 records establish termination, resource measurements, and the authors' resource diagnosis; they are not presented as mathematical counterexamples. Empty logs for killed processes are preserved as empty logs. Both deliberate termination receipts retain commands, reasons, and timestamps. The later structured-slice construction has separately successful evidence.

The audit also verifies **378** content-addressed development files and all **30** retired output records. Both coverage-helper attempts retain their exact sources, logs, and exit-0 records. No historical failure was rewritten as a pass or inserted into the final accepted manifest.

## Independent roles and completion

The frozen role record identifies the mathematical helper author as Agent #104 `/root`, the generated-instance author as `/root/scope_scout`, the nonauthor semantic reviewer as `/root/strategy_review`, and the complete-execution reviewer as `/root/runtime_scout`. The complete twelve-file review payload matches its freeze hashes. The three finite-control scripts match the hashes of their retained result files. All 526 published-source links in the final-connection control were checked against actual Git bytes, in addition to the original review's explicitly identified 13 direct-byte readbacks.

The semantic freeze's execution status remains pending at its historical timestamp. The later complete canonical report supplies the actual completion. The earlier author completion likewise retains its historical in-progress independent status. The current completion note clearly connects these records without rewriting them.

[Submitted review 5554394142](https://github.com/taco-jpg/p196-algorithm/pull/135#pullrequestreview-5554394142) was read directly and retained in `review-attribution.json`. It is a **COMMENTED** review at the original head, relayed by the author/publisher, explicitly attributing the work to the two real nonauthor specialists in the same session and shared GitHub account. It is attribution evidence, not an external peer review, separate-account platform approval, or substitute for the inspected raw evidence. No original reviewer execution is falsely claimed as work performed by Agent #22.

## Resolved README correction and repaired-head applicability

At the original head, the contribution README incorrectly grouped the 510 concrete modules and 13 generic dependencies under explicit `--trust=0` and one worker. Actual generic command records omit the trust flag; early concrete stages used two concurrent processes, with `-j1` per process.

The root delivery owner published the precise correction in [`32d2b92ec79becfbb4d2aa2cf9bd42f8bbd5597e`](https://github.com/taco-jpg/p196-algorithm/commit/32d2b92ec79becfbb4d2aa2cf9bd42f8bbd5597e). This audit independently confirms the complete delta is exactly:

1. Correct the contribution README's execution attribution.
2. Add its original bytes at `P/corrections/agent22-verification-wording/README-at-786ea690.md`.
3. Add `CORRECTION.json` with eleven checked command-evidence pins.

The preserved original README has SHA256 `c05c43508e33e93fbd820aa9b0aa92ed83ffd7a41cf8831c2cc4d59b5c70421f`; the corrected README has SHA256 `0f5f3eecd9c6d26f67fee7c400e9dc9180dc73f7ad81e0f2364a0583760f5dd7`. All prior paths except the README are unchanged. All 523 selected mathematical sources were rebound to the new head and match their existing Git blobs and SHA256 values. The original finding is retained in the old audit, and the final addendum marks it resolved. No proof obligation changed.

## This reviewer's real failed checks and reproducibility

The first offline checker run returned a failure because this reviewer incorrectly expected 1,475 recorded environment files instead of the actual **1,476**. All file digests already matched; the faulty assertion omitted one of four shared-library paths. `audit-attempt-001.json` and `check_retained_evidence-attempt-001.py` preserve that failure. The corrected checker derives the count from the standard-library and canonical compiler inventories. Attempt 002 passed 38 checks; attempt 003 added exact audit-program reconstruction, full statistics equality, original input pins, and generic re-audit equality, passing all 42. `AUDIT.json` records the successful seven-check repaired-head binding.

A first attempted root-level `PUBLICATION_POLICY.md` read returned an actual GitHub 404. The controlling policy was then found and read at `proofs/PUBLICATION_POLICY.md`. This was a path-discovery miss, not a missing repository policy. No failed Lean run was concealed: this specialist performed none.

The checkers require the already hydrated Git repository and the independently checked official-member/comparison manifests. Both disable Git lazy fetching and optional locks. Use new report paths because reports are created exclusively; earlier attempts are never overwritten. Example commands are in `REPRODUCE.txt`.

**Final scoped disposition:** retained verification **PASS and reusable** at `32d2b92ec79becfbb4d2aa2cf9bd42f8bbd5597e`; README finding resolved; no remaining evidence gap in this review. Delivery remains with Agent #22 root for the separately assigned semantic, current-target, platform, ownership, and integration actions.
