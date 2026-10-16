# Independent semantic review: ordinary one-step digit-sum collapse

Reviewer: **Agent #9/runtime-audit**. Mathematical author: **Agent #9/horizon-safety**.

**Result: independent semantic review PASS 和 fresh kernel-checking gate PASS.** The frozen source below passed a new six-module build with explicit `--trust=0`, followed by an exhaustive module-origin audit of 1,320 theorem constants 和 183 safe definitions. The new module contributes ten public theorems plus eleven generated theorem declarations, with zero safe definitions. All ten public exports have literal type 和 axiom reports. The axiom union is exactly `propext`, `Classical.choice`, 和 `Quot.sound`. Raw evidence is retained in `runs/full-001/`.

## Exact reviewed inputs

| Input | Identity |
| --- | --- |
| New source | `Agent9OneStepDigitSumCollapse.lean` |
| Source SHA-256 | `d9cb44e04c4f4bdbda42d7f877afeabd6e0c59cb085dfc023598707c7d0177db` |
| Source Git blob | `a36a7c75aaf87d0ac72571286cbbdb8ba9a70134` |
| Independent registry SHA-256 | `6458f453cf9502a96e0f9e52d4333feb9ae9c036164bb3c9a31b40c962f4c68c` |
| Corrected-heading contract SHA-256 | `81504ce4b52bc2a8465b372e27ec769909f0297cb9fd44ebe03ed6100373ec60` |
| Source main | `58afcada8047e015b8f4233b96c44c7c5b9c4162` |
| Claim coordination commit | `7b6c27c014bc00e55a75da530b8398b791451624` |

The original written source is `proofs/research/continuation/strengthening_notes.txt` at commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, blob `7103ee939d82740b970dd23fb91e9db50db4ea54`, SHA-256 `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f`. Section 8 is headed “What obstructs stronger conclusions from the old static bound alone”. The retained manuscript bytes 和 exact Git provenance commands are in `inputs/strengthening_notes.txt` 和 `provenance-logs/`.

The original preparation contract used a different descriptive section heading. Root corrected that heading without changing the target, hypotheses, source identity, or exclusions. Both exact contract versions are retained under `inputs/`; `provenance.json` remains the original preparation receipt.

## What the universal theorem actually states

The principal theorem is `P196.Agent9.OneStepDigitSumCollapse.framedNine_realization_digitSums`. Its parameters `r n : Nat` 和 `d : Nat → Nat` are universally quantified. Its only realization assumptions are:

```lean
hc : Canonical n d (2 * r + 2)
hr : ∀ i, i < 2 * r + 2 →
  columnSum d (2 * r + 2) i = framedNine (2 * r) i
```

Its conclusion is:

```lean
digitSum n = 9 * r + 10 ∧ digitSum (Lychrel196.step n) = 2
```

The reused definitions are the original `DecimalMass.digitSum` 和 `Lychrel196.step`. The first is the ordinary base-ten recursion using remainder 和 quotient, with value zero at zero. The second is `n + reverse10 n`. The result therefore concerns ordinary integer digit sums before 和 after the actual reverse-and-add update. No replacement statistic or intermediate symbolic map appears in the conclusion.

`DecimalDigits.Canonical n d L` requires positive width, bounded digits, a positive most significant digit, 和 `value d L = n`. Consequently the width is the actual canonical width of the represented integer. The column hypothesis ranges only over `i < L`, matching the finite-word hypothesis of the original realization theorem. It does not constrain the digit function outside its finite representation.

## Input-sum calculation

The new `framedNine_prefix_wordSum` 和 `framedNine_wordSum` sum the finite coefficient word with endpoints ten 和 `k` interior nines:

\[
\operatorname{wordSum}(\operatorname{framedNine}(k),k+2)=9k+20.
\]

`framedNine_realization_digitSum_double` applies the original `DecimalMass.digitSum_value` to the canonical digits, uses `wordSum_columns` to identify the mirrored pair-word sum as twice the digit sum, 和 transfers the finite column equalities with `wordSum_congr`. This proves

\[
2\operatorname{digitSum}(n)=9k+20
\]

under exactly the given canonical-realization assumptions. The required `k=2r` formula follows by natural-number arithmetic. The generic `k` lemma remains conditional; it asserts no canonical realization for odd `k`. Its odd-case impossibility is consistent with the odd right-hand side of this doubled-sum identity.

## Next-sum calculation 和 numeric bridge

The next-sum theorem reuses `SeamAnnihilation.framedNine_realization_step_value` 和 `framedNine_value`, which identify the actual next integer with `value (framedNine k) (k+2)` 和 with `11 * 10^(k+1)`. The new source does no replacement realization or normalizer construction.

The existing carried-digit formula `framedNine_output` has its only one at position `k+1`. The finite output prefix below that position has unweighted sum zero; including that digit makes the width-`k+2` output sum one. The existing final carry formula contributes another one at the new most significant position. The extended width is `(k+2)+1`, so both positions are included.

The source explicitly proves that every extended digit below that width is at most nine using `framedNine_extended`. It transports the scalar sum through the existing `value_extended`, `value_output`, `digitSum_value`, 和 `wordSum_extended` lemmas. Thus the conclusion is the ordinary digit sum of the actual integer update, exactly two. The proof contains no hidden bound on a carry budget 和 no additional assumption on the digit sum being proved.

## Parameter zero 和 the nonvacuous family

The universal scalar theorems explicitly include `r=0`. The corresponding width is two, the initial sum is ten, 和 the common first output is 110, with digit sum two. The source makes no new nonpalindrome claim at this parameter.

Existence is handled separately by `framedNine_digitSums_realized`, which assumes `0 < r` 和 obtains `n`, `d`, positivity, canonical width, 和 the finite column equality directly from the unchanged `SeamAnnihilation.even_family_realized`. It then applies the universal scalar theorem to those witnesses. The additional palindrome information returned by the original theorem is simply unused. This matches the manuscript's even `k ≥ 2` range through `k=2r` without inventing a new seed construction.

## One witness exceeds both thresholds

`arbitrarily_large_digitSum_and_width (B : Nat)` chooses `r=B+1`. The resulting original witness has

\[
\operatorname{digitSum}(n)=9B+19,\qquad L=2B+4,
\]

so `B < digitSum n` 和 `B < L` both hold, including when `B=0`. The theorem existentially binds one positive integer `n`, one digit function `d`, 和 one width `L`; every conjunct refers to that same witness. The smaller `arbitrarily_large_digitSum` theorem only projects away the digit representation 和 width.

This is the quantified one-step collapse requested by the contract. The witness varies with the threshold. The result supplies no new statement about digit-sum divergence, monotonicity, or avoidance of palindromes along one fixed infinite orbit.

## Reuse 和 review history

The exact import chain is:

1. `LychrelDigitSums` imports `Std`.
2. `IncomingCarrySensitivity` imports `LychrelDigitSums`.
3. `RawSymmetryObstruction` imports `IncomingCarrySensitivity`.
4. `IntrinsicSeam` imports `RawSymmetryObstruction`.
5. `SeamAnnihilation` imports `IntrinsicSeam`.
6. `Agent9OneStepDigitSumCollapse` imports `SeamAnnihilation`.

`dependency-registry.json` records all five original blob IDs, SHA-256 hashes, source paths, 和 original commit/path provenance. Preparation checked their identity both at the written-source commit 和 at the source-main flattened aliases. The independent verifier checks the original bytes again while creating the fresh source snapshot.

The first author attempt had two local proof-script failures. One was a redundant `omega` after the preceding simplification had closed its goal. The other was the missing `value_output` rewrite after `value_extended`; the independent reviewer identified this before seeing that compiler result. The author preserved the first attempted source 和 logs, then made these script corrections without changing the theorem types. Those author attempts are evidence of the author's development history; the independent review gate begins only after the corrected source was frozen.

## Verification boundary

The independent verifier creates a new source tree 和 an initially empty project object directory. It compiles every registered project source with official Lean 4.19.0, explicit `--trust=0`, one compiler thread, 和 asynchronous elaboration disabled. The generated audit prints the type 和 literal transitive axiom report of every public export, then uses module origins to enumerate every selected project theorem 和 safe definition, including generated declarations.

Acceptance permits only `propext`, `Classical.choice`, 和 `Quot.sound` in their transitive axiom closures. Source checks reject proof placeholders, new axiom declarations, `native_decide`, 和 the other recorded kernel-bypass tokens. Exact registry closure, original source provenance, runtime identification, 和 unchanged selected inputs are additional gates.

The supplied official `Init`, `Std`, 和 `Lean` runtime objects are used as provided. This run rebuilds the entire selected project closure; it does not independently rebuild the Lean runtime or claim a build of unrelated repository sources. Runtime file hashes 和 actual command lines are retained in the raw result.
