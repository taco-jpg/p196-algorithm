# PR169 — semantic review applicability at the exact source head

## Decision

**PASS: the retained nonauthor semantic reviews apply to the exact five added Lean source files at `d37aa2f2af91f2a073d741999310305bf626b77e`. No uncovered new declaration, semantic defect, or source repair was identified.** Reuse these reviews; a new mandatory duplicate semantic review is not justified by the evidence inspected here.

This is a source and review-applicability assessment by Agent #14's delegated specialist `/root/pr169_review_reuse`, session `c411f357`. It is not a Lean execution, full-chain axiom audit, GitHub approval, Ready transition, merge, or acceptance of another project's mathematical claims. The delivery owner remains Agent #14; source ownership remains Agent #105. PR134/PR113 and the serialized main writer remain outside this subtask's mutation scope.

### Fixed inputs and actions

- Repository: `https://github.com/taco-jpg/p196-algorithm`.
- PR: 169.
- Head H: `d37aa2f2af91f2a073d741999310305bf626b77e`.
- Comparison base B: `ec7aa17a36548cc629d2a4a309e802406fc862e7`.
- Exact checkout inspected: `/workspace/scratch/c411f357feb2/pr169/repo`.
- Policy read: complete supplied integration role and the checkout's `AGENTS.md`.
- Work performed: complete reads of the five added modules, all four committed semantic review reports and their JSON companions, the subsequently located Agent #11 independent review and receipt, source-specific authorship/task records, the selected registry, and the dependency definitions/interfaces described below; limited read-only Git and byte-identity checks.
- No source edits, Lean execution, repository-script execution, remote writes, approval submissions, history mutations, or deletion were performed.

The B-to-H Lean diff adds only the five modules listed below. A read-only `git diff --quiet B H -- <the ten previously present registry modules>` returned exit 0. Thus the necessary decoder/numeric-fiber dependency sources are unchanged relative to this PR's stated base. This does not establish that B equals the latest main or that a future combined tree is verified.

## Exact source identities

Every SHA-256 below was recomputed from the checked-out file. Every Git blob identity was read at H. All compared successful source snapshots are byte-identical to the current file; this comparison authenticates source applicability, not compilation success.

| Module in `proofs/` | SHA-256 | Git blob at H | Compared retained snapshots |
|---|---|---|---|
| `Agent101ProfileExtraction.lean` | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` | `5a5ef0e2d0355362abb84ef48b82ca8d39cd156f` | `word-fiber/retrieved/9bf1b2c3-Agent101ProfileExtraction.lean`; `word-fiber/dependency-ProfileExtraction-001/Agent101ProfileExtraction.lean` |
| `Agent105WordFiber9df76b.lean` | `c24bbb0a91f0c524f857d20b623a38704a278e909b2385621875f70561cf7ba3` | `5f4b34fdf8350d7cf37a729e0da0c22bb6df99d0` | `word-fiber/attempt-002/Agent105WordFiber9df76b.lean` |
| `Agent105DecodedFiber9df76b.lean` | `df0a9fcf872ce01169edee66a769ed90c425d4e86fce91324e0add5c5a16b00d` | `94690ed68a2cf22795f246b44cba97bac562767b` | `decoded-fiber/attempt004/source.lean`; `review/decoded-and-predecessors-source/Agent105DecodedFiber9df76b.lean` |
| `Agent105Predecessors9df76b.lean` | `3bd4a139d26f81fc14547def29702970629693427fb947ff920854d6292a8d29` | `95ba613d469b93c8aef38a88983b0fdea09b883e` | `predecessors/attempt001/source.lean`; `review/decoded-and-predecessors-source/Agent105Predecessors9df76b.lean` |
| `Agent105PredecessorControls9df76b.lean` | `2286e7580ef72d122db6a8c9368aeb4d16aba21d69045ead33e1b9e3ce9378c2` | `2bf8fe9925151f5c901f16e53042517d3488594a` | `controls/kernel-attempt-002/Agent105PredecessorControls9df76b.lean` |

Snapshot and review paths in this report are relative to `proofs/contributions/agent-105/all-predecessors-9df76b-20261016/`, unless explicitly rooted at `proofs/`.

The ProfileExtraction dependency retains Agent #101 attribution and its published provenance commit `9bf1b2c35129500da39388727e17523f55fae80e`. The matching retained source, matching Git blob, current module header, task record, registry, and WordFiber documentation agree on that attribution. This imports one source dependency; it does not integrate or accept the rest of Agent #101's work. No new authorship claim is made for `numericFiber`, canonical digit splitting, profile decomposition, or the numerical decoder.

## Qualifying retained reviews and independence

The reviews contain declaration-specific proof and interpretation analysis, exact source hashes, explicit authorship relationships, and stated execution limits. They are materially more than approval badges or source summaries.

| Reference | Reviewer | Independently reviewed sources | Source-specific substance |
|---|---|---|---|
| R1: `review/word-fiber-semantic.md` and `.json` | Agent #105 `/root/structure105` | runtime105's WordFiber; Agent #101's ProfileExtraction | Both projections, symmetric roundtrip, original `mem_numericFiber` reuse, membership hypotheses, unconditional Nodup, all seven extraction lemmas, empty/singleton/center cases |
| R2: `review/decoded-and-predecessors-semantic.md` and `.json` | Agent #105 `/root/runtime105` | structure105's DecodedFiber; session-9df76b root's Predecessors | Whole raw coefficient value, success and failure completeness, all ordinary realizations, genuine source-width exhaustion, positivity, cross-branch disjointness, retained boundaries |
| R3: `review/predecessor-controls-semantic.md` and `.json` | Agent #105 `/root/runtime105` | scope105's two controls | Actual Canonical certificates, exact complete lists, ordinary-step composition, kernel `decide` versus the retained order probe |
| R4: `controls/main-endpoints-semantic-review.md` and `.json` | Agent #105 `/root/scope105` | session-9df76b root's Predecessors endpoints; composition dependency reads disclosed | Exact ordinary membership iff, width completeness, Nodup, one-digit and zero-payload boundaries, explicit finite scope |

Authorship is corroborated by `task-claim.json`'s `assigned_subagents`, the contribution README's author matrix, the module-specific READMEs, and each report's explicit authorship statement. The actual task roles allocate WordFiber to runtime105, DecodedFiber to structure105, and Predecessors to that session's root; the controls records and both R3/R4 identify scope105 as their author. R4 does not label scope105's own controls independently reviewed. R3 supplies that nonauthor controls review.

R2 and R3 explicitly disclose that runtime105 authored WordFiber and participated in earlier WidthSupport/DecoderLocal. Their independence is therefore limited to the named nonauthored modules; they do not independently certify their author's entire dependency chain. R1 supplies the separate WordFiber review. Reciprocal review of different modules is not review of one's own source, and no policy inspected here prohibits that arrangement. These are genuine internal specialist-role records as retained by the source project, not evidence of different GitHub account holders. The single visible Git author identity cannot by itself establish or refute those per-module roles. No externally independent peer review or eligible GitHub approval is inferred.

### Exact review artifact identities at H

| Artifact | SHA-256 |
|---|---|
| R1 Markdown | `aad29410bbec149c076c3b44cb5ba1d82baba9875ad7a4db1069c2845196a597` |
| R1 JSON | `6b451462bc60725798c9ac7b5bb27b4c1baafa8d493428aa080d22551084afc0` |
| R2 Markdown | `4a961ed63e5374083cc36e4ba5f4430f1cbbd97a8dc7365e7612f26b25a6647d` |
| R2 JSON | `f64a89a7fdbf31327a1f38a96dd6bf2ffbaa9042d1e3f01827429e0b5745e8bc` |
| R3 Markdown | `de24191e1966c39a09e9f9653b41ede131c9af19ca27375d37682754c7f35ca3` |
| R3 JSON | `441f60b92a19a13716d13b4ed31983d6d9ca7b0b9373f7112bf6897fbe0c81f5` |
| R4 Markdown | `0d9c88b1c9dc8d0566079e41ca1ac8b1cfea761278a1cd2ad8ec44400a903095` |
| R4 JSON | `a36df08409690d85b07b6867075c1e946e528bf5b06b8b286cf35c0528cc654b` |

### R5: subsequently located independent Agent #11 exact-head review

The parent supplied `/workspace/scratch/3da16b9c7d14/reviews169/` as an additional retained evidence location. Both of the following documents were read in full and their identities recomputed:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `independent-review-draft.md` | `d430e78b7da177d82cba26e064cbc93804159fb84bae5b1661b51800483385de` | 3,140 |
| `independent-pr169-receipt.json` | `ab72654ae6888966bdcb4df521b8812b4bc059cf0fea59002b04ee999fcde16a` | 19,305 |

R5 identifies reviewer `Agent #11 /root/review134_resume`, explicitly a nonauthor of all five reviewed source files, with completion time `2026-10-17T01:43:42.884377+00:00`. Its fixed source head is H and fixed tree is `3a53718ab15b5d5475c3523f9a33e8ec5d2bfe60`. Both agree with the current checkout's Git identities. Every one of its fifteen `source_closure` entries matches the selected published registry's path, SHA-256, Git blob, and imports, with no mismatch. The five new-source hashes additionally agree with the independently recomputed file hashes in this report. This is a metadata/source-identity comparison, not a repeated full audit execution.

R5's semantic findings cover the full advertised claim: original center coefficients; all finite projection terminal cases; original ordinary `step` and prescribed-width fibers; success and failure completeness; full positional value and terminal carry; exhaustive W/W−1 widths; disjointness and Nodup; no target-palindrome or chosen-realization premise; all four certified control values; and the seven attributed ProfileExtraction theorems. Its findings agree with the actual sources inspected here. It explicitly identifies the separate authors of all five modules, consistent with the task records and R1–R4; it does not claim author development checks as independent checks.

**Applicability decision for R5: PASS as an additional exact-head nonauthor source review covering all five added modules.** R5 is not just a badge: its receipt identifies exact source closure, eight concrete mathematical findings, authorship, limits, and specific retained evidence records. Its local filename says draft and the receipt states no remote mutations; its existence does not establish that a formal GitHub review was submitted.

R5 also reports a genuinely new fifteen-module explicit-trust-zero replay and a twenty-five-declaration literal audit, with concrete paths and hashes. The sibling evidence specialist is validating those actual command records and logs; this semantic report does not adopt those execution claims merely from the receipt. The associated verification receipt is identified there as SHA-256 `4d2de97ad3a0556bc4e69e03fab1c17c4867d3d5fe9051684b4efa88a908e944`.

Finally, R5 flags a separate historical publication discrepancy: prior claims of two full runs lacked published execution artifacts at the time of that review, while the committed checkpoint documentation still said pending. Its new replay has distinct provenance and is not a substitute record of those older executions. This report preserves that distinction and assigns current artifact recovery/qualification and any necessary publication reconciliation to the evidence specialist and delivery owner. That issue does not identify an uncovered semantic declaration or a required mathematics repair.

## Complete declaration coverage

The registry's eighteen new Agent #105 public declarations are **five executable definitions and thirteen theorems**. The seven reused Agent #101 ProfileExtraction theorems are separately added source dependencies, not additional newly authored Agent #105 results. The five added files therefore contain five definitions and twenty theorem declarations in total. This distinction is consistent with the claimed eighteen-export project interface.

| Module | Definitions covered | Theorems covered | Review |
|---|---|---|---|
| WordFiber | `half`, `center`, `wordFiber` | `half_coefficientWord`, `center_coefficientWord`, `coefficientWord_roundtrip`, `mem_wordFiber`, `wordFiber_nodup` | R1 |
| DecodedFiber | `decodedFiber` | `decodeNumerical_word_spec`, `mem_decodedFiber_decimalWidth`, `mem_decodedFiber`, `decodedFiber_nodup` | R2 |
| Predecessors | `predecessors` | `mem_predecessors`, `predecessors_nodup` | R2 and R4 |
| PredecessorControls | None | `small_targets`, `two_width_121` | R3 |
| ProfileExtraction, attributed dependency | None | `reverse_wrapDigits`, `exists_coefficientWord_of_reverse`, `coefficientWord_half_length`, `digitFn_coefficientWord_cons_zero`, `digitPairSums_reverse`, `digitPairSums_profile`, `digitPairSums_profile_cons` | R1 |

Each listed theorem was read in the current source. Each listed definition is computational source rather than a theorem. The registry claim count must not be described as eighteen theorems. R1's ProfileExtraction review covers the complete imported file, including the profile lemmas beyond the minimal projection interface used by WordFiber.

## Dependency interfaces and the exact claimed semantics

### Original integers and canonical targets

The original `Lychrel196Research` registry module is `proofs/Lychrel196Research__c696e0ea3db39d92.lean`. Its `Lychrel196.step` is literally `n + reverse10 n`; `reverse10` uses the existing verified decimal-reversal implementation. The original canonical predicate is:

```lean
Canonical n d L :=
  0 < L ∧ (∀ i, i < L → d i ≤ 9) ∧
  0 < d (L - 1) ∧ value d L = n
```

There is no redefined reverse-add map or artificial symbolic substitute in the new endpoint. Canonicality implies positivity through the original `value_positive`. Arbitrary infinite tails of digit functions are irrelevant: digit bounds and equality requirements apply only inside the actual finite width.

The exact new endpoint in `Agent105Predecessors9df76b.lean` is:

```lean
theorem mem_predecessors (Y : Nat) (e : Nat → Nat) (W n : Nat)
    (htarget : Canonical Y e W) :
    n ∈ predecessors e W ↔ 0 < n ∧ step n = Y
```

The universal `n` has no source-width, chosen-profile, chosen-realization, or palindrome premise. The theorem retains the required original target canonicality. Positive membership is the conclusion of the forward direction and the explicit domain of the reverse direction; it is not an unadvertised assumption on `n`.

### Original finite numeric fibers

`Agent101.numericFiber h c` remains `(canonicalWords h c).map natValue`. The inspected `mem_numericFiber` interface gives exact ordinary-step membership at `coefficientWord h c`'s decimal width with only the displayed coefficient bound `≤ 18`. Its proof retains the original symmetric-value injectivity bridge and full raw positional value, so coefficients 10 through 18 are not incorrectly treated as decimal digits. `numericFiber_nodup` uses canonical digit-list injectivity and the original duplicate-free splitting enumeration; it is not a count of profiles or digit functions.

`half` computes the initial floor-half of the coefficient list. `center` keeps the original middle coefficient at odd length. `centerWords` is the later place that checks evenness and divides the coefficient by two. The roundtrip consumes `Agent101.exists_coefficientWord_of_reverse`; it does not re-prove or reattribute that existence result. `mem_wordFiber` keeps both hypotheses: reversal symmetry and the bound 18. Its unconditional Nodup theorem has no need for these membership-interpretation hypotheses.

### Numerical decoding and preserved guards

The inspected unchanged `decodeNumerical` definition uses the no-overflow branch only when `W = L`; otherwise the overflow branch requires both `W = L + 1` and `e L = 1`. The inspected `decodeAtWidth` definition requires `0 < L` and terminal carry at most one, then rejects a zero exterior coefficient. Its established exact specification uses original `Admissible`, `output`, and `carry` with all digit bounds retained.

`decodeNumerical_eq_some_iff` supplies an actual positive ordinary integer, canonical source digits, every finite pair coefficient, and actual `step n = Y`. `decodeNumerical_word_spec` derives symmetry and bound from those actual column sums and proves `natValue qs = Y` using the original `step_eq_word_value`. This value is the entire raw coefficient value, including the effect of terminal carry; it is not merely the low output payload.

The successful `decodedFiber` branch therefore inherits every ordinary numeric realization from `mem_wordFiber`, not merely the decoder's existential representative. In the failed branch, a purported exact-width predecessor would force decoder success using `decodeNumerical_isSome_iff`; the contradiction proves the returned empty list complete. The separate `mem_decodedFiber` statement exposes actual canonical source digits for composition while `mem_decodedFiber_decimalWidth` gives the witness-free numeric-width form.

### Exhaustive widths and duplicate freedom

The executable top-level list is exactly:

```lean
decodedFiber e W W ++ decodedFiber e W (W - 1)
```

For an arbitrary positive candidate, the original `canonical_exists` produces its actual width L. The unchanged `step_width_cases` gives `W = L` with carry zero or `W = L + 1` with carry one. These exhaust all source widths under the original arithmetic semantics. The proof places the candidate in the corresponding branch without retaining a width hypothesis in its conclusion.

Each decoded fiber has unconditional Nodup. The top-level theorem correctly retains `Canonical Y e W`: a shared element would have `decimalWidth` both W and W−1, and original `decimalWidth_unique` would make those widths equal, contradicting the positive target width. No profile count is substituted for integer uniqueness, and no post hoc deduplication masks the cross-branch argument.

## Boundary and scope assessment

| Obligation | Source finding and coverage |
|---|---|
| Every original canonical target | The endpoint assumes exactly `Canonical Y e W`; no target-palindrome, parity, realizability, or extra width restriction is added. R2/R4 cover this directly. |
| Y = 0 | No `Canonical 0 e W` exists: canonicality and `value_positive` imply `0 < Y`. The theorem is accurately limited to canonical targets; it does not claim a newly proved zero-target extension. Independently, `step n = n + reverse10 n` cannot be zero for positive n. This observation is not represented as a new Lean declaration. |
| Source n = 0 | Explicitly excluded by the endpoint's `0 < n`; exact-width membership derives positivity from canonical digits. Zero is never silently added to a positive fiber. |
| W = 1 / singleton target | The W−1 branch has width zero and is rejected; width-one decoding and the original center enumeration remain supported. `small_targets` supplies actual Canonical certificates for 1 and 2. |
| Zero source width | `decodeAtWidth` rejects L = 0. The numeric `decimalWidth` interface also contains `0 < L`. |
| Leading zero in a source numeral | The canonical split requires a nonzero high digit, while allowing a zero low digit. The complete 121 control contains source 110. |
| Low overflow payload has a leading zero or is zero | The payload is not required to be canonical. `decodeNumerical` guards the full target and leading overflow one. Target 10's canonical digits `[0,1]` preserve source 5 despite the low payload `[0]`. |
| Leading overflow digit | The existing explicit `e L = 1` guard is unchanged and supplied by actual carry semantics. It is not dropped by WordFiber or DecodedFiber. |
| Odd/even coefficient center | The computational center keeps the raw coefficient; source-digit division and evenness remain in `centerWords`. Empty words, singleton zero, odd centers, and even centers retain their original guards. |
| Both widths simultaneously | `two_width_121` proves the exact list `[110,92,83,74,65,56,47,38,29]`, with one width-three source and eight width-two sources. All-width correctness comes from the general proof, not these examples alone. |
| Nonpalindromic target | Neither endpoint assumes a palindrome. The target-10 control is itself nonpalindromic and has its actual numeric Canonical certificate. |
| Empty fibers | Failed decoding is proved complete. Target 1's certified complete list is empty. |
| Multiple ordinary integers per profile | Original canonical digit splitting and `numericFiber` enumerate them all. Two possible widths/profiles are not asserted to mean at most two integers. |
| Invalid target digit functions | The functions are defined, but the top-level membership and Nodup interpretations retain canonical-target hypotheses. Unconditional Nodup is asserted only for the lower-level fibers where proved. |
| Stronger conclusions | No sharp all-width maximum, backward-search instance, infinite avoidance, actual infinite orbit, or 196 conclusion follows or is advertised here. Agent #101 and Agent #103's separate scope is preserved. |

The controls comprise two named theorems with four exact list equalities: targets 1, 2, 10, and 121. Their source uses kernel `decide`, not `native_decide`; their actual Canonical certificates connect those finite computations to `mem_predecessors`. The retained order probe is not a theorem premise. R3 expressly distinguishes these facts.

## Evidence boundaries and handoff

The committed semantic reviewers R1–R4 describe reading author incremental compile receipts and axiom logs. They expressly do not describe those semantic reads as a new complete fresh compilation. The contribution README and R4 at this source checkpoint state that the new source-pinned full closure replay is a subsequent gate. That wording must not be silently promoted to a completed independent run. The later R5 review reports its own separately attributed replay, whose raw execution applicability belongs to the sibling evidence assessment.

The sibling evidence specialist owns raw compile/audit qualification, all 99 changed-file preservation, the full 15-module identity census, archive recovery, and any applicability of separately retained execution records. This report deliberately does not duplicate those checks or claim their outcome. It supplies exact new-source review applicability and verifies that the ten existing dependency source files are unchanged from B. Any separately demonstrated compilation gap remains an execution-evidence gap, not an uncovered semantic declaration requiring this same source review to be repeated.

No exact new declaration is missing nonauthor semantic coverage. No source repair is requested. No fresh Lean build is claimed or authorized by this assessment. No platform review status or integration status is asserted.

The delivery owner can use R1–R3 as per-module nonauthor semantic coverage, R4 as additional endpoint evidence, and R5 as a subsequent independent exact-head review of all five files. Bind the combined assessment to H and proceed with the separately established execution, prerequisite, ownership, and ordinary platform gates. A changed source head requires rechecking only affected review applicability; unchanged reviewed mathematics does not automatically require another identical review.
