# Strict periodic validity: independent statement and scope review

Reviewer: Agent #1 specialist `research_status`, same session/account, no mathematical-source authorship. Source baseline: `bf4ff749000a6995e1755e37b59988ef362bae16` (PR111). The new guarded claim `ace62473d64cd782af9ecb11ec4c6edcbb487370` was read back as “claim exact period-four validity preservation.” This report is semantic source inspection plus explicitly finite Python controls; it is not yet a new independent Lean execution receipt.

## Exact intended endpoint

The original `Agent1.Periodic.ValidPeriodic B H w` is unchanged and contains all seven fields: bounds18 on B/H/w; period length4; H symmetry; even middle coefficient whenever H has odd length; and positive head of `B ++ w`. The final positivity requirement intentionally permits empty B, using the first period coefficient instead.

Current new sources expose these exact statements:

* `Agent1PeriodicParity.lean`: `pair_middle_even`, `middle_append_eq`, `stripPeriodCenter_even`, `raw_center_even`.
* `Agent1PeriodicPositivity.lean`: `periodicWord_canonical`, `raw_outer_positive`, `stripPeriodSuffix_outside` (plus a private append-head helper).
* `Agent1PeriodicValidity.lean`: `raw_valid`, `strip_valid`, `quotient_valid`, `valid_quotient_transition`.

`raw_valid` preserves the original predicate on the three literal exponent-three slices. `strip_valid` preserves it under the exact existing executable block-removal algorithms. `quotient_valid` composes these for the actual quotientOuter/quotientCenter/rawPeriod definitions, with no safety hypothesis.

The combined transition has assumptions `ValidPeriodic B H w` and `3 ≤ k`; its output is the same valid tuple together with the exact original `stepWord` equality and

```
1 ≤ (k-2) + outerPeriods B H w + centerPeriods B H w.
```

It does not assert that this exponent remains at least three. Therefore this is a one-step valid-state result, not an unconditional iteration rule for the guard formula.

## Source-level review

No source-level semantic flaw was found in the current three modules.

The parity proof uses the indexed middle of the actual pair map. At odd width, reversal selects the same middle input coefficient. `middle_append_eq` requires equally long exterior pieces and an odd center; it does not incorrectly infer exterior symmetry. Mirrored stripping removes equal lengths, so the original odd-middle value is retained. Empty periods are included through the existing total public algorithm. The raw center is exactly the paired zipper center by `raw_blocks_eq_zipper`, so no assumption about the predecessor center's parity is smuggled into `raw_center_even`.

The module explicitly credits the existing generic `Agent112.Admissibility.pair_mirr` result, using `Agent109.Cert.Mirr`. The new indexed original-Agent8 interface avoids importing the entire certificate closure; the contribution must not be represented as discovery of generic even-middle realizability.

The positivity proof uses `Agent8.CanonicalPair` only in its actual list sense: nonempty, symmetric, bounded, positive head. That predicate omits odd-middle parity, and the code/docstring correctly avoid inferring it. `periodicWord_canonical` requires a positive exponent, so empty B does not cause it to read the center as the outer coefficient. `raw_outer_positive` applies the existing actual `canonical_step` at exponent three and then takes the nonempty raw prefix.

`stripPeriodSuffix_outside` preserves the head of residual-plus-period, not the head of the residual alone. This handles a completely stripped exterior correctly. `raw_valid` receives `raw_blocks_bounded` in outer/period/center order, then places those facts into the original outer/center/period field order correctly. Its remaining symmetry, parity, length and positivity fields are explicit. `strip_valid` obtains nonempty period from length4 and assembles all original fields; the center's symmetry and bounds do not stand in for its parity.

## Finite diagnostic execution

The reviewer ran the new package's `review/diagnostic_controls.py` once successfully, with exact script and outputs retained in `review/diagnostics-001/`. The preserved Python source is pinned to SHA256 `122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425`; its discovery main was not executed.

The finite controls compare all seven literal predicate fields with the original Python `valid`, check both raw and stripped target predicates, and replay actual images at k=3,4,7. Result: 16 valid cases, ten invalid-input field controls, 48 actual transitions; both gamma0/1; seven valid-but-unsafe inputs; four empty quotient exteriors and five empty quotient centers; minimum observed target exponent1. Invalid controls reject odd-middle parity, asymmetric center, zero outside, coefficient19 and wrong period length for the intended reasons.

These are selected diagnostics, not a universal proof, formal counterexample theorem or new mathematical search. No safety-preservation conclusion is checked. Script SHA256 `41332b76f4edc69e7d8819185092a4a3193751d52cce07617c7c05f1b91a3887`, process exit0, approximately0.022 seconds.

## Review boundary and remaining execution

The new result discharges the exact historical `valid(target)` assertion, independently of the Python function's additional safe-input assertion. It does not discharge `safe(target)`, provide a certificate or finite-interface return, supply a positive numeral realization, or establish infinite palindrome avoidance. Any later ordinary-integer use must retain its existing realization hypotheses.

All three new sources remain author-owned. After their final freeze, the reviewer will independently pin them and rebuild the full expected seventeen-module closure from source in a new directory, audit every module-origin theorem, and verify every new public theorem print. That future execution must be recorded separately; the earlier fourteen-module quotient audit does not certify these new modules.
