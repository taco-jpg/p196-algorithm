# Independent WholeWordBridge execution review

**Frozen preparation checkpoint: PREPARED_NOT_EXECUTED.** No Lean compiler or heavy computation has run for this review. The two compiler slots remain reserved by the independent 739 rebuild. This checkpoint is not a fresh-build PASS, a new mathematical result, or a P196 claim.

The immutable source pin is `4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7`. The local working HEAD differs from that source pin, so the runner extracts source bytes with `git show <pin>:<path>` and never substitutes working-tree files or a later remote HEAD. It makes no Git changes. `source-pins.json` gives exact Git blob identities, SHA-256 hashes, source sizes, direct imports, and explicit theorem counts.

The complete local closure consists of `LychrelDigitSums`, `PrefixModel`, `SaturationCertificate`, `SaturationTheorem`, and `WholeWordBridge`: 258,494 bytes and 330 explicit theorem declarations. The only nonlocal direct imports are official `Std` and `Lean.Elab.Tactic.Omega`. Comment/string-aware inspection found no custom axiom, sorry/admit, native evaluator shortcut, unsafe metaprogram, external implementation substitution, or kernel-check bypass. The generated audit metaprogram is separate review infrastructure and is not an imported theorem source.

`historical-evidence.json` pins the already published logs, audit checker, and relevant publication instructions. Those historical checks are not counted as independent execution here. They audit explicitly named supplied theorems; the new execution will enumerate all theorem constants in all five local compiled modules, including private/generated theorems, and check their complete transitive axiom sets using official `#print axioms`. Only `propext`, `Classical.choice`, and `Quot.sound` are permitted. Compiler-generated unsafe implementation axiom declarations are recorded separately and may not occur transitively in any accepted theorem. Any custom safe axiom is rejected.

Official Lean 4.19.0 toolchain provenance is inherited from the explicitly pinned `seven-column-kernel/review-final-clean/preflight-01` evidence. That published preflight matched 1,476 compiler/shared-library/standard-object members to the official release archive with SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`. This review claims no new independent archive download. When authorized, it will verify the exact version `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`, recheck the compiler and inspected compatibility-wrapper/shim pins, and hash every imported official object against the inherited official manifest. The wrapper only preloads the documented current-process `/proc/<pid>/exe` to `/proc/self/exe` readlink compatibility shim. No inherited `LD_PRELOAD` or `LD_LIBRARY_PATH` override is present.

The prepared build directory is `/workspace/scratch/7649db1e242c/build104-agent4-whole-word`, outside the repository. It contains only the five pinned `.lean` sources. The runner refuses any directory with pre-existing local `.olean` objects. Every local source is compiled afresh with one compiler, `-j1 -DElab.async=false`, and no imposed memory/time cap. Every compiler/audit exit status, full output, resource use, source/object/compiler hash, and failure will be retained. The sources must still match the immutable Git blobs at completion.

Preparation command (performs no compiler invocation):

```sh
python3 proofs/contributions/agent-104/review-agent4-whole-word/execution/rebuild.py \
  --repo /workspace/scratch/7649db1e242c/p196-agent104 \
  --build /workspace/scratch/7649db1e242c/build104-agent4-whole-word \
  --evidence /workspace/scratch/7649db1e242c/p196-agent104/proofs/contributions/agent-104/review-agent4-whole-word/execution \
  --lean /workspace/scratch/7649db1e242c/toolchain/lean
```

After the coordinator grants a compiler slot, append `--execute --slot-authorization '<exact grant>'`. A replay after the first execution must use a new build directory and a new evidence directory; failed or completed attempts are never overwritten. The runner's fixed source pin and source mapping remain unchanged.

`preflight-exclusions.tsv` inventories all five duplicate source snapshots by exact path, size, hash, and retained original. They are excluded from publication because the immutable original source bytes are already published. No substantive original source, attempt, log, or result is omitted. `preflight-manifest.sha256` freezes the current evidence files, excluding itself. Compilation products and the audit's duplicate build copy will receive their own exact exclusion inventory after execution.
