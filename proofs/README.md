# Current research entry point

Current sources live directly in this directory or in the separately integrated
contribution packages. Historical originals retain their source identities and
evidence labels. A historical tree is not the current proof, and a timestamp is
not evidence of validity.

[Results directory](RESULTS.md) · [Status](STATUS.md) · [Open problems](OPEN_PROBLEMS.md) · [Historical source mapping](SOURCE_MAP.json)

## Verify registered current sources

`verify_project.py` reads [ACCEPTED_BUILD.json](ACCEPTED_BUILD.json) directly from
the current checkout. It verifies every selected source's SHA-256, Git blob and
import closure, then stages only those exact sources in a new output directory.
It does not reconstruct an old checkout or consume pre-existing compiled project
objects. The verified foundation compatibility adapter remains part of the
registered source closure.

Use the official Lean 4.19.0 release, commit `6caaee842e94`. The accepted Linux
release archive SHA-256 is
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
The registered core uses the bundled `Init`, `Std`, and `Lean` libraries.

```sh
python3 proofs/verify_project.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --project consolidation-core \
  --output /absolute/new/output/directory
```

Each compilation and audit uses `--trust=0 -j1 -DElab.async=false`. The verifier
checks the exact registered claim endpoints, the transitive axioms of every
kernel-safe project constant, and a consumer in a separate working directory.
Only `propext`, `Classical.choice`, and `Quot.sound` are permitted mathematical
axioms. Unsafe and partial implementation declarations are recorded separately;
they do not receive a mathematical acceptance label.

The result directory retains exact staged sources, commands, exit statuses,
substantive logs, compiler/source hashes, `verification.json`, an elaborated
interface inventory, and a file manifest. Existing result directories are never
overwritten. `--check-only` verifies source and import identities without
compiling the mathematical proof; its output is labeled accordingly.

### Public entry for a verified project

A successful build generates `P196Project.lean` and its compiled module under
`<output>/<project>/source`. It imports that project's registered public roots.
The verifier separately compiles a consumer that imports `P196Project` and checks
every registered endpoint. A downstream file can use the same verified output:

```sh
LEAN_PATH=/absolute/output/directory/consolidation-core/source \
  /absolute/path/to/lean-4.19.0-linux/bin/lean --trust=0 Consumer.lean
```

`Consumer.lean` begins with `import P196Project`. The module is available through
the selected build output's `LEAN_PATH`; it is not a checkout-wide import that
implicitly accepts every retained research file. Different registered projects
have separate build outputs and can retain incompatible historical module names.

### Coverage is still incomplete

The registry currently contains the 38-source `consolidation-core` closure and
explicitly retains `catalogue_complete: false`. Other previously accepted
contributions remain accepted under their original source, review, and execution
records, but are not all registered in this command yet. Historical and WIP files
are not automatically accepted because they exist in the tree.

Omitting `--project` attempts every registered project. It returns exit status
`2` while the accepted-scope census is incomplete, even if those scoped builds
pass. A scoped `PASS` is not a full-repository build or completion of the cleanup.
The remaining census must identify all accepted sources, their dependencies,
and applicable verification commands before repository-wide success is possible.

## Reproduce historical original-layout checks

The frozen original layout has base
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
`replay_original_layout.py` reconstructs its exact mapped bytes in a new external
temporary directory. The mapping uses retained original registry bytes when
the current registry has advanced. It leaves the current checkout unchanged.

```sh
python3 proofs/verify_release.py
python3 proofs/replay_original_layout.py -- \
  python3 proofs/verify_project.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --project consolidation-core \
  --output /absolute/new/historical/output/directory
```

These commands reproduce the frozen historical release checks and their original
policies. They do not certify complete integrity or mathematical coverage of the
current tree. The current-source command above enforces the stricter explicit
trust-zero build and consumer check.

The [build repair preservation record](archive/migration/deep-clean-2026-10-17/build-coverage/originals-manifest.json)
identifies the exact replaced metadata and runner bytes. Existing Lean source,
theorem statements, original review attribution, failed research, and calculation
archives are unchanged by this build-wiring repair.
