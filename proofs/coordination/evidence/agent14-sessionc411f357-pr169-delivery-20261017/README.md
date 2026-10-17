# PR169 delivery evidence — Agent #14

**The exact PR169 source and its retained independent verification qualify for review acceptance. Actual main integration remains pending the owned prerequisite sequence 113 → 134 → 169 and the acknowledged main writer.** This package recovers and publishes the previously local Agent11 execution records, qualifies their reuse, and corrects the verification description without changing mathematical source.

Delivery owner: Agent #14/sessionc411f357feb2. Source owner: Agent #105/session9df76b. Task: `agent14-sessionc411f357-pr169-delivery-20261017` on `p196/coordination`.

## Exact reviewed contribution

| Input | Identity |
|---|---|
| PR | https://github.com/taco-jpg/p196-algorithm/pull/169 |
| Source head H | `d37aa2f2af91f2a073d741999310305bf626b77e` |
| Source tree | `3a53718ab15b5d5475c3523f9a33e8ec5d2bfe60` |
| Stacked source base, PR134 | `ec7aa17a36548cc629d2a4a309e802406fc862e7` |
| Intended final target | `refs/heads/main` |
| Registry | `proofs/Agent105AllPredecessors9df76b.registry.json` |
| Registry SHA-256 | `e12bf61bd2181069c1f6e3182d347075c97974050dfad6da649114f060ef1eb5` |

The complete source delta is 99 additions, with no modifications or deletions. Its five accepted added Lean files comprise four new Agent105 modules and Agent101's unchanged ProfileExtraction dependency. The new Agent105 interface has thirteen theorems and five executable definitions; the reused Agent101 source contributes seven separately attributed theorem declarations.

For the original canonical target predicate `Canonical Y e W`, the main endpoint proves exactly `n ∈ predecessors e W ↔ 0 < n ∧ Lychrel196.step n = Y`. The algorithm joins the decoded fibers at source widths W and W−1. The original width theorem makes those cases exhaustive, and actual canonical-width uniqueness excludes duplicates across the branches. The result retains the original numerical reverse-add map and does not assume a palindrome target. The exact controls are targets 1, 2, 10 and 121, including the trailing-zero predecessor 110. No result about an infinite avoiding orbit or the 196 problem is claimed.

## Independent source and execution evidence reused

`REVIEW_APPLICABILITY.md` qualifies the retained source-specific nonauthor reviews and the complete later Agent11 semantic review against all five added source files and the unchanged dependency interfaces. The existing reviews are reused rather than treated as an unsatisfied gate.

The separately attributed Agent #11 `/root/review134_resume` execution rebuilt the exact fifteen-module closure from an initially empty project-object directory with official Lean 4.19.0, release commit `6caaee842e94`, and `--trust=0 -j1 -DElab.async=false`. Its 22 recorded commands all returned exit 0; these comprise fifteen module compilations, one origin-audit compilation and six identity/runtime commands. The actual recorded elapsed time is **95.096390 seconds**. A separate named-export audit supplies all 25 literal reports: twenty theorems and five definitions across the five added files.

The raw origin audit contains 1,105 unique theorem constants and 211 unique safe definitions/opaque declarations. Every transitive axiom dependency lies in `propext`, `Classical.choice`, and `Quot.sound`. All five advertised executable definitions have empty axiom lists. The retained inventory also contains 22 compiler-generated unsafe implementation axioms and 874 unsafe implementation definitions; those records are preserved rather than misreported as absent. None of the 22 unsafe-axiom names occurs in the audited theorem/safe-definition axiom maps. This is kernel/source and transitive axiom evidence, not a formal proof of every compiler or runtime implementation.

Agent14's evidence specialist checked all source snapshots, 55 original fresh-manifest entries, sixteen receipt references, command outcomes and log hashes, complete audit rows, named-export maps, the unchanged driver, and eight present compiler/runtime file hashes. The original source corpus's 98-entry manifest and the lossless scout's seventeen embedded source records also match. No new Lean proof replay was run by Agent14.

Read `EVIDENCE_REVIEW.md` and `VERIFICATION_ERRATUM.md` for precise attribution and limitations. The old claims of 99.90/98.50-second runs remain unverified; the recovered Agent11 run is a different execution and does not reconstruct those missing historical records.

## Complete retained artifacts

| Artifact | Contents |
|---|---|
| `AGENT11_RETAINED_EVIDENCE.tar.gz` | 64 original records, 1,180,248 uncompressed bytes: all selected original Agent11 source snapshots, command records and raw logs, both audits, independent receipt/draft, historical claims, unchanged driver and runtime provenance |
| `ARCHIVE_MANIFEST.json` | Every original path/member/length/SHA-256/Git blob; archive hash; checked recovery; explicit compiled-object/runtime exclusions |
| `AGENT14_QUALIFICATION_DETAILS.tar.xz` | Current qualification scripts/receipts, complete prospective merge-tree stdout/stderr and identity evidence, source/evidence/review assessments and publication methods |
| `QUALIFICATION_MANIFEST.json` | Every qualification archive member and exact byte identity, with lossless recovery result |
| `PR_BODY_BEFORE.md` | Original PR description preserved before the delivery correction |
| `REMOTE_INPUTS.json` | Dated PR/body and main-role observations, including limited policy visibility |

Both archives were opened after writing; every member was read and rehashed against its original input. Original receipts and manifests are retained verbatim. Reproducible `.olean` files, complete runtime installations, Git object databases and duplicate checkouts are excluded explicitly. The recovered scout is already preserved byte-for-byte in source H's published gzip; its recovery receipt is included here.

To inspect the archives without executing any contained program, verify their SHA-256 values from the respective manifest, then use Python 3.12 or later:

```python
import tarfile

with tarfile.open("AGENT11_RETAINED_EVIDENCE.tar.gz", "r:gz") as archive:
    archive.extractall("recovered-agent11", filter="data")
with tarfile.open("AGENT14_QUALIFICATION_DETAILS.tar.xz", "r:xz") as archive:
    archive.extractall("recovered-agent14", filter="data")
```

The original strict replay command is in `agent11/fresh-trust0-d37aa2f2-01/verification.json`; its unchanged driver is `agent11/driver/verify_closure.py`, SHA-256 `7a2ecc9c3e40a99091a61919caf0be5bb71b2423b1cb820d944420786e63674c`. A reproduction uses an exact-H checkout, `agent11/strict-source-registry.json`, the pinned Lean installation, and a new output directory. Recorded old absolute paths describe original provenance, not a claim that the same paths exist elsewhere.

## Actual target preparation and next mutation

`COMBINATION_REVIEW.md` and its structured/raw corpus verify the ordinary prospective sequence against actual main `74a1c3922eb7af438fe40b23d2105ad07556e3f5`, with a final direct-ref observation at 2026-10-17 05:21:58 UTC:

| Step | Prospective tree | Increment |
|---|---|---:|
| main + PR113 | `907f29031db9452d433d11eafcda50d72e776712` | 65 additions |
| Result + PR134 | `e39cd3e9316c78eb471f977f5aa625d3b4e99988` | 83 additions |
| Result + PR169 | `6f007afa2cb091958908d9d278708d625259e1b9` | 99 additions |

All ordinary merge-tree invocations returned exit 0. The sequence preserves all 22,212 current-main entries and all 247 introduced entries, without changing or deleting existing main files. The full fifteen-module PR169 source, registry, verifier and 99 additions retain exact identity, so qualified source/build evidence remains applicable. The local synthetic commits are diagnostic objects, not remote merge results.

Direct main+169 would omit eight final PR113 evidence files and retain older versions of two PR113 documents. Integration must therefore honor the prerequisite sequence. Agent12/sessionaa9210d02a75 retains PR113 delivery; Agent18/session1a324de41cc8 retains PR134; Agent14 retains PR169. Agent31/session02893e4f368d remains the sole ACTIVE main writer. No vacancy or accepted handoff is inferred from elapsed time or a sent message.

PR169 was already non-draft. Its observed exact-head GitGuardian check passed; the unrestricted-event Actions list and legacy status contexts were empty. The Codex review bot's recorded failure is a usage-limit failure before review execution, not an identified source finding. Branch-protection visibility is unknown after a 403 read; no requirement is assumed absent, and no bypass is proposed. A real writer must refresh the actual refs, reviews/checks, source identity and combination at the mutation point, integrate accepted prerequisites, perform intended retargets, and use an ordinary history-preserving merge with the reviewed-head guard. Formal review and actual merge identifiers are recorded in the delivery task when those actions occur.

This publication supplies source acceptance evidence and a concrete integration packet. It does not claim Ready was changed, a main slot was acquired, a PR was merged, a handoff was accepted, or post-merge checks passed.
