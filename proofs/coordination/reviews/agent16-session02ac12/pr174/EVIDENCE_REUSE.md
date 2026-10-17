# PR174 retained-evidence qualification

**Result: PASS_REUSABLE.** All 44 final qualification checks passed. The existing exact-source independent review and strict clean verification are reusable for PR174 at the pinned head below. No new Lean execution, duplicate independent mathematical review, source edit, GitHub write, ownership claim, Ready transition, or merge was performed by this qualifier.

This report supplies the retained-evidence and complete changed-file obligations to Agent #16's delivery owner. It does not decide current-main integration, prerequisite delivery, target ownership, or platform merge requirements. Those are separately handled by the delivery owner. The independent reviewer is the existing Agent #1 specialist `control_review`; this qualifier does not reattribute that execution to Agent #16.

## 1. Exact identity and actual formal review

| Item | Pinned identity |
| --- | --- |
| Repository | `taco-jpg/p196-algorithm` |
| PR | [174](https://github.com/taco-jpg/p196-algorithm/pull/174) |
| Final head H | `790ee166caf3c60c7176d53209e3e755e7ed9a9d` |
| Independently checked source S | `bfa0247b78845558d087eec08e113e91decaaddb` |
| Stacked base B / PR172 | `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80` |
| Mathematical source | `proofs/Agent1PeriodicNinesExtraStrip.lean` |
| Mathematical source Git blob | `21dc3897b77499d95aee131ab02d7056ee676ae2` |
| Mathematical source SHA256 | `e50a7e04b272f8b0d78d380b1ec1e2df80fc4b1647719dd31bdac02109a8107e` |
| Scoped registry Git blob | `63e14fb184f63307f6810e1fecb408ceb51d19ac` |
| Scoped registry SHA256 | `faa3a7717ce7c1385d856c689afbb3d95bd35cacaf04c428dbf5aa41f8f693f3` |
| Actual formal review | [5555595181](https://github.com/taco-jpg/p196-algorithm/pull/174#pullrequestreview-5555595181) |
| Formal review state and binding | `COMMENTED`, `commit_id = H`, submitted `2026-10-17T02:36:44Z` |
| Formal review account | `sodium-qed` |

The actual REST review resource was read, rather than inferring its head from a summary or a review badge. The complete response content is preserved in `actual-review-5555595181.json`. It explicitly attributes the mathematical review to specialist `control_review`, says that specialist authored the scoped registry and review metadata, and states that the specialist authored none of the mathematical source. Its retained semantic report and frozen receipt agree. Specialist independence here is independence from mathematical authorship; the shared GitHub account is not represented as a separate platform identity. `COMMENTED` is not a GitHub approval.

The immutable [semantic review at H](https://github.com/taco-jpg/p196-algorithm/blob/790ee166caf3c60c7176d53209e3e755e7ed9a9d/proofs/contributions/agent-1/periodic-nine-control-20261017/review/semantic-review.md) records the source, scope, actual clean run, and independent authorship boundary. The receipt's historical `formal_PR_review_status = PENDING_FINAL_PUBLISHED_EVIDENCE_HEAD` is left intact. The later actual REST review establishes the delivered state.

## 2. Complete full-diff accounting

The native Git comparison B..H and the supported GitHub connector's complete changed-file list agree on **157 additions**, with no modifications or deletions. Every changed file was recovered in full and its Git blob recomputed from the exact bytes. The complete per-path record in `checks.json` contains Git blob, SHA256, byte length, category, local immutable source, and check result. `full-diff-name-status.txt` and `remote-changed-files.json` retain the independent enumerations.

| Changed scope | Files | Disposition |
| --- | ---: | --- |
| New mathematical source | 1 | Exact compiled and reviewed source |
| Scoped source registry | 1 | Exact frozen registry; no global registry mutation |
| Contribution README | 1 | Final additive account of the finite result and historical runs |
| `author/` | 11 | Original incremental attempt, two logs, commands, 14 dependency pins, driver and manifest |
| `parent-verification/` | 46 | Original parent clean run and faithful packaging/provenance |
| `registry-preflight/` | 27 | Source-only closure/pin validation, historical claim readback, source snapshots and manifest |
| `review/` | 69 | Existing independent semantic review, strict execution, audit, snapshots, provenance and complete seal |
| `scope/source-census.md` | 1 | Historical source-only bounded census, preserved without upgrading its status |
| **Total** | **157** | **All checked** |

Exactly 155 additions are below `proofs/contributions/agent-1/periodic-nine-control-20261017/`; the only other additions are the named source and registry. No changed workflow, default-build configuration, compiled object, shared library, or unrelated source is hidden in the diff. All nine retained Python files were fully parsed as source and the distinct driver implementations were inspected; none was executed in this qualification. The author, preflight and replay each retain exact executed-script copies. Generated Lean audit implementations were read in full, and their complete raw output was parsed.

The 116 paths changed between reviewed source S and final head H are all contribution evidence under that same directory. All 15 mathematical sources and the scoped registry are byte-identical at S and H. This is the concrete basis for carrying the existing source review to H.

The historical census and its duplicated review snapshot match exactly. The census deliberately calls the then-unverified proposed witness `UNVERIFIED`, records its bounded search and failed index postprocessing, and excludes generalized searches, cycles and current ownership claims. That early label is historical evidence; the later verified report is additive. The census's earlier broad search is not rerun or promoted to a present exhaustive claim.

## 3. Complete manifests and preservation

The following checks verify every listed SHA256 and byte count and verify that the manifest covers the entire corresponding directory except the explicitly excluded manifest/seal files. The excluded files themselves are still bound to exact head Git blobs and included in the overall changed-file map.

| Manifest | Entries | Exact coverage exclusions |
| --- | ---: | --- |
| `author/FILES.json` | 10 | `FILES.json` |
| `parent-verification/parent-clean-001/FILES.json` | 33 | `FILES.json` |
| `parent-verification/PACKAGE-FILES.json` | 44 | `PACKAGE-FILES.json`, `frozen-receipt.json` |
| `registry-preflight/FILES.json` | 26 | `FILES.json` |
| `review/FILES.json` | 67 | `FILES.json`, `frozen-receipt.json` |

Important immutable seals and raw audit objects:

| Object | SHA256 |
| --- | --- |
| Independent frozen receipt | `1c27268ba908bdf8224ad1234dd0ddd231c53c1a7eb7314854aadddd3155e779` |
| Independent complete manifest | `99b85e925da4941e9fae9390ef8f1d25501f3b2763b793f55afadc97dc0b19ee` |
| `ReviewAudit.lean` | `b1e01379318176549bdb7556a057d1e58a4462ca90b3c9e75da141e6655a212b` |
| Complete 265,723-byte `ReviewAudit.log` | `a14e77024e7a125649b3824464f1c37c2730231fcd561c8c0670005ab988acf0` |
| Actual independent `replay.py` | `a46937fe34e3e32fadd0c780dfdd88fbee147654f5ce4f5e475a321fa2813746` |
| Parent frozen receipt | `71926f130b13edb6bb9bbbfec674bb132129d52ee1a053c75d659deb52edff9c` |
| Original parent verification report | `cd029ab11060f30317c11bd82980bd68518ff33a840ae13b1120180ba543ea05` |

The parent seal binds its original manifest/report and the exact source and result receipts. The independent seal binds the source, registry, complete manifest, semantic report, actual verification record and elapsed-command sum. Helper provenance hashes for the adapted review drivers match the actual implementations. References to local-only predecessor helpers and earlier census products remain attributed historical references, not new claims that this qualifier recovered or executed those prior local sessions. Those predecessors are not source dependencies of the accepted theorem.

## 4. Source closure and byte-identical reuse

The actual import graph was derived from comment/string-masked source and checked against the registry and final identity manifest. The exact topological compilation order is:

1. `PeriodObstructions`
2. `ActualWordBridge`
3. `PrefixSemantics`
4. `LychrelDigitSums`
5. `IncomingCarry`
6. `Agent1RepeatedBlock`
7. `Agent1RepeatedBlockContext`
8. `Agent1PeriodicDigits`
9. `Agent1PeriodicSlices`
10. `Agent1PeriodicGuard`
11. `Agent1PeriodicGuardFacts`
12. `Agent1PeriodicOuterStrip`
13. `Agent1PeriodicCenterStrip`
14. `Agent1PeriodicQuotient`
15. `Agent1PeriodicNinesExtraStrip`

The only external source import in this project graph is the pinned toolchain's `Std`. The generated audit additionally imports `Lean` for environment and axiom inspection. The new source directly imports only `Agent1PeriodicQuotient`. Neither `Agent1PeriodicNinesCenter` nor `Agent1PeriodicNinesCycle` belongs to this source closure; in particular, PR173 is not a mathematical dependency.

All 15 source snapshots from independent compilation, the parent clean run and the preflight are byte-identical to their registry entries and Git blobs at both S and H. The 14 inherited sources additionally equal B and the exact source pins already qualified for PR168. Immutable cache entries were reused by their complete Git blob and SHA256 identities; no second semantic review or new compilation of those identical sources is claimed. This is byte-level evidence reuse, not an inference from matching filenames.

An auxiliary lexical scan found none of `sorry`, `admit`, `sorryAx`, `native_decide`, unsupported source `axiom`, `implemented_by`, `extern`, `unsafe`, `ofReduceBool`, `trustCompiler`, or `skipKernelTC` in the selected project source code. The transitive origin audit below supplies the substantive axiom evidence; this lexical scan is supplementary.

## 5. The three distinct verification histories

| Evidence | Actual execution | Correct classification |
| --- | --- | --- |
| Author `attempt-001` | New module compile and `ControlAudit`, both explicit `--trust=0 -j1 -DElab.async=false`, both exit zero | Incremental author check; **14 previously pinned project objects reused**, `fresh_closure = false` |
| Parent `parent-clean-001` | All 15 sources plus `ProjectAudit`, all 16 commands exit zero, `-j1 -DElab.async=false` | Fresh parent closure; **actual argv has no explicit `--trust=0`**; theorem audit only |
| Independent `review/clean-001` | All 15 sources plus `ReviewAudit`, all 16 commands exit zero, explicit `--trust=0 -j1 -DElab.async=false` | Qualifying fresh strict independent verification, including safe definitions and full runtime separation |

The independent replay uses an empty build directory created with `exist_ok=False`, copies only pinned source into it, sets the project `LEAN_PATH` to that directory and compiles every module in dependency order. It reuses no project objects. The actual invocation and each actual child argv are retained. Every raw log was rehashed against its command result; all 16 statuses are zero, with no timeout. Their recorded elapsed sum is `67.85137776000192` seconds.

The compiler record identifies official Lean **4.19.0**, release commit **6caaee842e94**, binary SHA256 **92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023**. Every independent command records an **8,192 MiB address-space limit**, **600-second timeout**, and default Lean stack setting. The compiler identity agrees with the already qualified toolchain record. This qualification does not claim to have launched the compiler.

The parent report retains its original `source_tree_clean: true`; the checker defines this as tracked-file cleanliness with untracked files excluded. Its 16 raw commands and log hashes are intact. It audits 1,348 theorem constants and separately lists 13 generated unsafe implementation axioms, but supplies no safe-definition audit and no explicit trust-zero flag. No compiler default is inferred. The packaging specialist `center_parent_receipt` ran no Lean; packaging is not reclassified as independent proof review.

The author record contains full source/object hash pins for the 14 reused dependencies. Object hashes are preserved provenance, not newly verified binaries. The strict independent fresh closure supplies the required noncached dependency verification. Registry preflight explicitly executes no Lean and preserves the historically pending fresh-review wording. No frozen historical registry or receipt was rewritten.

## 6. Full raw origin and axiom audit

`ReviewAudit.lean` enumerates `env.constants`, selects origins through `env.getModuleIdxFor?`, and selects exactly the 15 registered modules. For every theorem and every safe definition or safe opaque, it calls `Lean.collectAxioms`; it rejects dependencies outside the stated allowed set. A non-unsafe custom axiom triggers an error. Every selected module must have an audited theorem origin. Unsafe generated implementation entries are printed separately.

The complete raw log was parsed without truncation. `audit-extracted.json` preserves every extracted theorem, safe definition, public export and runtime entry, rather than only summary counts.

| Raw output class | Verified result |
| --- | --- |
| Theorem constants | **1,348**, unique names, every selected module represented |
| Theorem axiom union | Exactly `Classical.choice`, `Quot.sound`, `propext` |
| Safe definitions / safe opaques | **227** unique audited entries |
| Safe-definition axiom union | Exactly `propext` |
| Public Agent1 theorems | **68** unique exports; all have raw checked-type output and printed module axiom output |
| New module theorem constants | **5** |
| New module public theorems | **1** |
| New module safe definitions | **0** |
| New module runtime entries | **0** |
| New endpoint literal axiom output | `[propext, Quot.sound]` in both module compile log and full audit log |

The generated audit contains 69 `#check` commands because the one new public endpoint is checked again explicitly after the complete list of 68 exports. This does not inflate the unique public-theorem count. The parent theorem-origin output independently has the exact same set of 1,348 theorem/axiom rows; its narrower audit is not credited with safe-definition coverage.

The inherited runtime inventory is kept separate from mathematical axiom dependencies:

- **944** non-safe generated runtime definitions: **916** compilation-stage helpers and **28** `._unsafe_rec` helpers.
- Every unsafe-recursion helper has its corresponding safe base among the 227 audited safe entries.
- **13** unsafe compiler implementation axioms, all inherited from `LychrelDigitSums`.
- **0** unsafe opaques and **0** unclassified runtime helpers.
- No such runtime entry originates in the new control module.

The full theorem and safe-definition dependency unions exclude those implementation axioms. The raw inventory matches the retained inventory and verification JSON exactly. No `CUSTOM_AXIOM`, disallowed dependency, missing selected module, `sorryAx`, `Lean.ofReduceBool`, or error finding appears in the full audit output. The presence of separately inventoried inherited compiler implementation declarations is not represented as an unsupported mathematical axiom in the accepted dependency chain.

## 7. Qualified mathematical scope

The only new public theorem is `Agent1.Periodic.nines_extra_strip_control`. Its literal tuple is `B = [1]`, `H = [9,9,9,14,18,18,14,9,9,9]`, and `w = [9,9,9,9]`. The eight conjunctions establish original `ValidPeriodic`; initial literal `stripPeriodCenter w H = (H, 0)`; actual entry-carry sum one; unchanged next raw period; exactly two mirrored period pairs stripped from the next raw center; quotient center `[18,18]`; quotient outer `[3]`; and one further actual raw period equal to `w` at that computed quotient.

The existing independent review reads these as the original coefficient-word and carry operations. The coefficients 14 and 18 are within the original bound 18; they are not silently treated as ordinary base-ten digits. A count of two removes two four-entry blocks from each side, leaving the stated nonempty residual. The last equation does not return the complete original tuple.

The qualified claim is the finite counterexample to the stated blanket local one-pair center-removal bound on the specified original-valid, initially center-normalized domain. It does not supply a cycle, successor safety, all-time continuation, temporal descent, reachability from 196, or a solution to the 196 problem. The supporting semantic specialist's retained report is source-only; its execution is not invented. This qualification reuses that existing semantic verdict together with the exact-source proof evidence.

## 8. Acquisition, diagnostics, reproducibility and limits

The initial local Git cache lacked 59 unique blobs needed for 75 file occurrences. Their `git cat-file` diagnostics are preserved in `collection-initial-local-diagnostics.json`. Each missing blob was fetched successfully through the supported read-only GitHub `fetch_blob` connector and its exact Git blob identity verified. `fetch-responses.json` retains all 59 actual response payloads; `fetched-hashes.json` records their SHA256 and sizes. This was local cache absence, not remote evidence loss. The remaining immutable files came from already verified local Git/PR168 caches. The final `collection.json` maps all 157 changed paths plus `AGENTS.md` to exact byte sources.

The inspectable `check_reuse.py` performs only local file parsing, hashing and read-only Git tree/diff reads. It executes no retained driver, Lean source, or mathematical experiment. Running it as `python agent16-pr174-evidence/reuse/check_reuse.py` from the shared workspace regenerates `checks.json` and `audit-extracted.json` from the retained immutable inputs.

The first local qualification attempt passed the first 43 checks and failed a hard-coded expected Python-file count of eight; the actual fully parsed list contained nine, including the three executed-script snapshots. This was a qualifier bookkeeping error, not a contribution failure. The original script, log and JSON result remain in `check_reuse-attempt001.py`, `check_reuse-attempt001.log` and `checks-attempt001.json`. The corrected final check compares the complete exact path set to the pinned full diff and expects the observed nine entries. `check_reuse-attempt002.log` records the final exit-zero **44/44 PASS_REUSABLE** outcome. No prior diagnostic or failure evidence was erased.

`SHA256SUMS.json` seals the final newly authored/readback/derived artifacts. `checks.json` and `collection.json` supply the complete hash maps for immutable retained source and evidence. Immutable recovered blobs and byte-identical PR168 cache material may be referenced by these exact identities rather than copied again into the publication bundle. All substantive new outputs, actual readbacks, diagnostic results, final script and original failed-attempt script/log/result must be preserved losslessly by the delivery owner.

There is no remaining retained-evidence obligation requiring another build or independent review for unchanged H/S. Reuse remains limited to these exact source and environment pins. Platform-required checks are not replaced by this report. Current-main combined-tree validity, actual prerequisite disposition, accepted-build policy, live ownership and final guarded integration remain separate delivery-owner decisions.
