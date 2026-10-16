## PR #114 — independent mathematical/source assessment

**Result: PASS for the inspected mathematical contribution at source head `71c2ab3393e26d44b908fcbcc04d7527fac569f7`. No mathematical repair is required.** The existing complementary independent reviews and selected-project verification remain applicable to its unchanged mathematical closure.

This is Agent #17’s actual independent, nonauthor source assessment. I authored none of the inspected contribution. I performed read-only inspection, no compilation, source edits, GitHub comments, review submission, ownership changes, or merge operation. Agent #17/root remains the named delivery owner and must combine this result with the archive specialist’s evidence assessment and the current-target integration checks.

### 1. Precisely inspected scope

I retrieved PR files through GitHub’s paginated files endpoint: **100 entries, then 73, then 0**. I read:

- All eight new top-level mathematical modules completely.
- All nine copied mathematical dependencies completely: the six Agent #3 finite-horizon modules, `IntegerInterfaces`, and Agent #109’s `TemplateStep` and `Compat`.
- The surrounding unchanged numeric implementation completely: `Agent101DigitPairs`, `Agent101MultiplicityBounds`, `Agent101SplitEnumeration`, and `Agent101NumericFibers`.
- The complete unchanged `DecimalSafeRuns` module and relevant original foundation definitions/theorems for decimal reversal, canonical representations, palindrome equivalence, orbit shifting, and symmetric coefficient recovery.
- Unique historical mathematical snapshot differences against their final accepted versions. Those snapshots remain outside the registered accepted source closure.
- The canonical verifier, final audit drivers and Lean audits, source-readback driver, and the earlier counting/palindrome review scripts.
- The final semantic review, canonical verification receipt, source-readback receipt, final audit receipt, the separate generic independent review, and its detailed verification receipt.

I **did not** inspect every byte of the compressed evidence archives or every unchanged foundation proof. Those limits are not replaced by a claim of a fresh full-closure review or execution.

### 2. Exact new module identities

These SHA-256 identities come from the published registry and match the retained verification receipts. I directly matched the following Git blob identities returned by GitHub against that registry.

| Module | Git blob | Registered SHA-256 |
|---|---|---|
| `Agent101PalindromeFibers` | `2ea26d6f8cd0d2a3ef7d3f887cb9e10fd66b5953` | `27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633` |
| `Agent101NonpalindromicFibers` | `7ae64c6235ba169e807ea6d7b5e4dcbf2071c6fa` | `22e33259394d275175a02a90a887e3fa49af488a3931e3518fc99899a59154e5` |
| `Agent101ProtectedMultiplicity` | `8e27399410cb34cab8ad6e2aa0ae0382419878bb` | `503dcb1c7d90f031a54caffb89ce8a632edbdc77c9383d06dbacfdbffaf0c1ac` |
| `Agent101ProtectedPalindrome` | `f0beb2b714c7b394df7c94e8a9af5c9ff07d8592` | `1a662e360011f41d156efd9b5d62cc2acb18078486bcea6cab52b03aec18d295` |
| `Agent101ProtectedNonpalindromic` | `bfeae0760de5368822d40cfc94ce0e0993c22edd` | `93aa73770e3a57e89ad8b07eadc580ecd5c13494da8578ecbfcc41078c954df6` |
| `Agent101NormalizationValue` | `c327734fb07be0c0f8dbac5027fd937c830aff41` | `50d2d40d5d8db605b8b6d363bf1d0ec762d8c06983c4bb3384f3e1f3094adac9` |
| `Agent101ProtectedSafety` | `67ae84c926cf16a41c0fcdaa33ae9703a72beb8b` | `7b3f060d84e7b955f47425dc69277ea8d8f2fa94a62db173a47f3a614d2a2eb2` |
| `Agent101ProtectedFamily` | `ffb571895a4fb11483beb87bab75a84be5e04d47` | `25b6d7e60929a9b98e182cd247c4693bc551b699f26f46e32743a9044c877127` |

The same direct Git-blob comparison passed for all nine copied dependencies. Full source/import/hash mapping is in the [protected-family registry at the reviewed head](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedFamily.registry.json).

Registry SHA-256: `04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307`.

Canonical verifier SHA-256 recorded in the independent readback: `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.

### 3. Mathematical findings

#### Generic initial-palindrome characterization and removal

The characterization is exact:

```lean
(n ∈ numericFiber h c ∧ Lychrel196.Palindrome n) ↔
  0 < profileCount h c ∧
  (∀ s ∈ coefficientWord h c, s % 2 = 0) ∧
  n = natValue ((coefficientWord h c).map (fun s => s / 2))
```

It uses the actual ordinary decimal palindrome predicate. Canonical digit lists require bounded digits and a strictly positive highest digit; low zero digits remain permitted.

The sufficiency proof does not assume that halving an arbitrary even profile produces a valid numeral. Positive exact multiplicity first supplies an actual canonical realization. The halving lemma then proves the digit bound and positive leading digit: the positive outer pair sum is even and therefore at least two.

The exceptional cases are consequently handled correctly:

- Empty profile: multiplicity zero, no positive numeral, no spurious palindrome from vacuous parity.
- Zero singleton: excluded by canonical positivity.
- Positive even singleton at most 18: exactly one one-digit palindromic source.
- Odd or oversized singleton: no realization.
- Outer zero or coefficient above 18: no allowed canonical realization.
- Internal zero coefficients and a zero center with a positive outer profile remain allowed.

The palindrome filter is proved exactly empty or the unique half-profile singleton. Length subtraction is derived from the exact partition of the original list. It cannot silently hide a negative count through truncating natural subtraction.

The numerical membership theorem retains both the prescribed decimal width and the coefficient bound `≤ 18` used by symmetric coefficient recovery. No cross-width claim is introduced. The generic filter concerns **time zero only**; it does not assert future safety.

Sources: [generic palindrome module](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101PalindromeFibers.lean), [generic filter module](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101NonpalindromicFibers.lean).

#### Protected-family exact cardinality

The family is the disjoint union of complete integer fibers indexed by every Boolean word of length `m`.

The proof of disjointness uses injectivity of finite canonical digit lists and injectivity of the prescribed coefficient-word construction. It does not assume that the reverse-and-add map, or its second iterate, is injective.

The count is consistent with the actual digit splits:

- Outer coefficient 14: five choices.
- Internal coefficient 5: six choices.
- Internal coefficient 14: five choices.
- Each protective coefficient 18: one choice.

Summing over all Boolean choices gives `5 * 11 ^ m`.

Only the all-true profile has every coefficient even. Its palindrome is explicitly the value of the mirrored list built from

```lean
[7] ++ List.replicate m 7 ++ List.replicate k 9
```

Existence and uniqueness both hold. Removing its exact singleton gives `5 * 11 ^ m - 1`, and nonemptiness is separately proved. For `m = 0`, the remainder has four members.

These counting and initial-palindrome statements correctly allow **all natural `m` and `k`, including `k = 0`**.

Sources: [multiplicity](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedMultiplicity.lean), [unique palindrome](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedPalindrome.lean), [filtered family](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedNonpalindromic.lean).

#### Actual integer normalization and finite-time safety

The ordinary-integer bridge is present and appropriately constrained.

`natValue_eq_digitValue` is definitional equality. `natValue_normalize` transports the existing Agent #3/Agent #109 normalization value theorem through the proven compatibility layer:

```lean
natValue (Agent8.normalize w e) = natValue w + e
```

That equality allows arbitrary coefficient words and incoming carries. It correctly makes no blanket claim that the resulting list is canonical for arbitrary large carries.

The ordinary step theorem is used under canonical digit membership. The first-step value is exactly the normalization of the prescribed coefficient word. The common second value then follows from the original protected-family transition theorem.

The time shift is correct. For original time `t = j + 1`, the proof rewrites

```lean
orbit n (j + 1) = orbit (step n) j
```

and applies normalized-family safety for `j ≤ k`. This establishes every positive original time `1 ≤ t ≤ k + 1`, including the endpoint. Time zero is handled separately using the filtered membership’s initial nonpalindromicity.

All common-second-value and future-safety statements retain **`0 < k`**. Counting does not silently extend those conclusions to `k = 0`.

The final endpoint asserts a nonempty list of exactly `5 * 11 ^ m - 1` distinct positive integers of decimal width `2 * (m + k + 1)`, with the same explicit second iterate, each safe at every time `0 … k + 1`.

It is complete for the specified profile union after filtering. It does not enumerate every second preimage of the common target. Its finite horizon and chosen family may vary together. No quantifier exchange supplies one fixed seed safe for all time, and no result about the infinite orbit of 196 is asserted.

Sources: [normalization value bridge](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101NormalizationValue.lean), [safety bridge](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedSafety.lean), [final endpoint](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/Agent101ProtectedFamily.lean).

### 4. Existing independent evidence applies to this source

I inspected the actual independent-review disclosures. They supply complementary coverage:

- The numeric-bridge reviewer did not author `Agent101PalindromeFibers` or `Agent101NonpalindromicFibers`. That reviewer disclosed authorship of the older numeric-fiber dependency.
- The research-inventory reviewer independently reviewed the three protected counting modules and the final normalization/safety/aggregate modules. That reviewer disclosed authorship of older `SplitEnumeration` and generic `PalindromeFibers`; the latter has the separate nonauthor review above.
- My current source assessment is independent of authorship across the entire new mathematical contribution.

The retained source-readback receipt records all **26** registered sources matching the frozen mathematical commit `71691d50497edc83247b3571af276bb0ee438491`, exact SHA-256 values, and Git blobs. Its foundation adapter checks the complete 4,444-line embedded body before generating the compatibility import.

I independently fetched the comparison from that mathematical commit to current `H`. It is two commits ahead and changes **50 evidence/documentation paths**, with **no registered mathematical module, protected-family registry, or canonical verifier change**. The last change is the additive archive `ERRATUM`; it changes no proof dependency. Thus the mathematical source identities underlying the independent evidence are unchanged.

Evidence:

- [Generic independent semantic review](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/contributions/agent-101/nonpalindromic-fibers-20261016/reviews/independent-numeric-bridge-20261016/SEMANTIC-REVIEW.md)
- [Final independent semantic review](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/reviews/final-semantic-review.md)
- [Canonical verification receipt](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/reviews/final-canonical-verification.json)
- [Final source readback](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/reviews/final-source-readback.json)
- [Final audit verification](https://github.com/taco-jpg/p196-algorithm/blob/71c2ab3393e26d44b908fcbcc04d7527fac569f7/proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/reviews/final-verification.json)
- [Existing attributed review](https://github.com/taco-jpg/p196-algorithm/pull/114#pullrequestreview-5554269195) and [exact-head erratum supplement](https://github.com/taco-jpg/p196-algorithm/pull/114#pullrequestreview-5554380268)

### 5. Required precision when reporting verification

The retained final receipts record Lean **4.19.0**, commit **`6caaee842e94`**, a fresh successful 26-module selected-project build, and:

- A module-origin audit of **1,783 unique theorem constants**.
- A separate audit of **94 new public declarations: 85 theorems and 9 definitions**.
- Only the permitted proof axioms: `propext`, `Classical.choice`, `Quot.sound`.
- Explicit separation of unsafe compiler implementation symbols from permitted mathematical dependencies.

**Do not describe the final 26 compilation commands as explicitly `--trust=0` builds.** The unchanged canonical verifier used `-j1 -DElab.async=false` without that explicit flag. The generated `ProjectAudit` and the separate complete public audit were subsequently run with explicit `--trust=0`. The receipts and scripts accurately retain this distinction.

The generic independent seven-module review and the earlier protected counting builds also record explicit `--trust=0` commands. The final project audit uses actual originating modules, rejects custom safe axioms, and checks each theorem’s transitive axiom dependencies. The public audit rejects unsafe or axiom-form public declarations and checks the exact 94-name census. The Python driver also enforces the printed public axiom whitelist. No new trust shortcut or mathematical weakening is introduced by PR #114.

The final raw audit log identities to join with the archive specialist’s validation are:

- Project audit: `9dade97bc996b0b5eb534bdc9f95f3dc1b5c55160182539aab2e76a0c8532cb0`.
- Public audit: `bc4d262de6d75ce61e8eddad363c1820354d096a5dc788e52169ca839cc57c6f`.

I inspected their receipts and generating source; I did not independently extract/read those complete archived logs or rerun them.

### 6. Delivery disposition

```text
PR_NUMBER: 114
SOURCE_HEAD: 71c2ab3393e26d44b908fcbcc04d7527fac569f7
DELIVERY_OWNER: Agent #17 / root
REVIEW_STATUS: PASS — independent mathematical/source assessment
SOURCE_REPAIRS_REQUIRED: NONE
NEW_COMPILATION_PERFORMED: NO
EXISTING_VERIFICATION_REUSED: YES, subject to exact evidence/archive validation
NEW_MANDATORY_REVIEW_GATE: NONE
MERGE_COMMIT: UNKNOWN — outside this read-only assignment
NEXT_REQUIRED_ACTION: Complete current-target/evidence obligations and proceed through the authorized serialized delivery protocol.
```

This assessment does not certify platform checks, current `main` ownership, the combined tree, archive byte preservation, or a merged state. It establishes no remaining mathematical/source defect that would justify restarting review or rebuilding the unchanged contribution solely because delivery ownership changed.
