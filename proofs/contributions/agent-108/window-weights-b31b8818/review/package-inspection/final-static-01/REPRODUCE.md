# Reproduce the finite-window weight obstruction

This directory has its own reproducible build entry: **`check.py` with the adjacent `source-pins.json`**. It checks the 17-module import closure of `Agent108WindowIncoming`: seven existing modules and ten new `Agent108Window` modules. It does not use the repository's general `verify_project.py` source selection. The inspected general verifier and its fixed source map do not register this Mathlib package.

The checker reads every project source from a repository-relative pinned path, verifies its byte length, SHA256, and Git blob SHA-1, and copies those exact bytes to a new evidence directory under the original bare module names. It preserves all imports. It compiles all 17 project modules sequentially with:

```text
--trust=0 -j1 -DElab.async=false
```

The project build directory starts empty. No previously compiled project `.olean` is used. The Lean distribution and the prepared Mathlib dependency caches are external prerequisites; their scope is described below.

## 1. Prerequisites

Use Python 3.10 or later, Git, and the official Lean **4.19.0** release whose version output contains commit **`6caaee842e94`**. Pass the actual release binary in `bin/lean`, rather than an elan shim or a session wrapper. The checker derives `LEAN_SYSROOT` from that binary's installation directory and verifies that the matching `lib/lean/Init.olean` exists.

Start with a repository checkout containing this contribution, all ten `proofs/Agent108Window*.lean` sources, and the seven retained original paths in `source-pins.json`. A sparse checkout must materialize those seven paths before running. The checker does not retrieve missing files or search another checkout for substitutes.

The required Mathlib source revision is:

```text
c44e0c8ee63ca166450922a373c7409c5d26b00b
```

The exact dependency source pins are:

| Package | Git revision |
| --- | --- |
| plausible | `77e08eddc486491d7b9e470926b3dbe50319451a` |
| LeanSearchClient | `25078369972d295301f5a1e53c3e5850cf6d9d4c` |
| importGraph | `e6a9f0f5ee3ccf7443a0070f92b62f8db12ae82b` |
| proofwidgets | `c4919189477c3221e6a204008998b0d724f49904` |
| aesop | `5d50b08dedd7d69b3d9b3176e0d58a23af228884` |
| Qq | `fa4f7f15d97591a9cf3aa7724ba371c7fc6dda02` |
| batteries | `f5d04a9c4973d401c8c92500711518f7c656f034` |
| Cli | `02dbd02bc00ec4916e99b04b2245b30200e200d0` |

Their upstream URLs are pinned in the JSON file. A full run checks Mathlib and all eight package Git HEADs and rejects tracked source changes. It also verifies these exact file hashes:

| Mathlib file | SHA256 |
| --- | --- |
| `lake-manifest.json` | `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752` |
| `lean-toolchain` | `55e97be96000b5e9e290c9e74482e5e317861499a5540353ce845471bded8cea` |

### Prepare the public Mathlib cache

If the pinned Mathlib checkout and its caches already exist, use them directly. To prepare a new dependency checkout, choose new absolute paths for `task_mathlib` and the installed Lean release directory. These commands are dependency setup, outside the checker:

```bash
task_toolchain=/absolute/path/to/lean-4.19.0-linux
task_mathlib=/absolute/path/to/mathlib4-window-weights

git clone https://github.com/leanprover-community/mathlib4.git "$task_mathlib"
git -C "$task_mathlib" checkout --detach c44e0c8ee63ca166450922a373c7409c5d26b00b

(
  cd "$task_mathlib"
  export PATH="$task_toolchain/bin:$PATH"
  export LEAN_SYSROOT="$task_toolchain"
  "$task_toolchain/bin/lake" exe cache get \
    Mathlib/Data/Real/Sqrt.lean \
    Mathlib/Algebra/Order/BigOperators/Group/Finset.lean \
    Mathlib/Algebra/BigOperators/Ring/Finset.lean \
    Mathlib/Tactic/Linarith.lean \
    Mathlib/Tactic/NormNum.lean \
    Mathlib/Data/Real/Basic.lean \
    Mathlib/Tactic/Ring.lean \
    Mathlib/Data/Real/Archimedean.lean \
    Mathlib/Algebra/BigOperators/Group/List/Basic.lean \
    Mathlib/Algebra/Order/Field/Power.lean \
    Mathlib/Data/List/Nodup.lean
)
```

These are the eleven distinct direct Mathlib imports in the pinned project closure. At the pinned revision, the official cache tool accepts a list of files and obtains their transitive imports; this behavior is specified in [Mathlib's pinned cache command source](https://github.com/leanprover-community/mathlib4/blob/c44e0c8ee63ca166450922a373c7409c5d26b00b/Cache/Main.lean). Its [pinned README](https://github.com/leanprover-community/mathlib4/blob/c44e0c8ee63ca166450922a373c7409c5d26b00b/README.md) describes the compiled cache maintained by the Mathlib workflow. Do not run `lake update` to select newer revisions: the checked-in manifest is part of this reproduction.

All eight dependency source checkouts must be present and pinned. An unused dependency can have no compiled library directory after selective cache retrieval; the observed `Cli` checkout is such a case. The checker records absent cache directories, uses only existing libraries from those eight pinned locations, verifies each direct external import is available, and lets Lean reject any missing transitive import. It never adds an unrelated library directory as a fallback.

This is a complete rebuild of the **17 project sources**, with existing external Mathlib and toolchain `.olean` files. It is not a source rebuild of Mathlib, its packages, or Lean. The evidence records the external source pins, direct imported object locations, and a cache inventory of paths and sizes. It does not claim to establish the source-to-object derivation of the external cache.

## 2. Read-only input check

From the repository root:

```bash
python3 proofs/contributions/agent-108/window-weights-b31b8818/check.py \
  --repo-root "$PWD" \
  --check-inputs
```

This mode is pure Python: it makes no Lean or Git subprocess call, creates no evidence directory, and changes no file. It checks the pin schema, source hashes and Git blob identities, exact direct imports, topological order, complete 17-module root closure, and the supplementary explicit declaration inventory. Optionally supply `--mathlib-root` to check its manifest and toolchain bytes too.

Its successful status is **`INPUTS_VERIFIED_ONLY`**. That status is not a proof compilation or an axiom-audit result.

## 3. Full reproduction command

Choose a new, nonexistent evidence path. The checker refuses to reuse or erase an existing one.

```bash
task_repo="$PWD"
task_toolchain=/absolute/path/to/lean-4.19.0-linux
task_mathlib=/absolute/path/to/mathlib4-window-weights
task_evidence=/absolute/path/to/window-weights-evidence/run-001

python3 "$task_repo/proofs/contributions/agent-108/window-weights-b31b8818/check.py" \
  --repo-root "$task_repo" \
  --lean "$task_toolchain/bin/lean" \
  --mathlib-root "$task_mathlib" \
  --evidence "$task_evidence"
```

No session path, wrapper, object cache for the original project, or parent agent workspace is required. All project sources come from `--repo-root`. The default repository root is derived from the installed location of this contribution. If `--evidence` is omitted, a unique timestamped directory is created under this contribution's `reproduction/` directory. `--timeout-seconds` sets the timeout per command; its default is 3,600 seconds.

The checker replaces inherited `LEAN_PATH` with the fresh project build directory followed by Mathlib and the existing libraries of the eight pinned packages. It clears `LEAN_SRC_PATH`, sets `LEAN_SYSROOT` to the supplied release, and runs only one compiler process at a time. Each compilation and the final generated audit use the three flags shown above. The long `LychrelDigitSums` compilation is included, rather than supplied by an earlier project cache.

A process exit of zero and `verification.json` containing `"status": "PASS"` establish a successful run of this scoped checker. Any source mismatch, unavailable dependency, failed command, unmatched declaration, missing axiom report, or forbidden logical axiom makes the run fail. Logs and partial evidence remain available. If failure happens before an evidence directory is created, the input diagnostic is printed to standard error.

## 4. Source identity and build order

The original seven sources were first reviewed at commit `12a32789056f5eec8247166564ac2ef745c3c9d6`. Their retained paths were independently checked at main commit `3a405f49b391a91d8fc5cb3182487d34e818acad`; each retained Git blob is identical to the reviewed original. The JSON manifest records both original and retained paths and full hashes. Later commits can reproduce the result as long as every pinned byte is preserved.

| Order | Bare module | Explicit source declarations |
| --- | --- | ---: |
| 1 | `LychrelDigitSums` | 362 |
| 2 | `Trace` | 15 |
| 3 | `WholeWord` | 17 |
| 4 | `Safety` | 12 |
| 5 | `Indexing` | 12 |
| 6 | `FiniteWords` | 21 |
| 7 | `FamilyStates` | 9 |
| 8 | `Agent108WindowDefs` | 9 |
| 9 | `Agent108WindowProducts` | 5 |
| 10 | `Agent108WindowEndpoints` | 3 |
| 11 | `Agent108WindowWeights` | 9 |
| 12 | `Agent108WindowFamilyProducts` | 9 |
| 13 | `Agent108WindowEndpointWeights` | 13 |
| 14 | `Agent108WindowObstruction` | 11 |
| 15 | `Agent108WindowEmbedding` | 41 |
| 16 | `Agent108WindowFamilyRatio` | 12 |
| 17 | `Agent108WindowIncoming` | 18 |
| **Total** | **7 original + 10 new modules** | **578** |

Five retained original files have flattened filenames such as `proofs/Trace__60a10db5d110fcab.lean`. `FiniteWords` and `FamilyStates` are under fixed `proofs/archive/versions/` paths. They are copied to `Trace.lean`, `FiniteWords.lean`, and their other bare module filenames **only inside the new evidence sources directory**. This restores the source modules' existing import names without modifying a mathematical source or duplicating them in the repository.

## 5. Complete module-origin axiom audit

The generated `WindowPackageAxioms.lean` imports `Agent108WindowIncoming` and Lean's environment API. It iterates the environment's constants and selects declarations using `Environment.getModuleIdxFor?` and `header.moduleNames`, restricted to the **exact 17 module names**. It does not infer coverage from namespaces or a public declaration regular expression.

For every selected origin it records the actual declaration name, module, declaration kind, and `isUnsafe`/`isPartial` metadata. For every declaration that is neither unsafe nor partial, it runs `#print axioms` between matching `AUDIT_BEGIN` and `AUDIT_END` markers. This includes private declarations and safe generated helpers, recursors, constructors, and specializations.

The parser requires one uniquely identified axiom report for every safe, nonpartial origin, verifies that the printed declaration name agrees with the marker, and rejects an omitted, duplicated, or unmatched report. The logical axiom allowlist is exactly:

```text
propext
Classical.choice
Quot.sound
```

Unsafe or partial compiler artifacts are listed separately. They are not counted as successful logical declarations or silently added to the allowlist. The complete per-module origin counts are measured from the actual final run. A preceding independent audit of the ten new modules observed 363 origins: 269 safe and nonpartial declarations, 90 unsafe declarations, and four partial declarations. That historical observation is a reference, not a substituted result for the new 17-module run.

As an additional cross-check, the checker strips nested Lean comments while preserving line numbers, tracks `namespace` and `section` scopes, and inventories named explicit source declarations, including indented and private ones. All 448 original and 130 new declarations must match a unique safe origin in their own module. Private names are matched to their actual environment names. This inventory is supplementary: the full logical audit also includes origin declarations generated by Lean that are absent from the source inventory.

### Correction to the earlier “112 declarations” record

The historical script in `review/independent-dependencies/build_independent.py` compiled ten older modules but built its explicit audit list with `for module in order[1:]`. It therefore did **not** enumerate `LychrelDigitSums` in that list. Its 112 selected declarations consist of:

| Historical selection | Count |
| --- | ---: |
| `Trace`, `WholeWord`, `Safety`, `Indexing`, `FiniteWords`, `FamilyStates` | 86 |
| Older `Products` | 12 |
| Older `Obstruction` | 6 |
| Older `CarryPath` | 8 |
| **Selected declarations** | **112** |

That script selected only column-zero public `def`, `theorem`, and `abbrev` lines and assigned one of three known Agent #13 namespaces. There is no indented declaration omitted within those nine selected modules, but its selection excludes the `CarryPath` inductive declaration and all generated declarations. `LychrelDigitSums` was compiled and emitted some source-internal axiom reports; the old list did not establish complete coverage of its definitions, theorems, structures, or generated declarations.

The original seven modules contain **448** named explicit declarations after comments are removed. `LychrelDigitSums` supplies 362: 63 definitions, 296 theorems, two structures, and one inductive declaration. An initial column-zero count of 447 across the seven files missed the indented `CarryNormalizationSharpness.witness_carries` theorem at source line 3289. It was a source-inventory omission, not a mathematical source change. The historical 112 observation and its literal logs remain unchanged; their coverage must not be described as a complete module-origin audit of the original dependencies. The old build command also did not explicitly request `--trust=0`; this checker does.

## 6. Evidence produced by a full run

The new evidence directory contains:

- `inputs/`: the exact checker, pin manifest, reproduction instructions, Mathlib manifest, and toolchain file used for the run.
- `sources/`: the 17 byte-identical project sources and the generated module-origin auditor.
- `build/`: only newly compiled project objects and the generated audit object.
- `logs/`: every command's literal standard output and standard error, including version and Git checks, all compiler invocations, and the complete axiom audit.
- `verification.json`: input source identities, source inventories, execution commands with times and exit codes, Lean version and binary hash, Mathlib and package Git revisions, object hashes, audit totals, and source/package consistency checks after the run.
- `axiom-audit.json`: all 17 modules' origin metadata, every safe declaration's transitive axioms, source-to-origin correspondence, separately classified unsafe/partial entries, and any unexpected axioms.
- `cache-inventory.json`: the paths and sizes of external cached `.olean` files in the explicitly admitted libraries.

Each `verification.json` is a receipt for its own run. Read-only prechecks and earlier modular reviews do not manufacture a successful full-run receipt. Reproduction also does not replace the mathematical semantic reviews: the endpoint truncation, finite-window factorization, actual safe-fiber embedding, and final incoming-weight theorem have their own fixed-source review records in this contribution.
