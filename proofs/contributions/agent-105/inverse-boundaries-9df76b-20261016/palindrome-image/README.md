# Agent 105: complete one-step palindrome image classification

Claim: `agent105-9df76b-palindrome-image-20261016`.

Session: Agent 105, suffix `9df76b`; source author `/root/structure105`.
Coordination claim commit: `c9ef8561d8ac236117102ddeccc758a541591543`.
The integration writer is the parent Agent 105 session.

## Exact result

The frozen module is `proofs/Agent105PalindromeImage9df76b.lean`.
All declarations are in namespace `P196.Agent105.PalindromeImage9df76b`.

For every `P : Nat`, every digit function `e : Nat → Nat`, and every
`W : Nat`, under the assumptions

```lean
htarget : DecimalDigits.Canonical P e W
hpal : Lychrel196.Palindrome P
```

the main theorem is

```lean
palindrome_target_has_positive_predecessor_iff :
  (∃ n, 0 < n ∧ Lychrel196.step n = P) ↔
    W % 2 = 0 ∨ e (W / 2) % 2 = 0
```

Thus a positive ordinary decimal palindrome is a numerical
reverse-and-add image exactly when its width is even or its middle digit
is even. The existential quantifier covers every positive natural-number
predecessor, including both possible source widths. Targets with leading
digit 1 are included.

The constructive direction is stronger: `same_width_zero_carry_predecessor`
produces a positive predecessor whose canonical width is exactly `W`,
whose digit function is the existing `FoldedDecimal.realizingDigit e W`,
whose column-sum word equals `e` on all `i < W`, and whose entire carry
word is zero on all `i ≤ W`. The returned equality is the ordinary
natural-number equality `Lychrel196.step n = P`.

For `2 ≤ W`, `same_width_first_hit_one_predecessor` also gives

```lean
∃ n, 0 < n ∧ Canonical n (realizingDigit e W) W ∧
  orbit n 1 = P ∧ ∀ k, k < 1 → ¬ Palindrome (orbit n k)
```

The corollary `palindrome_target_first_hit_one_iff` proves that this
time-one first-hit existence condition has the same parity criterion.
The supplied target assumption already asserts that the state at time
one is a palindrome.

## Proof structure and reused results

1. Target palindromicity yields symmetry of its canonical digit word.
   Its first digit is positive by symmetry and its positive leading digit.
   The stated parity condition supplies precisely the even central
   coefficient needed by `realizingDigit_columns`. Existing
   `realizingDigit_bounded` and `realizingDigit_leading_positive` give a
   canonical positive source. Because each target digit is at most 9,
   `DecimalCarry.small_digit_sums_give_palindrome` gives every carry zero.
   The unchanged `step_value` and `value_output` identities establish the
   actual numerical image.

2. In the no-overflow case, the original
   `step_palindrome_iff_no_overflow` criterion makes all column sums at
   most 9, so all carries vanish. At odd width the central column is
   twice the source's middle digit. The output center is therefore even.

3. In the overflow case, the original `step_palindrome_iff_overflow`
   criterion makes every column sum either 0 or 11. When the source has
   even width `L`, its two central columns are reflections and have the
   same value. The carry into the higher central column is 0 in the
   zero case and 1 in the eleven case. Its output digit is consequently
   0 or 2. This is `overflow_palindrome_center_zero_or_two`.

4. The necessity theorem obtains the predecessor's actual canonical
   representation using `canonical_exists`, then uses the existing
   `canonical_next_no_overflow` or `canonical_next_overflow` to obtain the
   actual target digits. `Agent105WidthSupport9df76b` supplies canonical
   width and finite-digit uniqueness, reusing Agent101's published
   `decimalWidth_unique` and the original `value_injective`. This
   identifies the output width with `W` and transfers the appropriate
   central-digit conclusion to the user's target representation.

5. For the first-hit corollary, `W ≥ 2` makes the constructed source's
   units digit `e 0 - 9 = 0`, while canonicality supplies a positive
   leading digit. Digit symmetry therefore rules out a palindrome at
   time zero. The exact numerical image gives the palindrome at time one.

## Semantics and boundary cases

- `Canonical P e W` includes `0 < W`, bounded decimal digits, a positive
  leading digit, and `value e W = P`. It therefore describes the actual
  positive width; padded leading zeros and `P = 0` are outside the
  theorem's assumptions.
- The digit function's values outside `i < W` are unconstrained. The
  uniqueness interface compares only actual digit positions.
- The source is an ordinary positive natural number and can have trailing
  zeros. Reversal uses the original natural-number `reverse10`; such
  zeros disappear during reversal, as required by that definition.
- The main iff includes `W = 1`. In this case the admissible targets are
  precisely the positive even digits 2, 4, 6, and 8. The first-hit
  corollaries explicitly require `2 ≤ W`, since a one-digit predecessor
  is itself a palindrome at time zero.
- For an even-width target the middle-digit disjunct is unnecessary.
  For an odd-width target, source width `W` uses a genuine central
  source column, whereas source width `W - 1` uses two distinct central
  columns. The proof handles these cases separately.
- This module proves a one-step image classification and the stated
  existential time-one corollary. It neither counts predecessors nor
  establishes a reachability or avoidance claim for the orbit of 196.

Illustrative constructed sources include `100 → 101`, `110 → 121`, and
`1200 → 1221`. The positive palindrome 111 fails the criterion because its
width and middle digit are both odd.

## Preserved research and dependency provenance

The target statement is Section 3 of the retained research note
`proofs/research/persist_inverse_notes.txt`, Git blob
`ecd101823b261fdac15d185fea963d9c9f16c601`. Its preserved source is under
`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/`.
The source map was used to identify the original research module and this
note before the claim was made.

The original imported `Lychrel196Research` source has SHA-256
`f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`.
The shared support source `Agent105WidthSupport9df76b` has SHA-256
`3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7`.
The support chain reuses Agent101's published source pinned by the runtime
author at commit prefix `32664594`; its complete dependency manifest and
independent rebuild evidence are maintained by the integration team.

## Recorded compilation and source freeze

Lean: 4.19.0, invoked with `--trust=0`.

The actual recorded command uses the binary
`/workspace/scratch/fb513c1676b0/agent102-runtime/lean-4.19.0-linux/bin/lean`
and
`LEAN_PATH=/workspace/scratch/9df76b503b84/agent105-runtime/base-build`.
The absolute command, source hash, exit code, wall time, and dependency
search path are recorded in each `attemptNNN.json`; corresponding source
snapshots and complete stdout/stderr are `attemptNNN.lean` and
`attemptNNN.log`.

| Attempt | Added interfaces | Exit code | Wall seconds |
| --- | --- | ---: | ---: |
| 001 | Same-width construction and both local center lemmas | 0 | 0.876 |
| 002 | All-width necessity and complete positive-predecessor iff | 0 | 1.231 |
| 003 | Same-width first-hit-one construction and first-hit-one iff | 0 | 2.010 |

Each attempt is retained exactly as compiled. There were no failed
compiler attempts in this sequence. After attempt 003, only the English
docstring of `no_overflow_palindrome_center_even` was clarified; proof
terms and statements were unchanged. The precise delta is retained in
`attempt003-to-frozen.diff`.

Frozen source SHA-256:
`029bcf37c74d0d6a2b226cf60011ba7d66a3daee40087833f039b13be0e6cce6`.

Every theorem ends with a recorded `#print axioms` request. The two
constructive theorems depend only on `[propext, Quot.sound]`; the other
five depend on `[propext, Classical.choice, Quot.sound]`. The module
introduces no axioms and uses no `sorry`, `native_decide`, or external
oracle. Independent frozen-source semantic review is assigned to
`/root/runtime105`, and a fresh full-dependency build to `/root/scope105`.
