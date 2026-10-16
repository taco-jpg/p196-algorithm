# Independent integration review: PR #111

Reviewer: Agent #11, session `046f9285a650`, independent specialist `/root/review111`. This reviewer authored none of the submitted mathematical sources, made no repository or remote mutations, and claimed no exclusive integration slot. This is an internal review, not external peer review.

**Recommendation: acceptable to merge the frozen contribution within its finite list-algorithm and one-step quotient scope, using the explicitly attributed retained strict Lean evidence below.** No source-level correctness blocker was found. This reviewer did not complete a new Lean run: the supplied runtime failed even at `--version`. The current source/evidence integrity checks and finite Python diagnostics were executed successfully by this reviewer. No claim about decimal Lychrel existence or 196 follows.

## Exact review boundary

- PR head H: `bf4ff749000a6995e1755e37b59988ef362bae16`.
- Integration base B: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.
- Merge base: `95a17ceeaba51b7d2c14645401df5159a3d483d1`.
- Root-provided clean combined tree: `480cf6baefa41e32c0a57dc6b45dd980dc86df78`.
- All 159 changed paths are additions. Every changed blob is identical between H and the combined tree. All 14 registered source blobs, the scoped registry, and the checker are also identical in that tree.
- The three new mathematical modules contain 453 source lines, 26 explicitly named theorems and 10 safe transparent definitions. The other new root file is the scoped registry. The 155 contribution paths contain retained source versions, failures, successful logs, receipts, scripts and scope documents.

Full diff coverage: 44 Lean files, 34 JSON files, 8 Markdown files, 68 logs and 5 Python files, totaling 1,094,880 source/evidence bytes. The three current modules were read in full; relevant prerequisite definitions and proofs, original Python loops and written normalization statement were inspected. Historical source duplicates were compared byte-for-byte, all 154 entries in `EVIDENCE.json` were checked for byte count and SHA-256, and every changed path was retained. The only unlisted contribution path is the evidence manifest itself. Historical checkpoint hashes remain historical and are not confused with the final registry pins. No author failure is substituted for current accepted source.

## New mathematical claims and actual semantics

The original `Agent8.Word` is `List Nat`; `Bounded w 18` bounds every coefficient. `normalize` scans left-to-right using remainder and quotient by ten, retains the actual final carry, and `stepWord` pairs the normalized digits with their reversal. `periodicWord B H w k` is exactly `B ++ pow w k ++ H ++ pow w.reverse k ++ B.reverse`. The contribution reuses these definitions, including the actual carry and the literal exponent-three raw slices; it does not introduce a replacement arithmetic model.

The original target algorithm is retained as `frozen/proofs/periodic_word_quotient__8404d0a63dd1fa13.py`, SHA-256 `122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425`. Its two loops remove complete four-symbol suffixes from the exterior and complete nonoverlapping mirrored pairs from the center. The original written normalization subsection is retained as `original-METHOD_AND_PROOF.md`, blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`, SHA-256 `45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559`.

`stripPeriodSuffixAux_spec` proves reconstruction and stopping under the explicit fuel condition `B.length ≤ fuel`. Each removal shortens by a positive period length. The public operation supplies input-length fuel, so maximality describes the full loop and does not hide an arbitrary cutoff. Order is preserved. The empty period is explicitly returned unchanged with count zero; the maximality theorem requires a nonempty period.

`stripPeriodCenter_test_iff` establishes that the reconstruction equality test is exactly the original length/prefix/reversed-suffix condition. The length condition prevents overlapping removals. A successful nonempty removal strictly decreases length, which makes input-length fuel sufficient. The center auxiliary can count empty wraps at arbitrary fuel, but the public empty-period branch bypasses it. Decomposition is unconditional; maximality correctly assumes a nonempty period. Empty residual centers and exteriors, all-nine words, constant words and nonprimitive periods are allowed. Maximality is relative to the supplied whole period, not a unique representation modulo rotations or primitive roots.

`periodicWord_absorb` is an arbitrary-word list identity including zero exponents. It combines powers of the same word; it does not commute unrelated words. `raw_guard_of_stripped` and `stripped_width_balance` are conditional interfaces with explicit decomposition hypotheses. `quotient_step_bounded` supplies those hypotheses using the executable stripping functions. Its remaining assumptions are exactly input coefficient bounds 18, period length four, and `k ≥ 3`. Its result is the original `stepWord` image expressed with the computed exterior, center, raw period and natural exponent `(k-2)+outerPeriods+centerPeriods`.

`quotient_irreducible` proves both whole-period stopping predicates. The raw period is nonempty because the existing raw-length theorem gives length four. `exponentDelta` is the integer `u+v-2`; the width balance casts lengths to `Int`, preserving negative shifts. `quotient_exponent_accounting` proves the target natural exponent is at least one and agrees with `k+delta` after casting. It does not establish a target exponent of at least three.

The full existing `ValidPeriodic` predicate additionally includes center symmetry, odd-center evenness and a positive outside coefficient. Its output preservation is not proved here. Nor is safety, an ordinary canonical numeral bridge, nonpalindromicity, iteration in the guard domain, a finite-interface cycle, an infinite lift, or the P196 conjecture proved. The original Python `transition` has valid-and-safe assertions beyond these algebraic endpoint hypotheses. The contribution does not discharge all those assertions, and its documentation explicitly preserves that boundary. Bounds and symmetry of stripped pieces do not imply every missing valid-state or safety obligation.

## Evidence actually executed in this review

1. `python -B static_evidence_audit.py`: PASS. Validates frozen and combined source identities, exact import closure, comment-aware forbidden-token scan, all evidence entries, all retained command/log hashes, all 1,343 transitive theorem audit rows, 36 new public declarations, source manifests and compiler-file hashes. The original first attempt misparsed multiline axiom lists; its source and traceback are retained in `static-attempt-001/`. The corrected parser splits commas and strips whitespace.
2. The original diagnostic script was inspected before execution, then run unchanged with `python -B frozen/proofs/contributions/agent-1/periodic-block-strip-20261016/review/diagnostic_controls.py`. PASS: 12 generic cases, 14 actual raw inputs at five exponents each, 70 actual exponent comparisons, both carry values, shifts -2/-1/0, and minimum target exponent one. Six cases also exercised the original valid-and-safe transition. These are finite diagnostics, not kernel evidence or an exhaustive search.
3. All 159 changed blobs were compared against the combined tree in a separate read-only check, recorded in `combined-159-identity.json`.
4. An independent empty-output strict build was prepared in `independent_rebuild.py`, but the runtime identity command exited 1 with `error: failed to locate application`. `fresh-001/logs/version.log`, `fresh-001/failure.txt`, the command receipt and console log retain this failure. Zero Lean source modules were compiled by this reviewer, and the drafted environment census was not executed. No escalation or bypass was attempted by this reviewer.

## Retained Lean evidence deliberately reused

The accepted strict execution is `review/clean-001/` in the frozen contribution, performed by Agent #1's separate `research_status` specialist in the authors' session/account. It is not this reviewer's run. The inspected `review/replay.py` creates an empty build directory, copies only the fourteen source files, sets `LEAN_PATH` to that directory and compiles every module in dependency order before its audit. It contains no project-object copy step. All 15 retained commands (14 modules plus audit) have `--trust=0 -j1 -DElab.async=false`, exit code zero and matching retained log hashes.

That run records Lean 4.19.0, commit `6caaee842e94`, Release, and binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. This reviewer independently hashed the supplied read-only binary and four shared libraries, and all match the retained parent compiler inventory. The independent strict run pins the binary and version; the separate parent inventory supplies shared-library hashes. This byte comparison does not change the current execution failure into a successful identity check.

The retained audit enumerates all theorem constants by defining module across the exact 14-module closure, including generated/private proof constants. This reviewer independently parsed 1,343 unique rows, confirmed every selected module contributes rows, and checked every axiom set against `{propext, Classical.choice, Quot.sound}`. Their union is exactly that standard foundational set. Thirteen generated unsafe implementation axioms from the old `LychrelDigitSums` module are logged separately; none occurs in the transitive axiom set of any audited theorem. No `sorryAx`, `native_decide`, `Lean.ofReduceBool`, custom safe axiom or other unsupported axiom is accepted in these chains.

The generic repository checker was inspected, but is not used as evidence of an explicit trust-zero command because its compiler argv omits `--trust=0`. The retained separate reviewer script does include that flag. No repository-wide theorem-catalogue completion is claimed; the scoped registry correctly keeps `catalogue_complete=false` and does not modify the accepted global registry.

## Public declaration coverage

All 26 newly named theorems have direct rows in the retained transitive axiom audit. All 10 new definitions are ordinary safe transparent definitions with inspected bodies and no `unsafe`, `partial`, `extern`, `implemented_by`, opaque or custom axiom declarations. Each occurs explicitly in the type of the audited theorem identified below; the theorem axiom collector traverses referenced definitions. This is coverage of every new public declaration and its accepted mathematical chain, not a claimed fresh census of every safe definition in the entire imported environment.

| Module | Kind | Declaration | Retained audit witness |
|---|---|---|---|
| `Agent1PeriodicOuterStrip` | def | `stripPeriodSuffixAux` | `stripPeriodSuffixAux_spec` |
| `Agent1PeriodicOuterStrip` | def | `stripPeriodSuffix` | `stripPeriodSuffix_spec` |
| `Agent1PeriodicOuterStrip` | theorem | `stripPeriodSuffixAux_spec` | `stripPeriodSuffixAux_spec` |
| `Agent1PeriodicOuterStrip` | theorem | `stripPeriodSuffix_spec` | `stripPeriodSuffix_spec` |
| `Agent1PeriodicOuterStrip` | theorem | `stripPeriodSuffix_maximal` | `stripPeriodSuffix_maximal` |
| `Agent1PeriodicOuterStrip` | theorem | `stripPeriodSuffix_empty_block` | `stripPeriodSuffix_empty_block` |
| `Agent1PeriodicOuterStrip` | theorem | `stripPeriodSuffix_length` | `stripPeriodSuffix_length` |
| `Agent1PeriodicOuterStrip` | theorem | `stripPeriodSuffix_bounded` | `stripPeriodSuffix_bounded` |
| `Agent1PeriodicCenterStrip` | def | `stripPeriodMiddle` | `stripPeriodMiddle_wrap` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodMiddle_wrap` | `stripPeriodMiddle_wrap` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_test_iff` | `stripPeriodCenter_test_iff` |
| `Agent1PeriodicCenterStrip` | def | `stripPeriodCenterAux` | `stripPeriodCenterAux_decomposition` |
| `Agent1PeriodicCenterStrip` | def | `stripPeriodCenter` | `stripPeriodCenter_decomposition` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_empty` | `stripPeriodCenter_empty` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenterAux_decomposition` | `stripPeriodCenterAux_decomposition` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodMiddle_length_lt` | `stripPeriodMiddle_length_lt` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenterAux_maximal` | `stripPeriodCenterAux_maximal` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_decomposition` | `stripPeriodCenter_decomposition` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_maximal` | `stripPeriodCenter_maximal` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_length` | `stripPeriodCenter_length` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_length_le` | `stripPeriodCenter_length_le` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_bounded` | `stripPeriodCenter_bounded` |
| `Agent1PeriodicCenterStrip` | theorem | `stripPeriodCenter_symmetric` | `stripPeriodCenter_symmetric` |
| `Agent1PeriodicQuotient` | theorem | `periodicWord_absorb` | `periodicWord_absorb` |
| `Agent1PeriodicQuotient` | theorem | `periodicWord_length` | `periodicWord_length` |
| `Agent1PeriodicQuotient` | theorem | `raw_guard_of_stripped` | `raw_guard_of_stripped` |
| `Agent1PeriodicQuotient` | theorem | `stripped_width_balance` | `stripped_width_balance` |
| `Agent1PeriodicQuotient` | def | `quotientOuter` | `quotient_step_bounded` |
| `Agent1PeriodicQuotient` | def | `quotientCenter` | `quotient_step_bounded` |
| `Agent1PeriodicQuotient` | def | `outerPeriods` | `quotient_step_bounded` |
| `Agent1PeriodicQuotient` | def | `centerPeriods` | `quotient_step_bounded` |
| `Agent1PeriodicQuotient` | def | `exponentDelta` | `quotient_width_balance` |
| `Agent1PeriodicQuotient` | theorem | `quotient_step_bounded` | `quotient_step_bounded` |
| `Agent1PeriodicQuotient` | theorem | `quotient_irreducible` | `quotient_irreducible` |
| `Agent1PeriodicQuotient` | theorem | `quotient_width_balance` | `quotient_width_balance` |
| `Agent1PeriodicQuotient` | theorem | `quotient_exponent_accounting` | `quotient_exponent_accounting` |

## Evidence locations and recommendation limits

- `frozen/`: complete submitted diff contents plus the exact prerequisite closure, policy, registry, inspected checker and original target Python.
- `freeze.json`, `source-closure.json`, `full.diff`: frozen provenance and original source identities.
- `static-evidence-audit.json`: all source pins, all 36 declaration coverage entries, per-module theorem counts, all 13 implementation-axiom names and verified runtime hashes.
- `diagnostics-fresh.stdout.json`, `diagnostics-fresh.stderr.log`: complete actually executed finite diagnostics.
- `fresh-001/`, `independent_rebuild.py`, `independent_rebuild.console.log`: failed fresh runtime attempt and unexecuted strict-build/census plan.
- `static-attempt-001/`: preserved failed axiom-log parser attempt.
- `FILES.json`: complete local evidence byte/hash inventory (excluding itself and reproducible Python caches).

No source correction is required for the finite claims reviewed. A new fresh Lean run remains unexecuted in this session; the recommendation explicitly relies on the inspected and hash-matched retained strict evidence under the authorized reuse policy. The integrator must still apply current exact-head/current-target guards and handle remote publication/merge separately. Any changed mathematical source, imported closure or registry invalidates this scoped source identity conclusion until rechecked.
