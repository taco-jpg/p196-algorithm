# Final independent semantic review: actual spectral carry support

**Verdict: PASS — exact frozen source semantics.**

Reviewer: Agent 15 / `support_semantics`, a genuine nonauthor review subagent.
Task: `agent15-spectral-carry-support-43cf6e114472`.
Protected claim: `3de89d0bd03534c92f65886a29b7996525571ff5`.
Protected task record blob: `2707332dbc4dc1274bb8470b15e17f6350618bba`.
Reviewed remote commit: [`5d02e88f13f59f6fcd09cf75d8c7f188c6645727`](https://github.com/taco-jpg/p196-algorithm/commit/5d02e88f13f59f6fcd09cf75d8c7f188c6645727).
Verified commit tree: `f0594cce1d8b4888561edb4ed22770ab4a6a991a`.
Verified branch at time of remote read: `formalize/agent-15/spectral-carry-support-43cf6e114472`.

## Decision and independence

The frozen `ActualCarrySupport.lean` faithfully formalizes the selected original neutral-nine support claim and its exact connection to the already defined integer charge. All six obligations of the protected contract have matching declarations. There are no unresolved semantic findings. The sole preliminary finding, a docstring that called an unrestricted final carry a bit, is corrected in the frozen source without changing any definition, proposition or proof.

This reviewer read the original source, reviewed the contract before implementation, read the full authored source, retained the observed failed and corrected versions, and independently obtained the final source and all seven dependencies from GitHub at the exact commit. The reviewer did not author or edit a Lean source, did not run Lean, and made no Git or remote writes. The reviewer ran only the explicitly finite original-Python diagnostics and byte/hash comparisons documented below.

The semantic gate passes. This report does not determine the separate fresh-build, public-signature, all-origin declaration, axiom or integration gates. Those require their own accurately attributed records. This report supports an attributed **COMMENT** review on the actual pull request; it is not a fictional separate-account APPROVE or a claim that the reviewer performed another agent's execution.

## Exact source identity and remote evidence

The final source is [`proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/ActualCarrySupport.lean`](https://github.com/taco-jpg/p196-algorithm/blob/5d02e88f13f59f6fcd09cf75d8c7f188c6645727/proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/ActualCarrySupport.lean).

| Property | Verified value |
| --- | --- |
| Git blob | `c0e5562e1661570546bced3dca82dd4fb459fa5f` |
| SHA-256 | `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646` |
| Size | 10,166 bytes |
| Named source declarations | 22: two definitions and 20 theorems |
| Namespace | `P196.Agent15.SpectralSupport`, with four supplementary theorems in `Controls` |
| Direct imports | `SourceFormula`, `RawSymmetryObstruction` |
| Contract blob | `1b756b6a795f927043159e50e6c9c802ad86a66b`, unchanged |
| Claim blob | `2707332dbc4dc1274bb8470b15e17f6350618bba`, unchanged |

Read-only GitHub API responses independently establish the named branch-to-commit and commit-to-tree identities. Full source and dependency contents were fetched with `ref=5d02e88f13f59f6fcd09cf75d8c7f188c6645727`. Their UTF-8 bytes were preserved and independently hashed. `remote-freeze-5d02/remote-read-responses.json` retains the complete requests and connector responses; `remote-freeze-5d02/manifest.json` records per-file hashes, paths and comparisons. The verification script, complete stdout, empty stderr and exit-0 result are retained in the same directory.

All seven mathematical dependencies are byte-identical to the previously reviewed pinned snapshots:

| Dependency | Verified Git blob | Provenance |
| --- | --- | --- |
| `SpectralWeights.lean` | `40afa93196976972e5c0f6772a18e50c1e635a3f` | Existing PR145 source pin `e8d706dc8a67248e1531b0b828fbe05ff50052ed`. |
| `BinaryCode.lean` | `35ba9bee5afb9bb47f39738e44860a02ea9b2469` | Same PR145 pin. |
| `ChargeSymmetry.lean` | `f69efd4bc0642759dddf99834d5d093c929761a5` | Same PR145 pin. |
| `SourceFormula.lean` | `1db4a109629abddf355d12e8a14f2cfb0e26a39b` | Same PR145 pin. |
| `LychrelDigitSums__0810ace083af80c5.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | Original source pin `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`. |
| `IncomingCarrySensitivity__5d4952e23e746f6d.lean` | `9ccc745471fd509fb68652fef40454478087e92e` | Same original pin. |
| `RawSymmetryObstruction__5c1be305a04af2b7.lean` | `9d4250f3e5daa5ff26f097a7e12ce98830dd9e89` | Same original pin. |

The selected import closure therefore has eight mathematical modules, including the new module. This identity comparison is not an independent build or acceptance of every declaration in the old foundation.

## Original mathematical claim

At original snapshot `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`, the note `creative_global_spectral_notes.md`, blob `cb1c355fa05916a770816a4d5ef680e54079cccb`, lines 58–66 says that mirrored outgoing-carry differences can occur only where the symmetric coefficient is nine. It also says that J vanishes exactly when the carry word is symmetric, and consequently that absence of nine implies J=0. It expressly permits zero charge in the presence of nine.

The companion `creative_global_spectral.py`, blob `730acd722bf017b6bf1e51e5a0411169a7804da4`, lines 8–13 appends one computed outgoing carry for each original coefficient. Its optional extra output digit does not change this carry word. Lines 28–38 define J by the original integer U/S sums; lines 51–53 check the support property and one-way no-nine consequence. Complete preserved copies were read and their Git blobs independently recomputed.

The new equivalence for nonzero J is exactly the composition of those two original claims. It requires an asymmetric pair at a nine, not merely the presence of a nine. Original mathematical provenance remains with those sources; the new work supplies the arithmetic-to-list bridge and compositions.

## Exact definitions and contract coverage

The two definitions are literal adapters over existing objects:

```lean
def outgoing (q : Nat → Nat) (L : Nat) : List Nat :=
  (List.range L).map (fun i => DecimalDigits.carry q (i + 1))

def actualCharge (q : Nat → Nat) (L : Nat) : Int :=
  P196.Agent15.SpectralCarry.carryCharge (outgoing q L)
```

No carry recurrence, weighted charge, digit representation or target property is redefined. The charge remains an unbounded integer expression selected by the original full-word length parity.

| Protected obligation | Exact covering declarations | Assessment |
| --- | --- | --- |
| Exact outgoing length, entries and binary values under in-range coefficient bounds | `outgoing_length`, `outgoing_getElem`, `outgoing_getElem?`, `outgoing_last`, `outgoing_binary` | PASS. The last boundary L is present, including when its carry is zero. |
| Zero charge iff all reflected computed outgoing carries agree, under hb alone | `outgoing_reverse_iff`, `actualCharge_zero_iff` | PASS. No coefficient-symmetry premise is added. |
| Local nonnine support under hb and hs, using the existing arithmetic lemma | `outgoing_reflected_eq_of_nonnine` | PASS. Calls `RawSymmetryObstruction.nonnine_binary_div` on the two incoming carries. |
| Exact nonzero witness equivalence | `actualCharge_nonzero_iff_nine_asymmetry` | PASS. Both the nine coefficient and unequal reflected outputs occur in the existential conclusion. |
| Literal no-nine implication | `actualCharge_zero_of_no_nine` | PASS. The forbidden converse is absent. |
| Actual canonical digit specialization | `canonical_actualCharge_zero_iff`, `canonical_outgoing_reflected_eq_of_nonnine`, `canonical_actualCharge_nonzero_iff_nine_asymmetry`, `canonical_actualCharge_zero_of_no_nine` | PASS. Statements directly use existing Canonical, columnSum and carry. |

The two main statements preserve the intended quantifiers:

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

The source has no hidden section variables, and `autoImplicit` is false. The preliminary `SOURCE_REVIEW_001.md` contains a complete line-by-line declaration coverage table. Because the final source differs by exactly one docstring replacement, that entire mathematical source review applies to the frozen definitions, statements and proof text.

## Index, width, overflow and canonical checks

`DecimalDigits.carry q k` is indexed by the incoming boundary k. Thus the outgoing carry at column i is at boundary i+1, and the mirrored outgoing carry is at boundary `(L-1-i)+1=L-i`. The source establishes this identity only under i<L. Its list-extensionality proof separately handles out-of-range optional indices. Nat subtraction is not silently used as integer subtraction outside its justified range.

The outgoing binary proof invokes `carry_bounded q L hb` at i+1<=L. The local support proof invokes it at incoming boundaries i and L-1-i, unfolds the existing recurrence at both outgoing boundaries, and uses hs to identify their coefficient values. All required coefficient bounds are strictly inside the original width. No assumptions on q beyond that width are needed.

The complete word consists of boundaries 1 through L. It excludes the initial incoming zero and includes the final outgoing carry even when zero. Neither trimming nor padding occurs. Both parity branches of the existing U/S charge remain intact. The odd central carry reflects to itself, so it may be one even when J=0. General statements impose neither positive width nor an even central coefficient, outer positivity, a fixed overflow value, or an orbit premise. Explicit `actualCharge_width_zero` and `actualCharge_width_one` corollaries additionally cover the algebraic boundary cases, even for unbounded q.

The unchanged `DecimalDigits.Canonical n d L` is the actual positive canonical representation: L>0, all represented digits are at most nine, the top digit is positive, and `value d L=n`. Its digits are least-significant first. The wrappers take that object directly, use its digit bounds through `columnSum_bounded`, and use `columnSum_symmetric`; they never introduce an independently assumed carry word. The same foundation already proves `reverse10_value`, `step_value`, and `decimalLength_of_canonical`, tying positional reflection and the final carry to actual natural-number reversal, reverse-add and width. Input low-end zeros remain allowed. The general coefficient theorem covers additional algebraic words, while the wrappers retain all actual canonical integer cases; there is no realizability omission.

The proof contains neither a circular premise nor the desired conclusion disguised as a hypothesis. Its forward existential reasoning is ordinary classical logic applied to the universal zero theorem and local support. Supplementary concrete controls use ordinary `decide`; they do not replace the universal proof. No forbidden proof placeholder, new axiom or compiler oracle occurs in the new source text. The separate execution reviewer must establish the full transitive axiom and module-origin policy.

## Finding resolution and preserved versions

Preliminary finding S1 concerned the docstring of `outgoing_last`, whose formal statement has no coefficient bound. It called an unrestricted final carry an overflow bit. The author changed that wording to `the actual final outgoing carry`. A final carry for arbitrary q can exceed one, while the equality itself remains correct without hb. The frozen docstring is now accurate and no formal premise was weakened or strengthened.

The exact final byte comparison proves:

```text
frozen source = preliminary source with that one docstring replacement
```

`remote-freeze-5d02/delta-from-source-snapshot-001.diff` preserves the complete one-line delta. The mathematical definitions, theorem propositions and proof text are otherwise byte-identical.

Observed author attempt 0001, blob `0053c91903e8465cb5bf70039ea56236478396a2`, had recorded elaboration/tactic failures. Observed attempt 0002, blob `bd35276caf15dcbf38ddba834b39e7ebab304798`, corrected target-shape handling, replaced unavailable `by_contra` uses with explicit `Classical.byContradiction`, and simplified the two boundary proofs. The propositions did not change. Both exact sources and the observed command/result/stdout/stderr records remain in `source-snapshot-001/`, with a complete unified delta. Those outcomes are attributed author logs, not reviewer-run Lean evidence. The final remote version is separately retained. Nothing was deleted or overwritten to conceal a failed version.

## Finite diagnostics and their limits

The reviewer executed the unchanged original Python `qstep` and `carry_coordinates` functions through a script with a checked original-source SHA-256. This introduces no new carry recurrence.

- All 7,240 bounded coefficient words of lengths 0 through 3 were checked for full outgoing length, binary values, retained final carry and the zero-set equivalence without coefficient symmetry.
- All 14,479 symmetric bounded coefficient words of lengths 0 through 6 were checked for nonnine support, the exact nonzero witness equivalence and the one-way no-nine implication. Both parities and both final carry values occur. Outer zero coefficients and unrestricted odd central coefficients are included in this algebraic diagnostic domain.
- Ten positive ordinary decimal examples include n=18, whose q=[9,9] gives outgoing [0,0] and J=0; n=5, whose sole outgoing carry is one but J=0; and nonzero examples with each parity and each overflow value.

The finite diagnostic command exited 0 with empty stderr. Exact script, command, complete output, result and hashes are in `finite-diagnostics-001/`. An initial timestamp key was mislabeled as a start time although recorded after execution; `run-timing-correction.json` corrects that label while preserving the original record. No numerical failure was found.

These finite checks are implementation evidence only. They are not universal Lean proofs, Lean proofs of the concrete Canonical examples, fresh dependency builds or axiom audits. The final source verdict rests on the statement-to-source review and exact byte identities; theorem acceptance must additionally use the separately required Lean verification evidence.

## Scope and publication recommendation

The review covers the selected neutral-nine support bridge at the exact frozen commit. It does not establish T/R injectivity, H, Agent14 carryfree saturation, the four spectral evolution laws, the real quadratic interpretation, quotient classification, charge persistence, a new palindrome criterion, or any all-time claim about 196. It does not claim that J=0 iff no coefficient equals nine. Post-freeze source or checker additions require their own evidence and do not inherit this verdict automatically.

Root may attach `FORMAL_COMMENT.md` as a clearly attributed formal COMMENT anchored to this commit, together with the separate independent execution record. This reviewer did not submit that review. `REVIEW_MANIFEST.json` records the complete retained evidence inventory and hashes. The semantic handoff is complete; final integration remains with the designated integration owner.
