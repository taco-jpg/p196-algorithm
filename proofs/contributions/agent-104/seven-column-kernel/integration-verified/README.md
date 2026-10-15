# Merged-candidate clean whole-chain rebuild and axiom audit

**PASS.** The independent clean reviewer executed a separate merged-candidate source-only build of all 383 local modules selected by `Conclusion739` and `TerminalObstruction`, then independently rechecked the complete compiled theorem inventory and all source, object, log, and compiler pins. This is an actual merged-candidate execution, separate from both the earlier contribution-only independent build and the parent-run structural build.

Source commit: `4bdd59bdc8f3e8f0556c3decb0898e6c6f271b29`. Checker exit status: **0**. Started: `2026-10-15T06:30:41.461384+00:00`; checker completed: `2026-10-15T07:09:55.408833+00:00`. Every source matched the committed bytes before being copied into the new build directory. No pre-existing local `.olean` was reused. Subsequent evidence-only Git commits did not change this pinned source selection.

Merged candidate tree: `0185512ec6de577246450e83d703f11d84687ce4`. The 383 accepted source hashes are identical to the earlier independently checked contribution sources, but no earlier local object was reused: this merged candidate underwent a separate full rebuild and exhaustive audit. The earlier contribution-only evidence remains unchanged.

## Exact accepted results

- `SevenColumnKernel.Finite739.ancestry_bound39`: for every natural `A`, `P`, and `t`, if `A > 0`, `P` is a decimal palindrome beginning with 739, and the ordinary reverse-and-add orbit from `A` reaches `P` at time `t`, then `t ≤ 39`. There is no digit-length restriction.
- `SevenColumnKernel.Finite739.no_196_739_palindrome`: at every natural time `t`, the ordinary orbit from 196 is not a palindrome beginning with 739.
- `TerminalObstruction` additionally excludes the pair-column prefix `[1,9,6]` at positive times under its stated width hypothesis. These are pair sums, not the digits of 196.

The all-time conclusion concerns the restricted 739 palindrome family. It does **not** prove P196 or decimal Lychrel existence. The accepted statements have no unsupplied finite-certificate premises.

## Exhaustive theorem and axiom checks

The compiled local closure contains **7469 theorem constants**, including private and compiler-generated theorems; the source contains 3464 explicit theorem declarations. These are coverage counts, not numbers of independent mathematical results. `AllExportedAxioms.lean` discovers the complete compiled inventory by module ownership. The complete substantive output is retained at `logs/AllExportedAxioms.log`.

A separately executed inventory-only command counted the same 7469 theorem constants, including 3171 names in the `_private` namespace, and its per-module counts agree exactly with the exhaustive audit. This diagnostic starts only after the full original checker releases its compiler slot. It introduced no theorem and did not replace any axiom check. Its source, full output, timing, and the original audit's measured CPU-progress samples are preserved.

Every discovered theorem has exactly one returned axiom report. Every transitive axiom set is contained in `propext`, `Classical.choice`, and `Quot.sound`; the actual union is exactly those three. No `sorryAx`, custom logical axiom, or native evaluation axiom occurs. `allRowsFast` has no axioms. The endpoint-specific sets and the complete per-theorem inventory are preserved in the JSON reports.

There are 43 compiler-generated unsafe implementation axiom declarations. None occurs transitively in an accepted theorem. Their existence is not silently treated as logical proof: the runner rejects safe custom axioms and allowlists the transitive dependencies of every theorem. The inspected official `Lean.Util.CollectAxioms` implementation visits the checked kernel environment, recursively follows types and values, and records all `axiomInfo` entries regardless of their unsafe flag. Its source was byte-compared to the pinned release archive. The local source scan also found no proof escape or native evaluator constructs.

## Toolchain and isolation

Official Lean **4.19.0**, release commit `6caaee842e94`. Compiler binary SHA256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Official archive SHA256: `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.

Preflight compared 1,476 compiler, shared-library, and standard-object archive members with the installation. The final audit imported 383 newly built local objects and 1303 standard objects; every standard object matches that archive. The existing official archive was reused and independently hashed; no independent network re-download is claimed.

The transparent wrapper preloads only the documented `/proc/<current-pid>/exe` to `/proc/self/exe` compatibility shim. Its C source, binary SHA256, exported symbols, disassembly, and read-only data inspection are preserved. It does not interpose Lean or kernel functions. No inherited `LD_PRELOAD` or `LD_LIBRARY_PATH` override was present. The runner clears external Lean import-path variables and sets `LEAN_PATH` to the fresh source/object directory.

Two build workers were authorized. Each compiler used `-j1 -DElab.async=false`. No memory limit was imposed. Every compilation command, exit code, timing, peak RSS, and substantive output is retained in `verification.json`, `runner-output.log`, and `logs/`.

## Evidence and reproduction

- `independent-verification.json`: independent post-build acceptance checks and exact endpoint interpretation.
- `verification.json`: unmodified runner report, full source/object/compiler pins, complete theorem inventory, and all command records.
- `preflight-01/`: frozen historical checkpoint explicitly labeled full rebuild IN_PROGRESS at that time.
- `independent_controls.py`, `independent_finalize.py`, and `check.py`: the controls and exact committed runner used.
- `source-snapshot-inventory.json` and `recover_snapshot.py`: exact original-source references and SHA256-verified source recovery.

The generic runner retains `numerical_739_instance_established_by_this_report=false` because it does not interpret mathematical statements. This is not a failed finite check. The independent report additionally checks the final statements and complete unconditional application, and records the restricted numerical result explicitly. The runner also records original-source stability rather than enforcing it; this independent acceptance step separately enforces every original-source hash at completion.

From the source checkpoint, with a pinned Lean executable or the documented transparent wrapper:

```bash
python proofs/contributions/agent-104/seven-column-kernel/check.py /absolute/path/to/lean --evidence /new/empty/build --module Conclusion739 --module TerminalObstruction --jobs 2 --require-committed
```

The exact successful invocation and paths are in `invocation.json`. To reconstruct the flattened source snapshot, run `python recover_snapshot.py --repo /path/to/p196-algorithm --output /new/empty/snapshot` from this evidence directory. The recovery tool reads only the pinned Git commit and verifies every source SHA256.

Duplicate fresh-build sources and all `.olean` files remain outside the repository at `/workspace/scratch/7649db1e242c/build104-integrated/rebuild/snapshot`. They are excluded as reproducible build infrastructure. Their exact hashes, the committed original sources, all substantive logs, and the generated axiom-audit source are retained. No build error or rejected proof occurred in this independent run.
