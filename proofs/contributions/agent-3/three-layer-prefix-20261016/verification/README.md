# Reproducing the exact two-layer depth contribution

The retained canonical run passed all **27 pinned source modules** under
Lean 4.19.0 with `--trust=0`, with **zero warnings**. It audited **231
explicit declarations**, including **three private helpers**, across
**17 contribution modules**. Its **373 logical constants** comprise all
231 explicit declarations and **142 generated logical helpers**. Every
one received a complete `#print axioms` audit. The reported axiom union
is exactly `Classical.choice`, `Quot.sound`, and `propext`.

[verify.py](verify.py) is the Python standard-library driver, and
[source-pins.json](source-pins.json) fixes the complete source closure.
[evidence/verification.json](evidence/verification.json) is the full
canonical report. A separate clean rebuild and semantic review are
retained under [../review/](../review/).

## Run

Requirements: Python 3.9 or later, Lean 4.19.0 release commit
`6caaee842e94` with its standard library, and a checkout containing every
path in the manifest.

```bash
python3 proofs/contributions/agent-3/three-layer-prefix-20261016/verification/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --repo /absolute/path/to/p196-algorithm \
  --build-dir /absolute/path/to/a-new-clean-build
```

`--repo` defaults to the repository containing this script. `--build-dir`
must be new or empty. A nonempty directory is refused without altering
its contents. `--timeout` sets the per-command limit, which defaults to
600 seconds. The driver uses only Python's standard library and an
installed Lean distribution. It downloads nothing, invokes no Git
operation, and preserves the report and logs on a failed check.

Every proof compilation and diagnostic Lean invocation uses `--trust=0`.
The exact Lean version and release commit are checked. The run records
the executable path and SHA-256, complete version, compiler prefix, and
the installed `Init`, `Std`, and `Lean` root object hashes. The manifest's
Linux x86-64 compiler hash records the retained run's executable; another
architecture may use the corresponding Lean 4.19.0 release binary.

The driver copies each pinned source unchanged into a fresh flat
`modules/` directory and compiles every module there. `LEAN_PATH` is
replaced with that directory. Inherited `LEAN_PATH`, `LEAN_SRC_PATH`,
`LEAN_SYSROOT`, and `LEAN_OPTS` overrides are cleared. Existing
contribution objects and development caches are not used by this build.

## Source pins and order

The manifest fixes every module's repository path, SHA-256, Git blob
identity, exact direct imports, and source provenance. Audited modules
also list every explicitly named declaration with its kind and visibility.

| Order | Modules |
| --- | --- |
| 1–4 | `PeriodObstructions`, `ActualWordBridge`, `LychrelDigitSums`, `DecimalSafeRuns` |
| 5–10 | `FamilyDefinitions`, `FamilyCardinality`, `FiniteHorizonOverflow`, `SafetyBridge`, `NormalizedSafety`, `FiniteHorizonTheorem` |
| 11–14 | `InverseFibers`, `PathCounts`, `WordBridge`, `ActualWords` |
| 15–16 | `TemplateStep`, `Compat` |
| 17–23 | `HistoryInterfaces`, `TwoLayerCertificate`, `IntegerInterfaces`, `ActualHistories`, `HistoryFamily`, `HistorySafety`, `TwoHistoryTheorem` |
| 24–27 | `DeadPrefix`, `ActualDepth`, `SharpHistoryFamily`, `SharpHistoryTheorem` |

Imports must match the manifest and refer to earlier pinned modules,
except for the installed standard library. Original and copied source
bytes are checked before compilation and after every audit has finished.
The manifest and driver must also retain the exact hashes recorded at
the start of the run.

The prior 23 source files are unchanged from reviewed base
`89287c9d3eb7dd801c2b1a59eff03140d47d24ec`. Their historical core,
finite-horizon, Agent #9, and two-history provenance is retained in each
record. The four new proof sources are pinned to the complete published
mathematical checkpoint
`6ce47fddb10f15b4af1025954f1694825093673d`, tree
`a3448c1d0da258403a3e3f44cd2ca3eeec052da2`. The exact task claim is
`3fbf616030a09c373b62b285827ff4851ada2052`.

The final aggregate `SharpHistoryTheorem.lean` has SHA-256

```text
d6afdf3e252b1b223ad30548ba6f72a3ba17604dfba43563ea28a5a9435a2f29
```

Historical source-note pins distinguish the third-layer checkpoint,
generator, and result table from the inherited two-history safe-image
note. These provenance records establish original-byte identity. The
canonical Lean run does not execute the historical Python generator or
claim to verify its whole table.

## Complete compiled declaration audit

After compiling all 27 modules, the generated `ExportInventory.lean`
queries Lean's environment. `Environment.getModuleIdxFor?` selects every
constant by its originating source module. The 17 selected module owners
include public declarations, private declarations, and generated helpers
regardless of their printed namespace.

The source inventory and compiled inventory are cross-checked. Every one
of the 231 explicit declarations must have a unique compiled constant
in its declared module with matching privacy. `privateToUserName?`
recovers the source name for this comparison. No explicit declaration
may be unsafe or partial. This directly covers the inherited private
`jointData`, `nodup_map_of_injective`, and `replicate_join` declarations.

The retained inventory contains **620 compiled constants**. Of these,
**373 are logical constants**, **242 are unsafe compiler implementation
stages**, and **five are partial compiler helpers**. The 247 generated
implementation constants are recorded separately. Their classification
uses Lean's flags, not a name-based exemption. Every explicit source
declaration belongs to the logical inventory; no explicit declaration
is excluded from the audit.

`AllExportedAxioms.lean` emits `#print axioms` for every constant in that
logical inventory. Private kernel names can contain numeric components,
so the private-name diagnostic obtains their exact compiled `Name` and
uses `mkIdent` to elaborate the ordinary `#print axioms` command.
`pp.privateNames true` preserves the full identity in the output.
The axiom-result set must exactly equal the logical inventory; omissions,
duplicates, or extra results fail verification.

The permitted axiom set is fixed in the driver:

```text
Classical.choice
Quot.sound
propext
```

The manifest cannot expand that set. Every reported nonstandard axiom
is rejected. Output containing `sorryAx` or `Lean.ofReduceBool` is
explicitly rejected as well. Before compilation, every one of the 27
accepted sources is scanned after strings and nested comments have been
removed. The scan rejects `sorry`, `admit`, custom axioms,
`native_decide`, explicit unsafe or partial definitions, opaque
shortcuts, implementation replacement attributes, kernel-bypass options,
and the other forbidden identifiers listed in the driver. Ordinary
kernel-checked `decide` is permitted.

The generated inventory and private-name audit use diagnostic elaborator
commands only to inspect already compiled declarations; they introduce
no mathematical theorem. The accepted mathematical sources are checked
separately and may not contain those diagnostic extensions.

## Driver provenance and inherited guard results

This driver adapts the prior two-history verifier at SHA-256
`bf91485edd05e0afb993f4c67949300ce1251d2d74808d1e0e52dbb97372fdcb`.
Only its module description and the set of authorized contribution
namespaces change: `P196.Agent3.ThreeLayer` is added alongside the two
existing namespaces. Every other byte is unchanged. The parsed Python
AST is also identical after removing only the module docstring and that
namespace-set assignment. The exact diff and these checked identities
are retained in [development/verifier-provenance.json](development/verifier-provenance.json)
and [development/driver-adaptation.diff](development/driver-adaptation.diff).

The **14 previously passing guard outcomes are inherited evidence** for
the unchanged acceptance checks; they are not described as a new run
against this driver. The retained result explicitly identifies the old
tested driver hash. The cases cover comment handling, forbidden source
shortcuts, standard and nonstandard axiom parsing, actual CLI rejection
of a modified pinned source, and preservation of a nonempty build
directory. Their exact original script, result, and log are retained as
`development/inherited-*`, with predecessor paths, commit, and hashes.

[development/prepare_package.py](development/prepare_package.py) records
the adaptation and source-pin preparation. It verifies all prior source
hashes, the four announced freeze hashes, declaration counts, imports,
and the exact historical source bytes. It does not compile Lean or
rerun the inherited guard suite. All declarations in the four new source
modules are checked by the actual full build and compiled-owner audit
in this run.

## Reports and preserved evidence

The retained canonical run used a new directory,
`/workspace/scratch/4ce7c54d31f6/agent3-depth-canonical-build-001`, and
passed on its first full compilation attempt. It began at
`2026-10-16T22:19:19.567193+00:00` and finished at
`2026-10-16T22:20:47.650697+00:00`. All **31 commands** exited zero:
compiler version, compiler prefix, 27 source compilations, the compiled
inventory, and the complete axiom audit.

An accepted invocation exits zero and stores `status: PASS`. A failed
source check, compiler command, inventory check, or axiom audit stores
`status: FAIL` and exits nonzero. Earlier files survive because each
invocation requires its own new or empty build directory.

The full build directory contains:

- `source-pins.json`, the exact manifest used for the run.
- `modules/`, holding unchanged source copies, fresh objects, and the
  generated inventory and complete axiom-audit sources.
- `logs/`, holding separate compiler version, prefix, source compilation,
  inventory, and axiom-audit logs.
- `verification.json`, holding the manifest and driver hashes, all source
  and object hashes, command arguments and working directories, relevant
  environment, start and end times, durations, exit statuses, warnings,
  the complete compiled inventory, and every individual axiom result.

The portable evidence under [evidence/](evidence/) retains the complete
report, exact manifest, generated diagnostic sources, and all compiler
logs. Absolute paths in the report identify the original execution;
the copied logs can be inspected directly in `evidence/logs/`.
[evidence/artifact-index.json](evidence/artifact-index.json) records the
SHA-256 and byte length of **35 retained evidence files**, excluding the
index itself: 31 logs, two diagnostic sources, the manifest, and the
execution report. Runtime binaries and compiled proof objects are omitted.
[development/export_evidence.py](development/export_evidence.py) preserves
the exact copying and indexing procedure and refuses to overwrite a
nonempty evidence directory.

| Canonical artifact | SHA-256 |
| --- | --- |
| `verify.py` | `072d88ffbb7aeb2b93cc1d9deb240b8460690b18c88e86dbd6ce87ef99544e9e` |
| `source-pins.json` | `197e33a9262c10b1b3741c01bae6115dbb6219c136266e3a3c410b51e7d83462` |
| `evidence/verification.json` | `a0d59668274eb0ca91acf397ee94d5a97dcbbdaa34072bdede7ba3e13134c0b4` |
| `evidence/artifact-index.json` | `40ec646ad9bfd2563deab152e195cbffe42a626088d9989b7505c4bbf5b6c1d0` |

The proof authors' failed and successful source attempts remain under
[../development/](../development/). Existing failed private-name probes
and guard outcomes remain in the prior contribution's verification
package. [../review/](../review/) holds a separately executed independent
27-module rebuild and semantic review. A documentation-only patch
format refusal is retained in `development/packaging-attempts.json`;
it changed no proof, verifier, or manifest bytes. The current README
supersedes the preliminary status text preserved in
[development/README-before-packaging.md](development/README-before-packaging.md)
without editing historical checkpoints.
