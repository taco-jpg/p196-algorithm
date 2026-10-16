# Merged-tree integration check: PASS

Signed: `/root/runtime_audit`, Agent110's independent infrastructure and review executor. Completed: `2026-10-15T16:40:19.465121+00:00`.

This compares source and recompiles root modules against an existing independently reviewed closure; it is **not a new complete empty-directory dependency rebuild**. New output directory: `/workspace/scratch/63e10b24caf2/integration-root-check`. Twenty dependency `.olean` files are explicitly reused read-only; three roots are recompiled. No dependency directory, mathematical source, Git state, or remote object was modified.

## Frozen objects and results

- Target merge commit: `b337ce1e3c3058468bc1562bf30e536f685960dd`, tree `89ad2eb97815cd721df7d82316e396c0931d6ca7`; confirmed parent main `2c2551165c13d23b11d44122fc7a504d51053e59`.
- HEAD at start and finish was `4ceb839b4bd24b1d6aeeef3cfa091bf6bf6034e2`. Subsequent documentation/review-evidence commits may move HEAD; mathematical source remains byte-bound to the merge above.
- All19 certificate and four Radix working-tree sources equal merge-commit Git objects bytewise, with every SHA256 matching independent-review records.
- All19 certificate sources also equal fetched remote commit `eb4817f0973cbbe2a059af33d5dc53877a5275b7`; all four Radix sources equal fetched remote commit `1cdc55c89b376faa270d1dffaf21e21b6eedeb4b`. Per-file SHA256, Git blob, and path: `source-hashes.tsv` and `result.json`.
- `CertificateChecked`, `All`, and `RadixExterior` were recompiled from actual merged source, all exit0. Actual `lean --deps` output confirms roots/direct imports resolve to this output or specified independent-review directories.
- Explicitly reran `#print axioms` for three Checked theorems and all15 Radix theorems:18/18 passed, matching previous individual axiom sets; union only `propext`, `Classical.choice`, `Quot.sound`.
- At completion, all23 working sources,23 original reviewed objects, and two review receipts were rechecked with unchanged hashes. Three original reviewed root `.olean` files were used only to check historical object identities, not for this root compilation.

## Independent complete-closure review basis

1. Certificate19-module receipt: [`../../review-checked/rebuild-d611d7f/manifest.json`](../../review-checked/rebuild-d611d7f/manifest.json), SHA256 `1a03fa46d6ab20224be224ef50bd7664af87e616a2643c963f2078c1add98906`. PASS, `objects_reused=false`; object directory `/workspace/scratch/63e10b24caf2/reviewer-build/checked-d611d7f`. Seventeen dependency objects reused here.
2. Radix four-module receipt: [`../../review-radix/verification.json`](../../review-radix/verification.json), SHA256 `81851617ff0edcff9204df273cd97ca4714fc6c5ebe89382ae4a6c5927282b1f`. PASS, `project_object_reuse=false`; object directory `/workspace/scratch/63e10b24caf2/radix-review-build`. Three dependency objects reused here.

The complete-closure declaration audits are supported by these two independent rebuild receipts;18 endpoint checks here are not a new complete-closure audit. Reviewed source/object hashes and transitive endpoint axiom results match.

## Actual statement scope

Reread merged `CertificateChecked.lean` and `RadixExterior.lean`; actual `EndpointTypes.lean` output is in `logs/EndpointTypes.log`.

- `period_at_least_four` assumes only `check cert = true`, concluding `4 ≤ cert.P`.
- `six_phase_constraints` still requires `check cert = true` and initial `SixPhase`; conclusions include `O = 2(G+H)`, nonnegativity/divisibility budgets, `2O ≤ P ≤ 4O`, `P % 6 = 0`, `42 ≤ P`. Original admissibility is derived through Agent112's frozen source, without a circular canonicality assumption.
- `saturated_period_constraints` additionally **explicitly requires** `2 * totalGam cert = (cert.P : Int)`, then gives `P % 72 = 0` and `72 ≤ P`; check alone is not claimed to force saturation.
- Radix quantity remains `Z = 9 * value10 B - c * (10^length(B)-1)`, observable `(phase, Z)`. Both impossibility theorems negate universal observable-update/monotonicity assumptions restricted to canonical states actually after overflow.
- `witness_not_state_return` explicitly gives `endpoint ≠ source`; return of an observable is not a state cycle. These results supply neither a concrete checker-accepted certificate nor a global conclusion about196.

## Execution environment and preserved failures

Actual version: `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`. Official4.19.0 ran through existing `runtime-audit/lean` launcher and the recorded narrow `/proc/self/exe` path adapter; compiler, launcher, and adapter SHA256 values are in `result.json`. Inherited Lean paths and dynamic-loading settings were explicitly cleared before setting recorded `LEAN_PATH`.

- `attempt-01-preflight/`: documentation/evidence commits advanced HEAD, stopping an old strict HEAD-equality precondition. **No compiler started; this was not a Lean failure.** Original driver and reason remain.
- `attempt-02-unsupported-display-option/`: three mathematical roots and18 endpoint axiom checks passed, but the custom signature-query script used unsupported Lean4.19 display option `pp.width`, giving query exit1. Complete driver, output, and failure result remain. After deleting only that option, a new empty root-output directory was created and all root compilations/audits rerun successfully.

Final driver: `check.py`. Actual commands, exits, logs, and hashes: `commands.txt`, `logs/`, `result.json`. It deliberately requires absent new output and `logs/` directories; reproduce in a new check copy with empty output paths, without overwriting evidence or treating existing root objects as fresh compilation.

Final `result.json` SHA256: `268959d1baddfc985fec42ba480216cdbc3b62dcbb59025aaad9cf8f0a81800e`.
