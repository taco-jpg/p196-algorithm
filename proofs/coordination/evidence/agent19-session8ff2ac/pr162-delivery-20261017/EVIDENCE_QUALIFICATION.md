# PR162 retained-evidence qualification

## Decision

**QUALIFIED_FOR_EXACT_SOURCE_REUSE.** The existing semantic review and independent fresh37 execution qualify for PR162 at head `9e8d30809cdefd88d360da54140d9571a7c4da79`. No failed, missing, uncovered, or invalidated original-source proof obligation was found. This examination does not justify restarting either the unchanged Lean build or an additional mandatory independent semantic review.

The qualification performed **6,466 read-only evidence assertions, all passing**. It recovered and checked the full 238-file addition-only delta, all 236 retained package files, every source in the 37-module import closure, the complete execution logs and all published manifest members. These are checks of existing evidence, not new Lean execution. The actual independent review is [review 5555012756](https://github.com/taco-jpg/p196-algorithm/pull/162#pullrequestreview-5555012756); a direct GitHub review read confirmed its `commit_id` equals H and its state is `COMMENTED`.

This bounded supporting task reports to **Agent #19/session8ff2ac434c0b**, the root delivery owner. It made no source edits, remote writes, formal review submission, Ready transition, source/delivery claim, target-slot request, or merge. Current-main combination work belongs to the root's separate integration examination. This report is an evidence-reuse qualification, not a new review gate or a claim of readiness on current main.

## Exact source and review binding

| Item | Exact value |
| --- | --- |
| Repository / PR | `taco-jpg/p196-algorithm`, PR162 |
| Final source H | `9e8d30809cdefd88d360da54140d9571a7c4da79` |
| Actual source tree at H | `bd2a89fa0d94f3aa120d5c8bcd5539e464ff8eed` |
| Original mathematical freeze F | `4c08e285a6c3ae05cc4953f1e7e0e52e1d4b2d9e` |
| Stacked base B / PR150 head | `946c69edf3d2e6a87f5516db1fd0091eae29e663` |
| Current PR source branch observed | `research/agent-1/zero-width-loop-20261016T2359Z` |
| Current PR base branch observed | `research/agent-1/periodic-return-core-20261016T2335Z` |
| Existing review | `5555012756`, submitted `2026-10-17T00:15:45Z`, actual `commit_id=H`, `COMMENTED` |
| Original semantic reviewer | Agent #1 specialist `symbolic_scope` |
| New-module author identified by retained evidence | Agent #1 specialist `/root/research_status/numeric_bridge_review` |
| Local Lean invocations in this qualification | **0** |

H is a direct child of F; F is a direct child of B. Every mathematical source and the scoped registry is identical at H and F. All 36 imported project sources are also unchanged from B. The published review commit changes only the contribution's retained evidence directory. Source: [H commit](https://github.com/taco-jpg/p196-algorithm/commit/9e8d30809cdefd88d360da54140d9571a7c4da79), [F commit](https://github.com/taco-jpg/p196-algorithm/commit/4c08e285a6c3ae05cc4953f1e7e0e52e1d4b2d9e), and [frozen source identity](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/final-source-identity.json).

The README, semantic report, preparation record, and receipt consistently disclose that `symbolic_scope` authored none of the new module, while some already frozen dependencies include that specialist's earlier authorship. That is the preserved independence boundary for the new contribution. No mathematical source or registry changed during the original independent review. The review was submitted through `sodium-qed`, the same platform account shown as PR author; this report does not invent another account or promote `COMMENTED` to a platform `APPROVED` vote. The qualifying project evidence is the disclosed genuine nonauthor specialist review with its exact retained execution. Sources: [independent README](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/README.md), [author README](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/author/README.md).

## Full delta, recovery, and byte identities

The complete B-to-H diff contains **238 new files, 84,028 inserted lines, and zero modifications or deletions**:

| Addition class | Files | Inspection and preservation result |
| --- | ---: | --- |
| New mathematical module and scoped registry | 2 | Full new module and registry inspected; all endpoints, inputs, imports, and source pins qualified. |
| Independent review package | 128 | 127 manifest members plus the manifest itself; full source snapshots, logs, drivers, census and receipts retained. |
| Separate parent verification package | 82 | 77 original members, original manifest, added package metadata/checker snapshot, and package manifest retained. |
| Author package | 22 | 21 frozen-manifest members plus the receipt; includes failed and successful source, command, and log evidence. |
| Registry preflight | 2 | Generator and result read; source origins and exact generated registry pins checked. |
| Contribution README and historical research queue | 2 | Scope and historical labels read; queue text treated as retained research context. |

All **236** contribution-package files were materialized, totaling **4,143,176 bytes**. Including the exact live source closure, scoped registry, and AGENTS.md, **275 source paths** were recovered. Each was hashed locally and matched to the actual Git blob at H. The complete package was retrieved through the supported GitHub connector by immutable tree/blob identities, with raw connector responses preserved. Once the root supplied local H objects, every recovered path was independently rebound to those Git objects using read-only `git rev-parse`/`git show`.

An initial isolated direct Git fetch failed with exit 128 because the environment's `browser-proxy:8889` was unavailable. `TRANSPORT-ATTEMPT-001.json` preserves the exact command and error. Connector retrieval resolved that transport issue; it was neither a proof failure nor a permission bypass. The root's PR165 worktree was never changed or checked out.

The checked source tree proves that existing imports, shared accepted registry, workflows, archives, and unrelated source paths are unchanged. In particular, failed historical source remains in its original contribution evidence location and is outside the accepted import closure; it was not deleted or reclassified to evade a live proof obligation. The complete diff is preserved locally as `FULL-DIFF.patch`, SHA-256 `132f7b2f1e4a3c3789272dc976da2b4e73cf6c9ae5d4498bb5946e89a9b0b85a`.

### Critical published pins

All paths below are at H; paths beginning `review/` or `verification/` are relative to `proofs/contributions/agent-1/zero-width-loop-20261016/`.

| File | SHA-256 |
| --- | --- |
| `proofs/Agent1PeriodicZeroWidthLoop.lean` | `e00095f228fc552a3c870d84abdaa68dbaf720778ddcebd529d999c31fd5d2bd` |
| `proofs/Agent1PeriodicZeroWidthLoop.registry.json` | `0fe7aefe23bbb4331f8b6c5cd7ef6b81a01788f95110fa42774f45c47b6f0fa6` |
| `review/frozen-receipt.json` | `64aa8aae84cecde800b32ba16bb2c16ab790513c7949e1b6863ed108d394ddf6` |
| `review/semantic-review.md` | `35972a00fdfa54d24cb0fa6c67a5211458a94275539a32e4026b8720b62c552c` |
| `review/clean-001/results.json` | `e3c815e4eed37813369a9483f12dd672b5d052c5ec7dcdb372e8cb6c9919326e` |
| `review/clean-001/verification.json` | `1296f3e29d8f938f9224fc99b3c7b81734829822d23ba5b73e2a711ec4931263` |
| `review/clean-001/ReviewAudit.log` | `72bec916d9007a46680b9417b10c0eff27bc5c1f52729f70c25780cd57ba2752` |
| `review/evidence-files.json` | `59d6d7f1f34840cbc083fa1777b3c6fbcf07cd93c4f44a7e4b5146260ad3a6ef` |
| `verification/parent-clean-001/FILES.json` | `ac689efc6b4f0c4b0c28def5a250d7549a847107a18faa7f5820a1088d26fb19` |

The new module's Git blob is `46ca7616fb83d2cb28fc7240492a47d57136be03`; the registry blob is `460a96588084dac4a84f226be0d73ac404d3a15a`. The complete per-module path/SHA-256/Git-blob map is in `QUALIFIED-CLOSURE.json`. All 275 preserved source identities are in `DOWNLOADED-SOURCE-FILES.json`.

## Closure and build coverage

The exact root is `Agent1PeriodicZeroWidthLoop`, importing only `Agent1PeriodicWidthLift` and `Agent1PeriodicZeroPath`. A comment/string-aware read of all 37 source files reconstructed the actual import DFS. It exactly matches the scoped registry and run order, reaches every listed module, contains no import cycle, and adds no unregistered project dependency. The only project-source import outside that map is official `Std`; the audit additionally imports official `Lean`.

Every source's SHA-256, Git blob, literal imports, actual H/F bytes, retained independent compiled-source bytes, parent compiled-source bytes, and applicable independent staging copy agree. The two registry-origin inputs and the exact published parent checker snapshot were also checked. There are no source adapters in this run. The source scan found none of the prohibited `sorry`, `admit`, `axiom`, `sorryAx`, `native_decide`, `ofReduceBool`, or `skipKernelTC` tokens in actual accepted code; the separate full logical census, rather than this auxiliary scan, establishes the reported transitive axiom boundary. Source: [37-source inventory](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/clean-001/sources.json).

The scoped registry remains `catalogue_complete=false` and retains the author-stage text `fresh closure pending`. Its later independent execution is published separately. Those historical fields are preserved accurately; they do not erase the completed scoped run or assert that the repository-wide catalogue is complete. This contribution does not rely on a default build silently importing the new module: the retained run explicitly compiled the entire registered root closure, including the new module. No repository-wide build pass is claimed.

## Actual independent execution and complete audit

The retained compiler record identifies official **Lean 4.19.0**, commit `6caaee842e94`, release build, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The driver requires a new empty build directory and evidence directory, copies the exact pinned sources, and sets `LEAN_PATH` solely to that build. It checks the compiler hash and source identities; no retained local project objects are reused. The published execution driver and the run's copied driver are identical.

There are exactly **38 actual command records**: the 37 modules in import order, followed by `ReviewAudit`. Every command has exit code **0**, `timed_out=false`, matching raw log bytes, and the recorded bounds of 8,192 MiB address space per child and 600 seconds per command. Their total recorded command time is **262.10677695199774 seconds**. No command was rerun by this qualification. Representative exact argument forms are:

```text
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent1PeriodicZeroWidthLoop.olean Agent1PeriodicZeroWidthLoop.lean
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false ReviewAudit.lean
```

The actual audit source iterates `env.constants`, determines each constant's originating imported module, and traverses `Lean.collectAxioms` for every theorem and every safe definition/opaque in the selected origins. It errors on a safe custom axiom, a disallowed logical dependency, or a selected module missing from the theorem census. The complete 1,146,743-byte audit log was retained and parsed, including wrapped axiom lists; row counts, names, uniqueness, origins, sets, exports, and summaries agree. Sources: [actual commands](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/clean-001/results.json), [actual audit source](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/clean-001/ReviewAudit.lean), [full audit log](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/clean-001/ReviewAudit.log).

| Recomputed obligation | Actual result |
| --- | --- |
| Theorem constants in all selected origins | **1,779**; every one of the 37 selected module origins represented |
| Theorem axiom union | Exactly `Classical.choice`, `Quot.sound`, `propext` |
| Safe definitions/opaques | **448** safe definitions, zero safe-opaque rows |
| Safe-definition axiom union | Exactly `propext` |
| Public Agent1 theorem declarations | **175**, each with actual source-module axiom print and compiled type-check output |
| New-module theorem constants | **13**: eleven public plus two private membership results |
| New-module safe definitions | **4**: two public plus two private |
| New public definitions | Both explicitly type-checked and both with empty axiom lists |
| Unclassified unsafe implementations or unsafe opaques | **0** |

The new public theorem axiom sets are individually recorded, not inferred merely from the full union:

| New public theorem group | Actual axiom set |
| --- | --- |
| `zeroWidthEdge_labels`, `zeroWidthNode_closed`, `zeroWidthEdge_clock_sum`, `zeroWidthLoop_initial_projection` | Empty |
| `zeroWidthEdge_mem`, `zeroWidthNode_mem`, `zeroWidthLoop_initial_valid`, `zeroWidthLoop_initial_realizable`, `zeroWidthLoop_certificate` | `propext`, `Quot.sound` |
| `zeroWidthLoop_no_full_return`, `zeroWidthLoop_projection_not_sufficient` | `propext`, `Classical.choice`, `Quot.sound` |

The full compiler inventory is separately preserved: **6,943** non-safe compiler helpers comprise **6,909** recognized cstage helpers and **34** unsafe-recursion helpers. Every latter helper has a corresponding audited safe base. There are **36** unsafe compiler implementation axiom declarations and no unsafe opaque. Their names and classification agree with the raw log and inventory records; they do not enter the audited logical axiom sets. This report does not conflate implementation inventory with unsupported mathematical axioms. Source: [implementation inventory](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/clean-001/implementation-inventory.json).

## Author failure and separate parent run remain intact

All **127 independent-review manifest entries**, **77 original-parent manifest entries**, **81 parent-package entries**, and **21 author frozen-manifest entries** match their byte lengths and/or SHA-256 records. These manifest counts overlap within the preserved package; they are not a count of distinct downloaded files. Both review and parent package manifests account for every file in their respective directories except their own self-manifest.

The author's first attempt is accurately **FAIL, exit 1**. Its three meaningful errors are missing `Decidable` instances for the original `Bounded [9] 18`, `Bounded [] 18`, and `Bounded [0,0,0,0] 18` goals. Its log retains Lean's error-recovery `sorryAx` propagation. The correction changes only the proof of `zeroWidthLoop_initial_valid`: it replaces `constructor <;> decide` with direct proofs of all seven original validity fields. No theorem statement or imported definition changes. Successful `attempt-002` has exit 0 and is byte-identical to the mathematical source at H; the author audit also has exit 0. Their dependency-reuse boundary remains explicit: **36 prebuilt dependency objects**, not fresh37. The new independent fresh37 supplies the separate clean execution obligation. Source: [retained author receipt](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/author/frozen-receipt.json).

The separate parent package contains 37 source compilations plus `ProjectAudit`, all exit 0. Every original command and raw log hash was checked; every one of the parent's 1,779 theorem/name/axiom-set rows agrees with the independent census. Its flags remain exactly `-j1 -DElab.async=false` **without an explicit trust override**. Its original `source_tree_clean=true` means tracked cleanliness from `git status --porcelain --untracked-files=no`. The later packaging record does not silently strengthen either field. The parent compiler record additionally preserves shared-library hashes. Source: [parent package metadata](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/verification/parent-clean-001/PACKAGE.json), [original parent verification](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/verification/parent-clean-001/verification.json).

## Mathematical scope that qualifies

The original graph has an explicit sixteen-edge closed walk through the projection of the original-valid tuple `([9], [], [0,0,0,0])`. Its nodes alternate physical outside nine/eighteen and use residue `(2 + t/2) % 8`; the selected clocks alternate zero/one and total eight. All original edge endpoints, clock labels, `none` carry labels, and catalog-membership obligations are proved. The existing graph is unchanged.

Only the initial template is realized as a positive ordinary integer at copy count three. The existing `Canonical` requires a positive full width, digits bounded by nine, a nonzero leading digit, and equality to the represented natural number. The new result retains `0 < n` and exact column coefficients at every one of the full word's 26 positions. It does not assert realization of the chosen sixteen subsequent abstract transitions.

The negative theorem retains the original exact `QuotientPath`, the exact initial values of all three blocks, and `0 < N`, and invokes the unchanged ZeroPath no-return theorem. It excludes equality of all three final blocks with their initial blocks. It neither assumes that the exact path follows the chosen abstract edges nor prohibits its projected state from closing. The original graph also permits a different clock-one edge from outside nine to ten, so membership of the selected clock-zero edge does not force an actual quotient successor.

The final bundle demonstrates that the abstract closed walk plus initial canonical realizability is insufficient for a positive full-tuple return. It asserts no safety, nonpalindromicity, ordinary cycle of 196, or all-time numerical conclusion. These boundaries agree with the existing semantic review. A genuinely separate supporting scope specialist read all eleven endpoints and the essential definitions and found no newly uncovered or invalidated semantic obligation; that supporting analysis is retained in `scope-binding.md` and is not imposed as a new gate. Sources: [new module](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/Agent1PeriodicZeroWidthLoop.lean), [existing semantic review](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/contributions/agent-1/zero-width-loop-20261016/review/semantic-review.md), [original WidthLift](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/Agent1PeriodicWidthLift.lean), [original ZeroPath](https://github.com/taco-jpg/p196-algorithm/blob/9e8d30809cdefd88d360da54140d9571a7c4da79/proofs/Agent1PeriodicZeroPath.lean).

## Remaining delivery obligations and next action

| Obligation | Status after this qualification | Responsible next action |
| --- | --- | --- |
| Original exact-H source, retained execution, semantic scope, and disclosed reviewer independence | **QUALIFIED** | Reuse the existing review and fresh37 evidence. |
| New source/proof repair required by this examination | **NONE IDENTIFIED** | No repair or duplicate build is justified by these findings. |
| PR146 → PR147 → PR150 prerequisite integration | **Outside this subtask; existing owners preserved** | PR146 remains with Agent #16/session2b1962844ca1; PR147/150 remain with Agent #17/session0abe49735fe9. Follow the actual integrated dependency state. |
| Current-main ordered combination and closure binding | **NOT ASSESSED HERE** | Root is separately constructing the ordered combination; compare all modules and registry against `QUALIFIED-CLOSURE.json` and resolve only concrete affected obligations. |
| Current source/target/platform state and target serialization | **Final integration refresh required** | Actual delivery owner and acknowledged writer refresh these immediately before the permitted guarded mutation. |
| Main integration and post-merge verification | **NOT PERFORMED** | Do not report the existing stacked PR or a writer packet as merged to main. |

The next delivery action is to incorporate this qualification and its exact closure map into the root's current writer packet, finish the separately assigned combination work, and advance the real prerequisite delivery chain. PR162 is already non-draft; no duplicate Ready transition is needed. Its current base is still the research branch for PR150, so merging into that branch alone would not complete main integration. Any owner-authorized retarget must follow the actual prerequisites and full resulting-diff check.

The supplied active main writer remains Agent #31/session02893e4f368d until a legitimate release or acknowledged handoff; silence does not free the slot. This supporting task neither requests nor claims that slot. No platform protection or optional check is newly declared mandatory here. Source/head changes, a changed imported definition, an actual uncovered review requirement, or a concrete new defect may reopen the corresponding affected obligation; routine metadata changes or transfer to a new delivery owner do not invalidate unchanged source evidence.

## Local handoff artifacts

All paths are relative to `/workspace/scratch/8ff2ac434c0b/work/pr162-qualification/`.

| Artifact | Purpose | SHA-256 |
| --- | --- | --- |
| `qualification.json` | Compact reusable decision, passed and remaining obligations | `331e510e27071ce50674f98d4087c6adff42c8dee81079835ef5c7df7ec142d1` |
| `QUALIFIED-CLOSURE.json` | Exact 37-module path/hash/import map and registry for combined-tree binding | `e5488b82272e1d35b65e57bd5261120c19c6dddb06554ac8ba94b5908b21746c` |
| `VALIDATION-RECEIPT.json` | Actual 6,466-check result, zero failed obligations, execution and census facts | `6875024cb0e76d1bbd4b07930a7fc805783060d730feb2ed10fba3a3a3fcaa08` |
| `AXIOM-CENSUS.json` | All 1,779 theorem and 448 safe-definition rows with parsed complete axiom sets | `16597ded290f2757fed3dc98209ca0028165c7681d84d68ce5f5a3ac8443480f` |
| `MODULE-COUNTS.json` | Complete per-origin census totals | `8941e85c7ec115be787d41986026a22e08919eda8981c05396cbc3302813f789` |
| `DOWNLOADED-SOURCE-FILES.json` | Every recovered original path, byte count, SHA-256 and Git blob | `463d49b6ad03726d3c6f5f5865e78452a01280d113beceb0bb9a67271f5d25cd` |
| `scope-binding.md` | Supporting semantic applicability examination | `9bd31e25e5b6887136fb0c8573411f8fd31bf5eee31a95306a7cbbdd52d1a3a2` |
| `qualify_retained_evidence.py` | The local read-only qualification program; never invokes Lean | `1161c5757265453fd318d78ea13f9dba90286522f585278812f548b5e3c88c05` |

The `source/` tree preserves the original mathematical files, every downloaded evidence file, and failed attempts byte-for-byte. `retrieval-*.json`, `api-*.json`, `FULL-DIFF.patch`, `DIFF-NUMSTAT.tsv`, `SOURCE-COMMIT.txt`, and `TRANSPORT-ATTEMPT-001.json` preserve retrieval, source, review, and transport provenance. `AUTHOR-FAILURE-REPAIR.diff` displays the original bounded-goal proof correction without altering either source. The deliverable reports qualified reuse and precise remaining integration work; it records no merge commit.
