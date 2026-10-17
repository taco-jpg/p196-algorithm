# PR #152: bounded source and independent-review reuse memo

## Decision

**REUSABLE — the existing genuine nonauthor semantic review directly covers the advertised theorem, all 22 named declarations, and all four concrete source controls at final head `708aa41b28150a0618aa2aa8f1cf2b5bbed33615`. No uncovered semantic obligation was found.**

This is an evidence-applicability memo, not a newly commissioned mandatory proof review. The prior review should be reused. No Lean compilation, finite Python diagnostic, source edit, GitHub mutation, issue comment, ownership claim, recursive agent, or archive execution was performed for this memo.

- Investigator: Agent #50, session `4dce66859b6c`, genuine subagent `/root/pr121_source_review`, reassigned to the bounded PR152 source/evidence-reuse task.
- Parent delivery claim supplied for this assignment: `081d45cded05e4210092efbf17f4c279b459cca2`.
- Original source owner: Agent #15/session `43cf6e114472`, unchanged.
- Mathematical freeze: `5d02e88f13f59f6fcd09cf75d8c7f188c6645727`.
- Final examined head H: `708aa41b28150a0618aa2aa8f1cf2b5bbed33615`.
- Prerequisite: PR #145, delivery owner Agent #25/session `677aa81c663a`; mathematical pin `e8d706dc8a67248e1531b0b828fbe05ff50052ed`, final publication head `679d10a5b1382b51b68a7240bb9c6562ccf144d9`.
- Contribution prefix: `proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/`.

The sibling evidence task owns complete runtime, axiom, archive, and data validation. The parent owns readiness, prerequisite integration, current combined-tree validation, and guarded delivery. This memo adds no new policy gate and certifies none of those separate actions.

## Existing review, its authorship, and exact-head binding

The complete [FINAL_SEMANTIC_REVIEW.md](https://github.com/taco-jpg/p196-algorithm/blob/708aa41b28150a0618aa2aa8f1cf2b5bbed33615/proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/evidence/semantic/FINAL_SEMANTIC_REVIEW.md) was read first. Its Git blob is `edaf9dc566db8d174e2df8ff842da609f2978389`; its independently recomputed SHA-256 is:

```text
af17ee7e650b1b2ca70fbc6d9a7c13fcceaca63dc4826b7e789a267d7cf18765
```

The review names Agent #15 `support_semantics` as a genuine nonauthor semantic subagent, explicitly states that the reviewer authored and edited no Lean source, ran no Lean, and made no Git or remote writes, and confines its execution claim to original-Python finite diagnostics and byte/hash comparisons. The separate [AUTHOR_REPORT.md](https://github.com/taco-jpg/p196-algorithm/blob/708aa41b28150a0618aa2aa8f1cf2b5bbed33615/proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/evidence/author/AUTHOR_REPORT.md) identifies its contents as author work and describes the semantic correction as received from the independent reviewer through the coordinator. The parent’s final formal COMMENT expressly relays the nonauthor review.

The [formal COMMENT review 5554951379](https://github.com/taco-jpg/p196-algorithm/pull/152#pullrequestreview-5554951379), normalized ID `PRR_kwDOVHvrqM8AAAABSxnU0w`, contains the exact frozen source pin and a final publication binding to H. It is submitted through `sodium-qed`, the same account used by the PR author. Its text explicitly disclaims a separate-account or independent-person APPROVE. Therefore the qualifying distinction is the documented nonauthor specialist role under the project process; no distinct GitHub account or platform approval is invented.

The complete preliminary [SOURCE_REVIEW_001.md](https://github.com/taco-jpg/p196-algorithm/blob/708aa41b28150a0618aa2aa8f1cf2b5bbed33615/proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/evidence/semantic/SOURCE_REVIEW_001.md), blob `05faa50f93b5ff8a7677b724eab2edb35800e11c`, provides a declaration-by-declaration coverage table for all 22 named declarations, including the four controls. The final review explicitly carries that complete mathematical review to the frozen source after a single docstring correction.

The only prior finding S1 concerned calling an unrestricted `outgoing_last` result a bit despite that theorem having no coefficient bound. The final source now says “the actual final outgoing carry.” Its unrestricted index equality is preserved. The final review records that the replacement changes no definition, proposition, or proof. The current source contains that corrected wording. No unresolved semantic finding survives in the original final report or in this applicability check.

## Source identity and final packaging

The new [ActualCarrySupport.lean](https://github.com/taco-jpg/p196-algorithm/blob/708aa41b28150a0618aa2aa8f1cf2b5bbed33615/proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/ActualCarrySupport.lean) has:

| Property | Independently checked value |
|---|---|
| Size | 10,166 bytes |
| Git blob | `c0e5562e1661570546bced3dca82dd4fb459fa5f` |
| SHA-256 | `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646` |
| Direct imports | `SourceFormula`, `RawSymmetryObstruction` |
| Named declarations | 22: two definitions and 20 theorems |
| Source option | `set_option autoImplicit false` |
| Namespace | `P196.Agent15.SpectralSupport`; the last four declarations are in `Controls` |

All eight mathematical sources were fetched independently at H and at the mathematical freeze. Each H/freeze pair has the same Git blob and byte-identical content. All eight retained source snapshots were independently SHA-256 hashed, and their Git blob identities were recomputed from the actual bytes. Every result matches the published source pins. Every actual import list matches final `BUILD.json`.

| Module | Git blob at both H and freeze | SHA-256 |
|---|---|---|
| `LychrelDigitSums` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `IncomingCarrySensitivity` | `9ccc745471fd509fb68652fef40454478087e92e` | `52850d75999a8fdad298e2e9da638965472ab6507f88630bf428698576ac631f` |
| `RawSymmetryObstruction` | `9d4250f3e5daa5ff26f097a7e12ce98830dd9e89` | `922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87` |
| `SpectralWeights` | `40afa93196976972e5c0f6772a18e50c1e635a3f` | `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1` |
| `BinaryCode` | `35ba9bee5afb9bb47f39738e44860a02ea9b2469` | `8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9` |
| `ChargeSymmetry` | `f69efd4bc0642759dddf99834d5d093c929761a5` | `28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3` |
| `SourceFormula` | `1db4a109629abddf355d12e8a14f2cfb0e26a39b` | `be165a538963922f6096e63934e5f3c1010d760cabc9e08baa96a0bb43c105d8` |
| `ActualCarrySupport` | `c0e5562e1661570546bced3dca82dd4fb459fa5f` | `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646` |

Exact repository paths, requested refs, source URLs, actual imports, hashes, and H/freeze comparisons are retained in `READING_AND_HASH_EVIDENCE.json`. The charge branch is `SourceFormula -> ChargeSymmetry -> BinaryCode -> SpectralWeights -> Std`; the arithmetic branch is `RawSymmetryObstruction -> IncomingCarrySensitivity -> LychrelDigitSums -> Std`. The unrelated `ChargeControls` module is outside this eight-module closure.

The complete [CONTRACT.md](https://github.com/taco-jpg/p196-algorithm/blob/708aa41b28150a0618aa2aa8f1cf2b5bbed33615/proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/CONTRACT.md) was read and compared between H and freeze. It is byte-identical, with Git blob `1b756b6a795f927043159e50e6c9c802ad86a66b`.

Final `BUILD.json` has Git blob `2d1fb81576f5c21f2acc4f03b9ca71b9be1a6d18` and recomputed SHA-256 `2b7e1e9527ea69d093ac5dcef32ea10c5c1933f88311f1a4be386867f7de2c3e`. The same path returns 404 at the mathematical freeze. This observation is preserved accurately: this memo does not assert that final packaging configuration existed at the earlier mathematical commit. Its eight source pins and 22 explicit exports all match the reviewed source. Checker/configuration history remains in the sibling evidence lane; absence of that later packaging file at the source freeze is not a semantic source mismatch.

## Exact original claim and arithmetic convention

The contract cites the original note and script at `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`. Both complete originals were read as source text and their Git blobs independently recomputed:

- [Original note](https://github.com/taco-jpg/p196-algorithm/blob/5ff4f607535587d572fbc9e95ba9501d1fbe5fc5/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md), blob `cb1c355fa05916a770816a4d5ef680e54079cccb`.
- [Original script](https://github.com/taco-jpg/p196-algorithm/blob/5ff4f607535587d572fbc9e95ba9501d1fbe5fc5/proofs/creative_global_spectral__8de5a77a944d0d04.py), blob `730acd722bf017b6bf1e51e5a0411169a7804da4`.

The selected note passage says that, for symmetric bounded paired coefficients, unequal mirrored outgoing carries occur only at coefficient nine. Combined with charge faithfulness, absence of nine implies zero charge. The converse from mere presence of nine is expressly absent.

The original `qstep` starts incoming carry at zero and appends one computed outgoing carry to `cs` for each original coefficient. An optional extra output digit does not extend `cs`. The new definition follows that convention exactly:

```lean
def outgoing (q : Nat → Nat) (L : Nat) : List Nat :=
  (List.range L).map (fun i => DecimalDigits.carry q (i + 1))

def actualCharge (q : Nat → Nat) (L : Nat) : Int :=
  P196.Agent15.SpectralCarry.carryCharge (outgoing q L)
```

The unchanged foundation defines `carry q 0 = 0` and `carry q (i + 1) = (q i + carry q i) / 10`. Hence the word contains boundaries 1 through L, excludes the initial incoming zero, and retains the final outgoing carry even when zero.

The charge still uses integer U/S weights with recurrence `X(n+2) = 20*X(n+1) - X(n)`, initial values `U=(0,1,...)` and `S=(1,21,...)`, and the complete word length’s original parity. The inherited `SourceFormula` theorems identify it with the original sums of reflected carry differences: U(m-i) for odd length 2m+1, and S(m-1-i) for even length 2m. Differences and weights are in `Int`; no natural subtraction truncates the charge.

## All 22 declarations and protected contract coverage

The complete new source was read. Its literal declaration sequence exactly equals `BUILD.json.new_exports`; exact literal headers are preserved in `LITERAL_22_DECLARATIONS.json`. The existing preliminary review has a separate coverage row for each declaration below.

Let:

```lean
hb : ∀ i, i < L → q i ≤ 18
hs : ∀ i, i < L → q i = q (L - 1 - i)
```

All names below have prefix `P196.Agent15.SpectralSupport.`.

| Declaration | Exact reviewed role |
|---|---|
| `outgoing` | Definition of the L computed outgoing carries, with the existing recurrence. |
| `actualCharge` | Definition using the existing parity-selected integer `carryCharge`. |
| `outgoing_length` | Exactly L entries for arbitrary q and L. |
| `outgoing_getElem` | At i<L, the entry is `carry q (i+1)`. |
| `outgoing_getElem?` | The corresponding optional-index equation at i<L. |
| `outgoing_last` | At positive L, the last entry equals `carry q L`, without requiring hb. |
| `outgoing_binary` | Under hb, every outgoing entry is 0 or 1. |
| `outgoing_reverse_iff` | Unconditional equivalence between whole-list reflection and equality of computed reflected boundaries. |
| `actualCharge_zero_iff` | Under hb alone, charge zero iff every reflected outgoing pair agrees. |
| `outgoing_reflected_eq_of_nonnine` | Under hb, hs, i<L, and q i≠9, the reflected outgoing carries agree. |
| `actualCharge_nonzero_iff_nine_asymmetry` | Under hb and hs, charge nonzero iff an in-range nine has unequal computed reflected outgoing carries. |
| `actualCharge_zero_of_no_nine` | Under hb, hs, and no in-range nine, charge is zero. |
| `canonical_actualCharge_zero_iff` | The exact zero equivalence for `Canonical n d L` and `columnSum d L`. |
| `canonical_outgoing_reflected_eq_of_nonnine` | The local nonnine equality for that canonical column sum. |
| `canonical_actualCharge_nonzero_iff_nine_asymmetry` | The exact nonzero witness equivalence for that canonical column sum. |
| `canonical_actualCharge_zero_of_no_nine` | The literal no-nine consequence for that canonical column sum. |
| `actualCharge_width_zero` | Width-zero charge is zero for arbitrary, even unbounded, q. |
| `actualCharge_width_one` | Width-one charge is zero for arbitrary, even unbounded, q. |
| `Controls.nine_zero_charge` | Constant-nine coefficients at width two give [0,0], charge zero, and an explicit occurrence of nine. |
| `Controls.even_overflow_zero_charge` | Constant-ten coefficients at width two give [1,1] and charge zero. |
| `Controls.odd_free_center` | Coefficients [8,18,8] give [0,1,0] and charge zero. |
| `Controls.odd_nine_asymmetry` | Coefficients [9,18,9] give [0,1,1] and charge one. |

The two main statements are literally:

```lean
theorem actualCharge_zero_iff (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) :
    actualCharge q L = 0 ↔
      ∀ i, i < L → carry q (i + 1) = carry q (L - i)

theorem actualCharge_nonzero_iff_nine_asymmetry (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    actualCharge q L ≠ 0 ↔
      ∃ i, i < L ∧ q i = 9 ∧ carry q (i + 1) ≠ carry q (L - i)
```

The six numbered contract obligations are therefore already covered: exact outgoing entries and binary bounds; charge-zero faithfulness under hb alone; local nonnine equality using the original arithmetic lemma; exact nonzero witness equivalence; the one-way no-nine corollary; and the actual canonical specializations. The width lemmas and four concrete controls add explicit boundary evidence already included in the prior source review.

## Conditions and boundary checks preserved by the review

**Reflected indices.** The source converts list index L-1-i to outgoing boundary (L-1-i)+1=L-i only under i<L. Out-of-range optional indices are handled separately in list extensionality. The correct reflected output is `carry q (L-i)`, not `carry q (L-1-i)`; the latter is the incoming boundary used only inside the local division proof.

**In-range bounds.** The foundation gives `carry_bounded q L hb` at boundaries at most L. The binary adapter uses i+1≤L. Local support uses the two incoming boundaries i and L-1-i. No bound on q outside the original width is introduced.

**Original local arithmetic.** The support proof invokes the unchanged `RawSymmetryObstruction.nonnine_binary_div` with coefficient q i and the two computed incoming carries. Its exact premises are coefficient≤18, coefficient≠9, and each incoming carry≤1. Symmetry identifies the two coefficients before applying it. No new recurrence or independent carry witness replaces the original operation.

**Canonical inputs.** The inherited definition is exactly:

```lean
Canonical n d L :=
  0 < L ∧ (∀ i, i < L → d i ≤ 9) ∧
  0 < d (L - 1) ∧ value d L = n
```

The four wrappers take this definition directly, set q to `columnSum d L`, and obtain bounds and symmetry from `columnSum_bounded` and `columnSum_symmetric`. The existing `reverse10_value`, `step_value`, and `decimalLength_of_canonical` relate those unchanged digit objects to actual natural-number reversal, addition, and width. Low-end zero digits are permitted. Width zero belongs to the general algebraic extension, while the canonical wrapper retains its positive-width condition.

**Parity, center, and overflow.** No fixed parity, even-center, no-overflow, outer-positivity, or orbit premise is added to the general theorem. An odd central carry reflects to itself and can be one at zero charge. The final carry remains present at zero and one under hb. The unbounded width-zero/one lemmas do not mistakenly promote arbitrary carries to bits.

**Concrete controls and finite examples.** All four concrete source controls are explicitly covered by the retained preliminary review and remain unchanged at H. Their proofs use ordinary `decide`; runtime acceptance is the sibling’s evidence scope. The prior semantic reviewer also records finite original-Python diagnostics on 7,240 arbitrary bounded words and 14,479 symmetric bounded words, plus ten canonical numerical examples. Those are attributed retained finite diagnostics. They are neither new executions by this investigator nor a replacement for universal Lean proofs or separate Lean instantiations of those numerical examples.

The coefficient-nine control is decisive for interpretation: the formal conclusion requires a nine together with an asymmetric outgoing pair. A nine by itself is insufficient.

## Evidence performed here and boundaries

The independently performed work was limited to:

1. Reading the complete original final semantic review, complete preliminary declaration review, complete contract, complete new source, and author attribution record.
2. Reading the cited original note/script, the four small charge modules, and the required arithmetic/canonical interfaces in the original foundation.
3. Fetching all eight complete mathematical sources at H and freeze, and comparing their exact bytes and Git blob identities.
4. Checking all eight actual import lists and the ordered 22 named declarations against final `BUILD.json`.
5. Preserving 16 exact input files and recomputing all 16 Git blob identities plus ten explicitly supplied SHA-256 identities. All comparisons passed. The retained input files total 342,690 bytes.
6. Recording the final review submission, H binding, source equality results, exact declaration headers, and the accurate BUILD-at-freeze 404 observation.

There was no fresh Lean run, finite diagnostic, full-origin audit, archive validation, new proof, code edit, or remote action. Full source content was fetched for identity verification; this memo does not claim a new line-by-line review of all 5,490 lines of the inherited `LychrelDigitSums` foundation.

The accepted scope supplies no charge persistence, spectral evolution theorem, T/R injectivity, H interpretation, quotient classification, carryfree saturation, new palindrome criterion, or all-time conclusion about 196. The original report states these limitations, and no new source theorem contradicts them.

## Handoff

- Existing semantic review: **QUALIFYING AND REUSABLE for the unchanged eight-module source and all 22 named declarations at H.**
- Precise uncovered semantic obligations: **NONE FOUND.**
- Additional mandatory semantic review requested: **NONE.**
- New compilation or finite tests: **NOT_RUN by this investigator.**
- Delivery owner: **Agent #50 parent.**
- Prerequisite ownership: **Agent #25/session677aa81c663a for PR145; unchanged.**
- Remote readiness, merge, and target verification: **not performed or certified by this reviewer.**

The next action is the parent’s existing delivery workflow after its separate runtime/evidence and integration checks. Review reuse should advance that workflow rather than create another duplicate review gate.
