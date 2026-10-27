# Agent 112 — Numerical sufficiency for literal neutral-pair removal

Task: **T3.lean-numeric-trim-converse**, coordination
[#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433674540).
Status: **LEAN-VERIFIED + COMPUTED**, after the exact validation below.
Dependency: PR421's bounded-word numerical arithmetic, stacked on that PR.

## 1. The missing converse

The integer center model in PR368 removes v neutral pairs when its raw
signed value is divisible by b^v 和 the remaining width is allowed.
The following sufficiency statement justifies that scalar test for an
already realized bounded symmetric raw word.

Let b>=2, h=b-1, 和 let C be symmetric with coefficients in [0,2h].
For a natural v 和 an integer z, assume

\[
2v\le |C|,\qquad Z_b(C)=b^v z,
\qquad Z_b(C)=\operatorname{val}_b(C)+1-b^{|C|}.
\]

Then there is a unique literal middle word D such that

\[
\boxed{C=h^v\mathbin{++}D\mathbin{++}h^v,\qquad Z_b(D)=z.}
\]

The recovered D is symmetric, has coefficients in [0,2h], 和 satisfies
|D|+2v=|C|. The integer z may be positive, negative, or zero. The result
includes v=0, C=[], 和 complete even-width removal to D=[].

The scalar equality is divisibility with its quotient supplied. No prime
base or prime-adic valuation is assumed: it applies to composite bases,
including ten. The theorem concerns a specified v, not only a maximal
trim, 和 it does not claim a unique trim count for a neutral word.

## 2. One pair, then induction

For v>0, the signed value is divisible by b. Since |C|>=2,

\[
Z_b(C)\equiv C_0+1\pmod b.
\]

The coefficient bound gives 1<=C_0+1<=2b-1. Its only multiple of b is b,
so C_0=h. Symmetry forces the opposite endpoint to be h as well. Removing
those endpoints gives a literal middle D with inherited bounds 和 symmetry.

Evaluating the one-pair decomposition using A120's existing positional
identities gives Z(C)=b Z(D). Cancellation of the positive integer b
identifies the quotient. Repeating the same argument v times proves the
arbitrary-depth statement. The residual width bound follows at each step
from |D|+2=|C|, including the final empty-middle case.

Uniqueness of the middle word is pure list cancellation: two decompositions
with the same left 和 right neutral blocks have the same middle. This
uniqueness does not need numerical injectivity or symmetry assumptions.

The proof uses only the displayed bounded-word premises. In particular,
it does not need an actual source `Hyp`, an accepted edge, or a nonzero
signed value. Those are separate conditions when the theorem is applied
inside a certificate argument.

## 3. Premises 和 exact boundary controls

Each omitted premise can change the conclusion. Decimal examples are:

| Omitted premise | Input | Why the proposed removal fails |
|---|---|---|
| Symmetry | C=[9,0], v=1, Z=-90=10*(-9) | The high endpoint is0, so there is no neutral pair |
| Coefficient bound | C=[19,19], v=1, Z=110=10*11 | Both endpoints are19, outside the allowed bound18 |
| Width | C=[], v=1, Z=0=10*0 | Two coefficients cannot be removed from an empty word |
| Divisibility | C=[10,10], v=1, Z=11 | The signed value is not divisible by10 和 the endpoints are not neutral |

These are word-level arithmetic checks. The out-of-bound example is not
evaluated through the Python mirror's invalid-Hyp step conventions.

Zero states are included deliberately. By PR421's theorem, bounded Z=0
already forces the entire word to be neutral, without symmetry. Any
width-permitted pair removal then leaves a neutral middle of the exact
remaining width 和 quotient zero. Excluding zero would be unnecessary
for this local theorem, even though actual closed center cycles avoid it.

## 4. Attribution 和 relation to other work

PR349 section3 和 PR368 section2 already give this argument on paper.
The new work is its formalization in the unchanged A120 value/list API,
with complete natural-depth, zero, empty, 和 quotient handling.

Agent119's claim6433651344 owns the forward neutral-padding value identity,
accepted-edge signed recurrence, 和 its chain/cycle arithmetic consequences.
This result supplies the scalar-to-literal sufficiency excluded there. It
introduces no competing public forward-padding or accepted-chain theorem;
the local one-pair evaluation is proof support for the converse.

Agent114 retains raw-center symmetry 和 canonical-source trim-site gates.
Agent119 retains maximal center/joint canonicalization. The present
theorem takes symmetry as a premise 和 does not derive it from acceptance,
select a canonical trim, prove successor invariance, or move a trim schedule.

## 5. Files 和 reproduction

New modules in `P196.Agent112NeutralNumericalArithmetic`:

| Module | Public endpoint |
|---|---|
| `CenterPeel` | `exists_center_peel_of_signedValue` |
| `CenterTrimConverse` | `exists_center_trim_of_signedValue` |
| `CenterTrimConverse` | `center_trim_unique` |

The finite numerical controls are in
`calculation/agent-112/check_numeric_trim_converse.py`.

```bash
python3 calculation/agent-112/check_numeric_trim_converse.py
python3 -O calculation/agent-112/check_numeric_trim_converse.py
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

Both Python commands print
`PASS: complete finite numeric-trim converse, unique middle recovery, and attributed trim edges.`
Their complete outputs are byte-identical. All checks use explicit failure
branches 和 remain active under optimized execution. There is no sampling.

Every symmetric word in the ranges below is enumerated, with every
coefficient in [0,2(b-1)] 和 every v from0 through floor(width/2):

| Base | Maximum width, starting at0 |
|---|---:|
| 2 | 14 |
| 3 | 10 |
| 4 | 8 |
| 5 | 6 |
| 10 | 8 |
| 11 | 6 |
| 17 | 4 |
| 20 | 4 |
| 26 | 4 |
| 32 | 4 |
| 97 | 2 |

These81 base/width scopes contain335,301 words 和1,453,660 allowed-v
queries. Exactly358,270 queries are divisible 和 have literal padding;
22,969 of those use positive v. The other1,095,390 queries fail divisibility
和 have no literal padding. Every successful middle passes exact width,
bounds, symmetry, signed quotient, both-end cancellation, 和 independent
pair-by-pair peeling. Source values use positional sums; middle values use
Horner evaluation. Complete target dictionaries check all358,270 recovered
middles against the unique value in each finite width domain.

The successes include222 zero-Z queries 和179,024 of each nonzero sign.
There are eleven empty words,46 empty-middle successes, 和35 positive
trims that remove the entire even-width word. Base2 contributes6,559
words; composite bases contribute297,213. Every fixed-width cardinality
和 every trim-depth success count is checked against its exact alphabet
power. The largest permitted trim tested in this census is7.

Additional controls replay64 original center trims from nine full known
mirror certificates in bases2,4,8,11,16,17,20,26,32. Full `cycleOK` is
checked before their raw `nextC` calls. The base20 fixture retains
Agent116's pinned PR356 source/hash through the parent helper.
Agent101's PR381 decimal P24 CENTER-ONLY fixture supplies24 further
prescribed trims, including nonmaximal choices; every carry/raw/trim edge
和24-step center closure is replayed. It supplies no exterior B. These88
selected edges contain13 positive-v trims; total literal recoveries are
358,358. Known fixtures extend raw-word widths through44, without changing
the complete finite scopes above. All four premise controls pass separately.

The peel module compiles in0.918s/452,848KiB on one thread. The guarded
build of the peel 和 arbitrary-v wrapper together takes1.038s/458,356KiB.
Both use an8GiB address-space ceiling 和1200s timeout, so each new file
is below the8GB/20min budget. The actual unchanged
`python3 tools/verify.py --changed` reports5225 Lean files/302 projects,
eight modules built 和 kernel-replayed across the stack,31 public endpoints
audited (three new here), permitted axioms only, 和 `ALL CHECKS PASSED`.
Official Lean4.19.0 和 official lean4checker v4.19.0 are unchanged;
PR385 documents the narrow sandbox executable-path launch adaptation.
Independent cross-reviews cover both proofs, the exact scalar/list scope,
test coverage/counts, signed division, boundary controls, 和 fixture attribution.

## 6. What remains outside this result

The theorem starts with a literal bounded symmetric C. It does not prove
that arbitrary numerical states have such a representation. Establishing
that every numerical raw image is represented, then assembling periodic
images into a lifted cycle, remain separate proof obligations of PR368.
There is no new search exclusion, complete B+C edge list, decimal Lychrel
theorem, or unrestricted obstruction to the neutral-band route here.
