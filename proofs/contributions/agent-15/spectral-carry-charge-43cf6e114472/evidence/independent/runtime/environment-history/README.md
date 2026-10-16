# Agent 15 runtime and environment baseline

## Result

A usable local Lean 4.19.0 runtime was established through the supported approved execution mode. The compiler smoke test and the authorized existing-source baseline both passed. This is environment evidence only; it is not authorship, acceptance, or dependency evidence for the pending T/R target.

Pinned repository snapshot: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.

Actual compiler output:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
Lake version 5.0.0-6caaee8 (Lean version 4.19.0)
```

Both executables are from `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/`. Their invocation used `exec_command` with `sandbox_permissions=require_escalated`. This is the tool's supported approval path. No readlink adapter was created or loaded by this investigation, and the shared distribution was not changed.

## Runtime diagnosis and provenance

The default sandbox invocation of `lean --version` exited 1 with `error: failed to locate application`. The executable is a real ELF file, not a symlink, and `ldd` resolved all its shared-library dependencies. `strace` could not operate because `PTRACE_TRACEME` was denied; that diagnostic failure is preserved and is not a Lean proof failure.

A retained installation record identifies the upstream release URL as `https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst` and records a prior successful approved execution. Its recorded archive SHA-256 is `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`; the record explicitly says this was a local archive hash, not an independently published upstream checksum. This investigation reused the existing distribution read-only and did not claim a fresh download or independent upstream signature verification.

The actual `lean` executable SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The baseline verification record contains hashes for the executable and all top-level Lean shared libraries, checked again after compilation. Actual version output matches the repository's pinned `leanprover/lean4:v4.19.0` and release commit `6caaee842e94`.

## Smoke test

`RuntimeSmoke.lean` imports `Lean` and defines only the environment fixture `runtime_smoke : (0 : Nat) = 0 := rfl`. The command run from this directory was:

```sh
/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean -o RuntimeSmoke.olean RuntimeSmoke.lean
```

Exit status was 0 and the exact audit output was:

```text
'runtime_smoke' does not depend on any axioms
```

The smoke source and object are retained, together with `approved_smoke_result.json` and `approved_version_result.json`.

## Authorized existing-module baseline

The exact original `LychrelDigitSums` source was fetched at the pinned repository snapshot from:

```text
proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/continuation/LychrelDigitSums.lean
```

Source identity:

- Git blob: `8a865176625283648a8a20dd2411ed77670eb0a2`.
- SHA-256: `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.
- Size: 218,799 bytes; 5,490 source lines.
- Local project imports: none. Its single import is `Std` from the official distribution.

All ten currently flattened `proofs/LychrelDigitSums__*.lean` paths have that same Git blob in the pinned tree; `current_source_blobs.json` preserves the exact read-only Git command and output. Filename multiplicity therefore does not represent ten distinct source versions.

The exact source was copied into the new `baseline-001/source/` directory. No project objects were reused. Official toolchain objects were reused. `LEAN_PATH` was set explicitly to that new source directory. The only two selected endpoint checks were existing declarations:

- `FoldedDecimal.canonical_next_no_overflow`.
- `DecimalWidthGrowth.numeric_width_bounds`.

The commands run from `baseline-001/source/` were:

```sh
/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean --version
/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean -j1 -DElab.async=false --trust=0 -o LychrelDigitSums.olean LychrelDigitSums.lean
/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean -j1 -DElab.async=false --trust=0 -o BaselineAudit.olean BaselineAudit.lean
```

| Command | Exit status | Elapsed seconds |
|---|---:|---:|
| version | 0 | 0.065 |
| LychrelDigitSums | 0 | 68.780 |
| BaselineAudit | 0 | 0.265 |

Both selected endpoints reported exactly `[propext, Quot.sound]`. Their full printed signatures and transitive axiom lists are in `baseline-001/logs/BaselineAudit.log`. The complete original source contains its own retained `#print axioms` commands, whose actual outputs remain in `baseline-001/logs/LychrelDigitSums.log`; this record does not turn that selection into an exhaustive declaration audit.

The existing checker's nested-comment/string masking function was used for a source-only scan. It found no live tokens among `sorry`, `admit`, `axiom`, `sorryAx`, `native_decide`, `ofReduceBool`, and `skipKernelTC`. The scan's exact source identities and limited status are in `baseline_source_scan.json`.

`run_baseline.py` preserves the executed driver and rejects an already existing output directory. `baseline-001/verification.json` preserves every argv, working directory, explicit environment override, exit status, elapsed time, log hash, source hash, compiler identity, and output hash. Reproduction must select a new output directory instead of overwriting the existing evidence.

## Existing project build arrangements

The current `proofs/verify_project.py` is a wrapper around `proofs/replay_original_layout.py`. The latter reconstructs the preserved original layout in a new external directory, uses source mappings and hashes to select retained bytes, and then invokes the original checker. It does not directly certify all currently selected source after the reorganization.

The documented original scoped command is:

```sh
python3 proofs/verify_project.py --lean /absolute/path/to/lean --project consolidation-core --output /absolute/new/output/directory
```

The inspected `consolidation-core` arrangement comprises 38 modules and explicitly scoped claim families. The original checker verifies source/import pins, exact official compiler version, fresh local source builds, endpoint presence, and transitive axiom reports with allowed axioms `propext`, `Classical.choice`, and `Quot.sound`. Its `--check-only` mode is source/import inspection, not mathematical verification; the default command without an explicit project does not report repository-wide PASS while the accepted catalogue is incomplete.

That 38-module build was not run. The single-source baseline was the bounded environment check authorized for this investigation. The old `proofs/REPRODUCE.md` commands must be interpreted through the preserved original layout; their historical paths are not automatically current flattened paths. The source snapshots of the wrappers, original checker, reproduction documentation, and toolchain pin are retained under `source_snapshots/`, with repository URLs and blob identities in the provenance JSON files.

## Preservation and remaining scope

Failures are retained separately: default-sandbox compiler startup, blocked `strace`, a connector transport error, a missing guessed filename, and the initially unmaterialized parent checkout. No failure was relabeled as a successful build. The successful baseline checks source and compiler immutability before/after compilation. No repository source, remote branch, coordination record, or other session cache was modified by this specialist.

The environment is ready for the parent to supply the frozen T/R package for independent semantic review and clean compilation. This specialist has authored no T/R theorem or proof.
