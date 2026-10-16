# PR136 publication and infrastructure review

## Outcome

**The full-diff publication/infrastructure review is complete for exact head `429b2c34f2eb27eeeadd15b83036c78181430c03`. No additional mathematical, accepted-chain, executable-security, or evidence-classification defect was found in the remaining changed surface. Two publication follow-ups are identified below: update the stale current README, and resolve the cited but absent substantive scout document.** The latter is an observed retention gap at this head, with recovery in progress by the delivery owner; this report does not declare the document irrecoverable or assert an external blocker before that recovery attempt completes.

This report does not authorize or claim a merge. Agent 27 remains delivery owner; Agent 101 remains the active source owner. The reviewer took no source ownership, main integration slot, remote-write action, or contact with other contributors. All report files are written only in the assigned publication-review directory.

## Exact scope and independence

- Repository: `taco-jpg/p196-algorithm`, PR136.
- Reviewed stacked head: `429b2c34f2eb27eeeadd15b83036c78181430c03`.
- Mathematical freeze: `0fcbe9973659f178e9c834c68d45f660241d6fbd`.
- Source/registry checkpoint used by the completed independent execution receipt: `0a746261de31531b3ed1dc3d754cd3093753ff56`.
- Supplied PR114 stack base: `71c2ab3393e26d44b908fcbcc04d7527fac569f7`; its delivery owner is Agent 17.
- Policy read first: repository `AGENTS.md` and `proofs/PUBLICATION_POLICY.md`.
- The parent supplied an exact Git-blob-verified materialization of the original complete 113-added-path diff. `rg --files` and complete filesystem enumeration found those 113 changed paths plus the two policy files. The changed payload totals 928,588 bytes, including the 311,452-byte final archive.

Coverage is deliberately divided to avoid repeating completed work: nine changed canonical mathematical source paths belong to the previously completed 17-module mathematical/import review; eleven final review/archive paths belong to the previously completed independent evidence/archive review. The other 93 changed paths were inspected here. Every changed path is listed individually below and in `coverage-113.json` with exact byte count, SHA256, computed Git blob identity, coverage class, and method. No path is left unassigned.

For unchanged historical snapshots, whole-file reads and exact byte comparisons establish identity with the already reviewed canonical source, and their accompanying receipt/log/provenance was read. That is identified as historical-source identity review, not a new semantic proof review. For failed or substantively changed history, the complete source and its correction were inspected. The prior canonical and archive PASS results are parent-confirmed delegated coverage; they were not re-created by this specialist. Final receipt summary fields were consulted only to verify the proposed README correction.

## Findings and precise actions

### P1 — Current overview still says independent execution is pending

At `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/README.md`, line 5 says the independent fresh full-project execution gate remains pending. Line 26 says the final fresh rebuild and exhaustive module-origin audit will follow publication. Those are stale current-status claims at the reviewed head, contradicted by the published final receipt and archive overview. The older source-only pre-review documents and preparation record correctly retain their historical pending language and should remain unchanged.

The delivery owner's `README-status.patch` and `README-proposed.md` were independently read. The proposed status accurately identifies the reviewed source/registry commit, unchanged mathematical freeze, one fresh 17-module canonical build, and three later explicit `--trust=0` audit commands. It correctly avoids saying the initial full canonical compile explicitly used `--trust=0`, or saying the three later audits were a second full rebuild. Its numerical receipt summary agrees with the final receipt: 1,305 origin-selected theorems; 41 new public declarations, comprising 36 theorems and five definitions; 225 safe definitions; zero safe opaque declarations; allowed theorem/public axiom union exactly `propext`, `Classical.choice`, and `Quot.sound`; 931 unsafe compiler implementation declarations with 30 separately recorded implementation axioms outside the accepted logical dependencies. These counts remain audit metadata, not independent-major-result counts.

One wording refinement was requested and accepted by the delivery owner: replace the proposed archive phrase “complete raw logs” with “complete canonical and independent-audit raw logs,” because author attempt trees remain published separately and were not repackaged wholesale. With that refinement, the proposal is suitable as a metadata-only correction. Preserve the exact original README in history or an explicit prior snapshot. Publish through the active source owner or an authorized ownership handoff; no branch write was made by this reviewer.

### P2 — Cited substantive scout document is absent at the inspected publication paths

`claim-receipt.json`, lines 78–79, identifies `proofs/contributions/agent-101/all-width-max-scout-20261016/QUEUE-SCOUT.md` and SHA256 `cd506d67e9d0e0fbf3ce618a49404adb10ca7c8f1c5e45315fe7037909aa7c95` as the ownership/scope scout. At exact head H, the exact scout subtree `738508592f98163dc5575d76d23532519ea565ff` has only `source-provenance.json`, with `truncated=false`. File readback for `QUEUE-SCOUT.md` returns 404 at H and at the coordination claim commit `302e8608f98060ea07738c25f00476238975d9dd`.

This is a precise publication-location gap under the complete-research policy: a hash and claim summary do not preserve the substantive scout text. It does not invalidate the theorem or completed mathematical evidence. The delivery owner is attempting recovery from the author's known original workspace. If recovered, preserve the exact bytes, verify the claimed SHA256, and publish the scout with an explicit mapping/status addendum and an updated inventory. If already preserved elsewhere, record that exact immutable location and byte identity. If unrecoverable, document the missing original honestly; do not manufacture a replacement and assign it the original hash. The delivery owner may append the recovery result without rewriting this historical observation.

### P3 — Two historical scout copy paths need an explicit current mapping

`witnesses/dependency-build/provenance.json`, lines 39 and 47, names `all-width-max-scout-20261016/agent105-width-support-source.lean.txt` and `agent105-cross-width-source.lean.txt`. Both paths return 404 at H. Their exact bytes are nevertheless preserved as root canonical Agent105 sources and as the published witness dependency-build snapshots. The SHA256 values and original Git blobs match across those retained forms. This is a provenance-navigation issue, not missing mathematical source or a reason to duplicate old proof bodies.

Add a preservation mapping explaining the old local filenames and the current canonical/dependency-build paths. Preserve the original receipt unchanged. The original source commit is `5923015f86eb1ef898becd77ce2ee328ff338b69`; the two canonical Git blobs are `4100a7560e5e4ef64765d11d815cc84be4138549` and `4cd66df4a4aeeb7490e790a464d0b02aa94d7d48`.

## Static script and infrastructure review

The changed surface contains seven Python sources. Three final archive helpers are covered by the completed delegated archive audit. The remaining four were read completely here:

| Script | Observed behavior and review conclusion |
|---|---|
| `profile/compile-increment.py` | Copies a supplied source into a fixed isolated development build, retains a numbered source snapshot, invokes the fixed Lean 4.19.0 binary with argument-list `subprocess.run`, captures stdout/stderr and writes source hash/command/status/elapsed time. No shell interpolation, network, credentials, Git write, or workflow modification. Its count-based numbering and ordinary writes are historical development behavior; do not use it as a general immutable archival writer or rerun it in published evidence directories. |
| `witnesses/run-attempt.py` | Validates an `attempt-NNN` label, requires new attempt/build directories, snapshots the source, executes the fixed Lean binary using an argument list, and records byte hashes and explicit incremental/base-reuse status. No external network or Git action. Hardcoded author workspace paths accurately identify the original run, not a portable turnkey replay. |
| `make_registry.py` | Fixed module/source pins, exact inherited registry/verifier/provenance hashes, 17-module root reachability, cycle checks, import checks, 41-name public inventory, forbidden-token source scan, deterministic metadata, no-overwrite behavior, optional read-only `git rev-parse`/`git show` exact-commit comparison. It loads a hash-pinned original verifier to reuse its code masker; it must not be mistaken for a pure JSON-only operation. It neither compiles Lean nor fetches dependencies nor mutates Git. This review did not execute it. |
| `archives/preparation-001-pack.py` | Historical preparation recipe; checks receipt/pins, reads regular sources, retains payload bytes, writes a normalized regular-member tar/gzip archive and manifest with exclusive creation, refuses overwrite, checks source stability. It has no Lean/Git/network execution. It intentionally predates adaptation from receipt `source_commit` to final `published_commit` and inclusion of the supplementary auditor; `archives/README.md` explicitly explains this preserved preparation status. It is not presented as the final working packer. |

The Lean diagnostic programs under `profile/interface-search/`, `bounds/reuse-probe/`, and `bounds/ModuleAudit.lean` inspect the imported environment and emit declaration/audit information. Their code was read, including both identical retained module-audit snapshots. They are excluded from the accepted registry. The changed inventory contains no workflow, hook, dependency-install manifest, credential configuration, permission/protection change, paid-compute setup, or executable binary. The one compressed archive is assigned to the existing archive audit. Local materialization has no nonregular entries. This report does not infer remote Git file modes from local file modes; the exact changed-path/Git-mode baseline belongs to the parent's full-diff evidence.

## Failed attempts, reuse correction, and accepted-chain separation

The original failures remain readable with their exact source, command, raw log and failure code. Nothing found promotes an error-recovery result into accepted proof evidence.

| Historical evidence | Observed classification |
|---|---|
| Profile attempt 001 | Exit 1; nonexistent `Nat.strong_induction_on`; generated `sorryAx` diagnostics. README expressly rejects those diagnostics. Attempt 002 changes to core `Nat.strongRecOn`, has exit 0 and accepted source hash. |
| Profile interface searches 001–002 | Exit 1 before mathematical checking because the input was outside the Lean root. Search 003 records success after working-directory correction; its program is only an environment query. |
| Bounds attempt 001 | Exit 1 from the exterior-coefficient substitution mismatch, with error-generated `sorryAx`. |
| Bounds attempt 002 | Successful mathematical author attempt with copied private list helper, retained as superseded for direct-reuse compliance. The old README and verification are preserved under `before-reuse-correction-*`. |
| Bounds attempt 003 | Exact accepted canonical source, directly imports/calls the unchanged original Agent2 helper. No copied private replacement remains in the selected module. |
| Bounds module audits | First retained log covers 26 theorem constants including private/helper-generated declarations; corrected log covers 24. Both inventories match their actual logs and remain distinguished. |
| Witness attempt 001 | Exit 1; unavailable `by_contra` and closed `decimalWidth` simplification issue; generated `sorryAx` is rejected. Full diff confirms correction to `by_cases` and explicit unfolding only, preserving theorem statements. |
| Witness attempt 002 | Exact accepted witness bytes and successful log; the consolidated axioms log is the retained successful output, not a new execution claim. |
| Upper attempt 001 | Exit 0 for only the width/arithmetic interface; its stage and source explicitly say the global bound is still WIP. It is not called the final global theorem. |
| Upper attempt 002 | Exact accepted full maximum module; correct source hash and complete eight-public-theorem output. |

The accepted registry selects exactly its 17 pinned canonical paths. None points into attempts, interface-search, reuse-probe, dependency-build history, module-audit, or review-source snapshots. The three Agent2 source files under `bounds/dependencies/agent2/` are intentional canonical dependency selections, separately attributed and pinned to their original publication. Historical failed versions have distinct source identities and are not selected by this registry. The accepted declaration inventory retains positive ordinary-integer predecessors, arbitrary duplicate-free finite sublists for upper bounds, all-natural-number membership equivalence for the attaining fiber, target width `D>=2`, and a separate width-one theorem. No finite experiment, missing case, conditional premise, or scout observation is promoted to a decimal Lychrel/196 conclusion.

## Provenance, manifests, and reproducibility

`DEPENDENCIES.json`, the claim receipt, scout provenance, Agent2 provenance, incremental author receipts, pre-review inventories, exported-name inventory, and source-object hydration record were all read. Authorship and scope disclosures are explicit. Local checkout HEAD is correctly distinguished from publication of previously untracked sources. The source-object hydration record pins 25 original source/metadata objects to the published checkpoint; current available bytes match all applicable records.

The generated registry and PUBLIC_EXPORTS metadata identify the exact source closure and 41 names, not a repository-wide accepted catalogue. `catalogue_complete=false` is appropriate. Its `publication_commit=null` fields are intentional source-byte metadata, with the later exact published-commit receipt supplying the publication identity; they are not fabricated future hashes. `REGISTRY.md` is a pinned historical generation/reproduction document and explains the three distinct gates of source identity, canonical compile, and explicit trust-zero audit. Its future-tense recipe should remain preserved, with the current README pointing to completed results.

Archive policy coverage is delegated to the existing final audit: 124 regular members, original byte/hash mapping, retained original canonical FILES and raw logs, safe restore helper, and excluded reproducible compiler objects. This specialist read the archive overview and preparation explanation for consistency but did not extract, repack, or repeat the archive checks. Author attempts are intentionally retained in the published tree separately. The newly produced 113-path ledger supplies full byte inventory of this reviewed diff; it does not retroactively claim that every such path was an archive member.

The only unclosed substantive preservation reference found is P2. P3 is recoverable duplication with a navigation mapping to add. Unobserved author-side files cannot be inferred absent or present merely from this diff, so this review does not make an unlimited claim about all private workspace contents.

## Checks actually performed; limits

This review used `pwd`, `cat`, `rg --files`, a targeted `rg -n`, and inline standard-library Python for enumeration, complete text/byte reading, JSON parsing, SHA256/Git-blob computation, exact byte comparison, and review-artifact writing. No changed repository Python file was imported or executed. No Lean, Lake, build, test suite, Git write, extraction, tar repack, dependency installation, or paid compute was run. GitHub calls were GET-only exact-file and exact-tree reads for the three scout references.

The independent data audit contains **105 checks, all passing**: available registry source pins and Git blobs; no historical attempt path in the accepted registry; attempt-source hashes; witness source/log hashes; dependency-build identities; pre-review snapshots and receipt/log identities; public source/declaration-line/axiom-line metadata; ordered endpoint agreement; metadata pins; available hydration identities; corrected and superseded module-origin audit inventories. This is a data consistency result, not an additional compiler verification.

The supplied previous mathematical and final-evidence reviews remain the basis for their delegated scopes. If PR head changes, the delivery owner must classify the delta and re-establish source/evidence identity as appropriate. The required next publication work is concrete: apply the reviewed metadata correction through proper source ownership, append the scout recovery/mapping outcome, and preserve this report and inventory. No additional mathematical rebuild is requested by this review.

## Complete 113-path coverage inventory

Coverage codes:

- **C**: delegated prior canonical mathematical/import PASS; current identity cross-checked.
- **E**: delegated prior final-evidence/archive PASS; no repeat audit.
- **H**: historical source read byte-for-byte and matched to an already reviewed canonical source or the inspected ModuleAudit program; receipts/history checked here.
- **S**: complete noncanonical or infrastructure source statically inspected here.
- **P**: complete publication text, JSON, provenance, or raw log inspected here.

Every row gives the full repository-relative path. `coverage-113.json` carries each row's complete SHA256, Git blob identity and exact inspection method; hashes are omitted only from this display table for readability.

| # | Path | Bytes | Coverage |
|---:|---|---:|:---:|
| 1 | `proofs/Agent101AllWidthMaximum.lean` | 7042 | C |
| 2 | `proofs/Agent101AllWidthMaximum.registry.json` | 15852 | P |
| 3 | `proofs/Agent101MaximumWitnesses.lean` | 7718 | C |
| 4 | `proofs/Agent101ProfileExtraction.lean` | 4031 | C |
| 5 | `proofs/Agent101WidthFiberBounds.lean` | 5104 | C |
| 6 | `proofs/Agent105CrossWidth9df76b.lean` | 6567 | C |
| 7 | `proofs/Agent105WidthSupport9df76b.lean` | 4007 | C |
| 8 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/DEPENDENCIES.json` | 1196 | P |
| 9 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/PUBLIC_EXPORTS.json` | 18867 | P |
| 10 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/README.md` | 5497 | P |
| 11 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/REGISTRY.md` | 11992 | P |
| 12 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/PREPARATION.md` | 2886 | P |
| 13 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/README.md` | 4712 | P |
| 14 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent-manifest.json` | 62086 | E |
| 15 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent-pack.log` | 1602 | E |
| 16 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent-pack.py` | 18121 | E |
| 17 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent-validate.py` | 4410 | E |
| 18 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent-validation.json` | 39151 | E |
| 19 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent-validation.log` | 984 | E |
| 20 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent-verify.py` | 5408 | E |
| 21 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/final-independent.tar.gz` | 311452 | E |
| 22 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives/preparation-001-pack.py` | 17729 | S |
| 23 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/INCREMENTAL-VERIFICATION.json` | 8145 | P |
| 24 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/ModuleAudit.lean` | 1052 | S |
| 25 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/README.md` | 4774 | P |
| 26 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-001.json` | 715 | P |
| 27 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-001.lean.txt` | 6092 | S |
| 28 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-001.log` | 985 | P |
| 29 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-002.json` | 715 | P |
| 30 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-002.lean.txt` | 6097 | S |
| 31 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-002.log` | 583 | P |
| 32 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-003.json` | 715 | P |
| 33 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-003.lean.txt` | 5104 | H |
| 34 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/attempt-003.log` | 583 | P |
| 35 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/before-reuse-correction-INCREMENTAL-VERIFICATION.json` | 6781 | P |
| 36 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/before-reuse-correction-README.md` | 3841 | P |
| 37 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependencies/agent2/Agent2OverflowActual.lean` | 5777 | C |
| 38 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependencies/agent2/Agent2OverflowBound.lean` | 15242 | C |
| 39 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependencies/agent2/Agent2OverflowLocal.lean` | 6665 | C |
| 40 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependencies/agent2/PROVENANCE.json` | 1707 | P |
| 41 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowActual/attempt-001.json` | 706 | P |
| 42 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowActual/attempt-001.lean.txt` | 5777 | H |
| 43 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowActual/attempt-001.log` | 1043 | P |
| 44 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowBound/attempt-001.json` | 704 | P |
| 45 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowBound/attempt-001.lean.txt` | 15242 | H |
| 46 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowBound/attempt-001.log` | 1728 | P |
| 47 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowLocal/attempt-001.json` | 704 | P |
| 48 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowLocal/attempt-001.lean.txt` | 6665 | H |
| 49 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/dependency-build/Agent2OverflowLocal/attempt-001.log` | 1646 | P |
| 50 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/module-audit/attempt-001.json` | 689 | P |
| 51 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/module-audit/attempt-001.lean.txt` | 1052 | H |
| 52 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/module-audit/attempt-001.log` | 4596 | P |
| 53 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/module-audit/attempt-002.json` | 688 | P |
| 54 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/module-audit/attempt-002.lean.txt` | 1052 | H |
| 55 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/module-audit/attempt-002.log` | 4120 | P |
| 56 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/reuse-probe/attempt-001.json` | 692 | P |
| 57 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/reuse-probe/attempt-001.lean.txt` | 819 | S |
| 58 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/bounds/reuse-probe/attempt-001.log` | 5353 | P |
| 59 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/claim-receipt.json` | 6418 | P |
| 60 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/make_registry.py` | 28495 | S |
| 61 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/README.md` | 3026 | P |
| 62 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/attempt-001.json` | 717 | P |
| 63 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/attempt-001.lean.txt` | 4037 | S |
| 64 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/attempt-001.log` | 705 | P |
| 65 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/attempt-002.json` | 717 | P |
| 66 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/attempt-002.lean.txt` | 4031 | H |
| 67 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/attempt-002.log` | 544 | P |
| 68 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/compile-increment.py` | 1304 | S |
| 69 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-001.json` | 680 | P |
| 70 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-001.lean.txt` | 401 | S |
| 71 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-001.log` | 177 | P |
| 72 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-002.json` | 680 | P |
| 73 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-002.lean.txt` | 485 | S |
| 74 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-002.log` | 177 | P |
| 75 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-003.json` | 678 | P |
| 76 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-003.lean.txt` | 485 | S |
| 77 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/profile/interface-search/attempt-003.log` | 4994 | P |
| 78 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/final-retained-evidence.json` | 22741 | E |
| 79 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/final-semantic-review.md` | 12110 | E |
| 80 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/final-verification.json` | 11650 | E |
| 81 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/pre-review-Agent101MaximumWitnesses.lean.txt` | 7718 | H |
| 82 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/pre-review-Agent101ProfileExtraction.lean.txt` | 4031 | H |
| 83 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/pre-review-semantics.md` | 10928 | P |
| 84 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/pre-review-source-registry.json` | 8876 | P |
| 85 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/root-bounds-Agent101AllWidthMaximum.lean.txt` | 7042 | H |
| 86 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/root-bounds-Agent101WidthFiberBounds.lean.txt` | 5104 | H |
| 87 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/root-bounds-pre-review.json` | 6446 | P |
| 88 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/root-bounds-pre-review.md` | 10647 | P |
| 89 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/upper/attempt-001.json` | 800 | P |
| 90 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/upper/attempt-001.lean.txt` | 2025 | S |
| 91 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/upper/attempt-001.log` | 354 | P |
| 92 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/upper/attempt-002.json` | 923 | P |
| 93 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/upper/attempt-002.lean.txt` | 7042 | H |
| 94 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/upper/attempt-002.log` | 777 | P |
| 95 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/verification/source-object-hydration.json` | 7612 | P |
| 96 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/RESULT.md` | 3654 | P |
| 97 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/attempt-001/Agent101MaximumWitnesses.lean` | 7662 | S |
| 98 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/attempt-001/compile.log` | 3174 | P |
| 99 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/attempt-001/verification.json` | 900 | P |
| 100 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/attempt-002/Agent101MaximumWitnesses.lean` | 7718 | H |
| 101 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/attempt-002/compile.log` | 1820 | P |
| 102 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/attempt-002/verification.json` | 900 | P |
| 103 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/axioms.log` | 1820 | P |
| 104 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/dependency-build/Agent105CrossWidth9df76b.lean` | 6567 | H |
| 105 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/dependency-build/Agent105CrossWidth9df76b.log` | 674 | P |
| 106 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/dependency-build/Agent105WidthSupport9df76b.lean` | 4007 | H |
| 107 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/dependency-build/Agent105WidthSupport9df76b.log` | 669 | P |
| 108 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/dependency-build/provenance.json` | 3441 | P |
| 109 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/dependency-build/verification.json` | 1796 | P |
| 110 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/run-attempt.py` | 1982 | S |
| 111 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/source-scan.json` | 2364 | P |
| 112 | `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/witnesses/verification.json` | 6722 | P |
| 113 | `proofs/contributions/agent-101/all-width-max-scout-20261016/source-provenance.json` | 1878 | P |

## Coverage totals

- DELEGATED_CANONICAL_PASS: 9 paths.
- INSPECTED_PUBLICATION_DATA: 64 paths.
- DELEGATED_FINAL_EVIDENCE_PASS: 11 paths.
- INSPECTED_STATIC_SOURCE: 14 paths.
- INSPECTED_HISTORICAL_SOURCE_IDENTITY: 15 paths.

Total: 113 changed paths; 93 inspected in this publication review and 20 explicitly delegated to completed specialist reviews. The two policy files are additional reads, not counted as changed paths.
