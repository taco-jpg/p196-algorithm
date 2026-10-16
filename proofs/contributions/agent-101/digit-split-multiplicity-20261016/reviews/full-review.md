# Independent build and semantic review: Agent 101 digit-split multiplicity

Verdict: **PASS**, for the exact five source hashes below. The complete source rebuild and both axiom audits succeeded. The Core and Numeric statements match their advertised mathematical scope; no substantive correctness defect was found. This is a local review record, not a claim that a hosted verifier has run.

Reviewer: the runtime specialist in Agent 101's team. **Authorship disclosure:** this reviewer authored `Agent101DigitPairs.lean`; its compilation and axiom dependencies were checked afresh, but its authorship review is not independent. This reviewer did not author `Agent101MultiplicityBounds.lean`, `Agent101SplitEnumeration.lean`, `Agent101NumericFibers.lean`, or the preserved base module. Earlier read-only semantic feedback and a distributivity simplification suggestion do not constitute authorship of those modules. No accepted source was changed during this review.

## 1. Fixed inputs and independent build

Fresh build directory:

`/workspace/scratch/2a8a87fd78df/agent101-runtime/full-independent-ma1li9tl`

All five complete source files were copied before compilation. No `.olean` from an author's build was copied. The base source retained in the repository as `Lychrel196Research__c696e0ea3db39d92.lean` was copied under its import name `Lychrel196Research.lean`. `LEAN_PATH` pointed only at the fresh directory; `LEAN_SRC_PATH` and `LEAN_SYSROOT` were removed from the child environment. The original Lean distribution supplied `Std` and `Lean`. `LD_PRELOAD` was empty. Source identity was checked again at the end.

The same fixed source snapshots are preserved beside this report as `full-review.<Module>.lean`.

| Module | Source SHA-256 | Bytes | New public declarations | Compiled theorem constants |
| --- | --- | ---: | ---: | ---: |
| `Lychrel196Research` | `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c` | 177462 | base | 787 |
| `Agent101DigitPairs` | `5c76eae97efd2f30d1775650f7feca477c269419af1c02809800a95ca62821f8` | 4514 | 14 | 27 |
| `Agent101MultiplicityBounds` | `8fd487ce8025cfe7cbda3dc51b6a02595c856fbe3dd065a8781cea60b7e6b5c3` | 3749 | 12 | 28 |
| `Agent101SplitEnumeration` | `8ce57c88984df3a965e33c181f4d8f138258fe48b14e2b835333fe6c30d79684` | 13329 | 31 | 58 |
| `Agent101NumericFibers` | `bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97` | 17343 | 38 | 56 |

The four new modules contain **95 public declarations: 17 definitions and 78 explicitly named public theorems**. The compiled theorem inventory contains **956 theorem constants: 787 from the base and 169 from the new modules**, including private and generated theorem constants. These are different counts and are not presented as 956 newly proved mathematical results.

Runtime:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
Lean executable SHA-256: 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

Executable:

`/workspace/scratch/2a8a87fd78df/agent101-runtime/toolchain/lean-4.19.0-linux/bin/lean`

Compilation order was base, DigitPairs, MultiplicityBounds, SplitEnumeration, NumericFibers. For each module `M`, the actual command, with the executable above, was:

```sh
lean -j1 -DElab.async=false -o M.olean M.lean
```

The two final actual audit invocations were:

```sh
lean --trust=0 -j1 -DElab.async=false FullCompiledAudit.lean
lean --trust=0 -j1 -DElab.async=false NewPublicExportsAudit.lean
```

These commands ran in the fresh directory with its `LEAN_PATH`. The JSON record preserves every full argument vector, working directory, exit status, elapsed time, source/object hash, and raw log hash.

| Command | Exit | Seconds | Preserved raw output |
| --- | ---: | ---: | --- |
| `version` | 0 | 0.066 | `full-review.version.log` |
| `Lychrel196Research` | 0 | 57.862 | `full-review.Lychrel196Research.log` |
| `Agent101DigitPairs` | 0 | 4.550 | `full-review.Agent101DigitPairs.log` |
| `Agent101MultiplicityBounds` | 0 | 0.546 | `full-review.Agent101MultiplicityBounds.log` |
| `Agent101SplitEnumeration` | 0 | 0.979 | `full-review.Agent101SplitEnumeration.log` |
| `Agent101NumericFibers` | 0 | 1.783 | `full-review.Agent101NumericFibers.log` |
| `compiled-audit` | 0 | 17.825 | `full-review.compiled-audit.log` |
| `public-audit` | 0 | 1.420 | `full-review.public-audit.log` |

## 2. Axiom audit and all diagnostics

The compiled audit queries Lean's actual imported environment and selects theorem constants by their defining module, rather than estimating theorem coverage with a source regular expression. It runs `#print axioms` for every selected theorem, including private and generated constants. The parsed theorem inventory and all axiom responses match exactly. It also rejects any safe custom axiom declaration in the selected modules. Its generator was extracted, without running the checker entry point, from the frozen repository checker `proofs/check__4f76e6046a854590.py`, SHA-256 `9fea73de4ea0497a1747e0b635bd1ea5d74d15b7479f89ae1351272f7093a9af`. The generated audit source is preserved.

The separate public audit runs `#print axioms` on all 95 new public definitions and theorems. Those declarations were enumerated from the four source files, whose declaration layout was read directly. Every requested declaration has exactly one audit response.

The union of all theorem and public-declaration axiom dependencies is exactly:

```text
Classical.choice
Quot.sound
propext
```

There is no `sorryAx`, no native-decision axiom, and no additional mathematical axiom in that union. All five source compilations and both `--trust=0` audit invocations exited 0.

Diagnostics disclosed in full:

- `Agent101MultiplicityBounds.lean:27:4` emitted one linter warning: `try 'simp' instead of 'simpa'`. It is a proof-style suggestion. No proof was modified in response.
- The compiled environment contained **22 unsafe implementation axiom declarations** generated for executable implementation code: 13 in the preserved base, 3 in DigitPairs, 1 in Bounds, 4 in Core, and 1 in Numeric. The audit records every exact name in `unsafe_implementation_axioms` in `full-review.json` and in the raw compiled-audit log. None appears in any audited theorem or public-declaration axiom dependencies. They were recorded explicitly rather than silently treated as mathematical premises.
- No other warning, compilation error, audit mismatch, changed input, or runner exception was found. The runner's `exceptions` array is empty. This full-build attempt did not require a retry. Earlier author development failures remain in their separate original evidence directories and were not removed or overwritten.

## 3. Core semantic review

All finite digit lists use **least-significant digit first**. A profile consists of an outer-to-inner half-list `h` and optional center `c`; its symmetric coefficient list is:

```lean
coefficientWord h c = h ++ c.toList ++ h.reverse
```

Its length is `2 * h.length + c.toList.length`. `digitPairSums ds` is the pointwise sum of `ds` and its reversal. It includes the doubled center digit when the length is odd.

`canonicalDigits ds` requires every digit to be at most 9 and the final (highest-place) digit to be positive. Because digits have type `Nat`, their nonnegativity is intrinsic. For the empty list, `getLastD 0 = 0`, so the positivity test excludes it.

The central completeness statement has an ordinary arithmetic specification independent of the recursive enumerator:

```lean
ds ∈ canonicalWords h c ↔
  canonicalDigits ds ∧ digitPairSums ds = coefficientWord h c
```

The forward proof reads each selected ordered digit pair; the reverse proof decomposes every list of length at least two into its first digit, inner list, and last digit, and reconstructs the corresponding pair choice. Thus the recursive specification does not conceal a missing-surjectivity assumption. Equality of the pair-sum lists also forces the length, so the final theorem does not need a separate width hypothesis.

`canonicalWords_nodup` proves absence of duplicate digit lists. Its product argument checks both injectivity within a fixed outer pair and disjointness between distinct outer pairs via `wrapDigits_injective`. `length_canonicalWords` then proves the exact list length equals `profileCount h c`. The nodup theorem makes this an exact cardinality of distinct original digit lists.

### Canonical and invalid-profile boundaries

| Situation | Verified behavior |
| --- | --- |
| No half-pairs and no center (`h = []`, `c = none`) | Zero canonical words; the empty list is rejected. The internal `rawWords` base still contains the empty inner word, as needed for constructing even lengths. |
| A single-digit word (`h = []`, `c = some s`) | Exactly one word for `s` in `2, 4, ..., 18`; zero for `s = 0`, odd `s`, or `s > 18`. |
| A nonempty half-list with `c = some 0` | A zero center digit is permitted. The highest-place digit is controlled by the outer pair, so this is a valid interior zero. |
| Outer pair sum zero | No canonical split, because its highest-place digit would be zero. |
| An inner pair sum outside `0..18`, or an odd/oversized center | No realization; the relevant pair or center factor is zero. |
| A units digit zero | Permitted whenever the highest-place digit is positive; for example, `790` is retained in the 887 fiber. |

No condition incorrectly requires the units digit to be nonzero. The ordered pair's first coordinate is the units-side digit and its second coordinate is the highest-place-side digit. Only the outermost pair uses `pairChoices true`; all inner pairs use `false`.

## 4. Counts and sharp profile bound

The closed pair counts are:

- Inner pair: `s + 1` for `0 ≤ s ≤ 9`; `19 - s` for `10 ≤ s ≤ 18`; zero beyond 18.
- Outer pair with positive highest-place digit: `s` for `0 ≤ s ≤ 9`; `19 - s` for `10 ≤ s ≤ 18`; zero beyond 18.
- Center: one choice for no center; one for an even center coefficient at most 18; otherwise zero. The singleton canonical case separately excludes center zero.

For `s :: h`, the exact multiplicity is

```lean
pairCount true s * centerCount c * natProduct (h.map (pairCount false))
```

The outer factor is at most 9, every inner factor at most 10, and the center factor at most 1. Hence the count is at most `9 * 10 ^ h.length`. `sharp_profile_bound` supplies equality profiles with all pair coefficients 9 and either no center or center coefficient 0. They realize both parities at lengths at least two. The alternative outer coefficient 10 also attains its factor 9. The width-one maximum is separately 1, and the width-zero count is 0.

The prior independent Bounds review remains in `bounds-review.md` and `bounds-review.json`; the present review rebuilt that same source hash again. Together with Core and Numeric's exact length theorems, these bounds apply to the corresponding enumerated digit lists and ordinary integer fibers, with the numerical interpretation's hypothesis stated next.

## 5. Numeric semantic review

`natValue ds` evaluates the finite list as a decimal positional sum through the preserved `DecimalDigits.value`. `digitFn` extends the list by zero outside its actual length. `canonical_to_list` retains exactly the specified finite prefix of a base `Canonical n d L` representation; arbitrary function tails are never counted as distinct objects.

`canonicalDigits_iff` connects the new list predicate to the unchanged base `Canonical` predicate. The base's decimal value injection applies to equal-length lists with digits at most 9. `decimalWidth_unique` supplies the missing length equality for two canonical lists representing the same positive integer, so `natValue_injective_canonical` is valid even before equal length is assumed. As a result, mapping the duplicate-free canonical word list to `Nat` does not collapse distinct entries.

`step_natValue` transports the list pair sums to the preserved `Lychrel196.step`. Its proof uses `FoldedDecimal.step_eq_word_value`. The numerical converse uses `ReverseAddInverse.symmetric_value_injective` for **same-length symmetric coefficient functions bounded by 18**, which is the substantive carry-aware dependency. The related `same_width_step_eq_iff_digitPairSums` explicitly retains equal input length and uses the preserved `same_width_step_eq_iff_pair_sums`.

For `q = coefficientWord h c` and the explicit hypothesis `∀ s ∈ q, s ≤ 18`, the final theorem is exactly:

```lean
n ∈ numericFiber h c ↔
  decimalWidth n q.length ∧ Lychrel196.step n = natValue q
```

Here

```lean
decimalWidth n L = (0 < L ∧ 10 ^ (L - 1) ≤ n ∧ n < 10 ^ L)
```

This is a complete ordinary-natural-number inverse fiber **at the prescribed input width**. Its right side has no digit-list or digit-function witness. It is not a general claim of injectivity across different widths, and it does not count outputs of an autonomous pair-word transition. Cross-width reverse-add collisions exist, so the width qualification is substantive.

`mem_numericFiber` includes bounded but unrealizable profiles, such as an odd center or zero outer pair sum; the equivalence then says the corresponding fixed-width numerical fiber is empty. Its coefficient bound may not be dropped. For profiles with a coefficient greater than 18, the digit enumeration and its length/nodup theorems still apply and give no realizations, but the general numerical-fiber equivalence is not asserted without its bound. The wording “inadmissible profiles” in the source theorem's comment is therefore interpreted within that theorem's explicit bound hypothesis.

`numericFiber_nodup` and `length_numericFiber` establish exact distinct-number multiplicity `profileCount h c`; `length_numericFiber_cons` gives the product formula and `length_numericFiber_cons_le` gives the sharp profile upper bound. These do not use a count of infinite digit-function tails.

## 6. The complete 887 inverse image

The specific profile is `h = [7]`, `c = some 18`, so its least-significant-first coefficient list is `[7, 18, 7]` and its positional value is `7 + 18 * 10 + 7 * 100 = 887`.

`numericFiber_887` kernel-checks the concrete list:

```lean
numericFiber [7] (some 18) = [790, 691, 592, 493, 394, 295, 196]
```

`three_digit_preimages_887` proves the exact three-digit equivalence. The final theorem strengthens this particular example to **all natural numbers**, with no width assumption:

```lean
Lychrel196.step n = 887 ↔
  n ∈ [790, 691, 592, 493, 394, 295, 196]
```

The extra width exclusion is explicit. The private theorem `small_not_preimage_887` proves, by ordinary kernel-checked `decide`, that every `n : Fin 100` fails to map to 887. It is included in the compiled theorem audit and has no axiom dependencies. For any hypothetical inverse image, `n ≤ step n = 887` gives the upper bound below 1000; excluding `n < 100` gives the lower bound 100. The three-digit theorem then supplies the seven-element list. Conversely, membership in the list implies the same reverse-add equation through the three-digit theorem.

Thus the final 887 result is a genuine all-width inverse-image classification for that single output. It does not silently generalize the fixed-width profile theorem.

## 7. Scope and retained evidence

This review approves exact finite digit-split enumeration, its cardinality and sharp profile bounds, the corresponding ordinary integer inverse fibers at a fixed width under bounded symmetric coefficients, and the separately proved all-width 887 example. It establishes no infinite-orbit avoidance theorem and no resolution of the 196 conjecture.

Retained evidence under this report's prefix includes all five fixed sources, the runner, both generated audits, all eight command logs, and `full-review.json` with all per-declaration axiom responses and hashes. `full-review.semantic.json` records this semantic verdict and the report hash. There was no remote mutation, Git commit, source edit, or hosted-computation trigger by this reviewer during the review.
