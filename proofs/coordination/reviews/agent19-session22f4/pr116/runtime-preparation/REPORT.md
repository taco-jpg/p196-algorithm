# PR 116 exact-source runtime preparation

Scope: import-object preparation for new Lean bridge development. This is not an independent mathematical review and does not prove the missing all-width bridge.

Repository: taco-jpg/p196-algorithm. Pinned head: 51f8f8d523eb8434b6a80ad7dc1e30fe63ab8378.

## Ready-to-use environment

- Lean: /workspace/scratch/8b5152316f75/runtime-agent1/toolchain/lean-4.19.0-linux/bin/lean
- Version: Lean 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release.
- LEAN_PATH: /dev/shm/p196-agent19-session22f4/pr116-runtime/build
- Execution requires the host-visible `exec_command` `require_escalated` context.
- Available modules: ExteriorCore, BoundaryArithmetic, ShortWidths, NormTail, ZipTail, ExteriorCapTwo, ExteriorCoverage.
- Canonical is imported unchanged from ExteriorCoverage. Its project closure is ExteriorCoverage -> ExteriorCapTwo -> ExteriorCore -> Std.

## Evidence

`source-pins.json` records all GitHub blob IDs, locally computed blob IDs, SHA256 hashes, lengths, and pinned retrieval URLs. The five original CI source hashes match exactly. Both flattened Coverage variants are identical at the pinned head; both flattened CapTwo variants are likewise identical.

`CI-job-117215969204.log` retains the actual fetched decoded GitHub Actions job log. `CI-jobs.json` records successful job/run metadata. `CI-SOURCE-BINDING.json` preserves all five actual compiler command lines, their five source bindings, and the original endpoint axiom output. The original CI used `--trust=0 -j1 -DmaxHeartbeats=0 -DmaxRecDepth=100000`; it did not use `-DElab.async=false`. The original CI produced only the ExteriorCore object.

`baseline-build.json` records one fresh scoped build of the five exact pinned inputs with `-o` to supply import objects. `closure-build.json` records the additional exact CapTwo and Coverage builds needed to import the original Canonical. Every invocation exited zero; no failed compiler attempts occurred in this preparation task. Each compiler invocation has separate raw stdout and stderr logs. Source copies remain byte-identical to the fetched pins.

`PREPARATION-RESULT.json` records the full module/object mapping and transitive endpoint axiom results. All 20 printed existing endpoints use only `propext`, `Classical.choice`, and `Quot.sound`, or no axioms. These results concern existing helper/coverage declarations, not the missing all-width bridge.

`runtime-receipt.json` preserves the actual version output and key-file SHA256 comparisons. The selected runtime was previously retrieved as a pruned checker artifact; `runtime-agent1-provenance.json` records that provenance. The separate `runtime-agent6-provenance.json` records an authenticated official-release archive hash of 6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe. The selected binary, Init.olean, Std.olean, Lean.olean, and libleanshared.so exactly match that existing official-release runtime by SHA256. No archive was downloaded or toolchain rebuilt for this task.

## Boundaries

No remote mutations, claims, comments, branch creation, original-source overwrites, or changes to shared runtimes were performed. Historical comments calling helpers uncompiled were preserved verbatim, while the actual CI and preparation logs establish the later checks. All newly prepared files are inside this authorized temporary directory. The remaining exact-source-to-boundary bridge is owned by the bridge formalizer and requires its own final endpoint checks and a separate independent review.
