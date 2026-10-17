# Independent semantic review: contract checkpoint 001

Reviewer: Agent 15 / `support_semantics`, genuine nonauthor semantic reviewer.
Task: `agent15-spectral-carry-support-43cf6e114472`.
Protected claim: `3de89d0bd03534c92f65886a29b7996525571ff5`.
Task record blob: `2707332dbc4dc1274bb8470b15e17f6350618bba`.
Original source snapshot: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.
Existing charge source pin: `e8d706dc8a67248e1531b0b828fbe05ff50052ed`.

## Verdict and limits

**PASS — source-to-contract semantics.** No blocking mismatch was found between the selected original assertion and `CONTRACT.md`, blob `1b756b6a795f927043159e50e6c9c802ad86a66b`. This is a contract review before the new authored module was available. It is not an exact-head source verdict, Lean execution report, axiom acceptance, GitHub approval, or integration claim. The final semantic review remains reserved for the root's frozen published commit.

The reviewer did not author or modify a Lean module, did not run Lean, and made no remote or Git writes. All reviewer output is confined to this review directory. Root is responsible for attributed issue 61 relay and any eventual formal COMMENT review. No separate-person APPROVE is implied.

## Pinned source correspondence

The complete selected original note and script were read. Their local bytes independently hash to the requested Git blobs:

| Original source | Git blob | Exact relevant lines |
| --- | --- | --- |
| `creative_global_spectral_notes.md` | `cb1c355fa05916a770816a4d5ef680e54079cccb` | 6–12 define outgoing carries and retained final carry; 58–66 state nonnine support, faithful zero set, and the one-way no-nine implication. |
| `creative_global_spectral.py` | `730acd722bf017b6bf1e51e5a0411169a7804da4` | 8–13 append one outgoing carry for every original column; 28–38 define the original odd/even integer J; 51–53 check support and the no-nine implication. |

The original script's `cs.append(carry)` occurs once per input coefficient. Conditional overflow appending affects the output digit word, not `cs`. Thus the carry word has exactly L entries regardless of final overflow, and its final entry is retained even when it is zero. The specified adapter has exactly the same convention.

The new nonzero equivalence is a faithful composition of the two selected source statements, rather than an unsupported converse: J is nonzero exactly when some mirrored pair of outgoing carries differs, and such a pair can differ only at a coefficient equal to nine. The source does not assert that every nine causes a nonzero J.

## Contract obligation review

| Obligation | Assessment | Semantic reason |
| --- | --- | --- |
| `outgoing q L = (List.range L).map (fun i => DecimalDigits.carry q (i+1))` | PASS | `carry` is the existing incoming-boundary-indexed decimal recurrence. Shifting by one obtains the carry leaving column i. There is no new carry model. |
| Exact length and in-range entries | PASS | L entries include boundaries 1 through L, exclude the incoming boundary 0, and never trim a zero. |
| Binary under `hb : forall i<L, q i<=18` | PASS | Existing `carry_bounded q L hb` supplies every boundary index at most L, including the final boundary L. Bounds on q outside the represented width are unnecessary. |
| Zero iff reflected outgoing equality under hb alone | PASS | `carryCharge_zero_iff` requires only Binary. List symmetry at position i corresponds to equality of `carry q (i+1)` and `carry q (L-i)`. No coefficient symmetry is needed for this adapter. |
| Nonnine reflected equality under hb and hs | PASS | For j=L-1-i and i<L, j<L and j+1=L-i. Both incoming carries `carry q i` and `carry q j` are binary. Symmetry identifies q j with q i; `nonnine_binary_div` supplies exactly the required equality of decimal quotients. |
| Nonzero iff a nine with unequal mirrored outputs | PASS | The forward implication extracts a failed mirrored equality and uses nonnine support to force q i=9. The reverse implication contradicts the zero-set theorem. No global no-nine hypothesis is used here. |
| Literal absence of nine implies zero | PASS | Pointwise nonnine equality makes the entire outgoing word symmetric, so the original J vanishes. The converse is expressly excluded. |
| Actual canonical numeral specialization | PASS | `Canonical n d L` provides bounded actual decimal digits. `columnSum_bounded` supplies hb and `columnSum_symmetric` supplies hs. The carry function is then computed from those actual column sums. No independently assumed carry word replaces it. |

## Index and arithmetic details to verify in authored source

For an in-range index i, define j=L-1-i. The key identities are:

- i+1<=L, so the outgoing carry at i is bounded.
- j<L and j<=L, so the reflected coefficient and reflected incoming carry are in range.
- j+1=L-i, so the reflected outgoing carry in the finite list is the one stated in the contract.
- L-1-j=i, so reflection is involutive where it is used.

These equalities require the in-range premise; Nat subtraction must not be silently treated as integer subtraction outside that premise. At L=0 the in-range property is vacuous, so no unsafe reflected-index evaluation is needed. The general theorem also covers L=1, where the sole outgoing carry reflects to itself and the charge is zero.

The existing lemma is exactly:

```lean
RawSymmetryObstruction.nonnine_binary_div
  (a b c : Nat) (ha : a <= 18) (hne : a != 9)
  (hb : b <= 1) (hc : c <= 1) :
  (a+b)/10 = (a+c)/10
```

The source proof must instantiate b and c with the two incoming carries, not the outgoing carries. `carry_bounded` is already formulated for indices at most L, so both required incoming bounds and the final outgoing bound are available without extending coefficient bounds past L-1.

## Canonical decimal semantics and realizability

The existing `DecimalDigits.Canonical n d L` definition, foundation lines 907–908, is:

```lean
0 < L /\ (forall i, i < L -> d i <= 9) /\
  0 < d (L-1) /\ value d L = n
```

Digits are least-significant first. `value` sums the first L positional digits. The nonzero top digit makes L the actual canonical width. The same unchanged foundation contains `DecimalDigits.reverse10_value` at lines 739–744, proving that fixed-width reflection agrees with actual natural-number reversal, and `DecimalDigits.step_value` at lines 749–755, proving that the same column sums and carry recurrence compute actual reverse-and-add, with the terminal carry multiplied by `10^L`. It also contains `DecimalQuantitativeMass.decimalLength_of_canonical` at lines 5338–5342, explicitly identifying L with actual decimal length.

A low-end zero digit is allowed; actual reversal may then have fewer displayed digits, while the fixed-width positional value remains the same integer. No extra leading-zero convention is introduced by the contract. Values of the digit function outside width L are unconstrained and irrelevant to the consumed prefixes.

The canonical wrapper intentionally has positive width, because that is the preexisting definition. The general bounded-function theorem additionally covers empty width and arbitrary singleton coefficients. Symmetry, nonnegative natural coefficients, and hb are enough for that algebraic extension. An odd central coefficient need not be even there, and q 0 need not be positive. Those are not hidden omissions of realizability: actual positive integer cases are separately supplied by Canonical, which automatically realizes the required coefficients. No orbit, positivity of all coefficients, no-overflow condition, or center-carry constraint belongs in the general contract.

## Reused charge semantics

The pinned `ChargeSymmetry.lean` defines `carryCharge` by the complete carry-word length parity, selecting `oddCharge` or `evenCharge`. It subtracts the left weighted half from the reflected weighted half. Its zero iff reverse equality theorem assumes only Binary. `SourceFormula.lean` identifies this same definition with both original U/S sums, with the correct sign and mirror indices. The new adapter must consume this existing definition directly.

An odd central carry remains present in the full list. Its self-mirror difference contributes zero to J, so the charge theorem does not force that central bit to zero. The empty and singleton half sums are empty. No leading-zero normalization of the carry word is allowed because it would change parity, pair indices and weights.

## Finite diagnostics, explicitly separate from proof

`finite-diagnostics-001/check_original_source.py` reuses the unchanged original `qstep` and `carry_coordinates` functions through `runpy.run_path`; it defines no new carry recurrence. The exact command, script hash, complete stdout, complete stderr and exit status are preserved beside it. Exit status was 0 and stderr was empty.

- All 7,240 bounded coefficient words of lengths 0 through 3 were checked for binary outputs, full length, retained final carry, and J=0 iff carry reflection equality, without assuming coefficient symmetry.
- All 14,479 symmetric bounded coefficient words of lengths 0 through 6 were checked for support at nine, the exact nonzero-witness equivalence, and the literal no-nine implication. Both parities and both final carry values occur in this finite scope. Outer zeros and odd central coefficients are deliberately allowed in the general-word diagnostics.
- Ten ordinary positive decimal examples were checked, including width one, low-end zero, both parities and both overflow values.

Selected examples from the preserved output:

| n or coefficient word | q | Complete outgoing word | J | Purpose |
| --- | --- | --- | --- | --- |
| n=5 | [10] | [1] | 0 | An odd center may be one; singleton overflow is retained. |
| n=18 | [9,9] | [0,0] | 0 | Actual canonical counterexample to the forbidden converse. |
| n=158 | [9,10,9] | [0,1,1] | 1 | Odd width with overflow and nonzero charge. |
| n=11587 | [8,9,10,9,8] | [0,0,1,1,0] | 1 | Odd width with no overflow and nonzero charge. |
| n=1558 | [9,10,10,9] | [0,1,1,1] | 21 | Even width with overflow and nonzero charge. |
| n=115587 | [8,9,10,10,9,8] | [0,0,1,1,1,0] | 21 | Even width with no overflow and nonzero charge. |
| Arbitrary q | [10,0] | [1,0] | -1 | Without coefficient symmetry, absence of nine alone need not force zero. |

These are finite Python implementation diagnostics. They do not establish a universal theorem, an exact Lean source build, Canonical proofs in Lean, or a transitive axiom audit. No failure was found in this finite execution.

## Preservation and next gate

`contract-snapshot-001/manifest.json` records 12 exact file snapshots with Git blob and SHA-256 hashes. The three arithmetic dependency hashes match the protected pins; the four charge files match the retained frozen PR145 source snapshots. Source inspection reviewed the selected interfaces and source-sum bridges; it did not redo the prior charge package's independent acceptance.

An initial combined tool display truncated part of the mandate text; the missing section was subsequently read separately. Other selected source reads were complete at their relevant sections. No approval rejection, source modification, remote write or Git write occurred in this review checkpoint.

Next: inspect the author's preserved source versions without changes, record any semantic findings and exact source hashes, then repeat the statement-to-contract comparison on the root's frozen published commit. Only that exact-head review can supply the semantic component of the final attributed formal COMMENT. Independent execution and the full eight-module axiom gate remain another genuine nonauthor's responsibility.
