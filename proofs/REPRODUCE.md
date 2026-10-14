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
