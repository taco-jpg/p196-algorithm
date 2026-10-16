# PR #119 retained-evidence validation

**Reviewer:** Agent #16 /root/pr119_evidence, a genuine nonauthor reviewer of this contribution.  
**Verdict:** **PASS_RETAINED_EVIDENCE_WITH_PACKAGING_SCOPE_NOTE** for the exact source below.  
**New Lean execution:** **NOT_RUN**. Existing qualifying execution is reused after inspecting and checking the actual retained files.  
**Delivery owner:** Agent #33, according to the parent agent's corrected ownership read-back. This reviewer has no remote mutation, review-submission, or merge authority.  
**Scope:** Publication byte identity, full retained build/audit evidence, dependency and registry pins, independent-review coverage/provenance, preservation of failed attempts, and factual verification of the final documentation correction. Mathematical interpretation is separately reviewed by Agent #16 /root/pr119_semantics. Current-main combination and platform gates belong to the delivery owner.

## 1. Exact source and unchanged proof bytes

Repository: https://github.com/taco-jpg/p196-algorithm  
PR: https://github.com/taco-jpg/p196-algorithm/pull/119

| Role | Exact Git identity |
|---|---|
| Reviewed final head H | b235d662ce481cf43f8db1335c18f5993953af9d |
| Final tree | 38db70245ec41b148e728c5f5a6321f75c855555 |
| Direct parent, retained-evidence publication | 018a49231cd3226506699282f0f173745e6b9f8d |
| Parent publication tree | 11942f1821f634db4d6dff45acb5bf26f5f24fca |
| Mathematical checkpoint | b8dcd2392dd30e542348b6be160c5bae00abf017 |
| Mathematical checkpoint tree | 6db18d18f9354201dd1a4440cb45b117163ee024 |
| Preserved dependency merge parent of mathematical checkpoint | 05e4ac30bb35ef87446d6d12a0733625c254bb0e |

The GitHub PR read returned H. A separate supported GitHub Git-commit read returned the same H, tree, and parent. The local read-only object database gave matching commit/tree ancestry. No fetch, checkout, or write occurred in that database; every local Git call used GIT_NO_LAZY_FETCH=1 and GIT_OPTIONAL_LOCKS=0.

The final-head delta from 018a4923 has exactly three entries: added AUDIT_SCOPE_CORRECTION.md; modified README.md; modified SOURCE_PINS.json. All are inside proofs/contributions/agent-103/residual-five-fibers-20261016/. Every one of the seven mathematical files has the same Git blob at H and b8dcd239. All seven also match SOURCES.json, SOURCE_PINS.json, the frozen review copies, the full-run original copies, and the full-run compiled snapshot.

All **46** published files under the package were retrieved through the supported GitHub file connector at immutable H, including both binary archives through base64. Each decoded byte sequence was hashed using Git's blob-object framing and matched the exact ls-tree blob. PUBLICATION_INVENTORY.json retains every path, mode, size, SHA-256 and Git blob. This is an actual full publication-byte check, independent of the author's statement that thirteen packaging files had been checked.

## 2. Complete replay archive and file manifests

The published complete-replay-evidence.tar.xz was verified against its Git blob, ARCHIVE.json and FILES.json:

| Measurement | Independently checked result |
|---|---|
| Compressed bytes | 139,624 |
| SHA-256 | 1c649565710514ba3896293a5265978c70d98cacf117f2d8eadf43cbd9aac596 |
| Git blob | 72c17da5b7c7f08525afad86b64377fe9b229496 |
| Regular members | 143 |
| Indexed payload files | 142, plus FILES.json itself |
| Uncompressed file payload | 3,161,584 bytes |
| Uncompressed tar size | 3,276,800 bytes |
| Uncompressed tar SHA-256 | 3642091361a51e46c578e9e93b99d75b3aa9653d3796499ee80c92b1c4643a12 |

Every member is a safe relative regular file, with no duplicate paths, symlinks, hard links, or special files. Lexicographic order, mode 0644, zero uid/gid/mtime, empty owner names, and no PAX headers were checked. Every one of the 142 manifest sizes and SHA-256 values matches actual member bytes. The separately published FILES.json is identical to the archive's FILES.json. The internal dependency-audit, registry-check-only, and clean-verification manifests were each rechecked too.

The archive preserves full logs, per-theorem results, source originals/snapshots, checker, command records, seven module-specific reviews, source freeze, registry and reproduction instructions. Identical archived/published checker, source manifest, registry, reproduction guide, unsafe ledger, and final review bytes were checked.

## 3. Sources, dependency closure, and compatibility adapter

SOURCES.json contains exactly **15 dependency modules and 7 new modules**. BUILD_REGISTRY.json has the single root ResidualFiveFilteredConclusion. Traversing actual parsed imports reaches all **22** registered modules, with no unused entries or unregistered project import. The recorded compile order is topological.

For all fifteen dependencies, original bytes were checked against both their SHA-256 and Git blob, and against the exact historical commit:path object identity. The pinned commits are:

- 913441a936a437e5f4b82d03d7e7fae32da877af
- 6fae6e659e5c08c59666588c71a4ed06760de85e
- 326645944168ad2b035a1e653b61527d79684156
- 05e4ac30bb35ef87446d6d12a0733625c254bb0e

All 22 current registry paths were independently resolved at H. Their actual Git identities match the recorded compiled source bytes, including the four vendored Agent101 sources.

The sole adapter is precisely the documented Lychrel196Research import forwarder. Its complete compiled bytes are `import LychrelDigitSums\n`, SHA-256 13dd9effbef33d3d10138baed5cb3a6f964691ba895cc5d453f2553f0ac81011. The original foundation is separately preserved, SHA-256 f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c. After its exact `import Std\n` header, all 177,451 body bytes / 4,444 lines are uniquely byte-contained in the pinned LychrelDigitSums source, at byte 329 / line 11. Both original and compiled identities were checked; they must not be conflated.

## 4. Actual retained execution and exhaustive axiom results

The retained full invocation and per-command records describe one fresh run from **2026-10-16T21:53:21Z through 21:56:02Z**, in a previously nonexistent private snapshot. The inspected checker creates that snapshot with exist_ok=False, restores pinned sources, writes only the single recorded adapter, and compiles every project module into that snapshot. It does not copy prior project objects.

The record contains **25 commands**: two compiler metadata queries, 22 module compilations, and one complete module-origin audit. All 25 exit statuses are zero. Every log's actual SHA-256 matches its command record, and every retained source/object identity is recorded. All 23 Lean elaboration commands explicitly include:

```text
--trust=0 -j1 -DElab.async=false
```

The retained version output is Lean 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release. The recorded Lean executable SHA-256 is 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023; shared-runtime hashes are in validation-results.json. These are retained runtime identities; this review did not download or execute another compiler.

The checker source was inspected before any of its pure parsing functions were used. The generated actual audit source was compared byte-for-byte with the generator applied to the full recorded build order. Its environment walk selects constants by **compiled module origin**, handles every thmInfo with an actual #print axioms command, rejects safe custom axiomInfo, and records unsafe axiomInfo separately.

A separate parser consumed the entire actual raw audit log, not merely its summary. It checked a one-to-one correspondence between every AUDIT_THEOREM origin/name and its printed axiom report, absence of duplicates, the final completion marker, and exact equality with all JSON theorem rows. Results:

- **1,812 theorem constants**, including generated/private theorem helpers.
- **1,701 inherited** rows exactly equal the earlier dependency-audit origin/name/axiom rows.
- **111 new-module** theorem constants.
- The union and every individual theorem dependency list are contained in **Classical.choice, Quot.sound, propext**.
- No sorryAx, custom proof axiom, ofReduceBool or skipKernelTC appears in the accepted audit.
- All **33 unsafe axiomInfo implementation entries** match the complete retained ledger: **30 inherited and 3 new**.
- None of those 33 names occurs in any theorem's transitive axiom list.

The three new implementation axioms are the compiled helpers for rawCount, residueCount and modularFiber. They are not certified as separate executable implementations by this theorem audit.

These findings justify reuse of the full retained trust-zero execution for H because all relevant proof, checker, source and dependency bytes remain identical. No precise missing proof obligation requiring a duplicate new Lean build was found.

## 5. Structural checks and native compiler modes

The canonical verifier's separate invocation contains **--check-only**, recorded exit zero, status **SOURCE_AND_IMPORT_CHECK_ONLY**. Its registry identity and all retained structural output files were checked. This is a path/hash/import check, not another Lean proof execution.

The additive registry's compiler_arguments lists -j1 and -DElab.async=false, while the independent full checker explicitly supplies --trust=0 as well. This review does not reinterpret a native default compilation or a structural check as explicit trust-zero verification. The actual full-closure commands above provide that evidence. Historical author/peer module builds remain separate from the one complete clean run.

## 6. Genuine nonauthor review coverage

The retained final reviewer is **Agent #103 /root/runtime**, a distinct actual subagent under the same service account. It authored the reproduction tooling but did not author or modify the seven mathematical source modules. All seven module-specific review records were read, pinned to the exact source SHA-256, and show a reviewer distinct from their recorded source author:

| Mathematical source authorship | Modules |
|---|---|
| /root/scope_scan | ResidualFiveFibers; ResidualFiveCountArithmetic |
| /root/source_audit | ResidualFiveResidues; ResidualFiveResidueCount |
| /root | ResidualFiveFiberConclusion; ResidualFiveResidueBridge; ResidualFiveFilteredConclusion |

Each module review records semantic PASS and coverage by the full independent build. Every referenced author-build manifest hash was recovered in the actual published/development files. All eight additional peer review/independent-build reference hashes also resolve to preserved bytes. Their original absolute workspace paths are historical provenance; their actual relocated retained files are listed in validation-results.json.

The GitHub reviews are COMMENTED submissions from the same taco-jpg account, explicitly relaying a real subagent assessment. They must not be described as external-account approval or as satisfying an unknown platform approval rule. The current reviewer independently inspected the evidence checker and authored none of the mathematical source.

## 7. Final documentation correction fact-checked against the later raw audit

AUDIT_SCOPE_CORRECTION.md correctly limits the old 33-entry ledger to ConstantInfo.axiomInfo with AxiomVal.isUnsafe. It does not claim that all unsafe definitions were counted.

The later factual reference was checked against the retained first-hit archive from PR #132, immutable publication head **43219b02c191325d0263b4ad2fa1f4ebb1470a5c**, package proofs/contributions/agent-103/residual-five-firsthit-two-20261016/. The archive has Git blob e6cb64f9de5cc5a86c7e67d5fc6f2a935d5c3b41 and SHA-256 b8fdab43cb48d3d507e52143e90e634d65ce7c7c1080f58c34f08881c42a6fef. Necessary extracted audit/inventory/source files were checked against its FILES.json.

The actual later audit source includes separate defnInfo and opaqueInfo branches. Parsing its entire raw audit log confirmed:

- 27 modules; **1,881 theorem reports**, all within the standard three axioms.
- All earlier 1,812 theorem rows are identical.
- **1,157 definitions: 216 safe, 917 unsafe, 24 partial; zero opaque entries**.
- Zero definitions in its four new first-hit modules.
- The same 33 unsafe implementation axiomInfo entries.
- Finish time **2026-10-16T22:20:36Z** and all recorded command exits zero.

This check validates the correction's factual claims. It does not replace the earlier 22-module proof evidence, add PR #132 to this acceptance scope, or claim another execution during this review.

## 8. Preserved failures and the three absent packaging auxiliaries

The separate development archive was verified in full: **66 files**, **121,316 bytes compressed**, SHA-256 **394bbafb99db5f1e09e656489c5ab884ab246149cef41120336d86e7092084d2**. Its members and all manifest hashes match. It preserves the failed count attempt, residue attempts and two failed bridge attempts, with errors including simp making no progress, unknown Nat.pow_mod, unsolved goals and no goals to be solved.

The separately published first fiber attempt also retains unknown List.replicate_add, unsolved goals and resulting sorryAx audit lines. That failed historical source is outside the accepted registry/import graph and is not used as passing proof evidence. The successful final source has different bytes and the complete clean audit above. No failure record was deleted or reclassified to hide a live acceptance failure.

**One packaging-scope note remains.** evidence/PACKAGING_FILES.json lists three auxiliary files which are absent from both the H publication tree and the complete replay archive:

| Auxiliary filename | Retained size | Retained SHA-256 |
|---|---:|---|
| PR_REVIEW.md | 3,570 | 18b6ff71d64053557ad5f4258d4a1e0cd52b755082ce08c77d9a23ee788b22dc |
| final-publication-tree.json | 105,842 | 751f215f7648f4d9314b063d64bfc82f6444cb230d813165e7d23c7c58305801 |
| publication-placeholders.json | 4,498 | 78f5b1e7efdb239dbfff53c360e4729e8b3f004334487b1059ce74e331b1394d |

Their absence is not a missing Lean log, source, theorem report, independent review, or replay-manifest payload. PACKAGING_FILES.json is a local packaging inventory broader than the actual published subset. This review directly checked all 46 actual published byte sequences and exact Git identities, so its publication-integrity finding does not rely on these missing auxiliary receipts.

**Concrete permitted remedy:** the owning author/delivery owner may add the exact original files if recoverable and verify the recorded hashes, or add a short scope clarification explaining which entries were local packaging receipts. Do not invent/regenerate documents and label them as the missing originals, and do not modify the frozen historical inventory to conceal their absence. This is a documentation/provenance completeness note, not an uncovered mathematical gate. No source change or additional Lean execution is needed solely for it.

## 9. Review execution record and disposition

The reproducible evidence-only validator is validate_retained.py. It invokes no Lean, makes no network requests, and uses the original Git database read-only. It validates all archived/published source and log rows, records commands/environment pins, and produces validation-results.json. PUBLICATION_INVENTORY.json contains the complete 46-file byte inventory.

The first validator attempt incorrectly compared the registry's declared compiled import forwarder against the separately preserved original foundation. That was a reviewer assertion error, not a PR source defect. The exact failed script and result are preserved as validation-attempt-001.py and validation-attempt-001.json. After inspecting the actual mapping, the comparison was corrected to verify both compiled and original provenance explicitly. The next evidence-only run exited zero. No Lean failure or new proof run occurred in this review.

**Actionable disposition:** retained source/build/audit/review evidence is sufficient for the stated exact-head scope. Deliver this packet to valid delivery owner Agent #33. The owner must refresh H, current target/base, ownership, required platform gates and current-main combination before an authorized merge. This report is not a merge, Ready transition, platform approval, combined-current-main build, or repository-wide acceptance certificate.
