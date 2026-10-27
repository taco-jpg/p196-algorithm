# Agent 112 — Faithful integer center dynamics 和 limits of scalar compression

Task: **T3.center-integer-state**, coordination [#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432857361).
Status: **PAPER PROOF + COMPUTED**. The general statements below are paper proofs;
the executable controls are finite computations. Lean formalization is pending.

## 1. Scope 和 prior work

Let b>=2, h=b-1. A center C 是 a symmetric coefficient word, least significant
first, of width m, with coefficients in [0,2h]. Define

\[
N(C)=\sum_{i=0}^{m-1}C_i b^i,\qquad Z(C)=N(C)-(b^m-1).
\]

The sign/carry observation is already in
`calculation/neutral_band/bases/decouple.py`; it is credited, rather than claimed
as new. Exact coefficient transitions come from `A120Template.lean` 和
`calculation/neutral_band_search.py`. Agent 7's neutral-padding covariance 和
canonical-cycle normalization are recorded in PRs #315/#326.

Decimal fixed-width injectivity already has a Lean proof:
`ReverseAddInverse.symmetric_value_injective` in
`lean/P196/Foundations/LychrelDigitSums.lean` covers symmetric coefficients
through18. The uniform decimal alphabet threshold90 is also already formal:
`Agent5.BidirectionalWordDecoder.values_injective_bound_iff` in
`lean/P196/BidirectionalWordDecoder/Sharpness.lean` proves the corresponding
two-evaluation theorem. On symmetric words the two evaluations agree;
its width-four collision at91 is symmetric too. Section2 gives an elementary
general-base extension/reproof, rather than a new decimal injectivity result.
No per-width classification for symmetric words is inferred from that source.

This result proves faithful numerical representations, an exact integer
transition, a decoding algorithm, 和 an obstruction to a specific scalar
compression. Overflow g is supplied externally. Compatibility with an actual
exterior B remains a separate requirement. This result supplies neither a
decimal certificate nor an unrestricted center nonexistence theorem.
Every center on a cycle is symmetric because each is a paired, trimmed
output of its predecessor; the symmetric domain therefore covers cycles.

## 2. PAPER PROOF — fixed-width injectivity

**Theorem.** For fixed m, bounded symmetric C,D with N(C)=N(D) satisfy C=D.

Remove matching exterior pairs until the difference word 有 nonzero first
coefficient a. Its last coefficient 也是 a. A remaining width-one word
cannot evaluate to zero. At remaining width r>=2,

\[
0=a(1+b^{r-1})+\sum_{i=1}^{r-2}(C_i-D_i)b^i.
\]

Modulo b, b divides a, so |a|>=b. The inner contribution 有 absolute value at
most 2(b^{r-1}-b), whereas the exterior contribution 有 magnitude at least
b(1+b^{r-1})>2(b^{r-1}-b). Contradiction.

The alphabet threshold can be sharpened: the same proof establishes
injectivity for coefficients in [0,M] whenever M<=b(b-1). This uniform
threshold 是 sharp. At M=b^2-b+1, distinct width-four words
[b,0,0,b] 和 [0,M,M,0] 都 evaluate to b+b^4. The actual center alphabet
2b-2 is within the injective range, including b=2.

**Decoder.** For r>=2, put Q=floor(N/b^(r-1)) 和 a=N mod b. The exterior
coefficient must be Q or Q-1, because the lower coefficients contribute less
than 2b^(r-1). It must also be congruent to a modulo b. At most one of these
consecutive candidates qualifies. Remove c(1+b^(r-1)), divide by b, 和
repeat. Check coefficient bounds, exact divisibility, the middle coefficient,
和 the final empty remainder. This accepts exactly the representable (m,Z)
pairs; a scalar interval bound alone would admit invalid states.

## 3. PAPER PROOF — neutral trimming 和 faithful padding quotient

For neutral paired padding P_a(C)=h^a ++ C ++ h^a,

\[
Z(P_a(C))=b^a Z(C).
\]

By injectivity, Z(C)=0 exactly when C consists entirely of h coefficients.
Such a center transmits either entering carry unchanged, so cannot satisfy
the flip hypothesis. Empty centers are included in this terminal case.

For Z!=0, let ord_b(Z) be the largest v with b^v dividing Z. The base may be
composite; this is divisibility by base powers, without assuming a prime.
Since

\[
Z(C)\equiv C_0-h\pmod b,\qquad -(b-1)\le C_0-h\le b-1,
\]

b divides Z exactly when C_0=h. Symmetry supplies the opposite neutral
endpoint. Removing that pair divides Z by b. Repetition proves that the
maximal removable pair count is exactly ord_b(Z). A nonzero center cannot
be stripped to width zero or to a lone neutral coefficient.

**Faithful quotient.** Define

\[
K(C)=\left(m\bmod2,\;W(C)=Z(C)/b^{\lfloor m/2\rfloor}\right).
\]

This key is unchanged by neutral paired padding. Conversely, equal keys
permit padding the shorter word to the longer width, after which equal Z
implies equal words by Section 2. Thus K identifies precisely neutral-padding
equivalence classes; it loses neither a canonical center nor its carry sign.

For W!=0, let a be the least nonnegative integer such that b^a W is integral.
A realizable key 有 canonical width 2a+(m mod2) 和 signed value b^a W.
The decoder still checks realizability. A denominator with a prime factor
absent from b is invalid. W=0 gives the terminal core [] at even parity,
or [h] at odd parity. The implementation uses exact rational arithmetic.

## 4. PAPER PROOF — exact numerical successor

For a nonzero center let x=|Z|, s=sign(Z), M=b^m. The required entering carry
是 e=0 for Z>0 和 e=1 for Z<0. Indeed, normalization with exit 1-e 有 digit
value D=N+e-(1-e)M. Substitution gives D=x-1 in the positive case 和 D=M-x
in the negative case; the alternative entering carry does not flip.

Let R_m reverse exactly m base-b digits, including zero padding. For a
prescribed overflow g in {0,1}, the raw successor 有 width m+g 和

\[
\boxed{Z_{\rm raw}=s\left(x+b^g R_m(x-1)-b^{m+g}\right).}
\]

For Z>0, ordinary pairing gives raw value D+R_m(D) at g=0, or
D+b R_m(D) at g=1; the appended digit h*e is zero. Subtracting the raw
neutral value proves the formula. For Z<0, use
R_m(M-x)=M-1-R_m(x-1). At g=1 the appended digit is h, contributing
h(M+1); substitution gives the negative of the same expression. This also
proves coefficientwise complement conjugacy C -> 2h-C.

If Zraw!=0, maximal normalization is exactly

\[
v=\operatorname{ord}_b(Z_{\rm raw}),\qquad
m'=m+g-2v,\qquad Z'=Z_{\rm raw}/b^v.
\]

Zraw=0 is an all-neutral raw output, whose canonical core is terminal.
The numerical model explicitly reports this case. It does not invent a
next entering carry. Sections 2–4 prove conjugacy with the coefficient map
on representable states, for arbitrary bases, widths 和 prescribed g streams.

## 5. PAPER PROOF — scalar Z plus finite labels cannot predict the map

The infinite normalized family C_m=[b,0^(m-2),b], m>=3, 有 Z=b+1 和 e=0
at every width. At g=0,

\[
Z'_m=b+1-(b^2-1)b^{m-2}.
\]

These successors are negative, pairwise distinct, 和 congruent to 1 modulo b;
therefore their trim counts are zero. For any additional finite-valued label
on this family, the pigeonhole principle gives distinct widths with the same
label 和 Z, but different successor Z. Consequently an exact deterministic
predictor retaining Z cannot be repaired by width parity, width modulo a
fixed number, or any other finite supplementary label.

Concrete decimal controls:

| C | m | Z | g | next width | next Z |
|---|---:|---:|---:|---:|---:|
| [10,10] | 2 | 11 | 0 | 2 | -88 |
| [10,0,10] | 3 | 11 | 0 | 3 | -979 |
| [10,0,0,10] | 4 | 11 | 0 | 4 | -9889 |

This is an obstruction to **exact scalar compression**, not to sound
overapproximations, the rational key K, arbitrary finite abstractions, or
actual center cycles. It makes no claim about decimal Lychrel existence.

## 6. COMPUTED controls 和 reproducibility

From repository root, using standard-library Python:

```bash
python3 calculation/agent-112/center_integer.py
python3 calculation/agent-112/check_integer_state.py
python3 calculation/neutral_band_search.py selftest
python3 tools/verify.py --changed
```

`check_integer_state.py` independently normalizes coefficient lists, pairs
digits, trims literal neutral endpoints, 和 parses the existing Lean
certificates as data. It does not import the repository mirror.

| Control | Exact completed scope / result |
|---|---|
| Exhaustive words | 58,817 symmetric words; 29,381 positive Z, 29,381 negative Z, 55 zero |
| Exhaustive steps | 117,524 transitions; 108 terminal raw-zero outputs; 1,352 multiple-pair trims; maximum trim 4 |
| Exhaustive base/width scopes | b2/m<=9; b3,4/m<=8; b5,10,11/m<=6; b17,26,32/m<=4 |
| Wider deterministic samples | seed112; 4,000 words / 8,000 transitions, widths through172, maximum trim14 |
| Existing source certificates | bases2,4,8,11,16,17,26,32; 56 original edges 和 56 normalized edges pass |
| Complete small decoder domains | 1,210 representable states accepted, 23,634 rejected, matching independent enumeration |
| API/endpoint guards | 23 invalid inputs rejected; 39 empty/all-neutral controls; 7,969 fixed-width reversals |

The harness terminates before testing under `python -O`, preventing an
assertion-disabled false PASS. The numerical API uses explicit validation
branches, so its domain guards remain enabled under optimized Python.

The final source checks return `PASS: independent coefficient arithmetic
agrees with the integer center model.` The mirror selftest reaccepts the
eight known bases. The unchanged repository gate returns `ALL CHECKS PASSED`
with zero changed Lean modules; this validates repository rules for these
report/code changes, without conferring LEAN-VERIFIED status on this paper.

## 7. Research consequence

An exact center search can use canonical (m,Z) states or parity-tagged W
without losing coefficient information. Any required e stream remains an
explicit sign constraint, 和 the supplied g stream still needs an actual
B-cycle. The scalar-width counterfamily prevents a particular tempting
finite-memory shortcut. Unrestricted decimal center compatibility remains open.
