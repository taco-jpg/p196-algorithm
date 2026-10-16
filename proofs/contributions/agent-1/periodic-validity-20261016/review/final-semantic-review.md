# Strict periodic validity: independent statement and scope review

Reviewer: Agent #1 specialist `research_status`, same session/account, no mathematical-source authorship. Source baseline: `bf4ff749000a6995e1755e37b59988ef362bae16` (PR111). The new guarded claim `ace62473d64cd782af9ecb11ec4c6edcbb487370` was read back as “claim exact period-four validity preservation.” Final result: **semantic and independent execution PASS**. A fresh seventeen-module build and complete module-origin audit checked 1,367 theorem constants with only `propext`, `Classical.choice`, and `Quot.sound`. All eleven new public theorem printouts and 67 named prerequisite printouts were checked. Finite Python controls remain separately labeled diagnostics.

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

## Review boundary and completed independent execution

The new result discharges the exact historical `valid(target)` assertion, independently of the Python function's additional safe-input assertion. It does not discharge `safe(target)`, provide a certificate or finite-interface return, supply a positive numeral realization, or establish infinite palindrome avoidance. Any later ordinary-integer use must retain its existing realization hypotheses.

All three new sources remain author-owned. The reviewer independently pinned them after final freeze and compared all seventeen module entries with `Agent1PeriodicValidity.registry.json`, including source paths, SHA256, Git blobs and imports. Final new source identities:

| Module | SHA256 | Git blob |
| --- | --- | --- |
| Agent1PeriodicParity | `8eb97092e0c402f24e8163b51ed902f7e83f39b3c2a663698b08375147f2e129` | `c5a2bfb004aa8421110403195abf9951572e7b4b` |
| Agent1PeriodicPositivity | `481768dfb0d8884d61c038a886d5fc05131fc085286869c32190f80691e0b3d6` | `bc392c470c3bf3389f4ae0166cf67dcaf2462e89` |
| Agent1PeriodicValidity | `4652df468f38ed9696f5b68616f5bfd9225ab6f377a4d449289d8c2ad65b0e52` | `3c5673981d4c9a73a0ade71552f5867d8f73dd69` |

The new build directory was `/workspace/p196-agent1-session-20261016/periodic-validity-review-clean-001`. It began empty and received exact source bytes only, no project object files. All seventeen module builds and the complete audit exited0 using pinned Lean4.19.0 commit `6caaee842e94`, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, with `--trust=0 -j1 -DElab.async=false`.

The module-origin audit includes the private positivity helper and generated theorem declarations, not just the eleven public endpoints. Every selected module was required to contribute audited theorems, and safe custom axioms or nonstandard theorem axioms were rejected. All source hashes were rechecked at completion; there was no source drift and no failed reviewer compile attempt. Author builds, the parent's canonical replay, and the preceding fourteen-module quotient audit are distinct executions and are not counted as this run.

Full source identities, exact commands and logs, compiler identity, snapshots, complete `ReviewAudit.lean` and audit output, and `verification.json` are retained under `proofs/contributions/agent-1/periodic-validity-20261016/review/`. `replay.py` reproduces the build in fresh directories. `scope-review.md` preserves the earlier pre-build statement inspection; `final-semantic-review.md` and `final-review-receipt.json` are the completed result.
