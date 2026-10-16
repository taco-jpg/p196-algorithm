# Group III source review — compilation pending

Reviewer: `/root/research_status/numeric_bridge_review`, acting as an Agent #1 specialist.

This is a source-inspection checkpoint, not Lean verification or final acceptance. The author owns both new Lean files. The reviewer has not edited those files or performed Git writes. The intended result is the finite, two-step Group III delayed repair from the retained constructive `STATUS.md`, original blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`.

No semantic gap was found in the inspected statements and arithmetic bridge.

- `P196.Agent1.GroupIII.Domain` quantifies every natural `r >= 1`, `1 <= p <= 4`, `10 <= u <= 13`, `5 <= v <= 6`, `u+v <= 18`. The natural-number conditions select precisely `(10,5),(10,6),(11,5),(11,6),(12,5),(12,6),(13,5)`. The old `DelayedOverlapGate.Domain` remains unchanged and is not assumed by the new statements.
- `sixWord r p a b c` has exterior at indices `0,2r+5` and central pairs at `r,r+5`, `r+1,r+4`, `r+2,r+3`. For `r=1` these are distinct from the exterior and implement the intended empty intervening zero runs. `returnedComponent` is exactly `4p · 0^(r-1) · (2,4u-39,4v-17,4v-17,4u-39,2) · 0^(r-1) · 4p`, of width `2r+6`.
- The whole-word `middle` adds exterior and central contributions. At `r=1` the adjacent coefficients are therefore `2p+1`; the returned overlap has boundary coefficients `4p+2`. These are the required boundary merges, not excluded cases. The natural subtractions are nonnegative throughout the stated domain.
- Component and whole return statements use the original `OverflowCarryNormalization.iterPairs`, including its actual `nextWidth` and `nextColumns`. They identify the complete finite returned pair word and prove the original widths, `2r+6` and `2r+7`. The proofs use explicit carry identities and no-terminal-overflow results before composing two transitions.
- `actual_intermediate_overlap_fails` compares against the zero-extended **actual** component update before `shiftOne`. This is necessary: the original `nextColumns` has irrelevant values outside its represented finite width. `component_next_zeroExtended` connects that actual finite update to the explicit, zero-tailed `firstComponent`.
- The exact first coefficient difference is stated over `Int`, retaining its negative coefficient `-20`. This establishes a genuine first departure. The second whole-word equality is proved directly through actual carries; a separate Lean theorem for the normalized-digit defect is not needed for that proof.
- The numeric theorem quantifies arbitrary `n,d` satisfying the original `DecimalDigits.Canonical n d (2r+7)` and finite pair-word agreement. In the pinned `LychrelDigitSums`, `Canonical` requires bounded in-width digits, a nonzero most significant digit, and exact positional value (lines 907–908). Together with `value_positive` (693–700), this excludes zero and leading-zero padding. Trailing zeros are permitted. No out-of-width digit condition is added.
- `numeric_middle` and `numeric_return` apply the unchanged `representation_next` (pinned `LychrelDigitSums`:1568–1591) twice, giving canonical representations of the original `orbit n 1` and `orbit n 2` at width `2r+7`. That bridge derives ordinary decimal reversal from the original reversal algorithm; it is not a surrogate recurrence.
- Safety is about the two **positive outputs**, through `PairDelayBridge.palindrome_iff_bad`. `initial_not_bad` excludes the low pattern via center `2v >= 10` and the overflow palindrome pattern via outer `p != 11`. `middle_not_bad` uses inner coefficient `2(u+v)-18 >= 12` and outer `2p != 11`. There is no assertion about whether the seed itself is a palindrome.
- `numeric_delayed_return` bundles safety at times 1 and 2 with the complete canonical pair word at time 2 for every realization. `realized_safe_gate` additionally invokes unchanged `valid_word_realizable` (pinned `LychrelDigitSums`:1469–1481), discharging positive canonical realization for every allowed tuple. Thus the all-realizations statement is not left vacuous.

The pinned definitions of ordinary iteration are `step n = n + reverse10 n` and `orbit n 0 = n`, `orbit n (k+1) = step (orbit n k)` (pinned `LychrelDigitSums`:116–128). They continue at every time, without a palindrome stop rule. Nothing inspected asserts a third repair, a first palindrome time, persistent exterior reset, infinite safety, Lychrel existence, or a theorem about the entire orbit of 196.

## Finite diagnostic evidence

`finite_controls.py`, `finite-controls.log`, and `finite-controls-result.json` retain separate executable integer controls. All seven cores and all four outer values were checked at `r=1..12,32,128`: 392 parameter tuples and 1,176 canonical realization checks (three choices per tuple, not asserted to be distinct).

The checks compare `G²(A)` with the written returned component, `G(Q)` with the independent overlap, and `G²(Q)` with the returned overlap. They also check exact coefficient and normalized-digit defects, width, admissibility of the returned overlap, two actual decimal additions, and both positive-output safety claims. All finite checks passed, including every `r=1` case. **This is finite diagnostic evidence, not an all-parameter theorem.**

## Remaining verification

The author's local proof-script failures are not interpreted as counterexamples. `independent_build.py` is prepared to snapshot the six pinned dependencies and both completed roots into a new directory, verify exact SHA-256/Git blob pins and import closure, compile with official Lean 4.19.0 and `--trust=0`, and audit every theorem constant originating in all eight modules. It additionally issues literal `#print axioms` for every new public theorem. A successful independent run and review of its final source identities are required before changing this checkpoint's verification status.
