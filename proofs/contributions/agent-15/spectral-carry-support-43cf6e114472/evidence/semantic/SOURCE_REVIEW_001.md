# Independent semantic review: authored source checkpoint 001

Reviewer: Agent 15 / `support_semantics`, genuine nonauthor semantic reviewer.
Task: `agent15-spectral-carry-support-43cf6e114472`.
Source status: unfrozen local source; final remote commit not yet supplied.
Source Git blob: `bd35276caf15dcbf38ddba834b39e7ebab304798`.
Source SHA-256: `3add8a90d4068eccce8f18912651a6c3b942ade9edf82e66d6b9ebdb563f4b46`.
Source bytes: 10,158.

## Verdict

**PASS — preliminary source-level mathematical semantics.** All six contract obligations are covered by the actual new declarations, with the exact original outgoing-carry convention, hypothesis strengths, quantifier scope, and existing canonical decimal representation. No blocking mathematical finding was found. This verdict concerns the preserved source bytes above; it does not certify a remote head, independent Lean execution, all-origin axiom audit, or integration.

One minor documentation finding is recorded below. It does not affect a formal statement or its proof, and should be corrected by the source author before freeze.

The reviewer read the whole 233-line source and its selected inherited interfaces. The reviewer did not edit a Lean source or run Lean. Author execution records are described with attribution only. Final acceptance still needs root's frozen source commit and the separate independent execution gate.

## Complete declaration coverage

All declarations are in `P196.Agent15.SpectralSupport`, except the last four, which are in its `Controls` namespace. The source defines two objects and proves 20 named theorems; no hidden section variables or implicit global hypotheses are present, and `autoImplicit` is false.

| Source lines | Declaration | Exact role and semantic assessment |
| --- | --- | --- |
| 20–21 | `outgoing` | Exactly range L mapped to the existing `DecimalDigits.carry q (i+1)`. PASS. |
| 24–25 | `actualCharge` | Exactly the already defined `P196.Agent15.SpectralCarry.carryCharge` of that list, with result in Int. PASS. |
| 27–29 | `outgoing_length` | Proves exactly L entries for arbitrary q and L. PASS. |
| 32–35 | `outgoing_getElem` | Proves the exact computed outgoing carry at every in-range list index. PASS. |
| 37–43 | `outgoing_getElem?` | Provides the equivalent optional-index equation, including a proved length bound. PASS. |
| 46–50 | `outgoing_last` | For positive L, last entry equals `carry q L`; no final-zero removal. Formal statement PASS; docstring precision finding below. |
| 53–60 | `outgoing_binary` | Requires only coefficient bounds inside width. Uses `carry_bounded` at i+1<=L. PASS. |
| 63–95 | `outgoing_reverse_iff` | Unconditionally equates whole-list symmetry with the exact reflected boundary indices, handling out-of-range optional indices separately. PASS. |
| 98–104 | `actualCharge_zero_iff` | Under hb alone, J=0 iff every reflected outgoing pair agrees. Reuses charge faithfulness and the preceding list bridge. PASS. |
| 108–121 | `outgoing_reflected_eq_of_nonnine` | Under hb, hs, i<L, and q i!=9, concludes the exact reflected equality by the unchanged local division lemma. PASS. |
| 126–149 | `actualCharge_nonzero_iff_nine_asymmetry` | Under hb and hs, J!=0 iff an in-range coefficient is nine and its outgoing pair differs. PASS; does not infer nonzero merely from a nine. |
| 152–158 | `actualCharge_zero_of_no_nine` | The literal original one-way corollary under hb, hs, and pointwise no-nine. PASS. |
| 161–167 | `canonical_actualCharge_zero_iff` | Zero-set specialization for the actual canonical column sums and existing computed carries. PASS. |
| 171–177 | `canonical_outgoing_reflected_eq_of_nonnine` | Local support specialization using actual canonical digits. PASS. |
| 180–187 | `canonical_actualCharge_nonzero_iff_nine_asymmetry` | Main exact nonzero-support equivalence for existing `Canonical n d L`. PASS. |
| 191–196 | `canonical_actualCharge_zero_of_no_nine` | Literal no-nine consequence for actual canonical digit input. PASS. |
| 199–200 | `actualCharge_width_zero` | Explicit zero-width algebraic extension, valid for arbitrary q without bounds. PASS. |
| 203–204 | `actualCharge_width_one` | Explicit singleton zero charge, valid for arbitrary q without bounds. PASS; the sole carry is central. |
| 209–212 | `Controls.nine_zero_charge` | q identically nine at width two yields [0,0], J=0, and an actual occurrence of nine. PASS as a concrete general-word counterexample to the forbidden converse. |
| 215–217 | `Controls.even_overflow_zero_charge` | q identically ten at width two yields [1,1] and J=0. PASS; final overflow one is present. |
| 220–223 | `Controls.odd_free_center` | q=[8,18,8] yields [0,1,0] and J=0. PASS; odd central one is permitted while final carry is zero. |
| 226–229 | `Controls.odd_nine_asymmetry` | q=[9,18,9] yields [0,1,1] and J=1. PASS as a concrete supported nonzero charge. |

## Detailed adversarial checks

### The arithmetic object is unchanged

The two new definitions are only a finite-list adapter and a consumer. `outgoing` fully qualifies the existing `DecimalDigits.carry`; it does not introduce or assume a recurrence. `actualCharge` fully qualifies the existing charge namespace; it does not define J through the theorem's intended right-hand side. The module imports `SourceFormula` and `RawSymmetryObstruction`, supplying the exact selected eight-module mathematical closure. No T/R coordinate, H, quotient, reset-cut model, new positional arithmetic, or orbit transition is introduced.

The inherited charge uses Int throughout its weights and subtraction. The complete length L controls parity; the list is not padded, normalized, trimmed, reflected in advance, or extended with the initial incoming zero. The final carry at boundary L occurs at list position L-1 even when it is zero.

### Every reflection conversion has a proved in-range premise

In `outgoing_reverse_iff`, list position L-1-i is converted to boundary index `(L-1-i)+1=L-i` only after i<L. Both directions use the same identity. The reverse implication separately proves both out-of-range lists return none. This prevents a hidden Nat-subtraction assumption at L=0 or outside the word.

The local support proof rewrites `L-i=(L-1-i)+1`, unfolds the existing recurrence at both boundaries, and uses hs at the original in-range index. Its calls to `carry_bounded` use the incoming boundaries i and L-1-i. Their bounds are at most L, and all required coefficient bounds remain strictly below L. The outgoing binary adapter uses i+1<=L, which includes the final carry exactly.

### Hypotheses do not contain the conclusion

The zero-set theorem has only hb. It has no coefficient-symmetry, no-nine, final-carry, center or orbit assumption. The support theorem adds only hs and local nonnine. The exact nonzero equivalence adds no further condition and explicitly requires both a nine and an unequal outgoing pair in its existential conclusion. The converse direction uses the failed pair alone to contradict the zero theorem; it does not pretend the presence of a nine is sufficient.

The forward direction's `Classical.byContradiction` extracts a failed pointwise reflected equality and then proves that coefficient is nine using local support. This is ordinary classical reasoning over the universal theorem, not bounded enumeration or an external oracle.

### Actual numeral cases are realized by the inherited Canonical object

Every canonical wrapper takes `DecimalDigits.Canonical n d L` explicitly and uses q=`DecimalDigits.columnSum d L` in its statement. The proof extracts the existing in-range digit bounds from `hc.2.1`, invokes `columnSum_bounded`, and, where needed, `columnSum_symmetric`. The wrapper does not assume an independently chosen carry word or an arithmetic correspondence as a premise. Its result directly references the inherited carry computation on the actual digit pair sums.

The earlier contract review records the source definition of Canonical and the unchanged `reverse10_value`, `step_value`, and actual-width lemmas in the same foundation. Positivity of width, nonzero leading input digit, and `value d L=n` are therefore inherited precisely, including ordinary inputs whose low-end digit is zero. The general theorem remains valid on additional algebraic words that need not themselves be canonical integer pair sums. This extra generality does not omit the canonical cases.

### Boundaries, parity and overflow remain unrestricted

The general source has no `0<L`, positivity of q 0, even-center, no-overflow, fixed-parity, future-time, or persistence premise. L=0/1 are handled both by the general universal statements and explicit boundary corollaries. An odd center reflects to itself and is not forced to zero. Both final carry values are admitted by hb and are retained in the word. The finite diagnostics in the prior checkpoint exhibit nonzero J with either overflow value and either parity, including actual positive decimal inputs.

The concrete source controls are ordinary `by decide` proofs. They are supplementary examples; the universal theorems are proved by arithmetic/list reasoning and existing results. Source inspection found no `sorry`, `admit`, new `axiom`, `native_decide`, or `Lean.ofReduceBool` in this new module. This textual observation is not a substitute for the assigned transitive axiom and module-origin audit.

## Minor finding S1: unrestricted final carry is called a bit

Location: line 45, the docstring of `outgoing_last`.
Current text: `For every positive width, the last word entry is the actual overflow bit.`

The theorem correctly quantifies over arbitrary `q : Nat -> Nat` without hb. In that domain `carry q L` need not be a bit; for example, a one-column coefficient 20 has outgoing carry two. The formal theorem only asserts exact index equality, which is true. Calling the value a bit silently uses the extra bounded-coefficient property absent from this theorem.

Recommended correction by the source author: say `the actual final outgoing carry` in this docstring. No formal hypothesis should be added, because the stronger existing equality is correct and useful. This is a minor wording finding, not a proof or contract-strength blocker. Root was sent the attributed finding for issue 61 relay.

## Preserved development history

`source-snapshot-001/` preserves the current source and both observed author attempt directories, including exact command, result, stdout and stderr files. Hashes for every copied file are in its manifest. The current source is byte-identical to author attempt 0002.

| Author attempt | Source blob | Recorded author outcome | Semantic effect of the later delta |
| --- | --- | --- | --- |
| 0001 | `0053c91903e8465cb5bf70039ea56236478396a2` | Author log exit 1: optional-index rewrite shape, unavailable `by_contra` tactic, and two failed `rfl` boundary proofs. | None of the advertised propositions changed. |
| 0002 | `bd35276caf15dcbf38ddba834b39e7ebab304798` | Author log exit 0, empty stdout and stderr. | Adds an explicit target-shape `change`, uses `Classical.byContradiction`, and unfolds/simplifies the width-zero/one definitions. |

The complete unified delta is retained as `delta-001.diff`; `delta-002.diff` is empty because attempt 0002 equals the copied current source. These are recorded author runs, not this reviewer's independent executions. No failed source or log was deleted or overwritten by this reviewer.

## Remaining exact-head gate

Root must provide the frozen published commit and exact source/dependency identities. The reviewer will compare those bytes against this reviewed version, inspect every delta, resolve S1 if corrected, and issue an exact-head semantic report suitable for an attributed formal COMMENT. The separate execution reviewer remains responsible for fresh complete closure compilation, public signatures, safe module-origin declaration audit, generated implementation reporting and the allowed foundational axiom policy.

No conclusion here establishes T/R injectivity, H, Agent14 saturation, the four evolution laws, quotient classification, charge persistence, a new palindrome criterion or the 196 conjecture. No source-present, author-checked, independently-reviewed or integrated state is conflated.
