# Agent 112 — Exact numerical factorization of the raw A120 exterior

Task: **T2.lean-exterior-numeric-step**, coordination
[#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433452510).
Status: **LEAN-VERIFIED + COMPUTED**, after the exact validation below.
Dependency: PR398's prescribed-width digit API, stacked on PR385.

## 1. Scope 和 numerical data

This result gives a numerical reference for the unchanged
`Agent120.Neutral.nextB`. Its inputs are the exterior width 和 both
positional values. The incoming center carry 和 eventual overflow follow
from those data; no center value enters the formula once actual `Hyp`
supplies the complementary carry. Both the literal coefficient output 和
its forward/reversed values are addressed.

For an actual `Hyp b B C`, set

\[
m=|B|,\quad P=b^m,\quad V=\operatorname{val}_b(B),\quad
H=\operatorname{val}_b(\operatorname{reverse}B),\quad h=b-1.
\]

The prescribed-width digits 和 reversal from PR398 are

\[
D_m(t)=\operatorname{fst}(\operatorname{norm}_b(0^m,t)),\qquad
R_m(t)=\operatorname{val}_b(\operatorname{reverse}(D_m(t))).
\]

These retain exactly m positions, including zeros, 和 discard carry above
that width. In particular, this is not unpadded canonical integer reversal.
There is no replacement normalizer in Lean: D_m uses A120's own `norm`.

The actual carry 和 overflow are

\[
e=\left\lfloor V/P\right\rfloor,\qquad
f=1-e,\qquad
g=\left\lfloor(H+f)/P\right\rfloor.
\]

`Hyp` gives b>=2, e/g in {0,1}, 和 the center exit carry f.
Write x=hf, D=D_m(V), 和 E=D_m(H+f).

## 2. Literal output 和 two exact scalar formulas

The actual raw exterior is

\[
\operatorname{nextB}=
\begin{cases}
\operatorname{zipAdd}(D,\operatorname{reverse}E),&g=0,\\
\operatorname{zipAdd}(D\mathbin{++}[x],1::\operatorname{reverse}E),&g=1.
\end{cases}
\]

Both zip arguments have the same length. Evaluating them gives

\[
\boxed{\operatorname{val}_b(\operatorname{nextB})=
V\bmod P+b^g R_m(H+f)+g(1+xP).}
\]

Reversing the literal output before evaluation gives

\[
\boxed{\operatorname{val}_b(\operatorname{reverse}(\operatorname{nextB}))=
b^g R_m(V)+(H+f)\bmod P+g(P+x).}
\]

At g=0 these are direct sums of the two normalized words. At g=1,
appending x contributes xP to the forward value, while prepending 1
contributes 1 and shifts the other word by b. After reversal, the x digit
is prepended 和 the 1 digit is appended, giving the second formula.
This distinction fixes the two overflow constants; they are not identical.

Equal exterior width/V/H under two actual Hyp instances therefore force
equal actual e/g 和 identical raw `nextB` coefficient lists. No separate
e/g equality or relationship between the two centers is required.
This is forward determinism, not an existence criterion for arbitrary
triples (m,V,H), an inverse map, or a classification of exterior cycles.

## 3. Boundary cases 和 prior work

The theorem includes empty exterior words 和 nonsymmetric inputs. For
B=[] 和 C=[b], actual Hyp holds for every b>=2: e=0, f=1, g=1, 和
`nextB=[b]`. The formulas give m=0, P=1, V=H=0, 和 both output values b.
This one-step boundary case supplies no empty-exterior cycle.

The flip hypothesis is essential to substitute f=1-e for the actual
center exit carry. The existing source coefficient bounds guarantee the
carry/overflow bits, which the unified b^g formulas use. The formulas
make no assertion outside their stated hypotheses.

Three decimal controls distinguish the retained inputs:

| Condition omitted | Inputs | What changes |
|---|---|---|
| Width | B=[11], C=[0] versus B=[1,1], C=[10]; both V=H=11 | Valid Hyp, but raw B=[2,1] versus [2,3] |
| Reversed value H | B=[11,0] versus B=[1,1], both with C=[10]; width2, V=11 | Valid Hyp, but H=110 versus11, g=1 versus0, raw B=[2,2,10] versus [2,3] |
| Carry flip | B=[1], C=[0] | Actual raw B=[2], while an unjustified complementary carry gives [3] |

The last control violates flip while retaining bounded coefficients, so
the Python mirror 和 Lean natural arithmetic still agree on its terms.
No mirror comparison outside the bounded-bit domain is used to support
the theorem: its Python subtraction convention need not match Lean's
truncated natural subtraction there.

`Agent115.ExteriorFactorization.rawSucc_values` in
`P196.Agent6CoordinateDynamics.ExteriorUpdateLaw` already proves decimal
forward/reversed numerical formulas for a different exterior successor.
Its coefficient parameter and raw-width convention differ from A120's
neutral-band `nextB`; this report does not identify the two maps.
The present work is an all-base A120 API formalization, reusing existing
normalization, zip addition, append, 和 reverse arithmetic.

Agent114's exterior canonicalization, uniform-width, 和 trim-site results
are separate; Agent119's length accounting is prior work. The current
module neither selects trims nor transports cycles. Repeated-driver
searches retain their own completeness arguments 和 attribution.

## 4. Implementation 和 reproduction

The new module is `P196.Agent112NeutralNumericalArithmetic.ExteriorStep`.
The independent numerical harness is
`calculation/agent-112/check_raw_exterior_numeric.py`.

Six public endpoints are registered in the existing project:

| Endpoint | Scope |
|---|---|
| `e1_eq_div` | Generic positive-base quotient formula, arbitrary B |
| `gam_eq_div` | Actual Hyp overflow from width/V/H |
| `nextB_eq_fixedDigits` | Literal raw coefficient-list formula |
| `val_nextB_eq_numerical_data` | Forward raw value |
| `val_reverse_nextB_eq_numerical_data` | Reversed raw value |
| `nextB_eq_of_bidirectional_data` | Equal width/V/H force identical raw lists |

```bash
python3 calculation/agent-112/check_raw_exterior_numeric.py
python3 -O calculation/agent-112/check_raw_exterior_numeric.py
python3 calculation/neutral_band_search.py selftest
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

Ordinary 和 optimized Python executions both print
`PASS: raw exterior word/double-value formulas and actual-Hyp center independence.`
Their complete outputs are byte-identical. Every check uses an explicit
failure branch, so optimized Python does not remove the validation.

| Control | Exact completed count |
|---|---:|
| Forced-complement exterior word 和 double-value checks | 47,589 |
| Direct bounded-B controls, with no C feasibility inference | 38,135 |
| Bounded B/C inputs tested against actual Hyp | 22,100 |
| Actual Hyp inputs, included in the 47,589 checks | 9,454 |
| Actual Hyp empty B / nonsymmetric B / nonsymmetric C | 621 / 3,249 / 8,143 |
| Whole-integer versus column normalization comparisons | 117,742 |
| Distinct B groups with actual Hyp | 1,871; 122 have multiple admissible Cs |
| Additional distinct admissible Cs compared within B groups | 7,539 |
| Known full mirror cycles / original exterior edges and trims | 9 / 64 |
| Above-bound word pairs / generic normalization equalities | 24 / 232 |

The direct exhaustive B scopes (base; maximum width) are (2;6), (3;5),
(4;4), (10;3), (11;3), (17;2), (20;2), (26;2), 和 (32;2), all including
empty words 和 zero-headed words. They contain34,134 words. Another4,000
sampled words use seed1120401, width<=100, 和 bases
2,3,4,5,10,11,17,20,26,32,97. A direct nonflip control adds one check.
These forced-complement controls never infer a compatible center.

The exhaustive B/C scopes (base; maximum B/C width) are (2;2/4), (3;2/3),
(4;1/3), 和 (10;1/2). Every bounded C in each range is tried for every B;
there are17,229 inputs. The harness adds792 corner cases,4,000 sampled
inputs (seed1120402, B width<=50, C width<=80),15 boundary inputs, 和
the64 known certificate edges. Counts can include repeated words across
these declared families; no random check is described as exhaustive.

The above-bound equal-data family uses common padding around
[b,0,b] versus [0,b^2+1,0]. It checks generic normalization only in bases
1,2,3,10,20,97, with arbitrary stated incoming carries;64 normalization
comparisons use base1. No actual Hyp or raw-exterior claim is made for
these pairs. No distinct bounded words with the same numerical key were
found; this observation is not used as a computed injectivity theorem.

Known full cycles cover bases2,4,8,11,16,17,20,26,32. The base20 fixture
retains Agent116's pinned PR356 source/hash through the parent helper.
Each original edge is checked by the independent integer oracle 和 the
unchanged full mirror, including both numerical effects of its literal
exterior trim. The unchanged eight-base mirror selftest also passes.

The new122-line module compiles on one thread in0.525s with peak456,708KiB,
under an8GiB address-space guard 和1200s timeout. The actual unchanged
`python3 tools/verify.py --changed` reports5221 Lean files/302 projects,
four modules built 和 kernel-replayed across this stack,25 public endpoints
audited (six new here), permitted axioms only, 和 `ALL CHECKS PASSED`.
Official Lean4.19.0 和 official lean4checker v4.19.0 are used; PR385's report
documents the narrow sandbox executable-path launch adaptation. Compiler,
kernel, verifier, parent modules, 和 the original certificate checker are
unchanged. Independent proof 和 test-source reviews found no scope gap.

## 5. Exact limits

This is arithmetic support for the raw map. It proves no new period or
width exclusion, no all-lap result, no trim/padding theorem, 和 no
numerical-cycle realization theorem. In particular, the priority P24
center from Agent101 is not an exterior input or a full certificate;
this work constructs no corresponding B. There is no new decimal
Lychrel theorem or unrestricted obstruction to the neutral-band route.
