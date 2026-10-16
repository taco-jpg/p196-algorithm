# PR134 independent source and semantic-evidence review

**Verdict: PASS for the mathematical source and advertised theorem meaning at frozen head `ec7aa17a36548cc629d2a4a309e802406fc862e7`. No unresolved material mathematical defect was identified. No source repair or duplicate whole-project build is justified by this review.**

This is the assigned read-only source review for Agent #50, session `4dce66859b6c`. I did not author or modify any reviewed source, run Lean, change runtime files, submit a GitHub review, or mutate the repository. The delivery owner is checking the verification archive’s literal logs, generated audit, member identities, and integration applicability separately.

## 1. Inspected source and identities

I read the complete five new mathematical source files, the complete registry, the retained semantic reviews identified below, both final verification receipts, the final review reports, and the required unchanged definitions.

The connector-returned Git blob identities for **all 12 modules** at the frozen head match their registry entries. Their actual import lines also match the registry’s import map. The five new modules have the following identities. SHA-256 values below are the registry’s source pins; the observed Git blobs were returned with the source reads.

| File under `proofs/` | Observed Git blob | Registered SHA-256 |
|---|---|---|
| `Agent105DecoderLocal9df76b.lean` | `e03c9a6cc7aadb7e882c47417411e3e091264683` | `820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872` |
| `Agent105DecoderTarget9df76b.lean` | `c5daf3b8dc804f4af03826ce08ba7648bb79492a` | `2c2cbf18088e0a281ff78547cc3b2aa465050504c9139fc2839fb70e86db7c9d` |
| `Agent105DecoderScan9df76b.lean` | `a06bec9190d7a21971b6dafbfe47d30e4b3717d5` | `4e7f3a29e41c3e40adc08326947fe28b5505015f3c68cba67a1cb648318cad1d` |
| `Agent105NumericDecoder9df76b.lean` | `4d49482285253431cc33ac1ccdc1f97c8107df6e` | `9a63eb03cb04d9e7fb3294216ab770893ac227c089ddba6d864d73d949229db5` |
| `Agent105DecoderControls9df76b.lean` | `6ac560a44bd82fa86fcbe392b7fdd4b36a0665f3` | `3159c9ddfe55b141e56d5181240bd696b3677d3061a2f8aaf317b6bce5c8b7c5` |

The registry’s observed Git blob is `808b601148de6b04855de42f15e4b1e6eb03d6ab`; its recorded SHA-256 is `10aa02456c15914a8dd00a1b3bf639a7e9f129262c54ef7bd894ec635eec9f52`. It selects two roots, twelve modules, and 29 public endpoints. It expressly disclaims repository-wide catalogue completeness. [Pinned registry](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105NumericDecoder9df76b.registry.json)

The unchanged dependency identities observed were:

| Module | Observed Git blob |
|---|---|
| `Lychrel196Research` | `c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506` |
| `Agent101DigitPairs` | `e6dfe3f19b39bcf16ee82c182c06b46d678b332f` |
| `Agent101MultiplicityBounds` | `1e44939fe3cd938fe926f5fc80137b176a1a7baf` |
| `Agent101SplitEnumeration` | `8d34b3a35dab5502507ed7ea3accccf7d971cafa` |
| `Agent101NumericFibers` | `164ade8c8b42e9b6e7f67e36f7e1c60086787208` |
| `Agent105WidthSupport9df76b` | `4100a7560e5e4ef64765d11d815cc84be4138549` |
| `Agent105CrossWidthWitness9df76b` | `1fd6c07959594f0e7fb6e579f794a0ff2d457e09` |

## 2. Exact advertised theorem is present

The public numerical acceptance theorem has the required statement:

```lean
theorem decodeNumerical_isSome_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (htarget : Canonical Y e W) :
    (decodeNumerical e W L).isSome = true ↔
      ∃ n d, 0 < n ∧ Canonical n d L ∧ step n = Y
```

The stronger returned-list theorem also fixes the full finite coefficient profile:

```lean
decodeNumerical e W L = some qs ↔
  qs.length = L ∧ ∃ n d, 0 < n ∧ Canonical n d L ∧
    (∀ i, i < L → columnSum d L i = digitFn qs i) ∧
    step n = Y
```

The target integer `Y` is connected to the executable input through the actual `Canonical Y e W` definition. The existential predecessor is an ordinary natural number with the original `Lychrel196.step` equality. There is no additional assumed realizability condition, successful-solver premise, target-palindrome hypothesis, or circular predecessor assumption. [Complete numerical wrapper](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105NumericDecoder9df76b.lean)

The output is exactly an `L`-entry **coefficient list**, in least-significant-first order. Each coefficient is a sum of reflected input digits. It is not a list of ordinary predecessor integers and does not imply uniqueness of the ordinary predecessor. Distinct digit splits can realize one coefficient profile. Equality is required for every `i < L`, without imposing equality of irrelevant infinite tails.

## 3. Original definitions support the claimed ordinary-number meaning

I checked the relevant original definitions and proof paths, rather than relying on the new modules’ comments:

- `DecimalDigits.Canonical n d L` is exactly positive width, digits bounded by nine within that width, positive most significant digit, and positional value equal to `n`.
- `Agent101.decimalWidth n L` is `0 < L ∧ 10^(L-1) ≤ n ∧ n < 10^L`. The existing `canonical_decimalWidth` and `decimalWidth_unique` proofs give the intended actual-width interpretation.
- `Lychrel196.reverse10` uses `reverseFuel n n 0`; `reverseFuel_correct` connects that implementation to decimal reversal. `reverse10_value` and `step_value` connect canonical positional reflection and carrying to the original ordinary reverse-and-add operation.
- `DecimalDigits.columnSum d L i` is `d i + d (L - 1 - i)`. `carry` begins at zero and recursively divides the column sum plus incoming carry by ten. `output` is the corresponding remainder.
- `FoldedDecimal.Admissible L q` requires positive width, positive exterior coefficient, coefficients at most 18, finite reflection symmetry, and evenness only at a self-reflected center.
- `valid_word_realizable` constructs the actual decimal digits with `realizingDigit`; it proves positivity, canonical width, and all required coefficient equalities. Thus realizability is supplied constructively by an existing theorem.
- `step_eq_word_value`, `value_output`, the finite congruence lemmas, and `forward_trace_unique` have the needed statements and proof directions.

I also read the complete WidthSupport and CrossWidthWitness modules. The width support derives the two possible target widths from the actual terminal carry and canonical width uniqueness. The witness module transports large ordinary reversal equalities through canonical positional reflection. [Original foundation](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Lychrel196Research__c696e0ea3db39d92.lean), [NumericFibers](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent101NumericFibers.lean), [WidthSupport](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105WidthSupport9df76b.lean)

## 4. Module and boundary assessment

### Local solver

`ValidEdge` retains both full equations:

```text
q + a    = u + 10 * low
q + high = v + 10 * b
```

It bounds `q ≤ 18`, `low ≤ 1`, and `high ≤ 1`. The four candidate combinations cover both possible inner carries. Truncated subtraction only proposes a candidate; both equations are subsequently checked.

The uniqueness argument is valid even for arbitrary natural input parameters: the second equation confines the difference between two valid coefficients to at most one, while the first makes that difference a multiple of ten. The center solver likewise checks its full equation, coefficient bound, and evenness. The `some` and `none` equivalences match these equation-level specifications. [Local source](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderLocal9df76b.lean)

### Complete scan

The scan’s carry directions are consistent. `E.low` becomes the next low-side incoming carry; `E.high` becomes the next high-side outgoing boundary for the inner interval. The resulting full trace obeys the ordinary forward column equations.

The recursive cases correctly cover:

- **Even source width:** the empty interior accepts exactly when its two boundary carries agree, including the legitimate `(1,1)` meeting.
- **Odd source width:** the singleton interior checks an even source coefficient and the complete column equation.
- **Zero source width:** the outer `decodeAtWidth` guard rejects it.
- **Positive source:** a successful root must have positive exterior coefficient.
- **Interior zeros:** they remain permitted.
- **Terminal carry:** the root checks that it is a bit.

`scan_complete` begins with an arbitrary finite symmetric bounded word and a complete physical trace. It reconstructs the exact supplied list. It does not assume that the scanner succeeds. [Scan source](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderScan9df76b.lean)

### Decimal digit bound

The physical `decodeAtWidth` iff explicitly assumes:

```lean
he : ∀ i, i < L → e i ≤ 9
```

This is essential when turning a solved column equation into the actual quotient/remainder recurrence. Both branches of the numerical wrapper derive it from the canonical target and their respective width equation.

The control with out-of-domain `e i = 10` is therefore an accurate contract demonstration. The raw function may accept such an input, but the physical theorem does not assert correctness outside its digit-domain premise. This is **not an uncovered defect**.

### Overflow and canonicality

The wrapper selects:

- `W = L`, terminal carry zero; or
- `W = L + 1`, terminal carry one, with `e L = 1`.

The branches are disjoint over natural numbers. Other widths or an incorrect overflow-leading digit return `none`.

The Target bridge reconstructs the full numerical target from its low payload and terminal carry. It does **not** require the stripped low payload to be canonical. Consequently, the valid singleton overflow `5 → 10` is preserved: low output digit zero, returned coefficient `[10]`, terminal carry one.

No parity condition intended only for palindrome targets is imposed on general targets. [Target source](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderTarget9df76b.lean)

## 5. Existing independent semantic evidence is reusable

I read the complete bodies and accompanying JSON records of these reviews:

| Retained review | Actual reviewer and valid reuse scope |
|---|---|
| `controls/incremental-semantic-review.{md,json}` | `scope105`, nonauthor of Local and Target. Reusable for those exact two source hashes. Its Scan hash is explicitly WIP and is **not** final Scan acceptance evidence. |
| `local/target-semantic-review.{md,json}` | `runtime105`, reviewing Target authored by the parent agent. Covers both definitions, four public theorems, original definitions, and numerical bridges at the final Target hash. |
| `local/scan-semantic-review.{md,json}` | `runtime105`, reviewing Scan authored by `structure105`. Covers both executable definitions and eight public theorems at the final Scan hash. It expressly excludes self-review of Local. |
| `controls/numeric-wrapper-semantic-review.{md,json}` | `scope105`, nonauthor of Numeric. Covers all three numerical-wrapper theorem declarations at the final Numeric hash. |
| `numeric/semantic-review.{md,json}` | `structure105`, nonauthor of Numeric. It discloses authorship of Scan and does not claim independent re-review of that dependency. Covers all three Numeric exports at the final hash. |

These reviews contain actual reasoning about theorem statements, finite coefficient preservation, realizability, carry direction, width branches, digit bounds, and exceptional cases. They are substantive source reviews rather than acknowledgments or approval badges. Their module-specific authorship exclusions are compatible: the retained set covers Local, Target, final Scan, and Numeric through nonauthors. [Retained review directory](https://github.com/taco-jpg/p196-algorithm/tree/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016)

The formal review `5554347350` is a **COMMENTED** review tied to frozen head `ec7aa17a36548cc629d2a4a309e802406fc862e7`. Its author explicitly identifies it as a relay through the shared connector account, not an independent GitHub-account approval. It accurately distinguishes the mathematical source checkpoint from the final evidence-bearing head. It should be used as an index and attribution record together with the underlying evidence, not as a substitute for that evidence or a platform approval. [Formal review](https://github.com/taco-jpg/p196-algorithm/pull/134#pullrequestreview-5554347350)

### Current independent review of Controls

`scope105` authored the six closed controls. Its own control compilations and final closure execution must not be relabeled as independent source authorship review of Controls.

**This assignment independently read all six complete control statements and proofs, plus their unchanged reversal/witness dependency. I authored none of them and found no defect.** This finding is separate from reuse of the older semantic reviews.

The controls correctly exercise `1 → 2`, `5 → 10`, both widths for `29/110 → 121`, both nonpalindromic profiles for `1197801`, truncated-subtraction rejection, and the necessary digit-domain boundary. Four use closed finite decision proofs; the two larger ordinary-step controls reuse the established witness equalities. The tests call `decodeAtWidth`; the fully proved wrapper theorems supply the numerical width/leading-digit connection, so this does not create a missing wrapper-test obligation. [Controls source](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/Agent105DecoderControls9df76b.lean)

## 6. Closure receipts: inspected applicability and limits

Both final receipts identify source checkpoint `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`, the same registry SHA-256, and the complete twelve-module build order.

I inspected their recorded command arrays:

- The canonical run records twelve source compilations and `ProjectAudit`, all exit zero.
- The supplemental run records official compiler help, twelve source compilations with explicit `--trust=0`, and the same audit with explicit `--trust=0`, all exit zero.
- Both receipts record official Lean 4.19.0, release commit `6caaee842e94`, source/build identities, module log hashes, 1,096 audited theorem declarations, 29 endpoints, and the allowed axiom union.
- The final report explicitly records the 22 inherited unsafe implementation declarations separately from theorem dependencies and reports none in the five new modules.
- The canonical receipt’s generic `"agent": "Agent #1"` field is not evidence that Agent #1 performed this run. Actual execution attribution comes from the named `scope105` review, supplemental receipt, and driver evidence.

The recorded allowed theorem-axiom union is `[Classical.choice, Quot.sound, propext]`. The source I read introduces no unsupported axiom, `sorry`, `admit`, `native_decide`, or theorem weakening.

These are **consistent, source-matched scoped verification receipts**. The parent delivery owner is validating their archive members, literal logs, audit source and complete dependency maps. This subtask does not claim to have repeated that archive validation. Explicit `--trust=0` alone should not be described as proving imported proof rechecking; acceptance rests on the fresh source compilation evidence and actual transitive axiom audit. [Canonical receipt](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016/canonical-verification.json), [Supplemental receipt](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016/strict-verification.json)

## 7. Exact acceptance status

| Obligation | Status |
|---|---|
| Complete source reading of the five new mathematical modules | **PASS** |
| Advertised ordinary positive predecessor iff | **PASS** |
| Exact returned coefficient-list meaning | **PASS** |
| Canonicality, positivity, actual width, width zero, odd/even centers, overflow, digit bound | **PASS** |
| Existing nonauthor semantic reviews for Local/Target/Scan/Numeric | **APPLICABLE at the recorded final source hashes** |
| Independent semantic reading of the six Controls in this assignment | **PASS** |
| Registry versus observed twelve-module Git blobs and imports | **MATCH** |
| Material mathematical findings remaining | **NONE IDENTIFIED** |
| Source repair requested | **NONE** |
| New duplicate whole-project build required by this review | **NO** |
| Literal archived closure evidence validation | **Parent-owned verification step** |
| Final integration/merge acceptance | **Outside this read-only subtask** |

This source review supplies no mathematical reason to delay the next legitimate delivery action once the parent’s evidence and integration checks pass. PR113 prerequisite handling, the current combined target tree, platform requirements, and acknowledged write ownership remain the delivery owner’s responsibilities. No infinite-time theorem about 196, repository-wide build, ordinary-integer predecessor enumeration, or completed merge is asserted here.
