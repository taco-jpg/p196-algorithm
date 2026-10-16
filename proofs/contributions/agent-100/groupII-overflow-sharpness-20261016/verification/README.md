# Independent verification of Group II overflow sharpness

Status: **PASS — INDEPENDENTLY-REVIEWED; fresh canonical18 plus explicit trust0 full-import audit.** All 52 new explicit exports passed interpretation review and one complete fresh 18-module build. All 19 commands exited 0; the full module-origin axiom audit covered 2,576 theorem constants, including 384 in the five new modules. The complete multiline axiom lists for all 52 explicit new exports agree with their full-module audit entries.

Executor: Agent #100 `scope_audit`, who authored no Lean theorem in this task. Profiles and Numeric were authored by the dynamics specialist; Bridge and Sharpness by the runtime specialist acting as a formalizer; Defect by the parent. Author development checks are retained separately and are not this independent execution.

## Exact scope and pins

- Root: `Agent100GroupIIOverflowNumeric`.
- Complete actual local import closure: 18 modules; five new modules with 52 explicit theorem exports.
- Registry SHA256: `ac68e397f5a12326ed7a788a0e021edda22be46216bcc98c5bc45f71933c6533`.
- Official Lean 4.19.0, commit `6caaee842e94`; executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- Unchanged canonical verifier `proofs/verify_project__214bf7673efe116b.py`, SHA256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
- Independent replay wrapper SHA256: `1709e3abff96fce7b94e5690804f844835916d6f1bcf89ece7c2037abb18771e`.
- Actual run source HEAD: `491b477889b6336f5386287e3665f6ce58a34d9b`. Original branch base: `d591ce6d0cbf2bceab219fe915b1cebcc16a5879`. Complete source publication: `686cac2696e4e4e059c1b9d6a313f5519f6f4176`, tree `6f25211e084ebee89ca964820e03258cd294b361`, Draft PR125. Every one of the 18 immutable published files was independently read with `git show` and compared byte-for-byte to both its fresh build snapshot and post-run local source; see `post-build-source-identity.json`.
- General defect transport remains unchanged from Agent #8 source commit `8874b2ee291dc7a253b3b89fbbf0efd86812ae4d`. The shared foundation is represented once in the closure, with source-identical bytes.

The canonical report's `source_commit` records the actual run HEAD `491b477...`, separately from the original branch base `d591ce6...`. Its `source_tree_clean` field ignores untracked files, so it must not be read as asserting that the newly added sources were part of that base commit. The registry and fresh source snapshot pin the actual sources checked.

## Reproduction

For a future reproduction, supply the official Lean executable, an output path that does not yet exist, and the actual operator identity:

```sh
python proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/verification/reproduce.py --lean /absolute/path/to/lean-4.19.0-linux/bin/lean --output /absolute/path/to/new-overflow-verification --executor 'Actual reproduction operator'
```

The wrapper verifies the frozen registry and unchanged verifier. The verifier then checks every source SHA256, Git blob, and actual import, copies the exact closure into the new directory, and recompiles all modules without author oleans. Its module-origin audit visits every theorem constant from the selected modules, including generated theorem declarations, and checks all 52 new explicit endpoints. It rejects disallowed source tokens and nonstandard theorem axioms. The actual complete theorem-axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`. Of the 52 new explicit exports, 51 use `propext` and `Quot.sound`; only `two_step_overlap_iff` additionally uses `Classical.choice`. Fourteen existing unsafe implementation declarations were separately classified, and no audited theorem depends on them. The two inherited corrected endpoints `returnedComponent_core_table` and `returnedComponent_not_same_shape` each have all three actual axioms. The new ledger parses complete balanced brackets across line breaks and checks printed endpoint lists against the complete fresh module-origin audit; it does not copy earlier simplified ledgers.

The actual historical run used `replay.py`; its `independent-invocation.json` identifies `scope_audit` for that original execution. The unchanged historical wrapper and extractor contain embedded executor labels, which do not identify a future reproduction operator. The additive `reproduce.py` records the supplied current operator separately, performs the canonical build and explicit trust-zero import audit, and preserves raw historical labels. See `REPRODUCE-NOTES.md`. The new launcher has passed static checks only; its complete future workflow has not been executed here. The canonical verifier's internal Agent #1 label is preserved unchanged and does not identify this run's executor.

## Retained evidence

- `independent01/`: complete fresh source snapshots, compiler logs, generated audit source, commands, exit statuses, source/compiler hashes, and final verification report; all compilation and audit commands completed with exit 0.
- `independent01-driver.log`: retained command-level build output.
- `complete-axiom-ledger.json`: complete multiline raw-log cross-check for all 52 new endpoints, both inherited corrected endpoints, and the full 2,576-theorem module-origin ledger.
- `extract_axiom_ledger.py`: standard-library-only reproducible balanced-bracket parser; `multiline-parser-control.json` records the concrete regression control for the earlier truncated-list risk.
- `post-build-source-identity.json`: post-run local/build-snapshot/immutable-publication byte equality for every source in the closure.
- `environment-startup-probes.json`: the default-sandbox compiler-startup failures and the successful approved expanded-environment version check. These were environment probes, not Lean proof attempts. The compiler and verifier bytes were unchanged.
- `../controls/overflow-semantic-review.md` and `.json`: complete independent interpretation review, kept separate from execution status.
- `../controls/compression-manifest.json`: verified lossless archives of all 420 finite diagnostics and the original ownership snapshots. Those finite experiments were not rerun and are not Lean proofs.

No global accepted build registry was changed. This is a scoped independent verification, not repository-wide integration or a proof of infinite nonpalindromicity.

## Axiom ledger reproduction

For the retained historical replay workflow, after a successful replay use a new output file. The future `reproduce.py` workflow already performs this extraction automatically under its `canonical/` run directory:

```sh
python proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/verification/extract_axiom_ledger.py --registry proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/verification/registry.json --run /absolute/path/to/new-overflow-verification --output /absolute/path/to/new-complete-axiom-ledger.json
```

## Complete portable evidence archive

`independent01-complete-evidence.tar.xz` retains all fresh source snapshots, complete raw logs, the generated audit, full verification report, real-executor receipt, full multiline axiom ledger, exact replay/registry/parser, environment probes, post-build immutable source comparison, and final semantic reviews. Only generated `.olean` files and Python bytecode caches are excluded; no raw mathematical or failure log is omitted. The original uncompressed records remain present locally. `independent01-archive-manifest.json` records every member hash plus stored and decoded archive hashes. The archive was actually decompressed and every member compared byte-for-byte to its original.

## Explicit trust-zero gate and retained amendment

The original 19 canonical commands did not contain `--trust=0`; that original fresh build is not being relabeled as an explicit trust-zero build. A distinct actual follow-up ran the same original `ProjectAudit.lean` with `--trust=0 -j1 -DElab.async=false` in `independent01/groupii-overflow/source`, with `LEAN_PATH` set to that exact fresh directory. The command exited 0 after typechecking all imported modules and repeating the complete module-origin audit. All 2,576 theorem names and full axiom sets, all 52 checked new endpoints, and all source/fresh-olean post-hashes agree. This is **one fresh 18-source build plus one strict import audit**, not a second fresh18 build.

`strict01/ProjectAudit-trust0.log`, `strict01/strict-import-verification.json`, `strict01-driver.log`, and `run_strict_import_audit.py` retain the full command, explicit executor, timing, exit status, complete axiom ledger and before/after identities. The original `independent01-complete-evidence.tar.xz` remains byte-identical at SHA256 `b371c559c185f1cf28e621633a0c87a04b5e9d193801839f16255fa8fccd0e5a`; it is preserved as historical canonical evidence. `strict01-evidence-amendment.tar.xz` contains the new strict evidence and the updated interpretation documents, with a separate per-member manifest and verified decompression. No original mathematical source or original execution record was rewritten.
