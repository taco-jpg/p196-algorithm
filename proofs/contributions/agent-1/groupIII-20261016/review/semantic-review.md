# Independent Group III review: scoped PASS

Reviewer: `/root/research_status/numeric_bridge_review`, acting as an Agent #1 specialist. The reviewer owns only this `review/` directory; no author-source edits, Git writes, or external messages were performed. Results were sent to the parent for attributed coordination relay.

The written Group III two-step delayed repair is covered by the frozen new sources, with no semantic gap found. Independent fresh compilation and the full module-origin axiom audit passed. This is acceptance of the stated finite two-step result, not repository-wide catalogue acceptance or an infinite-orbit conclusion.

## Frozen source and executed verification

| Module | SHA-256 |
|---|---|
| `Agent1GroupIII` | `2adaef1e36b3a56022ac893251436f29c83e1d83d5e52b98a99a6cf7de7f0577` |
| `Agent1GroupIIINumeric` | `d9633f976619f74d569117d9fbb6ddd2907bca4dbf0dd570c802be12aedb023c` |

`clean-001/report.json` records all six original dependency pins, all eight source snapshots and their import closure, compiler identities, exact commands, elapsed times, log hashes, and source-stability checks. All pinned source SHA-256 and Git blob values matched `../source-pins.json`. Both new hashes match the parent's frozen handoff.

The reviewer executed `independent_build.py clean-001`. It created a previously nonexistent build directory, copied the exact eight-module source closure, and compiled every module with official Lean 4.19.0, commit `6caaee842e94`, using `--trust=0 -j1 -DElab.async=false`. `LEAN_PATH` contained only the new snapshot directory. No author or previous project `.olean` was used; the official installed Lean/Std library was used. All eight compilation commands and the audit command exited zero. Source snapshots and compiler files were unchanged at completion.

The audit checked **1,982 theorem constants**, including dependencies and generated proof auxiliaries. It separately checked and issued literal `#print axioms` for **all 27 new public theorem exports**. Every audited logical dependency is in `{propext, Classical.choice, Quot.sound}`. No unsupported safe axiom was admitted. Fourteen compiler-generated unsafe implementation declarations from unchanged dependencies are separately recorded in the report; none is a theorem's logical axiom dependency. No new root contributes such an implementation declaration. Source scanning rejected `sorry`, `admit`, custom `axiom`, `native_decide`, `ofReduceBool`, and `skipKernelTC` tokens outside comments/strings.

The audit and lexical scanner follow the retained repository verifier's approach; this was an independent clean execution, not a claim of independently designed verification infrastructure. The count 1,982 is not a count of new mathematical discoveries.

## Semantic findings on the compiled snapshot

References below use the immutable files in `clean-001/source/`.

1. **Exact domain and shortest boundary.** `Agent1GroupIII.lean:19–21` uses all natural `r>=1`, all `p=1..4`, and precisely the seven intended `(u,v)` pairs. The original Group I domain is unchanged. `sixWord` at lines 24–29 gives the six central coefficients at `r..r+5`, with exterior at `0,2r+5`. `returnedComponent` at lines 34–35 is the written component `4p · 0^(r-1) · (2,4u-39,4v-17,4v-17,4u-39,2) · 0^(r-1) · 4p`. All subtractions are nonnegative on the domain. `middle` at lines 38–44 adds coincident contributions, preserving the `r=1` values `2p+1`; the returned overlap correspondingly has `4p+2`. No extra spacer restriction is present.

2. **Actual two-step arithmetic and width.** The carry/no-overflow lemmas, complete finite-column identities at lines 127–173, and `component_two_step_return`/`whole_two_step_return` at lines 175–189 use the original `nextColumns`, `nextWidth`, and `iterPairs`. They prove both complete returned words and the unchanged component/whole widths `2r+6`/`2r+7`. The old generic `two_steps_of_explicit_columns` transports finite-prefix agreement, so irrelevant tails of the intermediate actual word do not become assumptions.

3. **Genuine delayed departure.** `component_next_zeroExtended` at lines 191–198 explicitly truncates the actual component update at its true finite width before applying overlap. `coefficient_defect_exact` at lines 201–207 states the first defect over `Int`, preserving its `-20` center. `actual_intermediate_overlap_fails` at lines 225–231 proves the intended first-step failure with that actual zero-extended component. The comparison word `Phi_1(G(A))` is a coefficient word; the proof does not silently normalize it or assume it is an admissible pair word.

4. **Canonical ordinary integers and arbitrary tails.** `Agent1GroupIIINumeric.lean:12–36` uses the unchanged `DecimalDigits.Canonical` and `FoldedDecimal.representation_next` twice. In the pinned `LychrelDigitSums.lean:907–908`, `Canonical` requires bounded in-width digits, positive width, a nonzero leading digit, and exact positional value; `value_positive` at 693–700 supplies positivity. Zero and leading-zero padding are excluded, trailing zeros are permitted, and values outside the represented width remain irrelevant. The original reversal and step definitions at 85–128, with `reverse10_value`/`step_value` at 739–754, ensure these are actual decimal reverse-and-add iterates.

5. **Correct safety times and universal packaging.** `numeric_two_step_safety` at lines 39–52 applies the original `PairDelayBridge.palindrome_iff_bad` to the initial and first-iterate canonical representations, excluding palindromes at exactly `orbit n 1` and `orbit n 2`. It does not require or assert a nonpalindromic seed. `numeric_delayed_return` at lines 55–62 quantifies arbitrary canonical realizations of the prescribed initial pair word and combines both safety conclusions with a full canonical representation of `orbit n 2` whose pair word is exactly `shiftOne returnedComponent` and whose width is `2r+7`. The literal printed theorem type in `clean-001/logs/IndependentAudit.log:118–129` confirms these are the exported hypotheses and conclusion.

6. **Nonvacuous realization.** `realized_safe_gate` at lines 65–75 invokes the unchanged `valid_word_realizable` after proving initial admissibility. It produces an explicitly positive ordinary integer and canonical digits for every allowed parameter tuple, together with both positive-time safety claims and the exact second-iterate return. No realization or recurrence assumption is left over. The literal exported type appears in the audit log at lines 130–143.

No unresolved correctness issue remains within this reviewed scope. The proof does not assert a third repair, a first palindrome time, persistent exterior reset, infinite safety, Lychrel existence, or a theorem about the complete 196 orbit. A separately named Lean theorem for the normalized-digit defect was part of a suggested proof route; the final proof establishes the requested return directly from full actual carry/column identities. The normalized-digit defect is checked only as finite diagnostic evidence here.

## Separate finite controls

`finite_controls.py`, `finite-controls.log`, and `finite-controls-result.json` retain successful arithmetic diagnostics for all seven cores and all four outer values at `r=1..12,32,128`: **392 parameter tuples and 1,176 canonical realization checks**. The three choices per tuple are not asserted to be distinct. Checks cover both written return identities, first failure, exact coefficient and normalized-digit defects, unchanged widths, returned admissibility, direct integer reversal/addition, and both positive-output safety claims. These remain **finite controls**, not the basis for the all-parameter theorem.

`semantic-review-source-only.md` is retained as the earlier unverified checkpoint. This report supplies its completed verification status without rewriting that historical checkpoint. `clean-001/FILES.json` inventories the executed source snapshots, logs, report, and generated objects.
