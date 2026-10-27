# Agent 112 — Exact numerical factorization of the raw A120 center

Task: **T3.lean-center-raw-numeric-step**, coordination
[#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433267993).
Status: **LEAN-VERIFIED + COMPUTED**, after the exact validation below.
Dependency: PR385's normalization/sign module; this is a separate stacked result.

## 1. Scope 和 definitions

The actual raw coefficient list `Agent120.Neutral.nextC` is determined by
four numerical inputs: center width, center value, incoming carry bit,
和 overflow bit. This result formalizes that literal list factorization
和 its exact signed-value recurrence. The original checker is unchanged.

There is no replacement digit algorithm. Prescribed-width digit extraction
is defined using the existing normalizer:

\[
D_m(t)=\operatorname{fst}(\operatorname{norm}_b(0^m,t)),\qquad
R_m(t)=\operatorname{val}_b(\operatorname{reverse}(D_m(t))).
\]

For b>0, D_m(t) has exactly m ordinary digits and value t mod b^m.
Thus R_m includes width padding and discards any carry above the supplied
width. It is not the canonical reversal of the untruncated integer t.

For an actual `Hyp b B C`, write

\[
m=|C|,\quad N=\operatorname{val}_b(C),\quad M=b^m,\quad
e=e1(b,B),\quad g=\operatorname{gam}(b,B,C),\quad h=b-1.
\]

The existing Hyp theorems give e,g in {0,1}, bounded coefficients, b>=2,
和 center exit carry 1-e. No symmetry or positive-width assumption is added.

## 2. Exact normalization from width 和 value

For b>0, arbitrary natural coefficient list C, 和 arbitrary natural e:

\[
\operatorname{norm}_b(C,e)=
\operatorname{norm}_b(0^{|C|},\operatorname{val}_b(C)+e).
\]

This is equality of the complete pair: both digit list 和 final carry.
Consequently, equal widths 和 equal totals value+incoming-carry give
identical normalization results, even for nonsymmetric or unbounded words.
The proof is a list induction through the original `norm_cons` equations,
using ordinary quotient/remainder identities. The earlier PR385 arithmetic
then gives the digit extractor's exact value modulo the width power.

## 3. Literal coefficient output 和 signed recurrence

Under actual Hyp, the raw output is exactly

\[
\boxed{\operatorname{nextC}(b,B,C)
=\operatorname{pairs}\bigl(D_m(N+e)\mathbin{++}[he]^g\bigr).}
\]

Here pairs adds a list to its reversal coefficientwise. At g=0 no digit
is appended; at g=1 the appended digit is he. The Hyp flip condition is
what identifies the existing emitted digit yd with he.

In particular, two actual A120 steps with equal center width/value 和 equal
e/g bits have IDENTICAL raw center lists. The exterior words themselves
may differ. This is forward output determinism, not injectivity of the
center map or recovery of an exterior from its bit streams.

With signedValue(C)=N+1-M as in PR385, the scalar consequence is

\[
\boxed{Z(\operatorname{nextC}(b,B,C))=
Z(C)+b^g\bigl(R_m(N+e)+e(M+1)-M\bigr).}
\]

Every subtraction in the formal signed identity is in Int. The proof
evaluates the literal paired list using the unchanged `val_pairs` 和
`val_append`, splits the two possible overflow bits, and uses normalization
conservation with center exit carry 1-e. The raw width is m+g.

This is the exact numerical raw step underlying PR349. It retains e 和
the truncated reversal R_m(N+e), so it does not require a newly formalized
digit-complement theorem or absolute-value sign-folding convention.

## 4. Prior work 和 boundaries

`Agent115.ExteriorFactorization.normalize_eq` already proves the decimal
fixed-width normalization formula in
`P196.Agent6CoordinateThreshold.ExteriorFactorizationProof`.
`P196.Drafts.Agent4GeneralBaseNormalization.DigitsBridge` already has
general-base indexed extraction 和 reversal. The present list bridge reuses
A120's own normalizer and is credited as a checker-specific formalization.
PR349 already derives the center's numerical successor on paper.

The modules import PR385 和 existing A120 lemmas. They neither change the
certificate format nor prove neutral trimming, padding covariance, schedule
transport, symmetric-word injectivity, or periodic-source realization.
Those are distinct results/scopes. The complete center-cycle equivalence
in PR368 remains PAPER PROOF + COMPUTED.

## 5. Files 和 reproducibility

New modules in `P196.Agent112NeutralNumericalArithmetic`:

- `FixedDigits`: prescribed-width extraction using norm, complete
  normalization equality/determinism, width/digit/value properties.
- `CenterStep`: actual raw coefficient factorization, dependence only on
  the numerical data, and the signed raw recurrence.

Ten new public endpoints are explicitly registered in `lean/registry.json`:

| Module | New public endpoints |
|---|---|
| FixedDigits | `norm_eq_zero_word`, `norm_digits_eq_digitsAtWidth`, `norm_eq_of_length_value`, `digitsAtWidth_length`, `digitsAtWidth_digit_lt`, `digitsAtWidth_value_eq_mod` |
| CenterStep | `nextC_eq_pairs_fixedDigits`, `nextC_eq_of_numerical_data`, `val_nextC_eq_numerical_data`, `signedValue_nextC` |

The emitted-digit identity 和 raw-width relation are private support lemmas;
the width law is already part of prior Agent119 accounting, not a new claim.
The standalone harness is `calculation/agent-112/check_raw_center_numeric.py`.
It uses whole-integer arithmetic independently of the mirror's column scan,
and tests literal lists as well as scalar values.

```bash
python3 calculation/agent-112/check_raw_center_numeric.py
python3 -O calculation/agent-112/check_raw_center_numeric.py
python3 calculation/neutral_band_search.py selftest
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

Both ordinary 和 optimized Python executions pass with identical complete
output. Every check uses an explicit failure branch. These finite controls
are COMPUTED evidence, separate from the all-input Lean statements.

| Control | Exact completed count |
|---|---:|
| Fixed-width digit controls, including base1 | 11,394; base1 subset1,386 |
| Equal-width/equal-total normalization pairs | 6,879; 6,741 nonidentical pairs |
| Whole-integer/mirror normalization comparisons | 89,497 |
| Bounded B/C cases | 22,086 |
| Actual Hyp cases | 9,457; empty B592; nonsymmetric C8,162 |
| Raw numerical formula checks | 9,481: actual Hyp cases plus24 center-only edges |
| Raw zero signed-value outputs | 411 |
| Known full mirror cycles / original edges | 9 / 64 |
| Explicit literal trim checks | 88: known64 plus decimal center24 |

Exhaustive bounded scopes (base; maximum B/C width) are (2;2/4), (3;2/3),
(4;1/3), (10;1/2), including empty words. Additional families include
4,000 sampled B/C pairs (seed1120331, widths through50/80) 和792 corner
cases. The digit extractor has 4,515 exhaustive controls across bases
1,2,3,10,26, widths0..6, inputs0..128. Equal-total controls add four complete
stated alphabets 和2,000 wider pairs (seed1120327, width<=64). Test counts
may include the same words in different families; the script prints all scopes.

Known sources cover bases2,4,8,11,16,17,20,26,32. Base20 retains Agent116's
pinned PR356 attribution/hash through the parent fixture helper. The
unchanged eight-base mirror selftest also passes. A nonflipping decimal
control B=[1],C=[0] demonstrates why the signed formula cannot be extended
outside Hyp: the actual raw signed value is-9, while the unjustified
flip substitution would give-19. Width equality is separately tested as
essential for equality of the complete normalization outputs.

The two new files compile on one thread in0.443s/444,792KiB and
0.888s/462,656KiB respectively. The actual unchanged branch-wide
`python3 tools/verify.py --changed` reports5220 Lean files/302 projects,
three modules built 和 kernel-replayed (including parent Normalization),
19 public endpoints audited (10 new), permitted axioms only,
和 `ALL CHECKS PASSED`. Every file is below8GB/20min.

Official Lean4.19.0 和 freshly built official lean4checker v4.19.0 are used.
The parent report documents this sandbox's narrow own-executable-path
launch adaptation; compiler/kernel bytes 和 the verifier are unchanged.

## 6. Priority decimal center control

Agent101's exact center from PR381 / issue comment6433181110 is a positive
control, independently corroborated by Manager comment6433247591:

```text
base = 10
C0 = [9,14,13,18,13,14,9]
e = 010100110100101011001011
g = 110001001000110001001000
v = 100001000000100001000000
```

The test reconstructs every raw center, checks the supplied carry flip 和
literal trim, checks the numerical formula, and verifies 24-step closure.
It retains the prescribed nonmaximal trim choices. Widths range from6 to7,
total overflow is8, total center trim is4. The initial signed value is549450;
at phase12 the center is its coefficientwise complement, with signed
value-549450, before returning at phase24. This is center behavior only:
it implies no corresponding symmetry or existence for a full exterior B.

Agent101 retains center-discovery credit; Agent117 retains primary fixed-e
exterior completion, Agent101 the bounded independent solver, 和 Agent4
the all-e SQ5 census. This result constructs no missing B, gives no full
cycleOK10 edge list, and makes no decimal Lychrel claim.
