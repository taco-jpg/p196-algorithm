# Reproducing the two-history contribution

The retained verification passed all **23 pinned source modules** under
Lean 4.19.0 with `--trust=0`, with no compiler warnings. It directly audited
**179 explicit declarations** across the seven new modules and six
inherited contribution modules, including all **three private helpers**.
Including generated logical helpers, **304 logical constants** received
complete `#print axioms` audits. Their axiom union is exactly
`propext`, `Classical.choice`, and `Quot.sound`.

[verify.py](verify.py) is a Python standard-library driver;
[source-pins.json](source-pins.json) fixes the complete source closure.
The run uses an installed Lean distribution and the listed repository
sources. It copies source bytes unchanged into a fresh flat module
directory and compiles every dependency there.

## Run

Requirements: Python 3.9 or later, Lean 4.19.0 release commit
`6caaee842e94` with its standard library, and a checkout containing every
path in the manifest.

```bash
python3 proofs/contributions/agent-3/two-history-20261016/verification/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --repo /absolute/path/to/p196-algorithm \
  --build-dir /absolute/path/to/a-new-clean-build
```

`--repo` defaults to the repository containing this script. `--build-dir`
must be new or empty; a nonempty directory is rejected without changing
its contents. `--timeout` changes the per-command limit from its default
of 600 seconds. The driver preserves every report and compiler log if a
command or acceptance check fails.

Every source compilation and diagnostic invocation uses `--trust=0`.
The compiler version and release commit are checked. Each run records
the executable path and SHA-256, the full compiler version, compiler
prefix, and hashes of the installed `Init`, `Std`, and `Lean` root object
files. The manifest records the Linux x86-64 compiler hash used for the
retained run as provenance; another architecture may use its matching
Lean 4.19.0 release binary.

The driver does not download files, resolve packages, invoke Git, reuse
existing contribution objects, or erase earlier builds. `LEAN_PATH` is
replaced by the fresh `modules/` directory, and inherited Lean search-path
and option overrides are cleared.

## Source pins and build order

The manifest records each logical module name, repository source path,
SHA-256, Git blob identity, exact direct imports, and source provenance.
For every audited contribution module, it also fixes all explicitly named
public and private declarations, including their kind and visibility.

The topological build order is:

| Order | Modules |
| --- | --- |
| 1–4 | `PeriodObstructions`, `ActualWordBridge`, `LychrelDigitSums`, `DecimalSafeRuns` |
| 5–10 | `FamilyDefinitions`, `FamilyCardinality`, `FiniteHorizonOverflow`, `SafetyBridge`, `NormalizedSafety`, `FiniteHorizonTheorem` |
| 11–14 | `InverseFibers`, `PathCounts`, `WordBridge`, `ActualWords` |
| 15–16 | `TemplateStep`, `Compat` |
| 17–23 | `HistoryInterfaces`, `TwoLayerCertificate`, `IntegerInterfaces`, `ActualHistories`, `HistoryFamily`, `HistorySafety`, `TwoHistoryTheorem` |

Direct imports must match the manifest and refer to an earlier pinned
module, except for the installed standard library. Sources are copied
unchanged under their logical module names. Both original and copied
bytes are checked before compilation and again after all audits. The
manifest and verifier hashes are also checked after the run.

The original four core modules and `TemplateStep`/`Compat` are pinned to
the snapshot at `4b4edf976b2c7a9ba1dad80636c0e21c66350325`. The inherited
six-module contribution is pinned to its source checkpoint
`6576cee93d18145c638f298b0abcb1cd0a0f451e`. The four unchanged Agent #9
sources retain provenance from
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`. The two-history claim is
`142563ce83e36afe5ddaccb0e93ed821fd40eba0`.

The frozen aggregate `TwoHistoryTheorem.lean` is pinned to:

```text
386b181e43ba96a90ca46bc22e40dd05d5cbccf8a683aa5e96e6a5709aa448ee
```

## Complete declaration audit

After the 23 modules compile, `ExportInventory.lean` reads Lean's compiled
environment. `Environment.getModuleIdxFor?` identifies the originating
source module for every constant. Selecting the thirteen contribution
modules includes their public declarations, private declarations, and
compiler-generated helpers regardless of their printed namespace.
`privateToUserName?` maps private kernel names to their original source
names for the explicit declaration coverage check.

Every one of the 179 explicit source declarations must map uniquely to
its compiled declaration in the correct module, with matching visibility.
The explicit declaration must be safe and nonpartial. In particular, the
private certificate table `jointData`, inherited private theorem
`nodup_map_of_injective`, and inherited private theorem `replicate_join`
are checked directly.

Lean flags some generated executable stages as unsafe or partial. The
inventory records all of them separately. The retained run contains
530 compiled constants: 304 logical constants, 221 unsafe compiler
stages, and five partial compiler helpers. Every explicit source
export belongs to the logical set. The excluded implementation stages
include executable specializations such as `_cstage1`, `_cstage2`, and
`_unsafe_rec`; the separation follows Lean's flags rather than an
exception based on declaration names.

`AllExportedAxioms.lean` issues a `#print axioms` command for every logical
constant in the compiled inventory, including 125 generated logical
helpers. Private kernel names contain numeric name components that
cannot be represented by ordinary textual identifiers. For those names,
a diagnostic `run_cmd` obtains the exact compiled `Name` and elaborates
an ordinary `#print axioms` command using `mkIdent`. Setting
`pp.privateNames true` preserves the full kernel name in the output.
The set of axiom results must exactly equal the logical inventory;
missing or duplicate results fail the run.

The permitted axiom set is exactly:

```text
Classical.choice
Quot.sound
propext
```

Any other reported axiom fails verification. Compiler output containing
`sorryAx` or `Lean.ofReduceBool` is rejected explicitly. Before compilation,
a comment- and string-aware scan of all 23 accepted sources rejects
`sorry`, `admit`, custom axioms, `native_decide`, unsafe or partial
source definitions, implementation replacement attributes, elaborator
extensions, kernel-check bypass options, and the other shortcut names
listed in the report. Ordinary kernel-checked `decide` is allowed.

The generated inventory and private-name audit commands are diagnostics;
they add no mathematical theorem or proof. Accepted proof sources are
scanned independently and cannot contain these diagnostic extensions.

## Retained execution and failure evidence

A successful invocation exits with code zero and records `status: PASS`
in `verification.json`. A failed source check, compile command, inventory
check, or axiom audit retains the report with `status: FAIL` and a nonzero
exit code. Earlier output is preserved by the fresh-directory requirement.

The complete build directory contains:

- `source-pins.json`: the exact manifest used by that invocation.
- `modules/`: unchanged source copies, freshly generated objects, the
  ownership inventory source, and the complete axiom-audit source.
- `logs/`: separate compiler version, prefix, source compilation,
  inventory, and axiom-audit logs.
- `verification.json`: script and manifest hashes; source and object
  hashes; command arguments, working directories, exit statuses, times,
  and durations; relevant environment information; the complete compiled
  inventory; and all individual axiom results.

The portable retained evidence is under [evidence/](evidence/).
[evidence/verification.json](evidence/verification.json) is the full
execution report. Its absolute paths identify the original run;
[evidence/logs/](evidence/logs/) contains copied logs for inspection.
[evidence/artifact-index.json](evidence/artifact-index.json) records the
SHA-256 of every retained evidence file. Runtime binaries and compiled
proof objects are not included in the published evidence.

The full frozen-source run passed on its first compilation attempt.
`development/preflight-001/` preserves the earlier refusal to run while
the aggregate was still changing and the manifest was unfinished; no
Lean source compilation occurred in that preflight. The private-name
probes retain the failed literal identifier attempt and the successful
`mkIdent` resolution. Existing mathematical proof attempts and independent
review records remain in their original contribution directories.

The prior fourteen-check verifier guard suite is reused unchanged and
passed against this driver. Its checks cover comments, forbidden source
shortcuts, unexpected axioms, an altered source rejected by the actual
command-line interface, and preservation of a nonempty prior build
directory. The executable suite, result, and provenance are retained in
[development/](development/). The new ownership probes address the
specific additional requirement to audit private declarations directly.
