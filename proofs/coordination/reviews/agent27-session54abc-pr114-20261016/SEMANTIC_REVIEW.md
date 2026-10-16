# Independent semantic review of PR #114

**Disposition: PASS for the exact mathematical contribution at `71c2ab3393e26d44b908fcbcc04d7527fac569f7`. No mathematical repair is requested.**

This is a genuine nonauthor semantic review by `/root/pr114_semantics`, delegated by Agent #27. I authored none of the eight new modules or their dependencies. The review is suitable for handoff to Agent #17, the current delivery owner. It does not create another approval requirement or supersede the qualifying independent reviews already attached to PR #114.

I fully read the eight new modules, retrieved and independently SHA-256 checked all 26 registered source modules, and traced the relevant decimal semantics, counting, normalization, and finite-safety dependencies. I did **not** execute Lean, perform a local build, inspect a combined integration tree, extract the evidence archives, modify source, submit a remote review, or mutate GitHub.

## 1. Exact source and verification provenance

Repository: `taco-jpg/p196-algorithm`.

| Identity | Commit |
|---|---|
| Reviewed PR #114 head, H | `71c2ab3393e26d44b908fcbcc04d7527fac569f7` |
| Mathematical source freeze | `71691d50497edc83247b3571af276bb0ee438491` |
| Previous evidence head | `2335bcaf40a70dd5e158d2ca033fed7134871897` |

Sources were obtained through the GitHub connector using the full immutable head H. I independently recomputed SHA-256 over the UTF-8 source bodies returned by the connector, using an in-memory JavaScript implementation checked against the standard empty-string and `abc` digest vectors. **All 26 source digests match the registry.** This is an independent check of the retrieved source bodies; it is not a claim of local-checkout hashing or a new Git-blob audit.

The same calculation confirmed:

| Item | SHA-256 |
|---|---|
| `proofs/Agent101ProtectedFamily.registry.json` | `04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307` |
| `proofs/verify_project__214bf7673efe116b.py` | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |
| Protected contribution `reviews/final-semantic-review.md` | `73074acf1732b73697e2b58f04bbc04d7f0765114f9f8409b3acad62c26a5e68` |
| Protected contribution `reviews/final-verification.json` | `7774847ae79f49026828fb8def45675e68efc13621953a056c02bcdd4deb3db4` |

I directly inspected both GitHub comparisons. The mathematical freeze to the previous evidence head changes 49 evidence/documentation paths, without changing the 26 registered sources, registry, or verifier. The previous evidence head to H adds only the 73-line `archives/final-independent-ERRATUM.md`, with no deletion or mathematical change. The existing mathematical reviews therefore concern the same proof sources reviewed here. [Source registry](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedFamily.registry.json), [first comparison](https://github.com/taco-jpg/p196-algorithm/compare/71691d50497edc83247b3571af276bb0ee438491...2335bcaf40a70dd5e158d2ca033fed7134871897), [second comparison](https://github.com/taco-jpg/p196-algorithm/compare/2335bcaf40a70dd5e158d2ca033fed7134871897...71c2ab3393e26d44b908fcbcc04d7527fac569f7).

I also read the current root `AGENTS.md` and `proofs/PUBLICATION_POLICY.md`. This review preserves their distinction between a finite result and an all-time Lychrel claim, and makes no publication, integration, history-rewriting, or source-writing action.

## 2. Files and dependency scope

### Eight new modules fully read

Every path below is relative to the repository root at H.

| File | SHA-256 |
|---|---|
| `proofs/Agent101PalindromeFibers.lean` | `27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633` |
| `proofs/Agent101NonpalindromicFibers.lean` | `22e33259394d275175a02a90a887e3fa49af488a3931e3518fc99899a59154e5` |
| `proofs/Agent101NormalizationValue.lean` | `50d2d40d5d8db605b8b6d363bf1d0ec762d8c06983c4bb3384f3e1f3094adac9` |
| `proofs/Agent101ProtectedMultiplicity.lean` | `503dcb1c7d90f031a54caffb89ce8a632edbdc77c9383d06dbacfdbffaf0c1ac` |
| `proofs/Agent101ProtectedPalindrome.lean` | `1a662e360011f41d156efd9b5d62cc2acb18078486bcea6cab52b03aec18d295` |
| `proofs/Agent101ProtectedNonpalindromic.lean` | `93aa73770e3a57e89ad8b07eadc580ecd5c13494da8578ecbfcc41078c954df6` |
| `proofs/Agent101ProtectedSafety.lean` | `7b3f060d84e7b955f47425dc69277ea8d8f2fa94a62db173a47f3a614d2a2eb2` |
| `proofs/Agent101ProtectedFamily.lean` | `25b6d7e60929a9b98e182cd247c4693bc551b699f26f46e32743a9044c877127` |

**Preservation note — SHA transcription correction:** The first chat rendering contained a transcription error in the `Agent101ProtectedMultiplicity.lean` table cell and immediately supplied the correct digest in a correction paragraph. This saved report corrects the table cell itself to the exact SHA-256 computed during review and recorded in the registry:

```text
503dcb1c7d90f031a54caffb89ce8a632edbdc77c9383d06dbacfdbffaf0c1ac
```

This is a report-transcription correction only. It changes no reviewed source, verification result, substantive finding, or review limitation.

### Eighteen exact dependencies inspected

The nine dependencies located directly under `proofs/` are:

```text
Agent101DigitPairs.lean
Agent101MultiplicityBounds.lean
Agent101SplitEnumeration.lean
Agent101NumericFibers.lean
Lychrel196Research__c696e0ea3db39d92.lean
LychrelDigitSums__0810ace083af80c5.lean
PeriodObstructions__70ce034b31b5b218.lean
ActualWordBridge__7f032d27940694a8.lean
DecimalSafeRuns__aaaac5a66315c5e2.lean
```

Seven are under:

```text
proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/dependencies/agent3/
```

Their names are `FamilyDefinitions.lean`, `FamilyCardinality.lean`, `FiniteHorizonOverflow.lean`, `SafetyBridge.lean`, `NormalizedSafety.lean`, `FiniteHorizonTheorem.lean`, and `IntegerInterfaces.lean`.

The remaining two are `TemplateStep.lean` and `Compat.lean` under the sibling `dependencies/agent109/` directory.

I inspected the relevant definitions and proofs throughout this closure, including the original reversal and canonical-representation bridge, symmetric coefficient-value injectivity, the complete digit-split enumeration, value-preserving normalization, the protected-word transition, and transport of finite safety to ordinary integer orbits. This is not a claim to have repeated an exhaustive semantic review of every unrelated result in the large historical foundation modules.

## 3. Ordinary decimal semantics and generic fibers

The underlying arithmetic is the unchanged `Lychrel196` arithmetic:

```text
reverse10 n = reverseFuel n n 0
Palindrome n = (reverse10 n = n)
step n = n + reverse10 n
orbit n 0 = n
orbit n (t + 1) = step (orbit n t)
```

The existing `reverseFuel_correct` and `reverse10_value` connect executable ordinary reversal to finite positional reflection. Leading zeros created by reversal are discarded numerically. For example, the interpretation permits a source ending in zero; it does not require its reversed numeral to retain the source width.

The new generic results count finite canonical digit lists mapped to natural numbers. They do not count infinite digit functions or unconstrained tails. Canonicality requires bounded decimal digits and a strictly positive highest digit. Consequently:

- Zero low digits are permitted.
- Zero high digits and empty positive numerals are excluded.
- `decimalWidth n L` requires `0 < L` and the actual interval `10^(L-1) ≤ n < 10^L`.
- Injectivity of `natValue` on canonical finite lists ensures that the list counts are counts of distinct ordinary integers.

The numerical fiber equivalence retains the prescribed input width and the coefficient bound at most 18. Its reverse implication uses the existing injectivity of fixed-width evaluation on symmetric coefficient words, including carries. It does not silently assume that coefficients greater than nine are ordinary digits or that general base-ten coefficient evaluation is injective.

### Initial-palindrome characterization

`palindrome_natValue_iff_reverse` correctly applies the existing decimal-palindrome theorem under canonicality. A palindromic source has each mirrored coefficient equal to twice its digit, so its entire digit list must equal the coefficient word divided by two.

Sufficiency is also established. Positive `profileCount` supplies an actual canonical realization. When all pair sums are even, halving them preserves the digit bound and produces a positive highest digit: a positive even outer sum is at least two. Thus the halved profile is proved canonical rather than assumed canonical.

The central endpoint is:

```text
Agent101.palindrome_mem_numericFiber_iff
```

It characterizes a palindromic member by positive exact profile count, evenness of every coefficient, and equality to the explicit half-profile value. Existence and uniqueness follow without hidden profile-validity premises.

### Empty and exceptional profiles

The generic statements correctly handle:

- Empty half with no center: zero realizations despite vacuous evenness.
- Singleton center zero: zero positive canonical realizations.
- Positive even singleton center at most 18: one one-digit source, which is palindromic.
- Odd or oversized center: no realization.
- Outer coefficient zero: no leading-positive realization.
- Any coefficient above 18: no bounded decimal split.
- Internal zero coefficients or a zero center with a valid positive outer profile: permitted.

The nonpalindromic filter removes initial palindromes only. Its membership theorem retains the ordinary first-step equation and fixed width; it makes no future-safety claim. For example, 20 is initially nonpalindromic and satisfies the profile `[2]`, but its next value is the palindrome 22. This interpretation agrees with the existing independent generic review. [Generic review](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/contributions/agent-101/nonpalindromic-fibers-20261016/reviews/independent-numeric-bridge-20261016/SEMANTIC-REVIEW.md).

The subtraction formula is justified by an exact partition into the palindrome and nonpalindrome filters. The palindrome filter is proved empty or a singleton, so natural-number subtraction cannot conceal a larger removal or a false count.

## 4. Protected family counting and the unique removed seed

For each Boolean word `xs` of length `m`, the specified half-profile is:

```text
[14] ++ xs.map choice ++ replicate k 18
choice false = 5
choice true  = 14
```

It is followed by its reverse, with no center.

The complete ordinary-integer realization count is obtained from:

- Five outer digit splits for coefficient 14.
- Six inner splits for coefficient 5.
- Five inner splits for coefficient 14.
- One split for every protective coefficient 18.

Summing over all Boolean words therefore gives `5 * 11^m`, independently of `k`. The proof also establishes duplicate freedom within each fiber and disjointness between different Boolean profiles. Disjointness follows from canonical digit-list injectivity and injectivity of `inputWord`; it does not assume injectivity of the two-step map.

A palindrome requires all coefficients to be even. The only eligible Boolean word is the all-true word. Its unique palindromic seed is the value of:

```text
palindromeHalf m k ++ (palindromeHalf m k).reverse
```

where:

```text
palindromeHalf m k = [7] ++ replicate m 7 ++ replicate k 9
```

Existence is proved from positive multiplicity. The theorem `protectedSeeds_palindrome_iff` therefore establishes exactly one palindrome across the entire union, not merely at most one.

The removal theorem proves that the palindrome filter is precisely `[palindromeSeed m k]`. Partitioning the full list yields:

```text
1 + (protectedNonpalSeeds m k).length = 5 * 11^m
```

The resulting count `5 * 11^m - 1` is accompanied by a separate nonemptiness theorem. It is a substantive family, including when `m = 0`.

### Boundary `m = k = 0`

The definitions specialize to the five seeds:

```text
95, 86, 77, 68, 59
```

Removing the unique palindrome 77 leaves four seeds, exactly as the theorem states.

As an interpretive arithmetic check, every seed has first value 154 and second value 605. By contrast, the formal expression `natValue (target 0 0)` is 6545. Thus `0 < k` is a materially necessary restriction on the stated target formula; it must not be dropped. The source correctly keeps counting, membership, and initial-palindrome removal valid at `k = 0`, while restricting the protected target and future-safety theorems to positive `k`.

This arithmetic observation is not represented as a new Lean theorem or build result.

## 5. Normalization, common second value, and exact finite horizon

`Agent101NormalizationValue` introduces no new arithmetic semantics. `natValue_eq_digitValue` is reflexive, and `natValue_normalize` directly reuses:

```text
P196.Agent3.TwoHistory.digitValue_normalize
```

That dependency passes through `Agent109.Compat.normalize_eq` and the existing `Agent109.evalL_norm`. The original attribution is retained.

The normalization-value equality permits arbitrary coefficient words and incoming carries. It does not assert that normalization with an arbitrary large incoming carry necessarily produces a canonical decimal digit list. Canonicality and digit bounds are supplied separately where numerical reversal needs them.

For a member of a protected input fiber:

1. Its first ordinary step is the value of the normalized complete input coefficient word.
2. The unchanged Agent #3 theorem identifies the next ordinary step with `natValue (target xs.length k)`.
3. Family membership replaces `xs.length` with `m`.

The common target is the value of the coefficient list:

```text
[5] ++ replicate m 10 ++ [14] ++ replicate (2*k - 1) 18
    ++ [14] ++ replicate m 10 ++ [5]
```

The result concerns ordinary integer values. The intermediate entries 10, 14, and 18 remain coefficients evaluated arithmetically; they are not misrepresented as individual decimal digits.

### Time indexing

The positive-time transport is exact. For `1 ≤ t ≤ k+1`, write `t = j+1`. The existing identity

```text
orbit (step n) j = orbit n (j + 1)
```

moves the statement to the normalized first value. The original finite-horizon theorem applies at `j ≤ k`. Therefore the final endpoint includes time `k+1`, without an off-by-one loss.

The unfiltered family contains its one initial palindrome, so its safety conclusion correctly begins at time one. The filtered family supplies `¬ Palindrome n` separately at time zero, then uses the positive-time theorem. Its safety statement is therefore exactly:

```text
∀ t, t ≤ k + 1 → ¬ Lychrel196.Palindrome (Lychrel196.orbit n t)
```

for the same selected member `n`, with `0 < k`.

## 6. Accepted endpoint scope

The ten registry endpoints are:

```text
Agent101.Protected.mem_protectedSeeds_numeric
Agent101.Protected.protectedSeeds_nodup
Agent101.Protected.length_protectedSeeds
Agent101.Protected.protectedSeeds_palindrome_iff
Agent101.Protected.mem_protectedNonpalSeeds_numeric
Agent101.Protected.length_protectedNonpalSeeds
Agent101.Protected.protectedNonpalSeeds_nonempty
Agent101.Protected.protectedNonpalSeeds_second_value
Agent101.Protected.protectedNonpalSeeds_safe
Agent101.Protected.protectedNonpalFamily_exact
```

They support the following precise conclusion: for every natural `m` and positive `k`, the explicitly defined filtered list has exactly `5 * 11^m - 1` distinct positive members, each of decimal width `2 * (m+k+1)`, each sharing the explicit second ordinary iterate, and each avoiding palindromes at every time from zero through `k+1`.

Completeness means complete ordinary digit-split realizations of the **specified profile union**, followed by removal of its unique initial palindrome. It does not mean all second preimages of the target.

The family and its seed width may change with the chosen finite horizon. The result does not exchange the quantifiers to obtain one fixed seed safe for all time. It establishes neither decimal Lychrel existence nor the claim for 196. The source, registry scope, and contribution documentation preserve these limits. [Final endpoint source](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedFamily.lean).

## 7. Foundation facade

The `verified_embedded_foundation` adapter is appropriate for this exact closure.

I independently compared the complete retrieved Research source after removing its first `import Std` line with the indicated block of DigitSums. All **4,444 remaining lines**, beginning at DigitSums line 11, match exactly. Both full source hashes match their registry pins.

I inspected the verifier implementation. It checks full source SHA-256 and Git-blob identities, verifies the embedded block using byte-preserving `splitlines(keepends=True)`, and then generates the facade:

```lean
/- Generated compatibility import; original foundation bytes remain retained and are verified in full inside the canonical module. -/
import LychrelDigitSums
```

I also read the retained generated facade, which has this content. The adapter does not replace proof bodies with assumptions or alter the original decimal definitions. It arranges for one shared set of original foundation declarations, already embedded unchanged in DigitSums, instead of compiling duplicate declarations into separate imported modules.

The original Research source remains retained. The registry's Research import of DigitSums describes the **generated build facade**, while the original retained Research file imports Std. That documented distinction is intentional, not an unexplained import mismatch. [Verifier](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/verify_project__214bf7673efe116b.py).

## 8. Existing independent evidence and axiom obligations

I read PR reviews [5554269195](https://github.com/taco-jpg/p196-algorithm/pull/114#pullrequestreview-5554269195) and [5554380268](https://github.com/taco-jpg/p196-algorithm/pull/114#pullrequestreview-5554380268), the underlying final semantic report and machine-readable result, the generic independent review, and the final public-audit source.

Their attribution is adequate:

- The numeric-bridge worker did not author either generic palindrome/filter module, although it authored the older NumericFibers dependency.
- The research-inventory worker did not author the three protected counting modules or the normalization, safety, and final aggregate modules.
- That worker's authorship of the older SplitEnumeration and generic PalindromeFibers dependencies is disclosed. The generic PalindromeFibers module has its separate nonauthor review.
- The parent submitted attributed comments using the shared authenticated account. No separate-account approval or external peer review is claimed.

The existing final receipt records a fresh 26-module build, 1,783 module-origin theorem audits, and audits of all 94 new public declarations: 85 theorems and nine definitions. The source-level census I independently obtained matches those 94 public declarations.

The permitted logical axiom set remains:

```text
propext
Classical.choice
Quot.sound
```

The documented trust-setting distinction must remain intact: the unchanged canonical verifier's original module commands did not explicitly pass `--trust=0`; the subsequent unchanged ProjectAudit and complete public audit did. I did not rerun either stage and do not relabel the historical build.

The module-origin audit checks theorem axiom dependencies and rejects custom safe axioms. The public audit additionally rejects unsafe public declarations and public axiom declarations, with an exact census. Compiler-generated unsafe implementation symbols are recorded separately and are not additional permitted mathematical dependencies. The historical report explicitly does not claim a separate census of every transitive safe definition.

My comment/string-masked scan of all 26 retrieved source bodies found no executable occurrences of:

```text
sorry
admit
sorryAx
axiom
native_decide
ofReduceBool
skipKernelTC
```

That scan is supplementary source inspection, not a substitute for the recorded kernel and axiom checks.

No duplicate independent-review or fresh-build gate is requested here. The existing qualifying evidence applies to the unchanged proof chain. Any integration-specific source or environment change must be assessed against the precise identities and audit scope above.

## 9. Defects, preservation correction, and limits

**Mathematical defects found: none. Required source repairs: none.**

The existing erratum concerns the prose description of the historical canonical `FILES.json`. It correctly distinguishes that 55-entry inventory—27 Lean sources, 27 logs, and one report—from the separate archive manifest recording omitted compiler objects. I read the correction and verified through the GitHub comparison that it is the only change from the previous evidence head to H. I did not independently extract or revalidate archive members.

This report accepts the exact source contribution's mathematical meaning and recognizes the qualifying prior independent evidence. It does not claim a new Lean execution, a repository-wide catalogue audit, accepted integration into main, or postmerge validation. The current delivery owner retains responsibility for the actual integration transaction and its reported outcome.
