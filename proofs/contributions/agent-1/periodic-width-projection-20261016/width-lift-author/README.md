# Width lift author verification

Frozen source: `proofs/Agent1PeriodicWidthLift.lean`.

* SHA256: `a3897a4d7dc58b2f33efb519be75ea5f7ef61b8e6c4602749c0249de52b49978`
* Git blob: `d8e7a0273ade37bcced1c1aab564020881057487`
* Eight public theorem exports are listed in `frozen-receipt.json`.
* Final source compilation: `attempt-002`, PASS, official Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`, 0.50s, sampled peak 451228 KiB RSS.
* Final new-module origin audit: `audit-003`, PASS, 1.81s, sampled peak 966120 KiB RSS.
* The audit checks 44 safe originating constants, including 20 theorem declarations and all eight public exports. Their axiom union is exactly standard `propext`, `Classical.choice`, `Quot.sound`. There are no custom axioms or unsafe theorems.
* 64 generated runtime implementations are inventoried separately. These are ordinary compiler `_cstage` and `._at.` specializations from computational definitions and derived instances. They are not logical proof declarations. The audit rejects unexpected unsafe declaration names or unsafe theorems. The code-token scan excludes comments and finds no forbidden proof construct; its initial documentation false positive is recorded in `metadata-scan-note.txt`.

This is an **author incremental check**, reusing 26 explicitly hashed dependency objects. It is not a fresh 27-module closure build. `reused-dependencies.json` records exact source/object origins and hashes. The real parent-confirmed OuterCatalog object comes from root `attempt-006` and the Width object from width-author `attempt-002`; no dummy or partial catalog object was used. The parent's independent combined check remains separate.

## Preserved attempts

* `support-001`: PASS; isolated generic list-length/membership check while the real catalog dependency was unavailable. It makes no final-module claim.
* `attempt-001`: PASS; complete original seven-export source before the requested node uniqueness theorem.
* `audit-001`: retained FAIL of the first audit harness, which rejected all compiler-generated runtime implementations. Every inspected logical axiom closure was standard-only. The mathematical source did not change to address this harness issue.
* `audit-002`: PASS; corrected runtime inventory policy, same seven-export mathematical source.
* `attempt-002`: PASS; final source adds `widthCatalog_nodup` using standard pairwise/list-product lemmas.
* `audit-003`: PASS; all new originating declarations of that exact final source.

Every attempt directory contains exact attempted source, full compiler output, exact command, exit status, and memory/timing receipt. No mathematical source attempt failed. No failed audit was deleted.

## Reproduction and limits

The official executable and SHA256 are in `compiler.json`. `stage-dependencies.py` copies explicitly supplied successful dependency sets and records their hashes. It must not infer proof success from a file merely existing. `run-attempt.py <unused-attempt-name>` checks the current source; append `audit` to check the current audit file. The runner preserves its input before invoking Lean and uses one core with a 1500 MiB physical-RSS watchdog.

The compositional catalog has 7,024 distinct nodes and a list of 11,664 labelled edges. The exact actual quotient projection retains the original clock and all-nine carry pair, and preserves the unchanged complete `ValidPeriodic` predicate. No edge uniqueness, archived traversal order, reachability, SCC, infinite-orbit, or arbitrary-path realization claim is made. `source-interpretation.md` records the detailed contract, including the existing exponent guard for finite-word step interpretation.
