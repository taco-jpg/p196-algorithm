# Independent review: Agent #109 kernel-only recheck of the 8/17 boundary exclusion

Task `agent103-review-agent109-boundary`. Replication/review only: **no new theorem**.
Reviewed commit `e5f2a566837b06fbc5099b49f10b27310fa68004`, directory
`proofs/contributions/agent-109/boundary-kernel-recheck/`, together with the unmodified
originals in `proofs/research/main_existence_attempt/boundary_resume/lean/`, which are
byte-identical to the reviewed baseline `ba0890e`. All 249 compiled sources are pinned
in `sources.sha256`; the Agent #109 files match the author's `SHA256SUMS`.

## Toolchain and rebuild

The compiler is the official `lean-4.19.0-linux.tar.zst`, downloaded independently
(SHA-256 `6fe3ce97...ba813fe`, commit `6caaee842e94`). The author's `build.sh` and
`run_chunks.py` were **not** used.

- `dagbuild.py` (written here) compiles every module from an empty directory once its
  imports are built.
  - Settings: two workers, `ulimit -v 6500000`, `-j1 -DElab.async=false`.
  - Excluded from the build: `Dump`, the `TranscriptionCheck` control and `AuditK`.
  - Record: `dagbuild.jsonl`.
- 243 modules compiled with exit 0 under the scheduler.
- One chunk, `ProjK6p36`, was SIGKILLed (exit -9) after 154 s while sharing 8 GB RAM
  with another kernel check. Recompiled alone, it passes in 26 s.
- My scheduler then stopped on its own retry bug. The remaining `ProjK6`,
  `BoundaryCertificateK`, `ArithmeticBridgeK`, `BulkTargetsK` and `BulkDerivationK`
  were compiled sequentially; all exit 0. These entries are marked `"sequential"` in the
  jsonl.

## Axiom audit

- **Author's `AuditK.lean`:** exit 0. Output is in `AuditK.out`.
- **Own audit (`AuditAllK.lean`):** covers **every** theorem declared in `BoundaryDataK`,
  `SoficFast`, `FastData0-7`, all `ProjK*` modules, and `BoundaryCertificateK`,
  `ArithmeticBridgeK`, `BulkTargetsK`, `BulkDerivationK`.
  - Results for the 298 theorems: 249 use no axioms, 12 use `[propext]`, 28 use
    `[propext, Quot.sound]`, and 9 use `[propext, Classical.choice, Quot.sound]`.
  - **None depends on `Lean.ofReduceBool`.**
  - As a control, the same file prints the original
    `BoundaryCertificate.no_936_or_9_12_15_exterior`, which still lists
    `Lean.ofReduceBool`. This confirms the trust boundary was real and has now been
    removed.
  - Log: `AuditAllK.log`.
- **Token scan** of all K sources: no `sorry`, `admit`, `native_decide`,
  `ofReduceBool`, `axiom`, `implemented_by` or `extern`.

## Statement fidelity (the key adversarial point)

1. **Same statement.** `#check` with `pp.fullNames` prints identical types for the new
   theorem and the original. `AuditK.lean` also elaborates the original statement text
   against the new proof.

   The statement mentions only the following constants:
   - `ReverseClosure.Path`
   - `BoundaryCertificate.ArithmeticColumn`
   - `BoundaryCertificate.derivedBulkWord`

   These unfold only to arithmetic definitions:
   - `ArithmeticColumn` is built from `Periodic`, `permitted` and `outputOf`.
   - `permitted` is defined by inline decimal-digit equations.
   - `derivedBulkWord` comes from `cutWord`, the explicit three-site carry recursion
     `step3`/`carry3`.

   **No string-encoded table appears in the statement.** So the kernel-only theorem
   proves exactly the original proposition, whatever the transcription.
2. **Transcription.** This matters only for the graph-relative theorems
   `no_finite_exterior`/`no_arithmetic_exterior`, which are correctly stated for
   `graph0K`.
   - `transcription_check.py` is independent of the author's script. It applies Lean's
     `splitOn " "` + `filterMap String.toNat?` semantics to all 32 original string
     tables: 8 graphs, 8 ranks, 8 maps and 8 root ranks.
   - It finds all 32 equal to the `BoundaryDataK` literals, over 37,698 entries.
     Result: `transcription_check.json`, PASS.
   - The literal graphs use the original `BoundaryCertificate.decodeEdge`; no
     redefinition is made.
   - The author's compiled `TranscriptionCheck.lean` control also prints `true`.
3. **Checker soundness.** `Sofic.Fast.fast_sound` concludes the original, unchanged
   `Sofic.Projection fiber output g h rank project`, with tree-defined rank and
   projection. Downstream, `projection_sound` accepts any rank/projection satisfying
   `Projection`, so replacing the original arrays with trees is sound. The
   hypotheses are the two Boolean checks over the complete `rawNodes` list.
4. **Scope is unchanged.** This remains an obstruction for the fixed alternating 8/17
   exterior ansatz. The correspondence to all ordinary orbits is the original written
   argument and is not formalized here. No claim about 196 is made.

## Verdict

INDEPENDENTLY-REVIEWED (PASS) at `e5f2a566`. The historical boundary exclusion's final
theorems are now kernel-checked without `Lean.ofReduceBool`. Not INTEGRATED by this
review; the FINDINGS row update belongs to the integration owner.
