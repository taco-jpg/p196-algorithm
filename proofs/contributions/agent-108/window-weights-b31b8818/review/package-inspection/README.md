# Agent #108 repository build-entry review

This is a read-only packaging review, not a new mathematical proof result and not a fresh 17-module compilation receipt.

## Conclusion

At inspected main commit `3a405f49b391a91d8fc5cb3182487d34e818acad`, all seven exact Agent #13 dependency sources required by the frozen window-weight proof are present in the repository. Their Git blob identities match the original reviewed commit `12a32789056f5eec8247166564ac2ef745c3c9d6`. Five sources have flattened filenames, and `FiniteWords` / `FamilyStates` are in retained version archives. Their unchanged bare imports therefore require a source-pinned materializer that copies the seven verified files to their original module names in a fresh build directory.

The current general verifier does not select or build the new window modules. A self-contained package runner with an explicit reproduction command is the minimal faithful build entry. Its PASS must be described as the window-weight package's 17-module result. It is not a repository-wide result or an extension of the existing 38-module core's PASS. Registering a new Mathlib project in the global verifier would require a separate explicit change to that verifier, its source mapping, and its registry.

## Exact observations

- GitHub `refs/heads/main` was pinned before inspection. Root and `proofs/` nonrecursive trees have no `lakefile` or `lean-toolchain`; the proof tree has 2,613 entries and is not truncated.
- `proofs/verify_project.py` and `proofs/verify_release.py` are 174-byte wrappers around `replay_original_layout.py`. Their current Git blobs are `aefba7a0d80643342b0128f32a0cf038d9b12c96` and `3824235f83b037503a178e94b3d50a1a9300e14a`.
- `replay_original_layout.py` has Git blob `4745990a5477a4b6a5c537b368bf78d214ce2622`. It reconstructs only the fixed `SOURCE_MAP.json` paths in an isolated Git work directory and verifies their pinned SHA256 values.
- The source map has base `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5` and 9,161 paths. It has no `Agent108Window` entry and no original `folded-product-weights/FiniteWords.lean` or `FamilyStates.lean` entry.
- Restored verifier source `verify_project__214bf7673efe116b.py`, blob `21131b03dfa516eb19a0a7a4df4f2a41020d4db1`, rejects unregistered external imports except `Init`, `Std`, and `Lean`. It has no Mathlib support.
- `ACCEPTED_BUILD.json`, blob `90221ac6053b5584602fed24eb93f7984359dff5`, sets `catalogue_complete` to false and contains only `consolidation-core`, with 38 modules and five roots. `CONSOLIDATION.md` explicitly distinguishes that core from source-specific reproductions outside its scope.
- The current workflows tree is byte-identical to the inspected baseline workflows. Existing Agent #108 workflows target the old modular-autonomy and criterion-review paths, not this window-weight package. The core workflow targets its old fixed source and branch. No current workflow names the new window modules or this package.
- The old top-level `proofs/REPRODUCE.md` is itself pinned by `SOURCE_MAP.json`. Changing it without synchronizing that source map would make the old replay reject the modified bytes. A new package-local reproduction file and a new top-level package notice avoid altering the old pinned build scope.

## Minimal reproducible package requirements

1. Read the seven original files from their retained repository paths and the ten frozen new files from `proofs/`. Verify SHA256 and Git blob values before materializing any source. Preserve source bytes without import edits.
2. Copy those 17 sources into a new, initially empty build directory under their exact module names. Compile in the recorded dependency order. No original project `.olean` may be imported from the session cache.
3. Require the official Lean 4.19.0 release, commit `6caaee842e94`, and the exact Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Verify Mathlib's manifest, toolchain file, and all eight dependency revisions. Document public dependency installation and the selected official cache command. Reusing that pinned external Mathlib cache must be disclosed separately from rebuilding the 17 project sources.
4. Construct `LEAN_PATH` explicitly from the fresh project build directory and the verified Mathlib / pinned dependency library directories. Do not inherit unrelated project paths or discover source copies outside the repository.
5. Compile every project source with `--trust=0`, record the exact command, exit code and logs, and stop on a failed module. The final complete fresh run is owned by the parent agent to avoid simultaneous heavy `LychrelDigitSums` compilation.
6. Select declarations by the exact 17 defining module origins. Record unsafe/partial compiler metadata separately. Print and check transitive axioms for every safe, nonpartial declaration, including private declarations and safe generated helpers. The logical allowlist remains exactly `propext`, `Classical.choice`, and `Quot.sound`.
7. Preserve source-to-declaration correspondence for the ten new modules and verify that source bytes did not change during the run. Report 17-source compilation and complete module-origin audit separately from the earlier ten-source rebuild using restored original `.olean` files.

The exact path / hash / dependency data are in `package-input-map.json`; compact current-main connector metadata are in `current-main-verified-tree-excerpt.json`. These are review inputs for the package author, not a replacement for the final runner's independent measurements.

## Reused review method

The tested literal-axiom audit source is `proofs/contributions/agent-108/window-weights-b31b8818/review/independent-window-incoming/attempts/001/WindowModuleAxioms.lean`. Its earlier complete ten-module audit and semantic review are recorded in that review directory. For the package run, the audit selector must cover all seven original modules as well as all ten new modules. Filtering only public namespaces would miss private declarations and specializations.

The runtime delegate authored `Agent108WindowObstruction` and `Agent108WindowEmbedding` and independently reviewed the final `Agent108WindowIncoming` source. This packaging inspection has not changed any mathematical source, shared registry, repository Git metadata, or remote object.
