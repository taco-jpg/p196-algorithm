# Independent PR106 packaging and evidence review

Reviewer: `/root/pr106_package_audit`, genuine separate subagent of Agent #30.
Review completed: 2026-10-16T23:37:26Z.
Coordination claim: `d32f6d09005db73e541d880275b775bf5d0badee`.
Task: `proofs/coordination/tasks/agent30-session4ab29b-pr106-delivery-20261016.json`.
Repository: `taco-jpg/p196-algorithm`.
Frozen source head: `ed9b9048adfdda70f699a8a40997a4330b76dc16` (PR106).

## Decision

**PASS for exact published byte identity and consistent retained source/log hash claims. FAIL for delivery completeness at the frozen head.** The failure is missing final independent evidence and portable scoped replay, not a mathematical counterexample or a discovered source hash mismatch.

I read every file in the complete additive PR106 diff: **50 paths, 45 distinct Git blobs, 3,039 added lines, zero deleted lines**. All 45 fetched UTF-8 blob bodies independently reproduce their advertised Git SHA-1 using the Git blob header and original bytes. All per-file SHA256 values, byte counts, exact paths, complete-read status, source/log hash cross-references, and 36 public theorem names are in `PACKAGE_MANIFEST.json`. There is no unread changed-file gap. Duplicate successful snapshots were identified by exact blob equality, not by filenames.

This is an independent static packaging review. I performed no Lean compilation, source change, remote write, combined-tree test, or integration. Semantic review and fresh six-source verification belong to separate reviewers. The parent owns the combined-tree check, final exact-source review submission, and integration.

## What the frozen publication establishes

The five final source modules exactly equal their retained successful development snapshots:

| Module | Successful snapshot | Git blob | SHA256 |
| --- | --- | --- | --- |
| Agent106CarryBudget | budget/attempt-001/Agent106CarryBudget.lean | 8ab159e79cbd601bb0fad884f0ac392574f38d7b | 5eb8d4684584f3941bec9a7ea61b8ca3d7049a8f2ae60d02d64d9e2b6f2b7edc |
| Agent106CongruenceSeed | seed/attempt-04.lean | 4af21bdc673ffebfbad5bda77b79fc788f281259 | 3c14410f4ccb7a7398c24ba5f24123197dfceb295d09b9aade9b4917e4aa36ed |
| Agent106SparseTarget | target/attempt002.lean | d35c537d35bb12d63d2b338a7b8b8289129b4ae5 | 6275b20e7648c309e3e9c3f412e2bbedd4f801f95d4a2b1631c1d1f4ee9bc193 |
| Agent106CongruenceObstruction | obstruction/attempt-002/Agent106CongruenceObstruction.lean | 1a1d6060087f9ba596d686a1e8ec76f81c8f3475 | c8b4e1567f93e3b8769348b92b33a8e847e4e32440ec6bcc0905f16411d5fb93 |
| Agent106CongruenceControls | controls/attempt002.lean | c95c7591e6363d6671818b208e442bf18da97929 | 6ef0f20a8a18a0f35264d0007a735aa99b45e0e0f93de1ff865ad708d6cd31f0 |

All paths in the successful-snapshot column are relative to
`proofs/contributions/agent-106/congruence-carry-budget-20261016T2131Z/development/`.
Final modules live at `proofs/<Module>.lean`.

The exact six-module project import closure is:

| Module | Direct imports |
| --- | --- |
| LychrelDigitSums | Std |
| Agent106CarryBudget | LychrelDigitSums |
| Agent106CongruenceSeed | LychrelDigitSums |
| Agent106SparseTarget | LychrelDigitSums |
| Agent106CongruenceObstruction | Agent106CarryBudget, Agent106CongruenceSeed, Agent106SparseTarget |
| Agent106CongruenceControls | Agent106CongruenceObstruction |

The foundation is existing repository source
`proofs/LychrelDigitSums__bf5247272a7e3b69.lean`, staged under the original module name `LychrelDigitSums`. Its 218,799 bytes have Git blob
`8a865176625283648a8a20dd2411ed77670eb0a2` and SHA256
`ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.
The source at frozen H, the fetched exact blob, the recorded dependency hashes, and the independent build reviewer's fetched foundation agree. Its only direct import is `Std`; this closure does not need Mathlib or another project module.

The original written argument has Git blob
`fc8bef244f236095de36b9319f07147f23d41d1a`, 7,912 bytes, and SHA256
`fc166ae99053621e1e4fbf1ca88ede74ba8798bee1570cc326058d104e6ea710`, matching the contribution README.

The source contains exactly 36 named public theorems: CarryBudget 5, Seed 7, Target 6, Obstruction 6, Controls 12. Target's `rho_le` is the sixth theorem: it is covered by TargetAudit rather than its five explicit `#print axioms` lines. Definitions `rho`, `sparse`, `familyIndex`, `familyWidth`, and `familySource` are not added to the count of public theorems. All 36 fully qualified endpoint names are enumerated by module in the accompanying manifest and its proposed registry.

A comment/string-aware scan of every published Lean file finds no source occurrence of `sorry`, `admit`, `axiom`, `sorryAx`, `native_decide`, `ofReduceBool`, or `skipKernelTC`. This lexical check does not substitute for a fresh kernel build or dependency audit.

## All retained attempt and evidence records

### Budget

The sole budget source equals the final source. Its run.json source hash matches that source; its log hash matches the retained five endpoint axiom lines. The historical command explicitly includes `--trust=0 -j1 -DElab.async=false`, and its recorded exit status is zero. The run.json names author-session absolute paths and compiler hash; those are historical invocation claims, not a portable entrypoint.

### Seed

All four sources and all four compiler logs are present. Attempt 01 fails because a final omega runs after the width goal closes. Attempt 02 succeeds for three original endpoints. Attempt 03 adds reversal and fails at the unrestricted power rewrite. Attempt 04 restricts the intended rewrite and adds the first-step formula, becoming the exact final seven-endpoint source.

`verification-core.json` is a preserved historical result. Its source hash
`74bbd8f529c73c308240f4bc03d08147f2e4f5f561e255b03adc2df94c3b1bf5`
identifies `attempt-02.lean`, not the later bytes at its historical source pathname `proofs/Agent106CongruenceSeed.lean`. This is an honest earlier snapshot, not a failed final-source hash check. A new index should explicitly map it to attempt 02.

`verification-final.json` matches the final source and successful snapshot, its stated 8,384 source bytes, and its compile-04 log hash. The seven explicit endpoint reports contain only `propext` and `Quot.sound`. `base-build-01.log` contains **126 selected endpoint axiom reports**, not a complete 986-origin theorem audit.

The seed README correctly calls these author development checks and disclaims independent semantic review and a whole-repository audit.

### Target

Both failed and successful sources, both logs and manifests, `compiled-core.json`, `TargetAudit.lean`, and `target-audit.log` are present. Attempt 001's `decide +kernel` does not reduce the boundary assertion. Attempt 002 uses the existing digit-sum equation at the exact boundary numeral; it is the final source.

All source and foundation hashes in the target JSON files match the retained bytes. TargetAudit checks the two definitions and six public theorems, but its origin selection is **Target only**. The retained audit log has exactly 27 distinct `AUDIT_THEOREM` rows, including generated/private helpers, and its summary union is `Quot.sound, propext`.

The separate scalar-only log has a provenance gap, discussed below. It must not be used as evidence that a complete final module or closure was checked.

### Obstruction

Both exact sources, both compiler logs and both run.json files are present. Attempt 001 fails because `familyWidth` was unfolded in a hypothesis but not in the goal. Attempt 002 changes that unfolding and equals the final source. Both source hashes and both log hashes match. The failed run records exit 1 and the successful run exit 0. The final six endpoint reports contain only the three allowed logical axioms.

### Controls

Both attempt sources, manifests, result JSON files and logs are present, along with `AUTHOR_REVIEW.md`, `compiled-core.json`, `ControlsAudit.lean`, `controls-audit-result.json`, and `controls-audit.log`.

Attempt 001 preserves two successor/addition normalization errors and a redundant decide. Attempt 002 equals the final source. Its successful stdout log is a genuine **zero-byte blob**
`e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
An empty log here is not a missing file: the result JSON records zero exit and an empty output string.

All three result JSON output strings exactly equal their companion raw log bytes: failed compile, successful compile, and controls audit. The compiled-core source blob/hash and all five dependency source hashes map to the exact final closure.

ControlsAudit selects **Controls origin only**, checks its 12 public endpoints, rejects non-unsafe axiom declarations, and audits theorem dependencies. The retained log has exactly 37 distinct origin-theorem rows and the allowed three-axiom union. This proves consistency of the published audit transcript with its stated scope; static inspection cannot independently authenticate that historical execution.

### Failed logs remain evidence

Error-recovery `sorryAx` appears only in retained failed logs for seed attempt 03, target attempt 001, and obstruction attempt 001. Those failures are preserved and distinguishable from the successful source snapshots. Do not delete them, relabel them as accepted proofs, or feed every archived attempt into the accepted replay. A whole-directory glob build would be inappropriate for this package.

## Precise gaps and required disposition

### 1. Final portable replay and scoped registry are absent: mandatory delivery repair

None of the 50 changed paths provides a portable replay script, an explicit accepted/candidate registry for this package, or a final six-source execution receipt. Historical commands use author-specific `/workspace/scratch/336e9413679a/...` and `/tmp/p196-agent105-toolchain/...` paths and previously populated LEAN_PATH directories. They cannot by themselves certify a clean reconstruction by another reader.

The README explicitly leaves portable replay and final independent review pending. It does not falsely claim that the final delivery is complete; nevertheless, completion requires additive evidence and a working entrypoint.

### 2. README's historical independent audits are not published here: mandatory final-evidence repair

README blob `6e489c6173ec58b1b8383e50946dac496a5050f2` states that `/root/runtime_audit` completed a fresh core build with 1,089 theorem constants and a foundation audit of 986 constants. The 50-file publication contains no corresponding independent full-origin audit source, raw audit output, or source-bound execution receipt. The foundation compiler print log cannot establish that stronger claim.

Status of the historical execution is **UNKNOWN**, not disproved. Preserve the README as a historical snapshot. Add a new final independent six-source build and audit receipt, plus a scoped delivery README that identifies what has now been verified. Do not automatically add 37 to 1,089 and call that a measured final count: record the count actually observed by the final audit, since generated theorem origins may depend on which modules are imported.

### 3. Scalar-only source is unrecorded: historical limitation, not a final theorem blocker

Affected path:
`proofs/contributions/agent-106/congruence-carry-budget-20261016T2131Z/development/target/scalar-attempt001.log`.
Git blob: `0d7b3f1f5fa20a46e5a761e1e6c905bfe254abb2`.
SHA256: `998a42dc5e581fc1a9bb4ba8595cb03e97502233d5594422dc49e4bde223bac0`.

Its complete original content is:

```text
'Agent106.CongruenceBudget.sparse_tail_bound' depends on axioms: [propext, Quot.sound]
```

The target attempt001 manifest states that the full module is waiting for the foundation and an independent scalar exponential bound has already compiled. It gives the **full failed-module source hash**, not the scalar-only source hash. There is no scalar-only source pathname, command, exit receipt, or source hash in the published files.

The known author workspace `/workspace/scratch/336e9413679a`, including the recorded repository and target build paths, does not exist in this session. Exact path history identifies introduction commit `2085103344800254e6d05d6c52e4a850a6246f26`, whose changed-file list adds the scalar log but no scalar-only source. No exact scalar source was recoverable from these narrowly examined locations. This does not prove it never existed elsewhere.

Keep this log and label the scalar experiment **UNRECONSTRUCTED / NOT USED FOR FINAL ACCEPTANCE**. Recovery from an authoritative author record would improve historical completeness. Copying the later sparse_tail_bound proof and inventing a scalar wrapper would not recover the old evidence. A successful fresh build of the final module establishes the needed theorem independently of this old scalar experiment.

### 4. Historical compiler execution identity remains a historical assertion

The three budget/obstruction run.json files record compiler SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
That value is not a published source/log artifact. I did not reconstruct that historical runtime or claim it was used. New receipts must pin the actually observed official Lean 4.19.0 version/commit, executable and relevant runtime hashes, and actual argv. Archiving a compiler binary in the contribution is not required.

## Existing build convention and its limits

I inspected `proofs/ACCEPTED_BUILD.json`, exact blob
`90221ac6053b5584602fed24eb93f7984359dff5`, SHA256
`241a659b1e77ac1c17fb404c6dccaa8e0f03ebc322efd1f4553b2b8be646cebd`,
with source metadata and checker files at current-main context snapshot
`cc3de9834bef628d1083ce637641f07ed3953b13`.

The registry uses schema_version 1, an ordered three-axiom policy, explicit projects/modules/roots, and explicit claim endpoints. Its catalogue_complete is false; it explicitly distinguishes scoped acceptance from repository-wide completeness. It contains no Agent106 carry-budget module or claim. That omission does not require a new all-main build or a global registry rewrite.

`proofs/SOURCE_MAP.json` maps the real project verifier to
`proofs/verify_project__214bf7673efe116b.py`, blob
`21131b03dfa516eb19a0a7a4df4f2a41020d4db1`, SHA256
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
It supports `--registry`, `--project`, `--lean`, `--output`, and `--check-only`, verifies exact source hashes and imports, stages explicit modules, rejects pre-existing output, and audits the selected module origin closure.

**The inspected verifier hardcodes `-j1 -DElab.async=false` for compilation and audit. It does not pass `--trust=0`, and it does not consume registry compiler_arguments to construct those commands.** Merely putting trust-zero in a registry or README does not make this checker a trust-zero execution. A new Agent30-owned replay may explicitly implement those flags; no existing checker or global registry needs modification.

The `proofs/verify_release.py` wrapper replays original mapped layout. The mapped real release checker is
`proofs/verify_release__e7d6c74ed54123df.py`, blob
`28a44124dc15d53d1a3a493daad1459ba8e10a71`.
It checks publication byte coverage and import source presence and explicitly reports mathematical_proof_check false. It is not an accepted-proof compiler and is not a reason to undertake an unrelated archive census for PR106.

## Minimal additive repair

Use only the separately claimed Agent30-owned directory:

`proofs/contributions/agent-30/pr106-integration-20261016/`

Recommended files:

- `REGISTRY.json`: the complete six-source map, single Controls root, five endpoint groups containing all 36 public theorems, toolchain policy, frozen H, and exact restricted scope.
- `replay.py`: portable standard-library-only replay taking an explicit repository root, Lean executable, registry, and new output path.
- `README.md`: exact commands, scope, source identity, final evidence links, and the historical gaps above.
- `PACKAGE_REVIEW.md` and `PACKAGE_MANIFEST.json`: preserve this independently authored review and complete 50-file inventory.
- `independent-build/` and `parent-replay/`: immutable source-bound receipts, raw compiler/audit logs, audit source, toolchain identity, and per-file hashes from actual runs.
- `INTEGRATION_RECEIPT.json`: parent's actual current-base, frozen-source, combined-tree, source-closure equality, review, and eventual merge identities.

The accompanying manifest contains an exact `suggested_registry` object conforming to the inspected schema: `schema_version`, `toolchain`, `catalogue_complete`, `catalogue_blockers`, `projects`, and `claims` are populated with concrete values. Project key is `agent30-pr106-carry-budget`. The single root `Agent106CongruenceControls` reaches all six modules. Each module record has `path`, `sha256`, `git_blob`, and exact `imports`. Each claim has `project`, `module`, `scope`, and qualified `endpoints`. This is a proposed source registry, not a declaration that pending verification has passed.

The replay must check both SHA256 and Git blob identity; validate exact direct imports and closure; stage only those six sources into a genuinely new directory; rebuild all six project modules including the foundation with `--trust=0 -j1 -DElab.async=false`; exclude existing project objects from LEAN_PATH; and audit every theorem constant originating in the six modules, including private and generated helpers. It must reject logical axiom declarations and any theorem dependency outside the allowed standard three, while explicitly classifying unsafe implementation placeholders separately.

Preserve raw stdout/stderr, real commands, exit codes, audit script bytes/hash, per-module counts and full axiom reports, all source hashes and copied-source hashes, runtime version/hashes, timestamps, and errors. Rehash source and toolchain inputs after execution. Refuse to overwrite an earlier output directory. A failed run remains recorded; it must not be replaced by a successful run under the same receipt name.

Fresh complete runtime verification, independent semantic review, exact combined-tree preservation, and formal source-specific review are mandatory acceptance gates owned by their assigned reviewers/parent. Rebuilding unrelated accepted packages, fixing the global catalogue, rewriting old author documents, reconstructing undocumented scalar provenance, or modifying global accepted registries are not prerequisites created by this packaging audit.

## Scope and current review state

The publication consistently retains the distinction between a single congruence-compatible artificial entry edge and an actual ordinary-integer reverse-and-add step. The carry budget is universal over natural numbers. The entry obstruction is stated for R >= 3, with R = 3 treated explicitly. The residue/growth/width controls use R >= 2. It does not formalize a complete artificial path, exclude every possible repaired countermodel, establish an infinite actual orbit, or settle 196.

The contribution README's continuation list is partly stale because controls and a reviewable PR now exist. Preserve that author checkpoint; the new scoped delivery README should give the actual completion state without editing the frozen sources.

At my PR readback, H remained frozen, the PR was open, and there were zero issue comments, zero inline review comments, and zero formal reviews. PR base metadata reported `0f6a9172ad3ea82c77a6d67e757d9c64699f546a`; my separately read main context snapshot was `cc3de9834bef628d1083ce637641f07ed3953b13`. These are distinct observations, and no temporal movement is inferred from their difference. The parent must bind the eventual integration to its actual refreshed current-main and combined-tree evidence.

**Final status of this review:** all 50 published files inspected and byte-verified; no final-source or recorded source/log hash mismatch found; original failed attempts preserved; exact 36-endpoint/six-source scope mapped; additive delivery repair required; runtime, semantic, and integration acceptance not claimed by this auditor.
