# Independent semantic review: normalized carry and certificate accounting

Status: PASS for the exact frozen sources below, following the independent fresh 21-module Lean build and complete axiom/module-origin audit. Reviewer: Agent #6's runtime/reproducibility specialist, separate from the three theorem authors within the same project. This is a same-project independent execution and source review, not an unaffiliated external review.

The source-publication target is remote commit `affa037ad537f3ae66a97008991850ce397f613a`. Its independent byte binding is recorded separately in `publication/`. The source snapshot, compilation, and audit receipts remain immutable.

## Exact reviewed scope

| Module | SHA256 | Bytes | Public theorem declarations | Full theorem constants | Safe definitions |
|---|---|---:|---:|---:|---:|
| NormalizedCarry | `9bfef7cc4d805ac06631c730173da7e2def6611d7f9e0773f1b5ac8cb2891459` | 2612 | 3 | 3 | 0 |
| CertificateCarryAccounting | `32404f75b0b740472825d3510dc52f5294a42ea89b75ddfe4a4b9629c932ec71` | 4211 | 6 | 9 | 0 |
| CarryControls | `abac509aeef647003b9cc5d78ceecd5a9536b907285449d6dea9aa408ed333fb` | 4446 | 7 | 18 | 1 |

There are 16 new public theorem declarations, no explicit private theorem declarations, and one explicitly authored helper definition, `controlState`. The additional three accounting and eleven control theorem constants are generated declarations captured by the full environment audit. Controls also has two generated unsafe implementation definitions, recorded separately from safe definitions. These inventories measure verification coverage; they are not counts of mathematical discoveries.

The complete import closure consists of the unchanged 18-module `CertificateCoordinates` closure plus these three modules. `CertificateFilter` and `CertificateControls` are excluded. All 176,626 source bytes match the frozen registry and live original files. The inherited current path for `ExteriorUpdateLaw` is `proofs/ExteriorUpdateLaw.lean`; its original Agent115 blob remains `db2f3c5ea38b8d49ef7da82631b2ed7a95a29bea`.

## Structural module

`gam_eq_overflow` is an unrestricted compatibility statement. The original `Agent109.Cert.gam` projects exactly the final carry from `Agent109.norm s.B.reverse (Agent109.kOf s.c)`. `Agent6.ExteriorCoordinates.overflow` uses the pair-valued `P196.Agent7.Finite.normalize` with the definitionally equal phase carry. The proof consumes the existing `Agent109.Outer.normalize7_eq`; it does not introduce or replace a normalizer. The interior words `A` and `C` do not affect this carry projection.

`overflow_stripSuffix_of_le18` preserves the numeric final carry under maximal constant-phase suffix removal for any finite natural-coefficient word, assuming only `c ≤ 18`. The proof uses the actual `stripSuffix_spec` decomposition, reverses it in the correct order, and applies the existing `norm_append` and `norm_band_tail`. The removed suffix becomes the beginning of the high-side scan. Processing that constant prefix from `kOf c` returns the same carry, so the remainder receives the same input. Only the `.2` final-carry projection is equated; normalized digit words can have different lengths.

This statement allows unbounded coefficients in the remainder and includes phases 0, 9, and 18. It uses `norm_band_tail`, whose phase premise is only `c ≤ 18`; the unrelated `c ≠ 9` premise of the more general incoming-carry lemma `norm_band` is not imported into the interface.

`overflow_stripSuffix_of_bounded` gives the needed unrestricted-phase result under `Bounded B`. The source splits the suffix witness by length. If the suffix length is zero, the original and stripped words are equal. If it is positive, `c` belongs to the original bounded word and consequently `c ≤ 18`, supplying the preceding structural theorem. Thus large phases are covered by the identity case without a new upper phase bound. This directly addresses the intended `c > 18` reasoning while also covering empty words.

The starting carry stays exactly `kOf c`. None of these statements asserts invariance for arbitrary incoming carry.

## Indicator and accounting module

`overflowBit_stateOuter` has exactly the local premise `Bounded s.B`. It uses the existing `stateOuter`, which preserves the phase and maximally strips the original exterior word, and the existing `overflowBit`, which is defined from whether the high-value quotient is zero. The proof first identifies the normalized numeric carry with the original `gam`, then invokes the existing `gamma_le` bound, and finally turns the quotient's indicator into that numeric carry. It does not confuse an arbitrary nonzero carry with the number one.

The bridge has no assumptions about `Phase`, phase positivity, phase 9, a maximum phase, interior coefficient bounds, a positive exterior head, nonempty words, canonicality, `validOuter`, an integer realization, or checker acceptance. These broader local states are legitimate inputs to the arithmetic bridge; their inclusion does not broaden the original certificate checker's validity predicate.

The final source introduces `hquot` from `overflow_eq_highValue` and unfolds `phaseCarry` in that equality before rewriting `overflowBit`. This makes the already intended quotient match explicit; it changes no theorem statement. The final independent build checked this exact source successfully.

`rowOverflowSum_eq_totalGam_of_bounded` is appropriately weaker than a checker theorem: it needs only bounded original exterior words at indices `i < cert.P`. It casts the state identity from `Nat` to `Int` and uses the existing `sumPrefix_congr`. The conclusion identifies the normalized-row indicator sum with the existing `totalGam`, whose definition sums `gam` on the original stored rows.

`valid_rowOverflowSum_eq_totalGam` extracts those bounds from the original `LocalOK` conjunct. `checked_rowOverflowSum_eq_totalGam` uses `check_sound` and keeps only `check cert = true` as its external certificate premise. These statements sum over the listed states. Since `Certificate.st` and `Certificate.lk` use `getD`, avoiding an unrestricted all-index validity claim is material: the proof extracts validity only in the exact range supplied by `Valid`.

The general bounded-row sum theorem also covers an empty certificate, where both sums are zero and the in-range premise is vacuous. Checker-facing results use the original checker's positive-period condition through `check_sound`. No extra equality of link-list and state-list lengths is inserted.

`checked_weighted_balance_totalGam` rewrites the final indicator sum in the previously verified `checked_row_weighted_balance`, preserving normalized-row evaluation of both weighted coordinate observables. Its final term is `9 * totalGam cert`. `checked_weighted_balance_gains` consumes the existing `totalGam_eq_twice_gains` using the same checker-derived validity and gives the final term `18 * (totalG cert + totalH cert)` in `Int`. Both have `check cert = true` as their sole certificate hypothesis.

These last statements reuse the preceding coordinate balance and Agent110's width/band-gain accounting. They do not establish those earlier results afresh, prove a converse to the checker, construct an accepting certificate, or assert an infinite safe orbit or a conclusion about 196.

## Exact controls and excluded generalizations

The seven public control statements use original `State` values with `A = C = []`. Their concrete equalities and false-universal conclusions passed the fresh kernel build. They are boundary and negative controls, not accepted-certificate witnesses.

| Control | Actual checked content | Review significance |
|---|---|---|
| `phase19_carry_drift` | At `c = 19, B = [19]`, the original numeric carry is 2, stripping gives `[]` with carry 1, and both indicators are 1. | Numeric carry invariance fails if both structural conditions are removed; indicator equality alone would miss the drift. |
| `phase2_unbounded_indicator` | `Phase 2`, unbounded `B = [20]`, unchanged stripped word, original carry 2, normalized indicator 1. | A permitted phase does not replace coefficient boundedness when identifying a numeric carry with its bit. |
| `phase18_empty_boundary` | Bounded `[18]` strips to `[]`, with original and normalized carry/bit still 1. | An empty normalization retains its incoming carry. |
| `neutral_and_zero_boundaries` | `[9]` at phase 9 and `[0]` at phase 0 strip completely and have carry/bit zero. | The local bridge correctly includes the neutral and zero phases. |
| `bounded_phase19_boundary` | At phase 19, bounded `[18]` is unchanged and has carry/bit 1. | The bounded-word result genuinely permits a phase above 18. |
| `unrestricted_strip_carry_invariance_false` | Refutes carry invariance for every natural phase and every word using the phase-19 witness. | The missing structural hypotheses are expressed as an explicit false-universal control. |
| `indicator_eq_gam_without_bounded_false` | Refutes the indicator/carry identity for every state, and also for every state satisfying `Phase`. | The bound cannot simply be omitted or replaced by the existing phase predicate. |

The empty-word behavior agrees in both definitions: `norm [] e` retains `e`, and the quotient denominator at length zero is `10^0 = 1`. The controls correctly preserve this convention. Additional parameter sweeps or new control expansion were unnecessary once these concrete risks and the generic proof paths were resolved.

## Independent execution and module origins

The compiler runner created a new empty object directory and rebuilt all 21 project modules. It reused the already verified official Lean runtime, not the inherited or author project objects. Every command used `--trust=0 -j1 -DElab.async=false` with genuine Lean 4.19.0, commit `6caaee842e94`; binary SHA256 was `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Supported executor escalation supplied the runtime's normal executable discovery; no runtime shim was used.

Compilation completed in 42.536113 seconds of recorded commands; the two independent audit commands took 31.093564 seconds. The complete audited closure contains 274 public theorem declarations, 376 explicitly named declarations, 712 theorem constants, 261 safe definitions, and 1,437 module constants. All theorem and safe-definition axiom lists are subsets of `propext`, `Classical.choice`, and `Quot.sound`.

The audit inspected actual environment origins, all theorem/safe-definition constants, explicit declarations, and private helpers. It separately retained 428 generated unsafe implementation definitions and eleven inherited generated unsafe implementation axioms. The complete multiline `#print axioms` parser agreed with structured `Lean.collectAxioms` records. Every one of the 16 new public theorems also has a literal source print receipt from its fresh compilation log, and those receipts agree with the separate full audit.

The fresh inherited subset exactly matches the preceding reviewed subset: all 1,404 inherited constant names, kinds, and origins are unchanged; all 942 inherited theorem/safe-definition axiom records agree. `MODULE_ORIGIN_COMPARISON.json` records no missing, added, or changed inherited names. All original/staged source bytes, project objects, and compiler files remained unchanged through compilation and auditing.

## Failed-attempt context and prior receipt correction

The parent author's accounting attempts 001 and 002 both actually exited with code 1 on a rewrite-matching error. Their failed logs contain error-recovery `sorryAx` dependencies, and those failure records remain failures. Attempt 003 exited with code 0 and has the exact frozen source hash reviewed above; its log has no `sorryAx`. The independently rebuilt final source also passed the complete allowed-axiom audit. The separate author-context receipt preserves exact references and byte copies of the accounting attempt sources, logs, and result JSON; none of the failed logs is used as accepted proof evidence.

This reviewer had no failed Lean attempt and made no theorem-source repair. The author failures are disclosed as author history, separate from the successful independent final execution.

The older 25/1,991 multiline-receipt correction is a different issue. A prior parser truncated 25 stored axiom lists; recovering the complete raw lists preserved the same standard three-axiom union. It was not a theorem failure. Its exact original correction receipt and the prior generated-origin explanation remain retained with the inherited provenance.

## Conclusion

The exact reviewed contribution establishes the intended compatibility and accounting interfaces with the stated weak hypotheses. Its negative controls expose the two distinct invalid generalizations. Independent compilation, axiom coverage, literal export receipts, source/registry alignment, and module-origin checks passed. The review identifies no source correction or additional Lean test needed; completion consists of the separate exact remote-source binding and portable evidence package.
