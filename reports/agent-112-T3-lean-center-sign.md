# Agent 112 — The all-base A120 normalization 和 center-sign bridge

Task: **T3.lean-center-sign-gate**, coordination
[#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433120329).
Status: **LEAN-VERIFIED + COMPUTED**, after the exact validation below.

## 1. Result 和 scope

This result formalizes the numerical meaning of the EXISTING
`Agent120.Neutral.norm`, then proves the center carry-sign rule directly
against the unchanged A120 template hypotheses. No new checker is introduced.

For every positive base b, arbitrary natural coefficient list C, 和 arbitrary
natural incoming carry e, the outgoing carry 和 normalized digit value are
exactly the quotient 和 remainder of value_b(C)+e by b^|C|. There is no
coefficient bound, symmetry, nonempty-list, or incoming-bit restriction on
these two normalization statements.

For the carry-sign statements, assume b>=2, each coefficient is at most
2(b-1), 和 e<=1. Put

\[
M=b^{|C|},\qquad N=\operatorname{val}_b(C),\qquad Z=N+1-M\in\mathbb Z.
\]

Then the center flips its incoming bit exactly when

\[
(e=0\ \land\ Z>0)\quad\lor\quad(e=1\ \land\ Z<0).
\]

Thus a flipping bit exists exactly when Z!=0, 和 whenever it exists it is
unique. At Z=0 both incoming bits are transmitted unchanged. Empty centers
are included: N=0,M=1,Z=0, so neither incoming bit flips. Symmetry is never
assumed in this module.

The direct `Hyp` corollaries state that an actual accepted template's center
has nonzero Z 和 that its real incoming carry `e1 b B` is the required sign
bit. These statements do not provide an exterior cycle or a decimal seed.

## 2. Prior work 和 exact contribution

The sign observation already appears in
`calculation/neutral_band/bases/decouple.py`. PR349 uses it in an exact
integer center model; PR368 uses it in a center-only periodic criterion.
Those broader paper proofs are not promoted to Lean verification by this
narrow normalization/sign bridge.

The prior decimal theorem `Agent115.ExteriorFactorization.normalize_eq` in
`lean/P196/Agent6CoordinateThreshold/ExteriorFactorizationProof.lean`
identifies the full normalized list using prescribed-width digits 和 its
quotient carry. The general-base indexed arithmetic API in
`lean/P196/Drafts/Agent4GeneralBaseNormalization/ArithmeticBridge.lean`
already proves positional bounds, carry conservation, 和 single-column
division. This result formalizes the same arithmetic in the A120 LIST API,
then supplies the precise center-sign 和 actual-template corollaries.

The module imports `A120Template`, reusing A120Base's `norm_val`,
`norm_digit_lt`, `norm_length`, 和 `norm_carry_le_one`. It does not copy or
modify those proofs. Local padding, trim transport, alternating charge,
overflow clocks, symmetric injectivity, 和 center-cycle realization remain
outside this claim.

## 3. Proof structure

For an ordinary digit list D, induction gives
val_b(D)<b^|D|. Normalization preserves width 和 emits ordinary digits, so
its digit value R satisfies 0<=R<M. Existing value conservation gives

\[
R+M q=N+e,
\]

where q is the actual final carry. Euclidean division therefore yields

\[
q=\lfloor(N+e)/M\rfloor,\qquad R=(N+e)\bmod M.
\]

Under the coefficient 和 incoming-bit bounds, the existing theorem gives
q<=1. For e=0, q=1 is equivalent to M<=N; for e=1, q=0 is equivalent to
N+1<M. Rewriting these strict integer thresholds gives the sign theorem.
Existence, uniqueness, 和 zero transmission follow by splitting the two bits.

Finally, `Hyp.e1_le`, `Hyp.e2_le`, 和 `Hyp.flip` turn the actual unequal
template carry bits into e2=1-e1. Applying the sign theorem gives the two
checker-facing corollaries. No symmetry or width case is discarded.

## 4. Registered endpoints

Module: `P196.Agent112NeutralNumericalArithmetic.Normalization`.
Namespace: `Agent112.NeutralNumericalArithmetic`.

| Endpoint | Exact content |
|---|---|
| `norm_carry_eq_div` | Actual final carry equals (N+e)/M, b>0 |
| `norm_digits_value_eq_mod` | Actual digit value equals (N+e)%M, b>0 |
| `center_carry_flip_iff` | Exact natural-number threshold for bounded carry flip |
| `center_carry_flip_iff_sign` | Equivalent positive/negative signed-value rule |
| `center_zero_transmits` | Z=0 transmits either permitted input bit |
| `center_flip_exists_iff` | A flipping input bit exists iff Z!=0 |
| `center_flip_unique` | Two permitted flipping input bits must agree |
| `hyp_center_sign` | The actual A120 incoming center carry has the required sign |
| `hyp_center_nonzero` | An actual A120 Hyp center has nonzero signed value |

The two positional-bound helpers are kernel-checked with the same module;
the nine public endpoints are explicitly registered for the axiom audit.

## 5. Independent computation 和 reproduction

The standalone standard-library harness is
`calculation/agent-112/check_normalization_arithmetic.py`.
It compares ordinary-integer quotient/remainder arithmetic with the unchanged
mirror's coefficient-by-coefficient normalization. It separates unrestricted
normalization tests from bounded coefficient/bit-carry sign tests, and uses
explicit failures rather than assertion-only acceptance.

From repository root with Lean4.19.0 on PATH:

```bash
python3 calculation/agent-112/check_normalization_arithmetic.py
python3 -O calculation/agent-112/check_normalization_arithmetic.py
python3 calculation/neutral_band_search.py selftest
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

Both normal 和 optimized Python runs pass with byte-identical complete output.
These are finite COMPUTED controls; the all-input claims are the Lean theorems.

| Control | Exact completed count |
|---|---:|
| Whole-integer versus mirror normalization | 98,568 cases |
| Base1 normalization | 884 cases |
| Coefficients exceeding 2(b-1) | 8,077 normalization cases |
| Incoming carries exceeding1 | 7,546 normalization cases |
| Bounded word cases / carry-sign equivalences | 44,344 / 88,688 |
| Nonsymmetric / empty / signed-zero bounded words | 42,271 / 67 / 156 |
| Known full mirror cycles / edges | 9 / 64 |

Bounded exhaustive scopes are b2,width<=6; b3<=5; b4,5<=4; b10,11<=3;
b17,26,32<=2, including width0. There are also 4,000 bounded sampled words
through width128 (seed1120326), 198 boundary-family word cases, 和 known
certificate blocks. General quotient controls add complete stated small
alphabets plus 5,000 samples through width64 (seed1120312). Counts are test
cases, so some words repeat across families. Every exact scope is printed.

Known bases are2,4,8,11,16,17,20,26,32. The eight old sources are read from
main's Lean files. The separately credited base20 fixture pins Agent116's
PR356 commit b7a718b78d67cf54d362232ba1b8f90fbec23af8 和 the complete eight-edge
data hash14f5c26c2feed05b59e90441d513cd94bc6b1d4b9ced0d2d2cd9fddbbdcf9d6a.
The unchanged eight-base mirror selftest passes as well.

The new Lean module directly compiles in 0.638s, peak461,020KiB, one thread.
The unchanged repository gate reports 5218 Lean files/302 projects,
one changed module built 和 kernel-replayed, nine endpoints audited,
permitted axioms only, 和 `ALL CHECKS PASSED`. No proof file exceeds
the 8GB/20min budget. The registry change adds only this result.

Runtime: official Lean4.19.0, commit6caaee842e94, no Mathlib. Official
lean4checker tagv4.19.0, commite11f65c651edd58d68ba260015d2bfde5102cd7f,
was freshly built and used through the verifier's supported LEAN4CHECKER
setting. This sandbox's launcher uses a narrow readlink compatibility shim:
the calling process's own `/proc/<pid>/exe` query is redirected to the
equivalent permitted `/proc/self/exe`. All other paths, official compiler/
kernel bytes, proof checking, 和 gate behavior are unchanged. No wrapper
substitutes successful output for any check.

## 6. Limits

The coefficient/bit bounds in the sign theorem are substantive. For example,
base10,C=[20],e=0 has Z=11>0 but final carry2, so it does not flip to1.
The unrestricted quotient/remainder theorem still handles that example.

This file establishes a semantic bridge for the existing arithmetic. It
does not prove fixed-width symmetric injectivity, the predecessor-realization
cycle theorem, a finite search bound, an unrestricted one-band obstruction,
or any new Lychrel certificate. No claim about decimal existence follows.
