# Agent 112 — Faithful numerical coordinates for bounded A120 words

Task: **T3.lean-numerical-state-injectivity**, coordination
[#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433564144).
Status: **LEAN-VERIFIED + COMPUTED**, after the exact validation below.
Dependency: the existing Agent112 numerical arithmetic project, stacked on PR414.

## 1. Exact scope

The raw formulas in PR398 和 PR414 determine outputs from numerical data.
This result addresses a different question: when do those data identify
the bounded input word uniquely?

For b>=2 和 coefficients in [0,2(b-1)], an arbitrary word is determined
by its width, forward positional value, 和 reversed positional value.
A symmetric word is determined by its width 和 signed value

\[
Z_b(C)=\operatorname{val}_b(C)+1-b^{|C|}.
\]

There is also a stronger zero characterization: for EVERY bounded word,
without a symmetry assumption, Z=0 exactly when the word is literally
all b-1 coefficients. All statements include the empty word.

These are injectivity 和 zero-fiber statements. They do not assert that
every numerical triple or every signed integer has a bounded-word
representation. No executable decoder, image classification, padding
quotient, or cycle realization theorem is included.

## 2. Bidirectional injectivity

Let A 和 B have the same width, all coefficients at most2(b-1), 和

\[
\operatorname{val}_b(A)=\operatorname{val}_b(B),\qquad
\operatorname{val}_b(A^{\rm reverse})=
\operatorname{val}_b(B^{\rm reverse}).
\]

Then A=B. No symmetry, positive head, nonzero value, or actual A120
`Hyp` is required for this word-level theorem.

The proof proceeds by removing one low coefficient at a time. For a
nonempty word a::T, put P=b^|T|, V=val(a::T), H=val(reverse(a::T)),
r=V mod b, 和 q=floor(H/P). Bounded-word normalization implies

\[
\operatorname{val}_b(T^{\rm reverse})<2P\le bP.
\]

Thus q=a+t for some 0<=t<b, while r=a mod b. The coefficient is recovered
exactly by the established arithmetic formula

\[
a=r+b\left\lfloor\frac{q-r}{b}\right\rfloor.
\]

Equal V/H 和 width therefore give equal low coefficients. Cancellation
in the two positional identities gives equal values for the shorter
tails, 和 induction finishes. The coefficient recovery identity is private
proof support; no new public decoder API is introduced.

## 3. Symmetric words 和 the zero value

For a symmetric word, its reversed value equals its forward value.
Equal widths 和 equal Z give equal forward values, so the preceding
bidirectional theorem proves equality of the literal coefficient words.

Symmetry is essential for this general one-value injectivity statement.
For example, at base10 the bounded words [11,0] 和 [1,1] have the same
width 和 value11, hence the same Z=-88, but are different. The first is
nonsymmetric. This does not contradict bidirectional injectivity, since
their reversed values are110 和11.

Width must also be retained for symmetric words. For every b>=2, the
bounded symmetric words [b,b] 和 [b,0,b] both have Z=b+1 but different
widths. PR349 already uses this family to analyze width information.

The zero fiber is more rigid 和 needs no symmetry. If Z=0 for a word of
width m, its value is b^m-1. Its low coefficient is congruent to b-1
modulo b. The bound2b-2 permits only the coefficient b-1: the next
candidate2b-1 is outside the alphabet. Subtracting b-1 和 dividing by b
repeats the argument on the tail. Conversely, m copies of b-1 have value
b^m-1 和 signed value0.

The bound matters even for this zero fiber. The nonsymmetric width-two
word [2b-1,b-2] has Z=0, just like [b-1,b-1], but uses a coefficient
one above the allowed bound. It is an outside-domain control, not an
admissible neutral-center state.

## 4. Attribution 和 mathematical limits

This is a formalization/generalization of existing arithmetic, not a
new injectivity discovery:

- `Agent115.ExteriorFactorization.eq_of_values` in
  `P196.Agent6CoordinateDynamics.ExteriorObservationInjective` proves the
  decimal two-value theorem for coefficients<=18.
- `P196.BidirectionalWordDecoder.Numeric` already supplies the decimal
  coefficient recovery method and decoder. Its `Sharpness` module gives
  stronger decimal alphabet results, including the uniform bound90.
- `ReverseAddInverse.symmetric_value_injective` in
  `P196.Foundations.LychrelDigitSums` already proves the decimal symmetric
  coefficient<=18 statement.
- PR349 gives the all-base symmetric PAPER argument, which also implies
  bidirectional injectivity by applying it to B++reverse(B).

The new endpoints use the unchanged all-base A120 list/value API at the
actual neutral coefficient bound. They do not formalize the sharp alphabet
threshold, a canonical observation map across widths, or inverse dynamics.
The existing decimal stronger results retain their full attribution.

## 5. Files 和 reproducibility

New modules in `P196.Agent112NeutralNumericalArithmetic`:

| Module | Public endpoint |
|---|---|
| `BidirectionalValues` | `eq_of_bidirectional_values` |
| `SymmetricState` | `symmetric_eq_of_signedValue` |
| `SymmetricState` | `signedValue_eq_zero_iff` |

The numerical controls are in
`calculation/agent-112/check_numerical_injectivity.py`.

```bash
python3 calculation/agent-112/check_numerical_injectivity.py
python3 -O calculation/agent-112/check_numerical_injectivity.py
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

Both Python commands print
`PASS: complete finite double-value/symmetric-Z dictionaries and all-word zero characterization.`
Their complete outputs are byte-identical. Checks use explicit failure
branches, so optimized execution preserves them. There is no sampling.

The complete ranges below all start at width0, using every coefficient in
[0,2(b-1)]. The symmetric suite enumerates every possible first half 和
reflects it, then checks the full word's width 和 symmetry.

| Base | Maximum arbitrary-word width | Maximum symmetric-word width |
|---|---:|---:|
| 2 | 9 | 16 |
| 3 | 6 | 12 |
| 4 | 5 | 10 |
| 5 | 4 | 8 |
| 10 | 4 | 8 |
| 11 | 3 | 6 |
| 17 | 3 | 6 |
| 20 | 3 | 4 |
| 26 | 2 | 4 |
| 32 | 2 | 4 |
| 97 | 2 | 2 |

The arbitrary-word suite checks365,398 words across54 base/width scopes:
6,050 symmetric 和359,348 nonsymmetric. Every fixed-width two-value
dictionary has exactly the full alphabet-size power, with no collision.
All365,398 words satisfy the zero equivalence; there are exactly54 zero
words, all neutral, 和 no nonsymmetric zero word. Base2 contributes29,524
words, 和 the eleven bases contribute eleven empty words.

The independent symmetric suite checks498,283 words across91 scopes,
with no fixed-width Z collision. It contains91 zeros 和249,096 words of
each sign. Base2 contributes19,681 words, again including width0.
These totals overlap the first suite where their scopes overlap; they are
not presented as a union count. The largest single dictionary has130,321
entries. Dictionary cardinalities 和 symmetry counts are checked explicitly.

Three bounded examples test the indispensable inputs from section3.
Each of the eleven bases also checks the known above-bound symmetric
collision [b,0,0,b] versus [0,M,M,0], M=b^2-b+1: both directional values
are b^4+b 和 both signed values are b+1. This retains the prior PR349 /
Agent5 attribution, without claiming a newly formalized sharp threshold.
Eleven separate bound-plus-one controls check the nonsymmetric zero
collision [2b-1,b-2] versus [b-1,b-1].

The two new modules compile on one thread in1.344s/438,992KiB 和
0.883s/440,692KiB, respectively, with8GiB address-space 和1200s limits.
The actual unchanged `python3 tools/verify.py --changed` reports5223 Lean
files/302 projects, six modules built 和 kernel-replayed across the stack,
28 public endpoints audited (three new here), permitted axioms only,
和 `ALL CHECKS PASSED`. Each file is below the8GB/20min budget.
Official Lean4.19.0 和 official lean4checker v4.19.0 are unchanged;
PR385's report documents the narrow executable-path launch adaptation.
Independent source reviews cover the core proof, stronger zero theorem,
test enumeration/counts, boundary examples, 和 stated limits.

## 6. Consequences not claimed

Together with the raw-step formulas, these endpoints justify using the
specified numerical data as identifiers of words satisfying the stated
bounds and, for the one-value theorem, symmetry hypotheses.
They do not make arbitrary integer inputs admissible, prove a numerical
cycle lifts, classify full A120 cycles, or establish a decimal certificate.
Agent119's canonical quotient, Agent104's finite bounded decision theorem,
Agent114's trim gates, 和 the repeated-driver searches remain separate.
