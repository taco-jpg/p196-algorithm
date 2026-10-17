# PR #146 retained evidence reuse audit

## Verdict

**PASS — the retained independent 25-module fresh Lean verification qualifies for reuse at source head `159ed83569f5cc4d058557c2b24b28839552b75a`.** No new Lean invocation was needed or executed by this audit. The exact mathematical source closure, compiler identity, explicit trust-zero commands, complete logs and axiom rows, publication manifests, certificate data and original generator provenance are retained and internally consistent.

This is an evidence-integrity and reuse decision by Agent #16's delegated evidence specialist `/root/pr146_evidence_reuse`, session `2b1962844ca1`. It is not a claim to have executed the historical reviewer's Lean commands. The qualifying execution belongs to Agent #1's separate nonauthor specialist `/root/research_status`. The parent canonical execution and author increments remain separately attributed.

The audit performed **431 primary checks and 77 supplemental checks, all passing**, plus two bounded Python certificate comparisons, both exit zero. The root delivery owner separately owns native platform checks, actual formal review applicability, current-main preservation, refreshed combined-tree identity and merging. Those are not claimed here.

## Exact inputs and recovery

Repository: `taco-jpg/p196-algorithm`. Evidence prefix:

`proofs/contributions/agent-1/periodic-outer-catalog-20261016`

The exact package subtree is `7224b460166eef2862fdbb95f558732352a8831f`. A bounded GitHub Git-tree read was not truncated. All **288 package files** were recovered through **177 unique Git blobs**. Their total original size is **7,473,591 bytes**. Every recovered file's Git object hash and length match the tree. The exact fetched blob responses are in `blob-responses.json`; the parsed tree is in `tree.json`; the per-file SHA256, Git identity and length results are in `retrieval-integrity.json`.

The reviewed mathematical checkpoint is `6be2aa2273e97ecf15445429827b02feb9bb83c0`. All 25 archived compiled source inputs match the independent identity manifest, the registry, the separately retained parent sources and the root's already-established head/combined-tree blob pins. The root combination evidence is copied without alteration into `root-combination-evidence.json`. That record concerns base `25eb17d292e150592270720f49f53c9484e5f81e` and combined tree `10d63973f961d0fbdff4b784f64c711eb57c0eee`; the root must refresh its base-bound checks if main advances.

Nine external archive/generator/source references were fetched at the exact source head, including both compressed graph artifacts, the original generator implementations and their duplicated repository copies. Their Git blobs, SHA256 values, lengths and API blob identities all match the historical provenance inventory. Exact raw responses and decoded source paths are retained in `external-responses.json`, `external-integrity.json` and `external/`.

## Source closure and accepted proof chain

The registry has SHA256:

`5465be12ac33810aba9807847481c944e25a39e9c6ee2ca4c8eedbb759875266`

For every one of the 25 modules, this audit checked the actual source bytes against both SHA256 and Git-blob pins, reconstructed the literal import list, matched the registry import list, verified topological execution order and traversed the root's actual import graph. The closure is exactly the 25 registered project modules; its only nonproject import is the standard library `Std`. The audit command additionally imports `Lean` for environment inspection.

All 25 sources were inspected after a nested-comment-aware removal of Lean comments. There are no accepted source occurrences of `sorry`, `admit`, `sorryAx`, `native_decide`, custom `axiom`, or `Lean.ofReduceBool`, and no source-level unsafe declarations. This static inspection supplements the actual compiled dependency audit; it is not substituted for it.

The four new source identities are:

| Module | SHA256 |
| --- | --- |
| Agent1PeriodicOuter | b30b54bce57542a649208c29900d511e9cc4b64429fb4a48f8da2a387d040678 |
| Agent1PeriodicOuterChoices | 9bd84fb0c22b2252fb71f0310fe763e6a07192ef0fb80299763459ab48fb76ad |
| Agent1PeriodicCatalogOrder | 0f59e74ecb35b9bb648150319beb3de9f7965c6a1aea7171e67a40f4bcb199c7 |
| Agent1PeriodicOuterCatalog | 1e6ebcc4e47df94162467d52826cee4e64c5707a622ac775008671d3fb0391e2 |

The complete inventory and source audits are in `source-closure-and-audit.json`.

## Qualifying independent execution

The exact executed replay driver is retained twice, with identical bytes and SHA256:

`1a4ddabcbcf90a3e6a374dbf861435eb6509cf6199593818d0f9b3b54d8d6d8c`

Its logic creates the build directory with `exist_ok=False`, copies only hash-verified source inputs into it before compilation, archives all 25 inputs and its own exact bytes, and sets project `LEAN_PATH` to that new build directory. No preexisting project objects are imported into the qualifying run. It verifies the compiler hash before the module commands and verifies source identity again after the audit.

Compiler: official Lean 4.19.0, reported commit `6caaee842e94`, executable SHA256:

`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`

Each module command is exactly:

```
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o MODULE.olean MODULE.lean
```

The final command uses the same compiler and flags on `ReviewAudit.lean`, without an output-object option. There are **25 module commands plus one audit command**, in complete source-dependency order. All **26 exit codes are zero**; no command timed out. Each has an 8,192 MiB address-space cap and 600-second timeout, with the compiler's default stack. Every full log's SHA256 matches its command receipt. No accepted log contains a proof escape, disallowed axiom diagnostic or compiler error.

The retained total is **250.61481323399858 seconds**, including **173.66662300000098 seconds** for the final Catalog source. These are the historical independent execution timings, not new timings from this audit.

The generated audit source was reconstructed byte-for-byte from the retained replay driver's template, source module order and public theorem enumeration, and matches the exact retained `ReviewAudit.lean`. The original full audit log is retained unabridged.

## Complete actual axiom and implementation inventory

This audit parsed every actual multiline dependency row, checked uniqueness and module origin, recalculated the per-module counts, and compared them to the retained summary.

| Inventory | Actual rows | Dependency result |
| --- | ---: | --- |
| Theorem constants, including private/generated theorems | 1,643 | Exact union: Classical.choice, propext, Quot.sound |
| Safe definitions/opaques | 401 | Exact union: propext |
| Named public theorem types and source axiom prints | 117 | Each present in actual audit output and matched to its theorem dependency row |
| New public endpoints | 18 | All covered |
| Prior public endpoints | 99 | All covered |

The four new modules contribute theorem/safe-definition counts of Outer **10/1**, Choices **18/20**, Order **4/5**, and Catalog **195/128**. Public theorem counts are respectively **2, 2, 3 and 11**.

The audit does not claim an environment free of compiler-generated implementation declarations. It separately verified **6,823 nonsafe definitions**: **6,794** `_cstage` helpers and **29** `_unsafe_rec` implementations. Each recursive implementation has its corresponding safe base among the audited safe definitions. There are no unclassified nonsafe definitions and no unsafe opaques.

There are **30 unsafe implementation specialization axioms**: 13 from unchanged LychrelDigitSums, seven from prior PhaseCatalog, seven from Choices, one from Order and two from OuterCatalog. None occurs in any accepted theorem or safe-definition dependency row. Foundational `propext`, `Classical.choice` and `Quot.sound` are explicitly distinguished from these implementation records and from rejected recovery placeholders.

Complete machine-readable rows are preserved in `complete-axiom-rows.json`, `complete-public-checks.json` and `complete-implementation-rows.json`. No sampled or truncated axiom list was used for the conclusion.

## Manifests and separately attributed parent verification

All 95 entries of `review/FILES.json` match their complete files and exhaust the review directory except the manifest itself. All 56 entries of the parent's `PACKAGE-FILES.json` similarly match and exhaust its package except that manifest. The original 53-entry parent `FILES.json` is preserved unchanged and every listed entry matches. The Outer author manifest's 12 entries also match exactly.

Historical `.sha256` manifests were checked entry by entry. A historical CatalogOrder `.olean` is intentionally not published; its recorded digest is retained as a historical object hash only. Its absence does not affect recovery of the qualifying fresh source verification, which uses complete source inputs and no historical author objects.

Every artifact hash in `final-review-receipt.json` matches, as do its separately referenced artifact-review receipt and parent package manifest.

The separate parent canonical report has 26 successful commands, all full log hashes matching, and 1,643 actual theorem rows with only the permitted foundational dependency set. Its original `source_tree_clean=true` remains preserved. Its recorded commands have **no explicit trust override**, and this is not silently rewritten as `--trust=0`. Reuse is justified by the independent reviewer's explicit trust-zero run.

The registry and older preparation files contain historical provisional status fields. The package README explicitly supersedes those statuses with the executed final review and parent reports while preserving the exact registry bytes used by both runs. Their historical fields are not treated as current failed compilation results or as a missing new execution requirement.

## Generated certificate, original formulas and recovery

Two bounded Python comparisons were executed locally, with exact commands, exit codes and complete logs in `artifact-validation-runs.json`. They do not execute Lean, BFS, a reachability search or an SCC algorithm.

The first comparison verifies all nine original provenance references, the decompressed payload, original outer/phase generator functions, **36 bounded exterior/clock cases**, all **878 source rows**, all **1,458 ordered labelled edges**, initial membership and target closure. It preserves **108 all-nine labelled product edges** and checks the removal of **406 duplicated incoming-bit edges** from **1,864** pre-dedup entries. Its complete outputs are byte-for-byte identical to the retained `catalog-review/run-001` outputs.

The second expands the actual public named-list flatten definitions of the final source, checking each of **59 node blocks and 59 edge blocks**, their exact order and complete edge labels. It matches the original archive and both earlier source snapshots, checks the unchanged `outerImages` and `outerOutputs` formulas and reproduces every retained `lean-data-003` output byte-for-byte.

The historical literal-generation prefix is recoverable as the first **91,787 bytes** of four preserved snapshots. Its SHA256 is exactly:

`1930c80ad58dea8cc7c00464f9f837015c5c262dc265369d16ddbc6ae545637d`

The recovered bytes are in `recovered-generated-prefix.lean`. The retained `root-author/chunk-catalog.py` describes the historical transformation to phase blocks; its input/output hashes match the corresponding attempt-001 and attempt-003 sources. The recorded block sizes match the final expansion. The historical chunk generator is not represented as generating the final structural proof assembly; final accepted Lean source, exact source hashes, proof-bearing block assembly and literal-data comparison supply that recovery point.

The resulting theorem scope remains necessary one-step projection and complete validity preservation for represented valid inputs whose projected source lies in the catalog. It does not establish arbitrary abstract-path realizability, reachability of all listed nodes, catalog minimality, safety closure, finite full interface state, a future exponent guard, an interface return, a palindrome hit or a conclusion about 196.

## Preserved real failures

All original source snapshots and full failure outputs remain unmodified in `package/`. The accepted proof chain excludes them.

| Historical attempt | Actual outcome |
| --- | --- |
| Catalog root attempt-001 | Exit -6; stack overflow |
| Catalog root attempt-002 | Exit -15; targeted stop after recorded RSS 23,079,892 kB, before shared memory exhaustion |
| Catalog root attempt-003 | Exit 1; out of memory |
| Catalog root attempt-004 | Exit 1; unresolved congrArg₂ references and propagated recovery sorryAx |
| Catalog root attempt-005 | Exit 1; out of memory during assembly |
| Catalog root attempt-006 | Exit 0 on the final accepted source; author increment only |
| Direct rfl probe | Exit 1; memory exhaustion under its explicit 4 GiB cap |
| Block probe | Exit 1; IO/BaseIO instrumentation type mismatches; no full acceptance inferred |
| Choices attempt-001 / attempt-002 | Exit 1 / exit 0 |
| CatalogOrder attempt-001 | Exit 127; command launch failed because /usr/bin/time was unavailable; Lean did not start |
| CatalogOrder attempt-002 / attempt-003 | Exit 1 with rejected recovery diagnostics / exit 0 |

The historical recovery `sorryAx` in rejected attempts is retained and is absent from the accepted source and accepted dependency logs. No local finite reduction from a failed whole-module attempt is counted as whole-module acceptance.

During this audit, two read-only local Git lookups found no exact-head object and exited 128. The audit then used the authorized connector. A first attempt to send the entire tree-response archive as one shell argument failed before process creation with an argument-list-length error. Chunked/streamed local transfer succeeded, with all 288 resulting Git object identities verified. These retrieval/transport failures are retained in `retrieval-failures.json`; no evidence validator, Lean command or certificate comparison failed in this audit.

## Reproduction and delivery boundary

The full package and raw responses permit reconstruction without access to the former author's workspace. At the original audit location, run:

```
python validate_retained_evidence.py
python validate_supplemental_evidence.py
```

The validators use the root's combination receipt at the parent-directory path `pr146-combination-initial.json`. For recovery elsewhere, first restore that file from the exact included `root-combination-evidence.json`; no remote repository mutation is needed. The bounded artifact comparison commands are recorded verbatim in `artifact-validation-runs.json`. Their output directories must be new, because the retained comparison scripts preserve prior attempts with `exist_ok=False`.

The execution and artifact hashes are consolidated in `reuse-receipt.json` and `FILES.json`. No remote mutation, comment, review, branch operation, merge, repository cleanup, new toolchain installation or nested-agent work was performed by this specialist.
