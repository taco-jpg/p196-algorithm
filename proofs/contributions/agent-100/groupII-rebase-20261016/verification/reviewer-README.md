# Independent Group II Rebase verification

Status: **PASS — independent fresh canonical21 build plus explicit trust0 full-import audit.** All22 explicit new exports pass interpretation review and complete multiline axiom-list cross-check. All21 module compilations and original ProjectAudit exited0; the separate actual --trust=0 ProjectAudit over the same fresh imports also exited0. This is one fresh source build and one strict follow-up, not two fresh builds.

Historical reviewer: Agent #100 `scope_audit`, author of no Lean theorem in this task. Actual executors are supplied explicitly with `--executor` and recorded in each invocation. The unchanged canonical verifier's internal Agent #1 label is not the identity of the caller.

## Scope and immutable pins

- Claim commit `e1bc61f552413f4a1ed6cef86c88265d39fd896d`; task blob `a277d7843d3509cf60a581ce06fb8d451975bea3`.
- Actual run start HEAD, original worktree base and old18 mathematical package: `686cac2696e4e4e059c1b9d6a313f5519f6f4176`. Complete new mathematical source: `bc178ab8735e9503ab25b325e5a8dc82bf1f1e37`, tree `9c59d8266aeba792f7a376c83c6f72d9aee24e25`, Draft PR138. Independent git show reads verified all21 published source files against both local files and fresh snapshots.
- Root `Agent100GroupIIRebaseNumeric`; actual closure 21 modules, with 3 new modules and 22 explicit new theorem exports.
- Registry SHA256 `333da8a41b75cd1ac5c2f9f3a0d0a8c85d3dc02d870d04d5330ba57bd45a129c`.
- Official Lean 4.19.0, commit `6caaee842e94`; executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- Unchanged canonical verifier SHA256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
- Every local module is pinned by exact source SHA256, Git blob and actual imports in `reviewer-registry.json`. No author olean is used by the fresh canonical build.

The mathematical scope is UpperDomain (all `r >= 1`, `p = 5..9`, seven Group II cores), a signed correction to the actual time2 component, nonnegativity before `Int.toNat`, original Admissible, full actual time2 whole overlap, arbitrary original canonical whole-input realizations, and positive canonical realizability of the new component. The new component differs from the original actual component at a valid column; future/infinite behavior and multiplication relations between ordinary integers are outside the claim.

## Reproduce the three distinct stages

Use the source publication containing the pinned modules and provide the official Lean executable. Select output paths that do not already exist; earlier attempts must remain retained.

```sh
python proofs/contributions/agent-100/groupII-rebase-20261016/verification/reviewer-replay.py --lean /absolute/path/to/lean --output /absolute/path/to/new-canonical-run --executor "local operator"
python proofs/contributions/agent-100/groupII-rebase-20261016/verification/reviewer-extract-axiom-ledger.py --registry proofs/contributions/agent-100/groupII-rebase-20261016/verification/reviewer-registry.json --run /absolute/path/to/new-canonical-run --output /absolute/path/to/new-ledger.json --executor "local operator"
python proofs/contributions/agent-100/groupII-rebase-20261016/verification/reviewer-run-strict-import-audit.py --canonical-run /absolute/path/to/new-canonical-run --registry proofs/contributions/agent-100/groupII-rebase-20261016/verification/reviewer-registry.json --comparison-ledger /absolute/path/to/new-ledger.json --lean /absolute/path/to/lean --output /absolute/path/to/new-strict-audit --executor "local operator"
```

The first stage uses the unchanged canonical verifier to check every source identity and import, compile the entire closure fresh, check all 22 explicit endpoints and audit all theorem constants originating in the 21 selected modules. Its compiler arguments do **not** explicitly set `--trust=0` and must not be described as doing so.

The second stage parses complete balanced axiom brackets across line breaks, compares every explicit new endpoint's raw printed list with the full module-origin ledger, and separately checks the two inherited endpoints whose historical simplified ledgers were corrected. No old endpoint ledger is copied as current execution evidence.

The third stage executes the same generated `ProjectAudit.lean` with explicit `--trust=0 -j1 -DElab.async=false` over the first stage's freshly generated local modules. It records exact commands, executor, timing, exit status, full axiom names/sets and before/after source/olean hashes. This is an additional imported-module type-check, not a second fresh21 source build.

The actual complete theorem-axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`. The audit covers2661 theorem constants,85 in the three new modules including generated declarations. Of22 explicit new exports,14 use propext/Quot.sound and8 additionally use Classical.choice; exact names and full sets are retained. Fourteen inherited unsafe implementation declarations are separately reported and occur in no audited theorem dependency set. Both inherited corrected endpoints are confirmed with all three standard axioms.

## Evidence boundaries

The canonical run is retained under `reviewer-independent01`; complete raw build/audit logs remain unedited. Strict follow-up evidence is retained separately under `reviewer-strict01`. The actual run HEAD is686cac and the complete publication isbc178ab; `reviewer-post-build-source-identity.json` records all21 immutable source comparisons and strict source/olean posthash checks.

`../controls/reviewer-semantic-review.md/json` separates interpretation findings from execution status. `../controls/reviewer-controls-manifest.json` records the one independent finite diagnostic run (105 cases, 840 integer additions) and verified lossless compression of all rows. Those diagnostics are not Lean proofs and were not repeated.

No global accepted registry is modified. A scoped independent review is not repository-wide integration or a proof of infinite nonpalindromicity.

## Complete retained evidence archive

`reviewer-complete-evidence.tar.xz` retains complete canonical and strict raw logs/reports, all21 fresh source snapshots, the generated ProjectAudit, exact registry/replay/strict/parser scripts, real-executor receipts, full multiline axiom ledger, post-build source correspondence, final review documents, and all105 finite control rows with original source/log/data. Generated oleans and Python bytecode caches are excluded; no substantive raw log is omitted. All originals remain retained locally. `reviewer-evidence-archive-manifest.json` records stored/decoded hashes and every member identity. The archive was actually decompressed and every member compared byte-for-byte.
