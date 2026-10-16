# Adversarial source-only review: periodic safety scope

Agent #1 separate specialist `research_status`, 2026-10-16. Reviewed `periodic-safety-scope.md` from `verification_plan` and the exact local original definitions. No new proof, Lean compilation, finite evaluation, mathematical source edit or task claim was performed for this scout.

**Statement review: PASS for the proposed Boolean/BadWord equivalence and stripping invariance.** No mismatch was found between the proposed executable state test and the preserved Python test on its original valid domain. This is a scoped source assessment, not acceptance of an unimplemented theorem.

## Exact target and premises

The proposed Boolean negates the disjunction of: every coefficient in `B ++ H ++ w` is at most9; or the outside head `(B ++ w).headD 0` is11 and every stored coefficient is0 or11. It faithfully implements Python `safe(s)` on the valid domain because the period has length4, so the stored alphabet is nonempty. No coefficient upper bound or symmetry is needed for the purely combinatorial equivalence with `FoldedDecimal.BadWord`.

For `k > 0` and `w ≠ []`, the proposed endpoint

```
safePeriodic B H w = true ↔
  ¬ FoldedDecimal.BadWord (periodicWord B H w k).length
      (fun i => ((periodicWord B H w k)[i]?).getD 0)
```

has the correct domain. Positive exponent ensures that every symbol from w occurs in the expanded word. Nonempty period ensures that `(B ++ w).headD 0` is the actual outside head even when B is empty. These facts also ensure nonzero expanded width, so index0 in the second BadWord branch is in range. A proof must not replace either premise by an unstated appeal to the intended period-four application. The original `ValidPeriodic.period_length` can discharge period nonemptiness in that application.

The theorem may classify arbitrary coefficient lists beyond the canonical digit model, but there it is only a Boolean/BadWord identity. Ordinary next-output interpretation needs the explicit canonical realization and finite column-sum hypotheses.

## Stripping invariance and exact quotient distinction

The proposed `safePeriodic_strip` is sound under nonempty w. Both tests must continue to include the stored period w after stripping, even when either remainder becomes empty. Every removed coefficient is a coefficient of w or its reverse; no symbol disappears from the stored alphabet because w is retained. The existing `stripPeriodSuffix_outside` supplies equality of outside heads. This requires reconstruction and head facts; it does not require reproving maximality or termination.

The resulting quotient corollary identifies safety of the **stripped target** with safety of its **raw target tuple**. It does not identify target safety with source safety. The preserved Python explicitly evaluates `safe(target)` and may return `unsafe_target`. A claim of forward safety closure would exceed both the proposed statements and the original algorithm.

The proposed positive-exponent statement naturally applies to the output exponent supplied by the existing validity package, which is at least1. It does not raise that exponent to3 or allow another uniform guard transition without the required source-exponent premise.

## Existing mathematics and attribution

Independently read exact current files:

* `proofs/LychrelDigitSums__75febdc48f0ca802.lean:883`, `DecimalDigits.step_palindrome_iff`: complete ordinary **next-step** palindrome criterion, with positive width, decimal-digit bounds, and positive most-significant digit.
* Same source at1526, `FoldedDecimal.BadWord`: exactly the low-coefficient or outer11/{0,11} disjunction, with no extra hidden admissibility conjunct.
* `proofs/PairDelayBridge__c453a1542e8182cd.lean`, `PairDelayBridge.palindrome_iff_bad`: already packages the generic `Canonical n d L` and finite column-sum realization interface.
* `proofs/Agent1PeriodicPositivity.lean:76`, `stripPeriodSuffix_outside`: already handles the head after complete exterior removal.
* Original Python `proofs/periodic_word_quotient__8404d0a63dd1fa13.py:37–39`: exact Boolean target.

The core contribution should remain the finite stored-block test, expansion-independent interpretation, and strip invariance. Do not present the generic arithmetic palindrome criterion as new. The scout's Agent105 integer-safety branch and Agent3 normalized-safety pointers are attributable remote-source findings by `verification_plan`; I did not rerun their builds or independently verify those branches in this scout. Reuse them if a later task requires their exact generic interfaces rather than launching a competing generic bridge.

The criterion is about the palindrome status of the integer **after one addition**, not the represented initial integer. A literal list-palindrome interpretation would concern `normalize Q 0`; `stepWord Q` is a pair word and is symmetric regardless of safety. Testing reversal symmetry of `stepWord Q` would therefore be an incorrect replacement endpoint.

## Publication and boundary controls

The written k=0 boundary observation and the proposed w=[10,10,10,10] failure of forward safety closure are not new formal results from this scout. If included in the claimed package, preserve the proposed exact fixed inputs, have the assigned author prove them by kernel-checked declarations, and record actual compiler and axiom evidence. No `native_decide` or finite Python run should be substituted for that required formal evidence.

Optional ordinary-integer packaging should retain `Canonical n d Q.length` and `columnSum d Q.length i = Q[i]?.getD 0` for every in-range index. It asserts neither existence of such a realization nor time-zero nonpalindromicity. No new finite horizon, return cycle, safe-language closure, affine-run dynamics or infinite-orbit result is part of this target.

A fresh guarded claim is the parent's responsibility. This review reserves no scope and infers no owner's release or acknowledgment. It confirms the proposed contract's semantics, while leaving live ownership and final source freezes to the established coordination workflow.
