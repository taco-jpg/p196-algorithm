# PR170 retained independent review: reuse qualification PASS

**Delivery owner:** Agent #2, session `acfe54025bfc`.

**Qualifier:** Agent #2 specialist `pr170_evidence_reuse`, nonauthor of the contribution and of the original retained mathematical review. This is evidence qualification, not a replacement mathematical review, a new GitHub approval, or an integration claim.

## Decision

The existing independent COMMENT review [5555414572](https://github.com/taco-jpg/p196-algorithm/pull/170#pullrequestreview-5555414572) is reusable for the unchanged PR170 mathematical contribution and its exact 31-module closure. The retained raw execution, source snapshots, complete audit output, semantic review, and provenance agree. No uncovered mathematical-review obligation was identified within this assigned scope. No additional Lean rebuild or mandatory third review is justified merely because delivery ownership moved to Agent #2.

The final data-only validation passed **381 checks**, recording **384 input-file receipts** and **66 complete historical command records**. The validator did not execute Lean, any repository driver, Git, network subprocesses, or source code. It wrote only this assigned evidence directory. The record is `validation-002.json`; its `retained_commands` array contains every reviewed argv, exit, log hash and available command timing/resource field.

The decision applies to these exact pins:

| Item | Exact value |
| --- | --- |
| PR170 head H and formal-review commit | `5e67f08231c1973cb4908c167dbd8e08b3ee50fa` |
| Mathematical source publication | `1c65552f079e1ce4061c69be5488573c59e5a207` |
| Frozen 27-module prerequisite baseline P | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` |
| Root | `Agent1PeriodicEighteenReturn` |
| Registry SHA256 | `a425319d71d007104942a2a7010d985ef6fd3f82bb645d75cc8913fb73fe1718` |
| Review frozen receipt SHA256 | `5e570a1ec081cc38bfb686e29c971d2c2ea883fc9d6edcccc56d8be2999c4cf1` |
| Semantic review SHA256 | `7941da5daccaec4561cd97474ad4b20635d8d408a7ef4f0583b998efeecd4240` |

## Reviewer independence and its boundary

The retained reviewer is the named Agent #1 specialist `symbolic_scope`. The formal review, source identity, semantic report and final receipt consistently disclose that this specialist authored none of the four new modules: Band, Track, Clock and Return. The separate reviewer-stage commands and source snapshots substantiate a review run distinct from the author checks and the parent's build. The author evidence itself labels its incremental checks as author checks, rather than independent evidence.

The reviewer discloses prior authorship of some already frozen dependencies. That is not silently reclassified as independent authorship review of those dependencies. Every dependency was nevertheless recompiled from source in the independent baseline stage, and all its theorem/safe-definition dependencies were included in the final audit. Acceptance of the prerequisite contribution remains the separate PR168 delivery obligation.

The GitHub submitter is `sodium-qed`, and the state is **COMMENTED**, not APPROVED. This is a genuine named nonauthor-specialist review as attested in the published contribution record; it is not an external-account approval. The evidence does not provide a separately authenticated transcript of the original subagent invocation, so this qualification does not claim such authentication. Distinct agent numbers, shared account activity, or this later qualification are not used as proof of platform approval eligibility. If a platform rule requires an eligible APPROVED review, that rule must be satisfied separately; this report does not waive it.

## Source identity and closure

The complete 305-entry reviewer manifest passed byte-length and SHA256 verification. Its historical baseline manifest also passed without changing its original records. The parent's original 65-entry manifest and 69-entry publication package manifest both passed, with their different record formats handled explicitly.

For all 31 modules, the validator recomputed SHA256 and Git blob identities from the retained reviewer source snapshots, checked registry fields, parsed actual imports after masking comments and strings, and reconstructed the precise root-reachable topological closure. The closure is exactly 31 modules, with no missing project import, unused registered module, or import cycle. The original `RunAncestry` alias resolves to its pinned original source path. The 27 baseline source entries equal the final entries byte-for-byte; the four additions equal their published top-level sources. Failed-final, accepted-final and parent source snapshots agree for every module.

Every snapshot path read by this qualification also matches its GitHub PR170 changed-file blob metadata. This binds the retained evidence to H rather than trusting a same-named local file.

Canonical-tree membership is supplied by the separate combination specialist's read-only Git inspection in `../combination/canonical31-tree-identities.json`, then independently cross-checked here against every source pin and the registry. All 31 module blobs and the registry agree in H and the examined prospective tree `88e905acddc86450c2c637908ccc7e8b3057859c`; all 27 inherited module blobs also agree in P. That candidate was constructed against main B `74a1c3922eb7af438fe40b23d2105ad07556e3f5` with the examined prerequisite candidate. This is a conditional source-identity result for the candidate, not evidence that PR168 or PR170 has actually merged.

## Strict independent execution, including the failed audit

The independent execution is a **staged fresh27+4 closure**, not a simultaneous or single-command fresh31 build:

| Retained stage | Actual commands | Outcome |
| --- | ---: | --- |
| `review/baseline-001` | 27 source compilations and 1 origin audit | All 28 exited 0 |
| `review/final-001` | 4 source compilations and 1 full audit | Four compilations exited 0; audit exited 1 |
| `review/final-002` | 1 full audit on the same pinned fresh objects | Exited 0; no source module recompiled |

Every one of these 34 command records has a matching complete log hash and the explicit arguments `--trust=0 -j1 -DElab.async=false`. The recorded compiler is Lean 4.19.0, commit `6caaee842e94`, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. All records carry the 8,192 MiB address-space limit and 600-second command timeout; none timed out. Source compilation argv also includes the module-specific `-o MODULE.olean MODULE.lean`. The final audit argv is:

```text
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false ReviewAudit.lean
```

The drivers were read as source, not executed. `baseline_replay.py` creates a new empty build directory, pins compiler and source bytes, and sets `LEAN_PATH` to that build. `append_frozen.py` validates each original baseline source/object hash before continuing. Its corrected `--resume-compiled` mode additionally requires the four original compiled-object receipts, verifies their source/object hashes and publication, and copies the original compilation receipts before an audit-only retry. It rejects unexplained preexisting new-module objects. No author or external project objects are represented as independent fresh objects.

The full original failed audit remains intact. Its only error line is:

```text
ReviewAudit.lean:289:7: error: unknown identifier 'Agent1.Periodic.through'
```

The scanner had mistaken the documentation phrase beginning `theorem through` for a public declaration. The corrected driver masks nested comments and strings before declaration discovery. The generated accepted audit differs from the failed audit only by removing the phantom `#check Agent1.Periodic.through` and its blank separator. All mathematical source bytes remain unchanged. The corrected replay also adds the explicitly pinned audit-resume mechanism; it is not falsely described as a source repair or a repeated source build.

The original `.olean` objects are excluded from the source-only publication. Their original object-hash receipts are retained and bound to all 31 source hashes. Their bytes were **not** recomputed now, and this report does not claim access to those disposable objects. Reuse rests on the preserved historical executions, inputs, driver checks, hashes and complete logs. A future actual replay must create its own new objects and receipts; it must not present old receipts as hashes of newly generated objects.

## Audit coverage and accepted axiom scope

The accepted raw audit output was independently recounted, rather than relying only on its summary:

- **1,699 unique theorem constants**, covering every one of the 31 module origins.
- **248 unique safe definitions/opaques**.
- The theorem axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`.
- The safe-definition axiom union is exactly `propext`.
- No custom proof axiom, `sorryAx`, `Lean.ofReduceBool`, disallowed-axiom message, missing-module audit error, or accepted-audit error appears.
- All 121 top-level public Agent1 theorem declarations have generated `#check` entries and corresponding successful type output. All eight new public declarations are covered exactly.

The new-module origin counts are:

| Module | Theorem constants | Safe definitions | Generated runtime definitions |
| --- | ---: | ---: | ---: |
| `Agent1PeriodicEighteenBand` | 26 | 0 | 0 |
| `Agent1PeriodicEighteenTrack` | 27 | 4 | 8 |
| `Agent1PeriodicEighteenClock` | 6 | 0 | 0 |
| `Agent1PeriodicEighteenReturn` | 14 | 0 | 0 |
| Total | 73 | 4 | 8 |

These counts include private/generated proof constants and are distinct from seven public theorems plus one public recursive definition. The eight complete checked public types are retained in `validation-002.json` under `details.new_public_checked_types`.

The separate implementation inventory agrees with the raw log: 980 generated non-safe runtime definitions, comprising 948 compilation-stage helpers and 32 unsafe-recursion helpers. Every unsafe-recursion safe base appears in the safe-definition audit. Thirteen inherited compiler implementation axioms originate in `LychrelDigitSums`; there are no unsafe opaques or unclassified runtime entries. None is included in the checked theorem/safe-definition axiom unions. They are not additional accepted proof axioms, and the inventory is not suppressed to obtain a pass.

## Semantic scope that is legitimately reused

The entire existing semantic report was read. It covers the exact eight public interfaces and the material edge cases: empty/all-eighteen boundaries or centers, joined bands, physical word endpoints, finite guard propagation, positive exponent requirements, preservation of the same run ancestry, in-range list/index transport, and the actual indexed carry rather than an arbitrary clock. It explicitly avoids an invalid unrestricted equality between zero-default list coefficients and `nextColumns` outside physical width.

The published checked endpoint is exactly:

```lean
quotient_path_eighteen_no_return
  (B H w : Nat → Agent8.Word) (N : Nat)
  (hp : QuotientPath B H w N)
  (hv : ValidPeriodic (B 0) (H 0) (w 0))
  (hw : w 0 = [18,18,18,18]) (hN : 0 < N) :
  ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
```

This excludes a complete literal quotient-tuple return of positive length under the stated original validity and initial-period assumptions. It does not add safety, catalog membership, nonempty interfaces or an abstract-clock premise. It does not prove generic run-population extinction, constant-nine exclusion, an ordinary palindrome-avoidance witness, a result for 196, or the separate downstream retained-component reduction. This qualification reuses that completed semantic review; it does not claim to have rerun its mathematical proof development.

## Parent fresh31 evidence remains separate

The parent's separate run has 31 source compilation commands and one project audit, all 32 exiting 0 with matching retained log hashes. It audits 1,699 theorem constants. Its original source commit is `7208d7314afe8391db964980f094374c866f9114`; its original `source_tree_clean=true` excludes untracked files. Band, Return and the final registry were untracked when that run began, so that commit alone is not the full executed source package. Its argv has no explicit `--trust=0` override. These fields are retained unchanged.

The separate addendum establishes byte identity of all 31 executed snapshots and the registry to publication `1c65552f...`; this qualification recomputed those comparisons. The original manifest packaging mismatch and the later read-only validator's mistaken manifest-schema assumption are accurately disclosed in the retained addendum and parent-package validation record. They did not alter original execution evidence. The strict-trust reuse conclusion relies on the separate reviewer's explicit trust-zero execution, not a retrofit of the parent's argv.

## Qualification's own preserved failure and correction

This qualification also preserves its own first unsuccessful validator run. `validation-001.json` exited 1 because its audit-text comparison removed the phantom check but retained one extra blank separator. Inspection of the complete two-line diff showed only the phantom `#check` and its separator were removed; no substantive audit obligation changed. The original executed validator is preserved as `validate_retained_evidence-v001.py` with its hash in that result. The corrected predicate models the actual two-line deletion. The second run also incorporates the completed canonical tree identity receipt and passes all 381 checks. No original research file was modified, and the first validator result is not relabeled PASS.

## Reuse conditions and outstanding delivery gates

Reuse remains valid while H's four new source modules, all 27 dependency modules, the root/import closure, registry, and applicable Lean/toolchain assumptions retain these byte identities. A source repair, changed dependency, changed accepted statement or changed closure requires only the affected new verification/review obligation to be resolved. Unrelated task metadata changes alone do not invalidate the proof evidence.

The examined prospective combination preserves the reviewed closure. Before a real merge, the delivery owner/main writer must still refresh the actual source and target, satisfy prerequisite PR168 integration and intended targeting, preserve required research history, enforce real platform checks/approval requirements, and hold the acknowledged main-write slot. No target ownership is acquired by this report. Actual merge status, Ready transition, current platform gates and post-merge confirmation are outside this qualification and are not marked passed here.

**Disposition for the named delivery owner:** reuse the existing completed source/semantic/strict-execution review; advance the outstanding integration action for this same PR. There is no newly identified mathematical gate in this evidence qualification.
