# Reproduction

Run commands in a disposable checkout: historical checkers write audit JSON/log files next to their source, and discovery scripts can regenerate large outputs. All files under `research/` retain their original relative locations and bytes. Python, Lean, solvers, compilers, upstream archives, and compiled outputs are not vendored here.

## Release integrity

From `proofs/`:

```sh
python3 verify_release.py
```

This verifies published file hashes, original-source identity, and completeness of local Lean imports. It is an integrity check, not a mathematical proof. `VALIDATION.json` records the publication-time checks and selected independent certificate replays.

## Dependencies

- Python 3 with its standard library suffices for the NFA terminal-certificate, delay, probability, and LRAT replay commands below. The published CPU harness uses Python 3.11+.
- The research solver requirements are pinned in `research/requirements.txt` (`z3-solver`, NumPy, and SciPy). Installing them is needed for the corresponding discovery scripts and some checkers that import discovery modules; it is unnecessary for the standard-library replays.
- Lean is pinned to **4.19.0** by `research/lean-toolchain`. The formal modules use `Std`, with all local source imports retained. No Mathlib download is required.
- C++ controls require a C++17 compiler. The CPU engine review additionally uses OpenMP and the pinned upstream v8 source archive; its report provides exact commands.
- CaDiCaL is required only for CaDiCaL discovery runs, not for replaying the retained positive-hint LRAT proof.
- LaTeX is needed to render the retained manuscript `.tex` sources. Rendered PDF duplicates are omitted.

Two historical discovery scripts contain environment-specific search paths. In `research/exist_periodic_bulk_cadical.py`, set `CADICAL` to the installed CaDiCaL executable. In `research/main_existence_attempt/boundary_resume/new_clock/synthesis.py`, the historical `sys.path.insert` names the original Z3 environment; install the pinned Python requirements in the active environment (the nonexistent old path is harmless), or adjust that line. These original source bytes were retained to preserve recorded hashes. Historical report commands mentioning `/workspace/.../lean` should use the absolute path to the reader's own Lean 4.19.0 executable.

## Direct certificate and arithmetic replays

From `proofs/research/`:

```sh
python3 main_existence_attempt/ancestry_direct_pass/language/check_terminal_certificate.py
python3 main_existence_attempt/ancestry_direct_pass/root_nfa_audit.py
python3 main_existence_attempt/ancestry_direct_pass/delay/check_delay.py
python3 main_existence_attempt/return_pass/root_probability_audit.py
python3 main_existence_attempt/conditional_score/check_lrat.py any
```

The first two use the retained 6,680-state NFA and complete 8,396-flag witness certificate. The delay check recomputes all 289 ordinary additions, not just the endpoint. The LRAT checker reads the retained exact CNF and proof trace; it does not invoke a SAT solver.

Further independent finite certificates, with the requirements appropriate to their imported modules, are documented in:

- [Boundary reverse-language proof](research/main_existence_attempt/boundary_resume/reverse/SOFIC_ALL_PERIOD_PROOF.txt) and [root arithmetic audit](research/main_existence_attempt/boundary_resume/root_sofic_audit.py).
- [Arbitrary-group certificate](research/main_existence_attempt/group_invariant/README.md), including the ordinary and automorphism/conjugacy versions.
- [Neutral-interface exclusion](research/persist_neutral_interface_exclusion.txt) and `persist_wake_eroder_check.py --all`.
- [Correlated-language method](research/main_existence_attempt/return_pass/language/METHOD_AND_PROOF.md) and its [status/reproduction commands](research/main_existence_attempt/return_pass/language/STATUS.md).

## Lean source builds and axiom scope

Set `lean_executable` to an absolute path. From `proofs/research/`:

```sh
lean_executable=/absolute/path/to/lean
"$lean_executable" --version
"$lean_executable" -o Lychrel196Research.olean Lychrel196Research.lean
LEAN_PATH=. "$lean_executable" astra_root_axiom_audit.lean
python3 main_existence_attempt/smart_pass/uniform_lean/compile_all.py "$lean_executable"
python3 main_existence_attempt/ancestry_direct_pass/lean/check.py "$lean_executable"
python3 main_existence_attempt/boundary_resume/lean/compile_all.py "$lean_executable"
```

The uniform checker copies the unchanged standalone dependency from `continuation/LychrelDigitSums.lean` and compiles the entire ten-module dependency chain in a temporary directory, then audits its main theorem declarations. The ancestry checker rebuilds that dependency and its new module from source. The boundary checker builds all seven local modules.

The canonical arithmetic, uniform-escape and ancestry results have the ordinary logical axiom scope recorded in their reports. Boundary finite computations additionally depend on `Lean.ofReduceBool` through `native_decide`. The distinction must be retained when describing formal verification. Generic theorem interfaces have explicit hypotheses; no formal file supplies the missing decimal Lychrel existence witness.

The older split sidecars are also preserved. They are historical module sources; the standalone integrated file is the normal entry point for their integrated results. Every non-`Std` Lean import resolves to a retained source file.

## Regenerating omitted large outputs

The publication omits large generated tables rather than silently truncating them. Saved outcomes, independent-check records, source hashes, exact search parameters in reports, and the original generators remain available. A checker that reads an omitted table must first have that table regenerated. The following are representative complete workflows; detailed bounds remain in the linked reports.

| Omitted data family | Regeneration and verification entry point |
|---|---|
| Large D3/D4 elimination tables and image-refined large kernels | The depth-three and depth-four observation tables themselves are retained; `observation_depth4.json` was added for the correlation certificate replay. For omitted elimination/kernel data, [Language STATUS.md](research/main_existence_attempt/return_pass/language/STATUS.md) gives `residual_kernel.py`, the listed `compact_kernel.py` continuation, then `check_eliminations.py` with the documented flags. The original D4 cap result remains UNKNOWN; the separate extended run is the completed exclusion. |
| Large reverse-525, all-bulk and forward-join graphs | [Reverse-525 status](research/main_existence_attempt/boundary_resume/reverse525/STATUS_AND_POWER_LIFT_PROOF.txt) and [forward-join proof](research/main_existence_attempt/boundary_resume/forward_join/STATUS_AND_PROOF.md): retained search programs regenerate the exact width-limited graphs before the audit programs read them. |
| Incomplete one-tile, direct-flow, context and monoid states | [Resumed status](research/main_existence_attempt/RESUMED_STATUS.txt) and [conditional-score report](research/main_existence_attempt/conditional_score/README.md): rerun the specified bounded searches. Timeouts/caps are UNKNOWN and need not recur at the same wall-clock instant on different machines. |
| Constructive bulk mixtures, front-language dumps and symbolic defect runs | [Constructive report](research/main_existence_attempt/constructive/constructive_report.md), [front status](research/main_existence_attempt/smart_pass/constructive/STATUS.md), [defect report](research/main_existence_attempt/defect_family/defect_family_report.md). Claims apply only to the reported templates/ranges. |
| Generated CNF/SMT inputs, periodic-bulk or conditional-threshold trials | Original generators and bounded outcome records, indexed in [INVENTORY.tsv](INVENTORY.tsv). The checked conditional-parity CNF/LRAT pair is retained in full as an exception. |
| CPU engine binaries and scratch cases | [CPU_REVIEW.md](research/main_existence_attempt/ancestry_direct_pass/repository_review/cpu/CPU_REVIEW.md) gives the pinned archive extraction, compiler flags, binary names and exact run commands. |
| Driver and hybrid-writer structural probes | [CERTIFICATION_REVIEW.md](research/main_existence_attempt/ancestry_direct_pass/repository_review/certification/CERTIFICATION_REVIEW.md) gives standalone build/run commands against the pinned unmodified headers. These are CPU source/probe findings; no GPU execution is implied. |

`OMITTED_OUTPUT_SUMMARIES.json` records only structural metadata extracted from omitted JSON outputs: scalar metadata and array/object sizes. It is not a substitute certificate and is not proof of any mathematical claim.

## Correlation-pass source and certificate replays

The [current aggregate](research/main_existence_attempt/correlation_pass/CORRELATION_PASS_STATUS.md) and [root review record](research/main_existence_attempt/correlation_pass/ROOT_REVIEW.json) connect the new reports with their audited evidence. From `proofs/research/`:

```sh
python3 -B main_existence_attempt/correlation_pass/language/check_correlated_collisions.py --certificate correlated_cegar_pairs5_result.json
python3 -B main_existence_attempt/correlation_pass/language/check_correlated_collisions.py
python3 -B main_existence_attempt/correlation_pass/language/focused_checks.py
python3 -B main_existence_attempt/correlation_pass/language/check_antichain.py
python3 -B main_existence_attempt/correlation_pass/constructive/seam_overlap.py
python3 -B main_existence_attempt/correlation_pass/constructive/variable_overlap.py
python3 -B main_existence_attempt/correlation_pass/constructive/delayed_overlap_gate.py
python3 -B main_existence_attempt/correlation_pass/free_clock/check_prefix_extension.py
python3 -B main_existence_attempt/correlation_pass/free_clock/check_arithmetic_controls.py
python3 main_existence_attempt/correlation_pass/lean/check.py "$lean_executable"
```

The antichain checker reads the retained `antichain_depth0.json.gz` directly; the release manifest hashes its compressed bytes. The collision and focused checkers read the unchanged `return_pass/language/observation_depth4.json`, now retained because it is an explicit certificate dependency. The earlier safe-two NFA, terminal-witness corpus, observer-zero table and source modules remain at their original paths. No discovery run is needed to reconstruct these inputs before the listed checks.

The Lean checker rebuilds the unchanged standalone dependency plus all four new mathematical modules and audits all 63 new theorem declarations. The exact source hashes and root's separate recompilation records are retained. This is a supporting-theorem audit, not a proof of the universal delay bound or of decimal Lychrel existence.

The generated `free_clock/*_depth*.json` cyclic graphs are omitted. Their initial, forward-bisimulation and bidirectional runs are reproducible with the exact commands in [free_clock/STATUS.md](research/main_existence_attempt/correlation_pass/free_clock/STATUS.md); all small candidate, extension, arithmetic and cap summaries remain present. A completed depth is not an all-depth exclusion, and the final depth-16 graph cap remains UNKNOWN.

## Early renewal tail certificates

The [tail report](research/main_existence_attempt/renewal_pass/tails/STATUS.md) supplies written exact first-hit proofs for five specified core branches. From `proofs/research/main_existence_attempt/renewal_pass/tails/`, run:

```sh
python3 -B check_symbolic_tails.py
```

This independent standard-library checker reads the complete retained symbolic certificate, verifies 26 all-parameter polynomial transitions, checks the explicit finite lower boundaries, and runs 208 ordinary-integer transition controls. The parameter conclusion comes from symbolic identities and run-length positivity, not from those sample controls. The staged publication replay reproduced `symbolic_tail_audit.json` byte for byte.

All ten files in this early batch are retained, including raw census results, failed affine-domain certificate attempts, generator configurations and logs. Optional regeneration uses `finite_tail_census.py` and `symbolic_tail_certificates.py`; the latter imports the already retained `../../smart_pass/collision/orthant_runs.py`. The 216-case census horizon is 512, and unresolved outcomes remain UNKNOWN. No Lean installation is needed for this batch; it adds no Lean theorem.

## Early renewal formal gate checkpoint

Use Lean 4.19.0. From the repository root, replace the executable path below:

```sh
python3 proofs/research/main_existence_attempt/renewal_pass/lean/check.py /absolute/path/to/lean
python3 proofs/research/main_existence_attempt/renewal_pass/lean/root_recheck.py /absolute/path/to/lean
```

The full checker builds the six original source modules and generated audit module, then audits all 49 new gate theorem declarations transitively. It verifies hashes before and after compilation, excludes proof placeholders/custom axioms/native_decide in the new source, and permits only the recorded standard logical axioms. Its five unchanged dependency sources are already published under `continuation/` and `main_existence_attempt/correlation_pass/lean/`. The second command reuses the first command's source-hash-checked dependency build, independently recompiles the gate, and repeats the complete theorem audit. Both reviewed records report PASS; their exact trust boundaries are retained.

These commands regenerate `fresh_build/`, `root_build/`, audit sources and audit logs. Use a working copy if preserving the originally published log bytes during replay. The original `dev_check.py` retains its historical absolute compiler path and prior development-build reference; it is provenance, while the two commands above are the portable release checks. All five development attempt logs and the available final source snapshot are retained. Only duplicate source copies and compiled/transient build products are omitted, individually inventoried. The separate unfinished prefix branch is outside this gate checkpoint.

The [formal handoff](coordination/2026-10-14-formal-gate.md) states the exact domain and arithmetic conclusions. `return_not_in_domain` excludes immediate reuse of this source's original six-core Domain, not every broader gate. No recurrence, p>=5 overflow formula, later-hit classification, decimal Lychrel existence or assertion for 196 is proved by this formal gate.

## Checked collision follow-up and lossless trace archive

Before any driver/family replay, run from repository root:

```sh
python3 proofs/contributions/2026-10-14-collision-review/restore_driver_trace.py
python3 -B proofs/contributions/2026-10-14-collision-audit/verify_driver_trace.py
python3 -B proofs/contributions/2026-10-14-driver-family/check_family.py
```

The restore command verifies five ordered parts, the exact original gzip,
and its complete decoded stream. See [all commands and proof scopes](coordination/2026-10-14-collision-results.md). The independent external-gate
rebuild uses the same Lean 4.19.0 pin. No partial trace is treated as a
complete certificate, and no finite driver is treated as infinite safety.

## Seven-step reset, carry clocks and collision mass

The [checked handoff](coordination/2026-10-14-seven-step-results.md) lists
commands for both fresh Lean builds, the complete retained reset catalog,
independent middle/operator checks and fixed-clock audit. The two gzip
catalogs are complete; inventory records include decoded hashes and exact
recovery commands. No growing-middle condition is inferred from a finite
initial-width census.

## Complete seven-step obstruction certificate

The [result handoff](coordination/2026-10-14-seven-step-obstruction-results.md)
lists all three independent graph audits and the fresh eight-theorem Lean
bridge build. Five complete gzip artifacts retain the direct graph, all
independent direct controls, and correlated-lift checkpoints. Their decoded
identities and recovery commands are recorded in the inventory. The
all-width theorem uses actual-orbit inclusion plus the complete finite
rank certificate, not a finite-width middle census.

## All-branch seven-step 44 hierarchy and finite bound

The [shared result handoff](coordination/2026-10-14-broader-return-results.md)
lists three independent audit commands for all control branches, every
raw/recurrent graph through width fourteen, and the complete weighted
condensation certificate. All 28 gzip artifacts are retained losslessly
with original-byte hashes and recovery commands in the inventory. The
finite bound includes all component transients and physical-width growth.

## Scalar clock, capped probes and weighted-path Lean proof

The [shared scalar handoff](coordination/2026-10-14-scalar-clock-results.md)
lists the complete arithmetic/rank audits, capped-probe inventory verifier
and fresh fifteen-theorem Lean build. Every complete gzip has compressed
and decoded identities and a recovery command. Two forensic truncated
streams are stored exactly as binary evidence and intentionally have no
decompression command; canonical repaired graphs match original hashes.

## Completed renewal pass

From the repository root, the three additional formal modules can be rebuilt with Lean 4.19.0 (replace the executable path):

```sh
python3 proofs/research/main_existence_attempt/renewal_pass/lean/prefix/check.py /absolute/path/to/lean
python3 proofs/research/main_existence_attempt/renewal_pass/lean/incoming_carry/check.py /absolute/path/to/lean
python3 proofs/research/main_existence_attempt/renewal_pass/lean/raw_symmetry/check.py /absolute/path/to/lean
```

Each directory also retains a `root_recheck.py`, its complete independently run audit and exact source hashes. The early gate's commands above complete the four-module, 135-declaration audit. Run in a disposable checkout: build directories and logs are regenerated. Historical `dev_check.py` files and failed source snapshots preserve development provenance and may require their original development environment; the completed `check.py` commands are the portable checks. Failed snapshots are not certified final theorem sources.

Standard-library arithmetic/certificate checks include:

```sh
python3 -B proofs/research/main_existence_attempt/renewal_pass/language/check_inverse_ladder.py
python3 -B proofs/research/main_existence_attempt/renewal_pass/language/check_prefix_obstruction.py
python3 -B proofs/research/main_existence_attempt/renewal_pass/language/check_exploration_archive.py
python3 -B proofs/research/main_existence_attempt/renewal_pass/seam_audit/check_overflow_local.py
python3 -B proofs/research/main_existence_attempt/renewal_pass/seam_audit/check_short_controls.py
python3 -B proofs/research/main_existence_attempt/renewal_pass/seam_audit/check_positive_safety.py
python3 -B proofs/research/main_existence_attempt/renewal_pass/external_review/check_collision_safety_examples.py
```

The language checkers use the retained cross-pass NFA, observer tables, collision helpers and original tail certificates at their original relative paths. The complete language exploration, all 5,204 affine comparisons, 2,737 seam controls, 58,221 partition controls and 2,495 active-safety controls are retained in lossless gzip archives. Their source generators, exact configurations, failed cases and independent audit records accompany them. Consult each branch's STATUS report before optional regeneration; no capped search must be rerun to read the established claim.

The raw-symmetry and incoming-carry modules prove the specified actual decimal/local statements. The full concatenated polynomial identity, generalized twenty-core classification and combined independent-closure safety corollary remain written proofs. The 22-seed/196 join search remains a finite 1,500-addition experiment. The external 10,000-state trace remains preserved with its original full replay record; this publication checks unchanged Git-object identity for its five large parts rather than claiming a new local trace replay.

## Refined component-specific bounds

The [latest bound handoff](coordination/2026-10-14-component-bounds-results.md)
lists independent replay of all 31 induced jobs and both fresh generic
Lean hierarchy builds. The complete job certificate preserves every
child restriction, induced edge, projection and weighted rank. Existing
scalar/broader graph checkpoints are read unchanged. The 18- and
19-declaration formal audit totals include the same fifteen published
weighted-path prerequisites; this package adds seven declarations.

## Arbitrary-block all-base seams and interval safety

The [shared seam handoff](coordination/2026-10-15-general-base-seam-results.md)
lists the decimal partition replay, complete all-base controls, independent
block-response audit and fresh nine-declaration Lean build. Both complete
gzip artifacts and all six binary failures are retained. The interval
review pins the final supplemented mathematical proof; the earlier
arithmetic proof hash remains unchanged as development provenance.

## Intrinsic seam and finite-seed continuation

Use a disposable checkout because the checkers recreate audit outputs. From `proofs/research/`, with `LEAN_BIN` set to an absolute path to Lean **4.19.0**:

```sh
python3 -B main_existence_attempt/continuation_pass/lean/check.py "$LEAN_BIN"
python3 -B main_existence_attempt/continuation_pass/finite_seed/check_finite_seed_obstructions.py
```

The first command rebuilds all five original dependency/new-module sources and its axiom audit, checking all 31 new theorem declarations and 5 definitions. All source dependencies are retained at their original relative paths. The second repeats the finite controls for the written all-parameter countermodel and safe-fiber proofs; enumeration alone is not their all-parameter proof. `root_review/lean_rebuild.json` and `finite_seed_review.json` record the separate root audit and exact accepted source hashes. The original `root_review/rebuild_lean.py` preserves the historical compiler path; the portable formal command above accepts your compiler path explicitly and covers the same sources and declarations. Original development failures are historical records, not expected successful build targets.

## Complete sharp-clock formalization and reciprocal audit

The [shared formal checkpoint](coordination/2026-10-15-sharp-kernel-and-renewal-audit.md)
lists the full fresh Lean runner, independent rank audit, resume fixtures
and exact-source external 42-theorem rebuild. The expensive finite checks
are retained with explicit source/object/dependency lineage and a documented
one-time reconciliation. Legacy records lacking dependency fingerprints
are rejected; the supplied history does not claim an additional independent
full kernel build. All source snapshots and compiler/audit logs are retained.

## Four-state whole-word language certificate

From `proofs/research/main_existence_attempt/continuation_pass/safe_language/` in a disposable checkout:

```sh
python3 -B restore_artifacts.py .
python3 -B check_lrat.py dfa4_neg2
python3 -B check_encoding.py dfa4_neg2
python3 -B restore_artifacts.py /tmp/safe_language_integrity --all --verify-only
```

The default restore creates the exact primary CNF and complete refutation. The first checker proves UNSAT of those bytes; the second independently audits their complete clause multiset and arithmetic semantics. The all-width argument is in `METHOD_AND_PROOF.md`. `--all --verify-only` streams and verifies all six original artifacts, including the incomplete five-state trace, without retaining expanded outputs. To repeat the root source-freeze check after restoring the primary artifacts, run `python3 -B ../root_review/check_primary_sat.py`. No solver is required for these replays. Discovery commands and the 180-second cap are preserved in the source and status. The five-state trace is not a refutation.

## Shared seam and formal bridge replay

The [checkpoint](coordination/2026-10-15-seam-persistence-and-formal-bridges.md)
and individual README files specify exact Lean 4.19.0 runners, finite control
checks and independent audits. All new formal sources have fresh dependency
build reports with standard-axiom checks. Historical failed drafts, earlier
successful checkpoints and their logs remain available. Source-only external
reviews are explicitly distinguished from independent fresh compilation.

## Local-weight, mixed-band and zero-exterior follow-ups

From `proofs/research/` in a disposable checkout:

```sh
python3 -B main_existence_attempt/continuation_pass/finite_seed/check_folded_weights.py
python3 -B main_existence_attempt/continuation_pass/seam_persistence/verify_neutral_quotient.py
python3 -B main_existence_attempt/continuation_pass/safe_language_followup/verify_four_band.py
python3 -B main_existence_attempt/continuation_pass/lean/zero_exterior/check.py "$LEAN_BIN"
```

`LEAN_BIN` must be an absolute Lean 4.19.0 path. That command independently rebuilds the retained decimal dependency, the zero-exterior module and all 15 declaration audits. Root's historical `recheck_zero_exterior.py` additionally depends on its earlier `lean_build` output and preserves the original compiler path; its receipt explicitly records reuse of the exact root-rebuilt dependency. The graph checkers use full retained certificates and ordinary integer arithmetic; written all-gap identities provide the universal bridge. These replays do not search larger interfaces or assert a recurrent safe construction.

## All-base intrinsic criterion

Run the [intrinsic package checker](contributions/2026-10-15-base-intrinsic-formal/check.py)
with Lean 4.19.0 following its README. It rebuilds nine exact sources and audits
109 declarations, including 82 prior prerequisites. Full logs, rejected drafts,
independent review and source identities remain in the package.

## Actual hierarchy and construction replay

The [shared checkpoint](coordination/2026-10-15-actual-hierarchy-and-renewal.md)
links the fresh Lean dependency/audit runners, independent sequential carry
checks and finite congruence-path verifier. The path gzip retains every state;
its inventory records compressed and decoded hashes and recovery command.
The external four-state reciprocal review is source-only and does not claim
another LRAT run. The numerical hierarchy table checks remain separate work.

## Positive gate and variable-return certificates

From `proofs/research/` in a disposable checkout:

```sh
python3 -B main_existence_attempt/continuation_pass/variable_return/check_affine_catalogue.py
python3 -B main_existence_attempt/continuation_pass/variable_return/check_regeneration_graph.py
python3 -B main_existence_attempt/continuation_pass/variable_return/check_regeneration_gate.py
```

The exact frozen source and dependency hashes are in `variable_return/FROZEN_MANIFEST.json`. The three commands independently verify the affine all-time catalogue reduction, the complete 83,679-state graph, and the nine-step positive-gate trace. Root ran them in a duplicate copy and obtained byte-identical audit outputs. The generator and finite multiplicative/prefix probe configurations, full results, failure and editorial history remain available; these finite probes have their stated restricted domains.

The accepted extensions can be checked from `proofs/research/`:

```sh
python3 -B main_existence_attempt/continuation_pass/seam_persistence/followup_absorbing_core/check_absorbing_core.py
python3 -B main_existence_attempt/continuation_pass/periodic_bulk_followup/verify_periodic.py
python3 -B main_existence_attempt/continuation_pass/lean/regeneration_gate/check.py "$LEAN_BIN"
```

Use an absolute Lean 4.19.0 path. The formal command rebuilds all six sources plus the declaration audit. Root's historical formal replay uses its exact previously rebuilt dependencies and original compiler path; the review explicitly distinguishes that reuse from the branch clean rebuild. The combined `root_review/recheck_absorbing_and_periodic.py` has both source bundles present and recreates its independent outputs in disposable duplicate directories. No additional discovery search is required to replay the accepted certificates.

## Full high-region return verification

The [checkpoint](coordination/2026-10-15-full-high-return-bound.md) lists
complete finite generation, independent arithmetic/rank checks, explicit
witness replay and the small Std-only Lean certificate. All four gzip
artifacts retain decoded hashes and recovery commands in INVENTORY.json.
The actual-orbit reduction remains written; reciprocal external reviews
are source-only. No safe-three sharpness or infinite-orbit claim is made.
