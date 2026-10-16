# PR114 retained-evidence review — Agent #17

## Decision and scope

**PASS: the exact-source retained verification may be reused.** No missing mathematical verification obligation was identified by this evidence review. This is a fresh integrity/provenance/log inspection of existing verification, not a new Lean build. I executed zero Lean commands.

Reviewer: genuine nonauthor Agent #17 subagent /root/pr114_evidence. Delivery owner: Agent #17 /root. I did not author PR114 or its prior proof/evidence package. This report does not assert platform approval, a merge, or repository-wide verification.

Repository/PR: https://github.com/taco-jpg/p196-algorithm/pull/114

- Mathematical source: 71691d50497edc83247b3571af276bb0ee438491.
- Prior evidence commit: 2335bcaf40a70dd5e158d2ca033fed7134871897.
- Reviewed current head: 71c2ab3393e26d44b908fcbcc04d7527fac569f7.
- Registry: proofs/Agent101ProtectedFamily.registry.json.
- Registry SHA256: 04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307.
- Registry Git blob: 32858e441e8d5b3632e464aca1956334dc5a1bbe.
- Canonical verifier: proofs/verify_project__214bf7673efe116b.py.
- Verifier SHA256: c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a.
- GitHub changed-file inventory: 173 unique added paths, pages 100 + 73. A preliminary chat count of 172 was wrong; the saved direct Git blob inventory has all 173.

Both actual prior formal reviews were read, including their independence qualifications:

- https://github.com/taco-jpg/p196-algorithm/pull/114#pullrequestreview-5554269195
- https://github.com/taco-jpg/p196-algorithm/pull/114#pullrequestreview-5554380268

Both are COMMENTED by taco-jpg. They are attributed worker reviews, not external-account APPROVED reviews. Their actual logs and sources, not their PASS prose, support this reuse decision.

## Fresh archive validation

Every member of each mathematical-evidence archive passed independent compressed-size, SHA256, raw Git blob, member-set, member-size and member-SHA256 checks. Duplicate, unexpected, nonregular, or unsafe member paths were rejected. All archives lack compiler-object payloads. The three mathematical-evidence archives have no overlapping member paths.

| Archive | Compressed bytes | Members | Original file bytes | SHA256 |
| --- | ---: | ---: | ---: | --- |
| final-independent.tar.gz | 352620 | 142 | 1941455 | 31347b5afacef968f6eb9ecdac2985612a9457a7ad5400d84b2bcb9c3a455332 |
| generic-verification.tar.gz | 82565 | 41 | 463734 | 6aaa2a53fa4d8490c37b974304b3a0bc24a3cbea82eeba682674e0d73d2c3250 |
| runtime-development.tar.gz | 140683 | 102 | 1040000 | 6c1ec4e2aa0084369ad16f8133a24d8148b006dfbdaabab48ce0eb3a8e45a130 |

The respective Git blobs are d99f1971f633863e0b3f2864838abcf6eb5116d9, 1af9f0df1a716e2b6876dcb88945f5cee2360087, and f3f780263ce71f94996c5091ec07d08d26a30359.

Manifest SHA256 values respectively are e7eca667f6472c081d37a88f8200e24ecc5dd91ea10520e0820cbe65c93a9e02, b6f2641ddb5d53cf028ff755677744c2a024dc70d08353015a5a29b0d0d02071, and fc082c2b127fdd9c49f59e6172a23149a830a6ec34fe6562ab641d93c5232d81.

The additional historical ownership/source census archive passed all 18 member checks: 357968 bytes, SHA256 173ac2bd8f7f0b7daff072379a14bddeb07689033ba4ac45f5119a12c0e2600f, Git blob 555dd32a4df6b73de7f4f4d3c1a2a7081c175950. Its purpose explicitly excludes mathematical proof or exhaustive repository acceptance, and I used it only as preserved historical provenance.

Additionally, 51 archived members that also occur directly in PR114 match their authoritative published Git blobs at the reviewed head. Complete results are retained in evidence-validation.json and supplemental-integrity.json.

I read the original final packer and verification/recovery helper before running any source script. The helper verifies the whole compressed archive and all members before optional extraction; it rejects traversal, nonregular entries, duplicate paths, path collisions and differing existing destination files. Extraction uses exclusive creation. Only verify-only mode was run, with exit 0, members_verified 142 and files_written 0. No extraction, packer execution, or Lean invocation occurred.

## Complete source closure and adapter

All 26 archived original source files, totaling 584163 bytes, match both registry SHA256 and raw Git blob identities. Their actual canonical build snapshots match the original report's build_sha256. All normal build snapshots are byte-identical to their published source.

The documented exception is the foundation facade. Lychrel196Research has 4445 lines. Removing its first import Std line leaves exactly 4444 lines, which I compared byte-for-byte to the embedded block starting at line 11 of LychrelDigitSums. The complete blocks match. The canonical verifier compiles LychrelDigitSums and creates a Lychrel196Research facade importing it; both original and actual-build hashes are preserved. This does not mean the original Research source was separately compiled in that final closure.

The 26 modules are LychrelDigitSums, Lychrel196Research, Agent101DigitPairs, Agent101MultiplicityBounds, Agent101SplitEnumeration, Agent101NumericFibers, Agent101PalindromeFibers, Agent101NonpalindromicFibers, PeriodObstructions, ActualWordBridge, FamilyDefinitions, FamilyCardinality, Agent101ProtectedMultiplicity, Agent101ProtectedPalindrome, Agent101ProtectedNonpalindromic, DecimalSafeRuns, SafetyBridge, NormalizedSafety, TemplateStep, Compat, IntegerInterfaces, Agent101NormalizationValue, FiniteHorizonOverflow, FiniteHorizonTheorem, Agent101ProtectedSafety, and Agent101ProtectedFamily.

Root separately checked published current-source hashes/imports and the intended current-main combination. Those integration operations are not claimed as this reviewer's work. Reuse applies to the byte-identical closure and verifier, not to arbitrary subsequent edits.

## Original commands and environment: accurate trust distinction

The final independent canonical command was:

~~~text
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent101ProtectedFamily.registry.json \
  --project agent101-protected-family \
  --lean /workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean \
  --output /workspace/scratch/2a8a87fd78df/agent101-final-family-independent-71691d5
~~~

The original report records Lean 4.19.0, x86_64 Linux, commit 6caaee842e94, Release. Executable SHA256 is 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023. Exact shared-library hashes are preserved in the original report and the new JSON receipt. The run used a new output directory and its own source directory as LEAN_PATH; all 26 selected modules were compiled freshly.

Original module commands use:

~~~text
lean -j1 -DElab.async=false -o MODULE.olean MODULE.lean
~~~

Each recorded module command returned zero. All 27 complete canonical logs (26 builds plus initial ProjectAudit) match their original SHA256 and the retained review copies. No error, sorryAx, or Lean.ofReduceBool occurs in those successful logs. Some legitimate successful compiler logs are empty.

**The final 26 module-build commands did not explicitly pass --trust=0.** They must not be reported as 26 explicit-trust-zero fresh builds. After that run, the independent reviewer executed the unchanged generated ProjectAudit and the separate complete public audit with:

~~~text
lean --trust=0 -j1 -DElab.async=false ProjectAudit.lean
lean --trust=0 -j1 -DElab.async=false FinalPublicAudit.lean
~~~

Both returned zero; recorded durations are 36.974023739 and 5.478505403 seconds. Exact audit-source and log hashes match. These are explicit-trust-zero audits of the compiled closure, not a second full fresh build.

The original verifier report retains its hardcoded agent: Agent #1 field. The independent receipt identifies the actual executor, Agent #101's research-inventory worker. This legacy label is not used to invent executor identity.

## Actual axiom and declaration audit

I inspected the generated ProjectAudit, final-audits.py, complete retained logs, and separate public audit. ProjectAudit selects declarations by actual originating module, rejects safe custom axiom declarations, applies Lean.collectAxioms to every selected theorem, and rejects any dependency outside the three permitted foundations. Unsafe implementation axioms are logged separately and are not added to the proof allowlist.

Independent parsing of the complete output yields 1783 unique theorem constants. Every individual axiom list is a subset of, and their exact union is:

~~~text
propext
Classical.choice
Quot.sound
~~~

There are 32 separately recorded unsafe implementation axioms, matching the original inventory. None occurs in any of the 1783 mathematical theorem axiom lists.

The public audit has 94 unique declarations: 85 theorems and 9 definitions. The exact same 94 names each appear in printed axiom results and as PUBLIC_SAFE. It rejects public unsafe declarations and custom axioms. Counts per module are:

| Module | Public declarations |
| --- | ---: |
| Agent101ProtectedMultiplicity | 18 |
| Agent101NormalizationValue | 5 |
| Agent101ProtectedSafety | 10 |
| Agent101PalindromeFibers | 14 |
| Agent101NonpalindromicFibers | 18 |
| Agent101ProtectedPalindrome | 15 |
| Agent101ProtectedNonpalindromic | 10 |
| Agent101ProtectedFamily | 4 |

Actual public axiom distribution: 12 axiom-free; 11 only propext; 15 propext plus Quot.sound; 56 all three permitted axioms. The final endpoint Agent101.Protected.protectedNonpalFamily_exact has exactly propext, Classical.choice, Quot.sound.

Complete log hashes:

- ProjectAudit trust zero: 9dade97bc996b0b5eb534bdc9f95f3dc1b5c55160182539aab2e76a0c8532cb0.
- PublicAudit trust zero: bc4d262de6d75ce61e8eddad363c1820354d096a5dc788e52169ca839cc57c6f.

Initial ProjectAudit output and later explicit-trust-zero ProjectAudit output are byte-identical, while the command records remain distinct. No separate complete census of every transitive safe definition is claimed.

## Review independence and earlier verification

The numeric-bridge worker did not author either new generic module it reviewed. It did author the older NumericFibers dependency and explicitly disclosed that limitation. Its independent seven-module fresh build used --trust=0 -j1 -DElab.async=false with isolated LEAN_PATH. I checked all nine command records and complete logs: seven sources, BoundaryReview and ExportAudit. The public/boundary audit includes exactly 32 public exports plus 19 independent boundary theorems.

Its compiled-environment audit contains exactly 48 logical declarations: 44 theorems and four definitions, all with permitted foundational axioms. Fourteen narrowly classified unsafe compiler implementation symbols are separately recorded. The preserved initial classifier failure has exit one; it rejected an unsafe specialized filter implementation too broadly. The corrected classifier rejects safe custom axioms and audits every safe logical export. Original source and failure evidence remain intact; this is an audit-instrumentation correction, not authorization for unsafe mathematics.

The research-inventory worker independently reviewed the protected counting/filter modules and final normalization, safety and aggregate modules. It authored the older SplitEnumeration and generic PalindromeFibers dependencies and does not present its own dependencies as independently reviewed by itself. Generic PalindromeFibers has the separate numeric-bridge review. I read all three protected counting semantic reports and the final semantic report, including authorship disclosures and source pins. The current session's separate semantics specialist has also independently read the mathematical sources.

These are genuine separately attributed worker reviews within the same session/account, as permitted by the project. They are not independent GitHub account approvals and cannot replace an actual platform-required approval.

The generic parent's additional canonical verification at bbbcc8572f9c9f9c2e17b39d0358c8eda34d8386 also has matching original logs and command hashes: seven fresh modules and 1000 audited theorem constants. It is author verification, not the independent review.

## Historical failures, provenance and inventory correction

The 102-member development archive accurately preserves failed attempts, alternative SafeHigh work and an early 21-module author snapshot. The latter's observed HEAD e3802562ce44ce2c5211b6396e5f4d1693c39fc5 did not yet publish four new source paths, and the original clean flag ignored untracked files. That run is correctly labeled an exact-hash local author snapshot, not an exact published-commit rebuild. The later published 71691 source readback and fresh 26-module verification close that provenance gap. Accepted normalization/safety snapshots in the development archive match final source hashes.

The additive erratum is correct: the original canonical FILES inventory has 55 entries, comprising 27 Lean sources, 27 logs and one verification report. It has zero .olean or .ilean entries. It is 9248 bytes, SHA256 83e61b850839dc09e4f8b6e301e64d44e1973559a1ede988bf40df83e75f13e0.

Every one of its 55 entries matches actual archived bytes. Its canonical and review copies inside the archive are byte-identical; the direct published review copy also has the matching raw Git blob. The original historical external local canonical directory was unavailable to this reviewer, so I do not claim to repeat the historical four-local-copy check.

The separate final archive manifest has 142 members and records 26 excluded canonical .olean files. It includes later public audit/review materials beyond the 55-entry earlier snapshot. Preserved old wording that FILES itself listed compiler objects was false; the additive erratum explicitly corrects that wording without rewriting historical archive/manifest/packer bytes. No discrepancy remains in the actual inventory.

## New artifacts, reproducibility and limitations

New evidence files comprise the English report, validate_retained_evidence.py, validate_supplemental.py, their machine-readable results, full logs, execution receipt and published-blob inventory. The first validator attempt incorrectly searched generic source copies under the review directory instead of the canonical verification directory. Its script and AssertionError are preserved as validate_retained_evidence-v01.py and evidence-validation-v01.log. Only the new validator's path selection was corrected; original evidence was unchanged.

The full disk was respected. Work used an approved isolated temporary-memory directory, without deleting anything. An initial default-sandbox read could not see that namespace and did not run the helper; approved executor mode was used thereafter. No access-control bypass, remote mutation, paid compute or Lean execution occurred.

Original archive locations at the exact reviewed head are:

- proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/archives/final-independent.tar.gz and final-independent-manifest.json.
- proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/archives/runtime-development.tar.gz and manifest.json.
- proofs/contributions/agent-101/nonpalindromic-fibers-20261016/archives/generic-verification.tar.gz and generic-verification.manifest.json.
- proofs/contributions/agent-101/nonpalindromic-fibers-20261016/ownership/source-scope-inventory.tar.gz and manifest.json.

Recovery uses github_fetch_file at head 71c2ab3393e26d44b908fcbcc04d7527fac569f7, with encoding base64 for binary tar files, followed by exact decoding. Immutable identities are recorded above and in JSON. New validator scripts expect the copied archives/manifests in their own directory. Original large archives need not be republished with this report; new observations and logs should be retained completely.

## Delivery consequence

The exact published closure, pinned environment, original full command/log evidence, scoped independent reviews, precise trust labeling, transitive theorem axiom checks, public safety census and fresh archive validation justify reuse. No duplicate 26-module Lean build is required by the examined evidence.

The delivery owner must confirm the same source/verifier/configuration in the latest combined main tree, satisfy actual ownership and platform gates, execute the guarded permitted merge when qualified, and verify the published target. This PASS is a delivery checkpoint, not an integrated status.
