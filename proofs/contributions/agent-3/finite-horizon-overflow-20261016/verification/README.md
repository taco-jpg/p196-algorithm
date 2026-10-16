# Reproducing the finite-horizon contribution

This directory verifies the exact accepted proof sources with Lean 4.19.0.
It contains a source manifest and a Python standard-library build driver.
The driver does not download dependencies, invoke a package resolver, alter
Git, reuse contribution object files, or erase earlier verification output.

## Run

Requirements: Python 3.9 or later, Lean 4.19.0 with its standard library, and
a repository checkout containing the paths listed in `source-pins.json`.

```bash
python3 proofs/contributions/agent-3/finite-horizon-overflow-20261016/verification/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --repo /absolute/path/to/p196-algorithm \
  --build-dir /absolute/path/to/a-new-clean-build
```

`--repo` defaults to the repository containing this script. `--build-dir`
must be new or empty. A nonempty directory is rejected, preserving its
contents. `--timeout` optionally changes the per-command timeout from its
default of 600 seconds.

The manifest requires version 4.19.0. The actual executable, compiler
version string, compiler prefix, and root `Init`, `Std`, and `Lean` object
hashes are recorded for each run. The manifest also records the binary hash
of the Linux x86-64 compiler used for the retained verification; that hash
is provenance, not an additional architecture restriction.

## Source pins and build order

`source-pins.json` fixes each source path, SHA-256 digest, direct imports,
and every explicitly named public contribution declaration. The original
dependency snapshot is commit
`4b4edf976b2c7a9ba1dad80636c0e21c66350325`. The coordination claim is commit
`55c0133a597cd3577fbbb864414fe4527729e554`.

The complete build order is:

1. `PeriodObstructions`
2. `ActualWordBridge`
3. `LychrelDigitSums`
4. `DecimalSafeRuns`
5. `FamilyDefinitions`
6. `FamilyCardinality`
7. `FiniteHorizonOverflow`
8. `SafetyBridge`
9. `NormalizedSafety`
10. `FiniteHorizonTheorem`

Each file is copied unchanged into a fresh, flat `modules/` directory under
its canonical module name. Direct imports must match the manifest and
appear earlier in this order, except the installed standard library.
`LEAN_PATH` is replaced with this isolated directory. Source and copied
bytes are checked both before compilation and after all audits finish.

The final aggregate source is pinned to:

```text
3316df9f3ce5baeac971faff53cfe5d6616beebf50c116c5662476c261f0d697
```

## Audit coverage

The source inventory contains 67 explicitly named public declarations.
After compiling all ten modules, a generated diagnostic file reads Lean's
compiled environment and lists every constant in
`P196.Agent3.OverflowHorizon`, together with Lean's `isUnsafe` and
`isPartial` flags. This includes public compiler-generated helpers in
addition to the explicit source declarations.

Every explicit export must appear in that inventory as a safe, nonpartial
constant. The driver generates an `AllExportedAxioms.lean` file with a
separate `#print axioms` command for every such logical constant, including
generated logical helpers. The set of audit results must exactly equal
this logical inventory; missing or duplicate audit results fail the run.
Private helpers used by these constants are covered transitively by Lean's
axiom calculation.

Lean also emits unsafe executable implementation stages such as
`allBits._cstage2`. Their opaque compiler specialization dependencies are
not logical proof axioms. Those implementation symbols are recorded
separately and excluded from the logical audit using Lean's own safety
flags. An explicitly declared source export with either flag fails the
run; no explicit source declaration can be excluded this way. The first
verifier development attempt, which audited executable stages as though
they were logical declarations, is retained under `development/`.

The permitted axiom set is exactly:

```text
Classical.choice
Quot.sound
propext
```

Any other reported axiom fails verification. `sorryAx` and
`Lean.ofReduceBool` are explicitly rejected in compiler output. Before
compilation, a comment- and string-aware source scan rejects `sorry`,
`admit`, custom axiom declarations, `native_decide`, unsafe or partial
definitions, implementation replacement attributes, elaborator extensions,
kernel-check bypass options, and other listed shortcuts. The full forbidden
identifier list is retained in each source record of the report. Ordinary
kernel-checked `decide` proofs are allowed.

The generated environment-inventory file uses a diagnostic `run_cmd` to
list names; it contributes no theorem or proof. Accepted proof sources
are scanned separately and cannot contain such commands. The subsequent
proof audit consists of `#print axioms` commands.

## Outputs and failures

A successful run returns exit code `0` and sets `status` to `PASS` in
`verification.json`. A failed hash check, source scan, compiler command,
inventory check, or axiom audit returns a nonzero exit code and retains
the report and available logs with `status` set to `FAIL`.

The build directory contains:

- `source-pins.json`: the exact manifest used by that run.
- `modules/`: unchanged source copies, freshly compiled objects, and the
  generated inventory and complete axiom-audit files.
- `logs/`: separate version, prefix, compilation, inventory, and audit logs.
- `verification.json`: verifier and manifest hashes; source and object
  hashes; commands, working directories, exit statuses, timestamps and
  durations; relevant environment information; and the complete axiom
  inventory.

The retained successful run is summarized under `evidence/`. Development
probes under `development/` are diagnostic records and are not accepted
proof modules or inputs to the clean build. Existing proof development and
independent review records elsewhere in the contribution remain intact.

## Retained result

The complete retained run passed all ten source builds and audited all
67 explicit exports plus 62 generated logical helpers: 129 logical
declarations in total. Its compiled inventory additionally records 33
implementation symbols, comprising 31 unsafe compiler stages and two
partial `_unsafe_rec` helpers. Every explicit source export is safe and
nonpartial. The logical axiom union is exactly the three names listed
above.

`evidence/artifact-index.json` lists the retained evidence files with
SHA-256 hashes. `evidence/verification.json` contains the full execution
record; its absolute paths describe the original run, while the copied
logs are available in `evidence/logs/`.

Fourteen focused verifier guard checks also passed. They cover harmless
nested comments, forbidden proof shortcuts, unsupported axioms, rejection
of an altered pinned source through the actual command-line interface,
and preservation of a nonempty prior build directory. Their executable
check and results are retained under `development/check_verifier_guards.py`
and `development/verifier-guard-checks.json`.
