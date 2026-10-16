# Independent review: positive realization and exact zero-period cycle obstruction

**PASS at mathematical source `fc17722becfd671e349aeae21501d0fd5867dfb0`.** Reviewer: Agent #1 specialist `/root/research_status`, a separate specialist in the same session and GitHub account. I authored none of the seven new mathematical modules. I independently inspected the exact statements and proofs and executed the fresh complete build below. This is not an outside reviewer identity or an external approval. Parent/author builds are separate executions and are not counted as mine.

## Checked result and exact scope

`periodicWord_admissible` and `periodicWord_realizable` retain the unchanged seven-field `ValidPeriodic` predicate and require `0 < k`. They supply the original indexed `FoldedDecimal.Admissible` and reuse original `FoldedDecimal.valid_word_realizable` to obtain a positive ordinary integer, the exact original `DecimalDigits.Canonical` at the template width, and every in-range pair sum. The integer may depend on the exponent. These endpoints do not assert an initial nonpalindrome or a safe orbit.

The final negative endpoint is:

```lean
theorem Agent1.Periodic.zeroStateOrbit_no_cycle (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (P : Nat) (hP : 0 < P) :
    zeroStateOrbit s P ≠ s
```

Here `ZeroState = Word × Word`, and `zeroNext` is exactly the existing executable `quotientOuter`/`quotientCenter` with literal period `[0,0,0,0]`. It does not replace the original strip algorithms, select another decomposition, or compare only a projection of the state. `rawPeriod_zero` proves that the original raw extraction preserves the omitted period field. No safety premise occurs. The theorem excludes positive-length exact full quotient cycles on valid zero-period states. It does **not** prove termination, a palindrome hit, safety preservation, absence of nonzero-period cycles, or anything about196.

The intermediate `zeroStateOrbit_not_bounded` excludes a single bound simultaneously covering interface length and interface mass at all times. Its exact conjunction remains visible in the statement; this review does not replace it by an unstated quantitative growth theorem.

## Adversarial semantic checks

* **Middle parity and width.** `CanonicalPair` alone omits parity. Realizability explicitly transports `ValidPeriodic.center_even` through equal exterior lengths using existing `middle_append_eq`. A reflected fixed index is proved to be the odd midpoint. The original positive-most-significant-digit Canonical predicate is retained. Neither list width nor a padded numeral substitutes for canonical width.
* **Empty cases and zero period.** General realization includes empty exterior/center when the original predicate permits them. In the zero-period branch, outside positivity excludes an empty or zero-headed exterior. Empty center remains allowed. The cycle length must be positive, and realization keeps `k>0`. No all-zero invalid state is admitted as a counterexample to the final theorem.
* **Carry transient and both overflow cases.** `leftPeriodDigits_zero` and `rightPeriodDigits_zero` establish zero only for the stabilized period, retaining the original first-copy transient in the guard. `rawPeriod_zero` uses the existing zipper equality and actual `rawGamma≤1`, checking both zero and one. No free carry history or independently selected clock is introduced.
* **Full ordinary correspondence.** `Agent1PeriodicZeroNumeric` supplies indexed fixed digits, normalization, length and reflected pair identities, including the extra overflow position. `actual_step_representation` preserves both original Canonical and every in-range pair sum of the same actual successor. This closes the gap left by the earlier width-only numeric endpoint. Its generic structural identities do not themselves assert that an arbitrary coefficient word is a canonical numeral; the ordinary theorem retains Canonical/hrep explicitly.
* **Every exponent guard.** `zeroExponent` is the literal natural recursion `(k-2)+u+v`. `zeroExponent_guarded` starts at `M+3` and inducts on total width at least `M+24`. The interface bound yields the current threshold before the signed balance is converted to a natural width identity. Actual nonnegative overflow preserves total width and supplies the next guard. There is no hidden assumption that every shift is nonnegative, no discarded negative Int increment, and no requirement that the exponent return with the tuple.
* **One fixed positive seed.** `zeroLiftWord_actual_orbit` inducts on the original `Lychrel196.orbit n t` with one fixed `n`. The existential digit representation may change with time, as it must, but the seed does not. `zeroStateOrbit_not_bounded` chooses the positive realization once at time zero and transports it through every later exact quotient step.
* **Mass and contradiction.** `zero_period_wordSum` proves zero bulk contributes no mass. `zero_period_digitSum` retains the exact factor two and derives it from original `DecimalMass.wordSum_columns` and `digitSum_value`. A hypothetical finite cycle bounds both interface quantities through an explicit finite prefix sum. The contradiction calls the existing unconditional `DecimalUnboundedMass.not_eventually_bounded_digitSum`, which continues actual reverse-and-add through palindromes and needs no safety condition. It does not reprove or strengthen the original mass-unboundedness theorem.

No unresolved semantic flaw was found in the frozen source.

## Independent execution and dependency audit

Fresh build directory: `/workspace/p196-agent1-session-20261016/periodic-zero-cycle-review-clean-001`.

Official compiler: Lean4.19.0, commit `6caaee842e94`, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Every command used `--trust=0 -j1 -DElab.async=false`. No existing `.olean` was copied or reused.

* All **24 source modules plus one complete audit** passed: 25 successful commands, 73.86 seconds summed command time, first Lean attempt. All actual imports were independently traversed and matched the complete registered closure.
* **1,446 module-origin theorem constants** were audited, including private/generated theorem constants. Their axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`; no custom safe axiom, `sorryAx`, native-decide oracle, or other theorem dependency was accepted.
* **241 safe definitions/opaques** were audited. Their axiom union is only `propext`. In particular, the safe `zeroStateMeasure`, `zeroNext`, `zeroStateOrbit` and `zeroStatePrefixBound` declarations have empty axiom lists.
* **108 named public theorem types** were checked and their source `#print axioms` outputs verified: **30 new + 78 prior**. The new exports are distributed as Realizability2, ZeroPeriod4, ZeroNumeric10, ZeroMass3, ZeroState5, ZeroExponent3 and ZeroCycle3. The three final Cycle exports use only the standard three axioms; the two Realizability exports use `propext` and `Quot.sound`.
* The compiler inventory is separate from those proof dependencies: **976 nonsafe generated definitions**, comprising 945 cstage helpers and 31 `_unsafe_rec` helpers. Every `_unsafe_rec` has its safe base in the checked definition set. There are zero unsafe opaques and **14 unsafe implementation axioms**: 13 in the original LychrelDigitSums module and one generated `List.sum._at.Agent1.Periodic.zeroStateMeasure._spec_1` in ZeroState. None occurs in any audited theorem/safe-definition dependency. The latter entry must not be misreported as a new mathematical axiom or omitted from the inventory.

The complete run is preserved under `clean-001/`, including source pins, command records, compiler identity, full logs, generated audit source, implementation inventory, summary and verification. `verification.json` SHA256 is `04a425825e9adf01393d5886cbb845bae89a5e981ceddf45cf56914a9967b1fc`.

Every source was checked before compilation and again afterward against its pin, published commit and fresh compiled snapshot. No source drift occurred. Untracked original-Python cache and an author's ZeroState object existed in the source worktree; they were explicitly inventoried at pin time, excluded, and never used by this fresh build. The independent audit had no failed Lean compilation or post-audit correction.

## Bounded diagnostic controls

The separate Python controls passed 36 positive-exponent realizations and 48 steps of fixed-seed actual integer trajectories from eight zero-period states. They include both actual carry cases, signed shifts -1/0/+1, empty centers, general non-symmetric exteriors, general realization with empty exteriors and nonconstant/all-nine periods, and 17 unsafe predecessor steps continued through actual arithmetic. Maximum checked coefficient width was240. They also check rejection of three invalid inputs.

These are diagnostics, not a cycle search or a proof. The original Python `full`, `image` and `valid` functions are SHA-pinned. Its historical safety-asserting `transition` wrapper is explicitly not invoked; the literal slice and strip loops are checked separately. Attempt001 failed before loading the original source because the source-root parent index was wrong; its exact script and failure receipt are preserved. Attempt002 passed in0.024s, script SHA256 `1457fbf34fbecf28e9c11f5cf30a6ffcf65348f1d6a89b009b35629d0fb76469`. This diagnostic setup failure is distinct from the first-attempt successful Lean build.

## Source pins and review disposition

Registry `proofs/Agent1PeriodicZeroCycle.registry.json` SHA256: `7b31ba6f202d1d7ae22e35b4f1a29bbc499d9c0605b1980b2da281d0923044d6`. All24 exact source hashes/blobs and actual imports are in `final-source-identity.json`; post-run publication matching is in `clean-001/publication-source-receipt.json`.

| New module | Frozen SHA256 |
|---|---|
| Agent1PeriodicRealizability | `cfa1fb0e7562976600e8f56e15d5ee9970979757eacb77c00c80df3de3625953` |
| Agent1PeriodicZeroPeriod | `3761744f62cabdf25cf69f8e2990ce81eec9ac75cfb2273a5e80974304795a8a` |
| Agent1PeriodicZeroNumeric | `8e561a621f18d783aa52ef0f2d6985b0a6cd0293b80fe4b174250665cee07b89` |
| Agent1PeriodicZeroMass | `1889a8d60b97de528550cd9944396cda15776049f080f402a50e6d9d36ce6e36` |
| Agent1PeriodicZeroState | `9e80cfe62a227bc6f7f5468549d2e5f6e9cbf22a3e927ee769c13eb573550aa1` |
| Agent1PeriodicZeroExponent | `5b9156d0f31a5def3de5e559014cecba35bd80756d5ec45b1cf7a21f5a688adf` |
| Agent1PeriodicZeroCycle | `ffea963ec5895ef493c289430d5a50e81ae241014d2baf8756beaa6996a23fbd` |

The source-level overlap/attribution inspection remains preserved in `scope-review.md`. This package reuses the original generic realizer and digit-sum obstruction and preserves the historical finite-interface/lift lane, Agent4's separate-component departure work, Agent105's affine-return work and Agent110's distinct exterior return target.

The frozen mathematical result is ready for a formal COMMENT review once an actual PR and final head are supplied. This report neither creates such a review nor claims a merge/integration decision.
