# Independent semantic review of Agent4's alternating strip

This initial checkpoint records **semantic review with compilation pending**.
No defect was found in the abstract theorem's stated scope. Kernel acceptance
requires the separate executor's fresh build and axiom audit. Source-only
fixtures and proposition contracts below are not claimed as checked results.
Later execution evidence should be recorded in an addendum, preserving this
checkpoint's historical status.

The review is owned by Agent104 under coordination claim
`1f5743c1b104a14c3b096fbb685342eda1d2caf9`. Agent4 retains ownership of the theorem
and any actual-map extension. No Agent4 source was edited. No Lean process was
started by this semantic reviewer.

## Exact source and endpoint

Reviewed main commit: `5bd98567b259659fd3195f5aa61617422aa80914`.

Source: `proofs/agent4/temporal_strip/NoAlternatingReturn.lean`.

SHA256: `49b1065166c02c2efd1bf58c3391c5166b44106f12e82af371304e9fe3ae7ba0`.

The only import is `Lean.Elab.Tactic.Omega`. All seven named theorem headers
are transcribed without changing their binders in `statements.json` and
`ExactTypes.lean`. The namespace is `P196.Agent4.TemporalStrip`.

The main theorem is exactly an impossibility result for abstract arrays:

```lean
theorem no_alternating_six_twelve_strip {J : Type} (j0 : J) (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (cuts : Nat → Cut J)
    (x y : Nat → J → Nat) (width : Nat)
    (hv : ∀ i, i≤width → Valid (cuts i))
    (hc : ∀ i, i<width → Column next (cuts i) (cuts (i+1)) (x i) (y i))
    (outside : Outside (cuts 0))
    (tail : LeftAligned (cuts width) ∨ RightAligned (cuts width)) : False
```

`no_finite_alternating_six_twelve_strip` specializes `J` to `Fin N`, assumes
`0 < N`, and uses successor modulo `N`. Its temporal interpretation is **2N
ordinary updates**, paired as nonoverflow followed by overflow. It is not a
theorem for arbitrary overflow words or arbitrary finite forward paths.

`width` counts spatial columns from an outside cut toward an interior cut.
It is arbitrary and may be zero. It is not a decimal width parameter. There
is no spatial cap, period cap, presumed minimal period, or finite search in
these endpoints. The general theorem permits any inhabited temporal type
with an onto successor, including infinite types. The finite corollary has
no temporal restriction beyond `N > 0` and the stated equations.

## Proof semantics checked

`Cut` records four natural-number carries and one delayed digit. `Valid`
bounds the carries by one and the digit by nine; nonnegativity is supplied
by `Nat`. `Column` bounds both coefficients by eighteen and gives seven
equalities: two low-carry transitions, two backward high-carry transitions,
one delayed-digit update, and the two successive temporal emissions.
Neither a freely chosen carry word nor an ordinary-number realization is
silently identified with a canonical representation.

The scalar classification is exact within its explicit assumptions:

| Alignment at the inner cut | Exceptional possibility | Regular possibility |
| --- | --- | --- |
| Left | `x=1, y=3, a=1, r=0, u=0, v=0` | `x=6, y=12, a=0, r=1, u=0, v=1` |
| Right | `x=17, y=15, a=0, r=1, u=1, v=1` | `x=12, y=6, a=1, r=0, u=1, v=0` |

The unlisted low odd carry `b` may be zero or one. An independent Python
enumeration checked all 11,552 bounded input tuples for each classifier;
each has exactly four satisfying tuples, all covered by the source result.
This is a finite diagnostic, not a replacement for the kernel proof.

For `left_backward`, every temporal index has a predecessor by `onto`.
The predecessor's final emission and either scalar branch give `x ≥ 2`.
This removes the exceptional `x=1` branch everywhere. The remaining branch
fixes `x=6,y=12`; the final emission then gives the required source equation
`delayed + lowOdd = 4`.

For `right_backward`, the same predecessor argument instead yields
`x ≤ 16`. This removes `x=17`, leaves `x=12,y=6`, and yields the source
equation `delayed + lowOdd = 6`. No assumption of injectivity, temporal
finiteness, or eventual return is used in these two proofs beyond `onto`.

The main proof inducts on the finite spatial distance, transporting the
same aligned disjunct backward to cut zero. At the supplied index `j0`,
`Outside` has `(lowEven,lowOdd,highEven,highOdd,delayed)=(0,0,0,1,1)`.
This conflicts with the left sum `4` and with the right low-even carry `1`.
At width zero this contradiction is immediate; there is no omitted edge
case. All accessed cuts and columns lie within their quantified bounds.

`cyclic_successor_onto` treats index zero using predecessor `N-1`, and a
positive index using predecessor `j-1`. `N>0` is used for `Fin` construction
and modulo bounds. The finite endpoint supplies `j0=0` and invokes the
general theorem. Its use of `2N` in the comment agrees with the two temporal
emission equations per `Fin N` index.

The tail disjunction is global: either **every** temporal pair has the left
alignment or **every** pair has the right alignment. It is stronger than
allowing an independently chosen alignment at each index. Neither symmetry,
canonical leading digits, nor odd-center parity is a hypothesis of the
abstract theorem. This makes its input relation more permissive; it does
not itself supply an actual-word interpretation.

## Adversarial scope checks

`ScopeTests.lean` contains explicitly named fixtures, initially uncompiled:

* On `Empty`, validity, outside, and both tail predicates all hold
  vacuously. The inhabitant `j0` cannot be dropped from the general result.
* The constant cuts `(0,1,0,1,3)` and `(1,0,1,0,6)` are valid aligned
  interiors with respective columns `(x,y)=(6,12)` and `(12,6)` under the
  identity temporal successor. Thus aligned columns themselves are
  consistent; the external boundary is material.
* The genuine outside cut is valid and satisfies neither aligned predicate.
* For temporal type `Nat` with successor `Nat.succ`, the exceptional scalar
  branch can occur at index zero, while every later index is regular.
  Explicit source/target arrays satisfy the relevant column equations and
  aligned target, but have an unaligned source. These refute dropping
  `onto` from **the backward lemmas**. They do not claim that `onto` is a
  logically minimal assumption of the full outside-to-tail theorem.

The independent ordinary-number diagnostic in `check_scope.py` computes

```text
15 -> 66 -> 132
pair words: [6,6] -> [12,12] -> [3,6,3]
overflow bits for the two steps: 0,1
```

All ordinary numbers here use canonical decimal notation and literal digit
reversal. At spatial cut one, the first two words yield the left-aligned
cut `(0,1,0,1,3)`. At cut zero they yield `Outside`. All first-column
equations hold for the open actual update with next exterior coefficient
`3`; the cyclic equation would incorrectly replace it by the initial `6`.
Thus alternating overflow and an interior 6/12 band do **not** suffice to
instantiate the finite theorem. The generated `diagnostics.json` records
each equality and the precise failing cyclic equality. This is a checked
finite arithmetic diagnostic, not an asserted Lean ordinary-map theorem.

## Exact missing actual-map obligations

For an actual iterated pair word, write `q_t` for its coefficient function
and `L_t` for its current canonical width. At spatial cut `i`, the intended
interpretation is:

| Strip field at temporal index `j` | Required actual value |
| --- | --- |
| `lowEven` | `carry q_(2j) i` |
| `lowOdd` | `carry q_(2j+1) i` |
| `highEven` | `carry q_(2j) (L_(2j)-i)` |
| `highOdd` | `carry q_(2j+1) (L_(2j+1)-i)` |
| `delayed` | `extended q_(2j+1) L_(2j+1) (L_(2j+1)-i)` |

In particular, the delayed field is the previous high **output digit**,
including the appended one at `i=0`; it is not another carry or a reflected
source coefficient. Every high-side index uses its own time's actual width.

`ActualMapObligations.lean` defines the following two unproved propositions,
using actual `OverflowCarryNormalization.iterPairs` rather than a surrogate
sequence. Defining or typechecking these propositions does not prove them.

1. `ActualPrefixTransportObligation`: admissibility, a common in-range
   spatial prefix, actual overflow zero at even steps and one at odd steps,
   and actual prefix equality at time `2N` must imply every `Valid`, every
   `Column`, and `Outside` for the displayed interpretation. At indices
   before `N-1` the final temporal equation is an ordinary successor update;
   at `N-1` it specifically needs the asserted prefix return to wrap to zero.
2. `UniformBandTailObligation`: at one positive common cut `w`, positions
   `w-1` and `w` lie within the actual words at every sampled time and have
   coefficients uniformly `(6,6)` at even times and `(12,12)` at odd times,
   or uniformly the opposite. These adjacent coefficients reset both
   carries and supply the appropriate aligned tail at `w`.

The second contract is a sufficient, explicit tail condition, not a claim
that every 6/12 template return satisfies it. A further template/certificate
argument must locate such a common cut despite varying exterior lengths,
choose sufficiently long permitted gaps, preserve source guards throughout
the finite traversal, and establish prefix closure. The current strip
module contains none of these arguments. It also contains no hypothesis
about positive or negative total gap gains and no conclusion about accepted
`Agent109.Cert` certificates.

Relevant existing foundations are
`FoldedDecimal.folded_carry_transition`, `folded_emission_no_overflow`,
`folded_emission_overflow`, `folded_delay_update`,
`DecimalDigits.carry_bounded`, `CarryHistory.iterPairs_admissible`,
`NormalizationBridge.canonical_admissible`, and
`OverflowCarryNormalization.iterPairs_representation`. These supply real
arithmetic ingredients, but are not imported by the reviewed strip file.

Agent4's existing `WholeWordBridge.lean` proves
`P196.Agent4.WholeWord.nextColumns_prefix3`, `iterPairs_prefix_evolution`,
`actual_width_overflow_identity`, `actual_saturated_prefix_return`, and
`numeric_saturated_prefix_obstruction` (plus `iterPairs_width_ge`). Those
results concern three-column projection and saturation. They neither
construct these arbitrary-width temporal cuts nor discharge their common
tail and wraparound premises. A pinned-main Lean-source reference search
finds `TemporalStrip`/`NoAlternatingReturn` only in the reviewed file itself.

## Acceptance boundary and remaining gate

The source supports this semantic statement, subject to successful kernel
checking: **no valid abstract finite spatial strip can join the specified
outside cut to either uniformly aligned tail under the stated onto temporal
equations**. Its finite specialization covers every positive `N` and every
finite spatial width with those equations.

This review does not accept an ordinary 6/12 quotient-return exclusion, an
exclusion of arbitrary overflow schedules, a finite-forward-trajectory
obstruction, a bound on all complementary-band returns, a Lychrel existence
claim, or a result about 196. The missing actual-map transport and common-cut
composition are applicability obligations, not a discovered counterexample
to Agent4's abstract theorem.

Required next gate: the separate executor must rebuild the exact source,
check exact elaborated types, audit all theorem dependencies for forbidden
axioms, and typecheck the reviewer fixtures and unproved contracts with
pinned dependencies. No successful execution is inferred from `by omega`,
the source's `#print axioms` commands, or the finite Python diagnostics.

## Reproduction and evidence

From the repository root:

```sh
python proofs/contributions/agent-104/review-agent4-temporal-strip/semantic/check_scope.py
```

The script reads the pinned source through `git show`, checks its SHA256,
and performs only finite arithmetic controls. It starts no Lean process and
does not mutate Git. Its diagnostic output is retained in `diagnostics.json`.

Related source pins at the same reviewed commit:

| Source | SHA256 |
| --- | --- |
| `proofs/research/continuation/LychrelDigitSums.lean` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `proofs/agent4/prefix_growth/integration/WholeWordBridge.lean` | `483fc3084a9e9b796f9fd56e9640962839417386a30a2c803c9dd9b09ffa5b87` |
| `proofs/contributions/2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md` | `223800d0194dde564b5d4e32274a45d2ca2540242470f78dba203d17fc7a7e19` |
