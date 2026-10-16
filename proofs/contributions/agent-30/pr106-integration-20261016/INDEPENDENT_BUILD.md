# Independent exact-source PR106 build and audit

## Result and scope

PASS for the six-source slice at commit `ed9b9048adfdda70f699a8a40997a4330b76dc16` in `taco-jpg/p196-algorithm`. Agent 30 performed this run independently of source author Agent 106. No mathematical source was changed and this specialist performed no remote writes. This is not a whole-main build claim or a proof that 196 never reaches a palindrome.

All six sources were freshly retrieved through the supported GitHub connector at the exact commit. Git blob hashes and SHA256 hashes were checked before compilation and again after auditing. The dependency retained its original bytes and was staged as `LychrelDigitSums.lean`. The fresh directory contained zero project `.olean` files before the successful build. Only the existing upstream Lean runtime was reused.

## Compiler execution

Runtime: `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`.

Every source compile used this exact argument pattern:

```sh
LEAN_PATH=FRESH_BUILD /path/to/lean --trust=0 -j1 -DElab.async=false -o MODULE.olean MODULE.lean
```

The successful baseline compile used a 4 GiB address-space cap after its preserved 2 GiB out-of-memory failure. Each of the five new modules used a 2 GiB cap. Every child had a 900-second CPU cap and 960-second wall timeout. All successful source compiles returned zero with empty stderr.

- `LychrelDigitSums`: exit 0, 70.046 seconds.
- `Agent106CarryBudget`: exit 0, 0.710 seconds.
- `Agent106CongruenceSeed`: exit 0, 2.472 seconds.
- `Agent106SparseTarget`: exit 0, 0.775 seconds.
- `Agent106CongruenceObstruction`: exit 0, 0.759 seconds.
- `Agent106CongruenceControls`: exit 0, 1.560 seconds.

The complete argv, timestamps, return codes, output hashes, and output bytes are retained in `build-execution.json` and the corresponding stdout/stderr files. The final full audit returned zero in 91.659 seconds; the corrected endpoint printer returned zero in 0.985 seconds.

## Complete module-origin logical audit

The audit selects declarations by actual Lean module origin, including private and generated constants. It runs Lean's `collectAxioms` on every theorem, every definition whose safety is genuinely safe, and every other safe constant. It separately builds a transitive graph from the kernel environment, traversing types, definition/theorem/opaque values, projection structures, inductive families and constructors, and recursor rules.

| Module | Theorem constants | Safe definitions | Other safe constants | Named new public endpoints |
|---|---:|---:|---:|---:|
| LychrelDigitSums | 986 | 131 | 14 | 0 |
| Agent106CarryBudget | 14 | 0 | 0 | 5 |
| Agent106CongruenceSeed | 51 | 0 | 0 | 7 |
| Agent106SparseTarget | 27 | 3 | 0 | 6 |
| Agent106CongruenceObstruction | 11 | 3 | 0 | 6 |
| Agent106CongruenceControls | 37 | 0 | 0 | 12 |

Totals: **1,126 theorem constants, 137 safe definitions, 14 other safe constants: 1,277 safe roots**. Their complete logical closure contains **3,027 kernel constants**. Both independent axiom computations have exactly the same union: **`propext`, `Classical.choice`, `Quot.sound`**. No disallowed axiom, `sorryAx`, native-reduction oracle, unsafe definition, or partial definition occurs in that accepted logical closure.

The full selected module environment also contains **795 compiler implementations**: 765 unsafe definitions, 13 unsafe axiom placeholders, and 17 partial definitions. They are explicitly listed in `audit-unsafe-selected.json`, with actual `unsafe` and `partial` flags retained. Their intersection with the safe-root logical closure is empty. Environment-level implementation placeholders are therefore not misreported as proof dependencies. All 13 unsafe axiom placeholders originate in the unchanged baseline.

The first complete audit incorrectly seeded the 17 partial `_unsafe_rec` implementations because Lean's `ConstantInfo.isUnsafe` is false for `DefinitionSafety.partial`. That failed harness, log and all JSON outputs are preserved in `audit-attempt-02-partial-classifier-failure`. The correction excludes both unsafe and partial implementations from logical roots, continues rejecting either if actually reachable, and explicitly checks that excluded implementations have empty intersection with the safe closure. Upstream Lean source creating these partial compiler implementations is retained in `upstream-api-evidence.txt` with source hashes.

## All 36 public theorem endpoints

`Agent30EndpointTypes.stdout.log` contains literal Lean-printed types and `#print axioms` output for all 36 source-level public theorem endpoints. This includes `rho_le` and all 12 Controls endpoints, which are not all covered by the source files' original print directives. The source census and module mapping are in `endpoint-manifest.json`; the environment result is in `audit-endpoints.json`.

Among those 36 endpoints, 25 use exactly `propext` and `Quot.sound`; 10 also use `Classical.choice`; one uses only `propext`. All exact individual results remain in the files.

## Preserved failures and corrections

1. The first combined source-staging request exceeded the system argument-length limit before process creation. Exact source content was then staged in chunks and hash-verified.
2. The initial compiler command included `-M 2048`; Lean 4.19.0 rejected the resulting unknown `max_memory` option before source elaboration. That runner and logs remain in `attempt-01-invalid-max-memory-option`.
3. The baseline at a 2 GiB address-space cap returned exit 1 with `INTERNAL PANIC: out of memory` after 27.032 seconds. The full snapshot remains in `attempt-02-baseline-2gib-oom`. Only the baseline limit was raised for the successful build.
4. The audit at a 2 GiB address-space cap terminated with signal 11 after 0.316 seconds and empty output. The cause is not established; the later successful process used more than 2 GiB of virtual address space. The failed snapshot remains in `audit-attempt-01-2gib-sigsegv`.
5. The first full audit's partial-classification failure is preserved as described above. Only the harness was corrected; successful source objects were retained unchanged.
6. The first endpoint printer rejected the unsupported formatting option `pp.width`. Its full output and execution receipt are preserved in `endpoint-attempt-01-unsupported-pp-width`; only that option was removed and only the printer was rerun.

`preflight-failures.json` records these outcomes. No failed run is represented as a pass.

## Portable replay

Run the independently reviewed `replay.py` with its adjacent frozen `Agent30FullAudit.lean`, `Agent30EndpointTypes.lean`, and `runtime-components.json`:

```sh
python3 replay.py --lean /path/to/lean-4.19.0-linux/bin/lean \
  --source-dir /path/to/exact-source-checkout \
  --work-dir /tmp/pr106-fresh-nonexistent-directory
```

The script accepts either the repository `proofs/` layout or these staged module filenames. It verifies exact Git blobs, source SHA256, imports, topological closure, harness hashes, runtime manifest identity and all 1,503 bundled runtime components. It copies only source, starts with no project objects, uses a clean explicit subprocess environment, and records/rechecks original and staged sources, harnesses, the script, runtime components, and dynamically resolved libraries before and after execution. The parent owns the fresh portable replay; this specialist did not duplicate the successful project build solely to exercise the replay wrapper.

The bundled runtime manifest was freshly measured after this original build/audit. Its historical official archive digest comes from the existing runtime receipt; the archive is no longer at its historical path, so no fresh archive validation is claimed here. The original run pinned the Lean executable and isolated `LEAN_PATH`; its inherited environment was inspected only after the run. The hardened portable replay supplies full clean-environment before/after identity evidence.

## Evidence verification and primary files

`verify_evidence.py` independently recomputes graph reachability from the retained edges, checks all source/object/harness/log identities, checks successful compiler outcomes, and verifies the exact 36-endpoint source/environment/printed census. Its result is `evidence-verification.json` with status PASS.

Primary entry points: `INDEPENDENT_RECEIPT.json`, `build-execution.json`, `audit-execution.json`, `audit-summary.json`, `audit-roots.json`, `audit-dependency-graph.json`, `audit-unsafe-selected.json`, `Agent30EndpointTypes.stdout.log`, `source-manifest.json`, and `preflight-failures.json`.
