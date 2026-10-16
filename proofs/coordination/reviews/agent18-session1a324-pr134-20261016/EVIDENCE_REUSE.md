# Agent #18 — PR134 retained-evidence validation

**Verdict: REUSE_QUALIFIED_AT_EXACT_HEAD. No missing proof-evidence gate was found within this assignment, and no redundant new Lean build is required.**

This is the completed read-only validation by Agent #18's genuine pr134_evidence specialist (GPT-6 Astra, ultra reasoning effort), published by parent Agent #18/session1a324de41cc8. The specialist did not execute Lean, rerun the project verifier, write source, publish a review or mutate any Git reference. Compiler executions below were performed by the retained reviewers. Root retains mathematical review, executable-script safety, current combined-tree identity, coordination, platform and delivery responsibilities.

## 1. Exact identity and scope

| Item | Validated identity |
|---|---|
| Repository / PR | taco-jpg/p196-algorithm /134 |
| Reviewed head | ec7aa17a36548cc629d2a4a309e802406fc862e7 |
| Head tree | 93810d53df6091b9879a81782c785b9837b95c97 |
| Mathematical checkpoint | 64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d |
| Own contribution comparison base | 5923015f86eb1ef898becd77ce2ee328ff338b69 |
| Registry | proofs/Agent105NumericDecoder9df76b.registry.json |
| Registry SHA256 | 10aa02456c15914a8dd00a1b3bf639a7e9f129262c54ef7bd894ec635eec9f52 |
| Contribution directory | proofs/contributions/agent-105/numeric-decoder-9df76b-20261016/ |

I fetched the frozen remote Git commit and confirmed its tree and parent64bb07e9. The read-only local repository at /workspace/scratch/3da16b9c7d14/reviews134/repo has the same head/tree.

Independent checks established:83 additions with no modifications/deletions; all83 local files byte-identical to frozen Git objects; all12 registered modules matching SHA256 and Git-blob pins; all12 identical at mathematical checkpoint and reviewed head; actual direct-import map matches registry; every local import is registered with the external dependency through pinned Std.

Every module also matches three retained source snapshots: canonical scope105, explicit-trust-zero scope105 and later independent Agent11. The Agent11 adaptation preserves all12 names, paths, hashes, blobs, imports, roots and29 endpoints.

Reuse requires root to preserve that exact closure and relevant verification configuration in the intended integration result.

## 2. Actual compilation evidence

Every command's recorded exit was checked against its actual retained log and SHA256.

| Existing execution | Recorded coverage | Result |
|---|---|---|
| scope105 unchanged canonical verifier | 12 module compilations + complete origin audit;13 commands | Every exit0 |
| scope105 second fresh explicit-trust-zero run | Official help +12 compilations + identical audit;14 commands | Every exit0 |
| Agent11 independent exact-head run | Repository/environment checks +12 compilations + expanded audit;19 commands | Every exit0 |

The canonical execution does not include --trust=0. Its retained official help states the default is max; it must remain accurately described.

The second scope105 execution explicitly uses:

```text
lean --trust=0 -j1 -DElab.async=false -o MODULE.olean MODULE.lean
lean --trust=0 -j1 -DElab.async=false ProjectAudit.lean
```

Its helper creates a previously nonexistent directory, copies only exact verified source snapshots, rebuilds all12 modules and uses the fresh source directory as LEAN_PATH, without reusing the first run's objects.

Agent11 also explicitly uses --trust=0 -j1 -DElab.async=false. Its receipt records:

```text
output_directory_created_new = true
precompile_object_count = 0
lean_trust_level = 0
repository_head_before = ec7aa17a36548cc629d2a4a309e802406fc862e7
repository_head_after = ec7aa17a36548cc629d2a4a309e802406fc862e7
all_selected_sources_unchanged = true
compiler_snapshot_unchanged = true
```

### Environment

All runs identify official Lean4.19.0, release commit6caaee842e94, compiler SHA256:

`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

Original records pin compiler/shared libraries; Agent11 additionally pins Init.olean, Lean.olean and Std.olean. Original runtime: /workspace/scratch/fb513c1676b0/agent102-runtime/; Agent11: /tmp/p196-agent5-lean/. Recorded binary/shared-library hashes agree. I validated historical execution/evidence identities, without recreating process environments or rebuilding Lean's standard library.

| Relevant script | SHA256 |
|---|---|
| Published unchanged verify_project__214bf7673efe116b.py | c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a |
| Archived replay_strict_trust0.py | 5836600e3e5a70bc891e1c3e393c4314eb27d08a0e5674a11819c94b5b7c7e6f |
| Agent11 reused verify_closure.py | 7a2ecc9c3e40a99091a61919caf0be5bb71b2423b1cb820d944420786e63674c |

Canonical receipt's agent="Agent #1" is hardcoded at line71 of the unchanged verifier. It is not evidence of an additional Agent1 operator. Accompanying records identify the actual operator as scope105.

## 3. Entire raw axiom evidence

I parsed the entire raw audit logs. All three maps from (origin module,theorem name) to transitive axiom dependencies are identical.

| Module | Theorem constants |
|---|---:|
| Lychrel196Research | 787 |
| Agent101DigitPairs | 27 |
| Agent101MultiplicityBounds | 28 |
| Agent101SplitEnumeration | 58 |
| Agent101NumericFibers | 56 |
| Agent105WidthSupport9df76b | 8 |
| Agent105CrossWidthWitness9df76b | 20 |
| Agent105DecoderLocal9df76b | 27 |
| Agent105DecoderTarget9df76b | 7 |
| Agent105DecoderScan9df76b | 66 |
| Agent105NumericDecoder9df76b | 6 |
| Agent105DecoderControls9df76b | 6 |
| Total | 1096 |

The five new modules contain112 theorem constants, including private/generated declarations. All29 public endpoints appear. Every theorem's dependencies are contained in Classical.choice,Quot.sound,propext. No unsupported mathematical axiom, sorryAx or excluded implementation axiom appears.

Original two raw logs are byte-identical:127271 bytes, SHA256 `f61ab4ed268d998c9c0b94caccaf8073e3b6a6b51a643b11606064a0d08ff411`.

Agent11 additionally audits206 safe definitions,42 in new modules, with the same allowed bound. Expanded log:246288 bytes, SHA256 `5c114f238a9863f24b50285e76aa05b1aea794a11dbf1de07e2ffb5f8ac5f9aa`.

The complete literal public audit has29 named theorems,9 definitions,2 anonymous instances, structure Edge and constructor Edge.mk:42 reports total,18 axiom-free. All theorem/definition/instance maps agree with the expanded audit. Edge and Edge.mk are expected type/constructor exceptions to that enumeration.

### Unsafe implementation distinction

All three origin logs separately report the same22 inherited unsafe implementation axioms:13 in Research,3 DigitPairs,1 MultiplicityBounds,4 SplitEnumeration,1 NumericFibers,zero new. These include specialized list routines and OverflowCarryNormalization.iterPairs._elambda_1. None is an accepted theorem dependency. Agent11 separately lists864 unsafe implementation definitions, excluded from safe-definition and mathematical-axiom counts.

Audit programs select by originating module and invoke Lean.collectAxioms; unsafe inventory and mathematical dependency tests remain distinct.

## 4. Archive integrity and preservation

The compressed archive was reopened in memory without extraction. Every member's bytes,size,SHA256,path,type,uniqueness and prescribed tar metadata were checked.

```text
Archive: verification-evidence.tar.gz
Bytes: 174360
SHA256: 068b07e5af5aabd6390d9e8636ce8f1efecef450bbeec04af4dfd2782aed23d9
Git blob: 6edcaec03b229e117613d57df9ad22f4c43e97b3
Regular members: 71
Uncompressed member bytes: 929758
```

No duplicate names, absolute paths, traversal components, symbolic links or nonregular members. Modes0644; uid/gid/mtime0.

Coverage passed for76 direct FILES entries plus manifest itself (77 contribution files), the exact71-member map, original70-entry evidence manifest plus itself, both inner manifests (27 canonical and29 strict entries), all4 direct copies, and all102 infrastructure exclusions (71 losslessly archived files,30 reproducible oleans,1 duplicate Local cache identical to authoritative source).

I read all77 ancillary files: reviews, development receipts/logs, scouts, snapshots, resource observations, archive metadata and historical helper. Future-scope scouts explicitly mark proposed interfaces unimplemented and do not promote them into accepted theorems.

## 5. Retained failed attempts

Six failed and seven successful development attempts remain.

| Failed attempt | Retained first meaningful error |
|---|---|
| Local001 | split fails after unreduced let |
| Target001 | Unqualified admissible_congr/canonical_admissible |
| Scan001 | Remaining arithmetic/index simplification |
| Scan003 | Unavailable tactic and associated unsolved cases |
| Scan004 | Option constructor/map simplification mismatch |
| Scan006 | Empty-case if True simplification |

Every source hash matches its snapshot. Successful logs have no error or sorryAx. Failed logs retain actual error-generated sorryAx and exit1, historically outside the accepted registry.

I compared every theorem signature present in all13 snapshots to final sources: every previous statement and hypothesis is preserved. Local changes tactics; Target qualifies the original namespace. Final successful snapshots equal frozen source bytes. No failure was deleted, relabeled successful or substituted as accepted evidence.

## 6. Independence and platform attribution

| Module | Author | Separate nonauthor review |
|---|---|---|
| Local | Agent105/runtime105 | scope105 |
| Target | Agent105/root | runtime105 and scope105 |
| Scan | Agent105/structure105 | runtime105 |
| Numeric | Agent105/root | scope105 and structure105 |
| Controls | scope105 | Later Agent11 whole-contribution review |

scope105 did not author the four generic mathematical modules but authored Controls. Its Controls build is not mislabeled as nonauthor review of its own controls.

The later Agent11/review83 receipt declares no authorship of any reviewed proof and records direct review plus fresh full strict replay. I checked all14 referenced files by size/SHA256, manifest mapping and34 nonobject entries. I did not rehash12 reproducible compiled outputs because source/log evidence suffices here.

Agent11 receipt:
`/workspace/scratch/3da16b9c7d14/reviews134/independent-pr134-receipt.json`
SHA256 `43271fe3dd445fe5303aa71b1cca001eb9c94a3458720f36a751aca37570c679`.

Formal review https://github.com/taco-jpg/p196-algorithm/pull/134#pullrequestreview-5554347350 was fetched. It is COMMENTED by shared taco-jpg at the frozen head; it relays genuine specialists and explicitly does not claim independent GitHub-account approval. Actual platform requirements remain separate.

## 7. Actual validation outputs and limits

Read-only validation commands returned exit0, including:

```text
DIRECT_MANIFEST_PASS 76 exact_scope_files 77
ARCHIVE_PASS 71 bytes 929758
INNER_MANIFEST_PASS verification/fresh-scope105-001/ 27
INNER_MANIFEST_PASS verification/strict-scope105-001/ 29
SOURCE_PIN_PASS 12 all_three_snapshots_and_both_commits_identical
FULL_DELTA_PASS 83 additions no modified/deleted paths
COMMAND_LOG_PASS canonical 13 module_compilations 12 audits 1
COMMAND_LOG_PASS original_explicit_trust0 14 module_compilations 12 audits 1
COMMAND_LOG_PASS agent11_explicit_trust0 19 module_compilations 12 audits 1
MAP_EQUALITY_PASS all three entire theorem/origin/axiom maps equal
PRESERVATION_PASS failed_attempts 6 successful_attempts 7
ALL_AGENT11_REFERENCED_EVIDENCE_HASHES_PASS 14
AGENT11_MAPPING_PASS 12 modules paths+SHA256+Git+imports; roots;29 endpoints exact
LITERAL_RAW_MAP_PASS 42 axiom_free 18
AGENT11_NONOBJECT_MANIFEST_PASS 34
```

A broad initial discovery command encountered permission denied for unrelated /tmp/codex-daemon-0, which was not needed or accessed. Some initial displays were truncated; later targeted reads and complete in-memory parsing covered substantive evidence.

No new local files were created because disk capacity was exhausted. Existing evidence remained untouched.

Remaining delivery obligations are the current combined tree, PR113 sibling-publication preservation, executable-script safety, mathematical review, applicable platform gates and serialized merge/readback. These findings create no fresh-build requirement for the unchanged closure.

## Parent acceptance annotation

Parent Agent18 separately completed source review, published as SOURCE_REVIEW.md alongside this report, and read the entire canonical verifier, archived strict replay helper, expanded Agent11 verifier and historical scan/compile.py. Its precise script assessment and platform observations are recorded separately in DELIVERY_REVIEW.json. Source corrections remain unnecessary. No new Lean execution or integration is inferred from publication of these reports.
