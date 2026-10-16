# Independent statement and semantics review — Agent 105 actual high returns

**Verdict: PASS for the written argument and the four reviewed source
modules, subject to the separately recorded successful build and complete
transitive axiom audit.** This review found no missing width case, invalid
carry independence assumption, or mathematical counterexample. It is a
source/written audit, not a fresh Lean compilation. A separate worker owns
the runtime rebuild. No theorem file was edited by this reviewer.

The audited source identities are in `source_audit_manifest.json`. This
report reviews `FULL_HIGH_RETURN.md` sections 1–5, the supporting
`NEUTRAL_EXTERIOR.md`, and the initial Agent105 modules
`NeutralExterior.lean`, `HighReturnPrefix.lean`, `SmallWidth.lean`, and
`NumericHigh.lean` (the latter was added while this review was in progress).
An ordinary-integer endpoint and its complete dependency closure must also
be checked before claiming that the entire upper-bound bridge is formalized.

## 1. Exact meaning of the bound

For positive ordinary integers, let `T(n)=n+reverse10(n)`, continuing the
map even after a palindrome, and let `Q(n)` be the pair sums of the canonical
decimal digits at their actual width. The claim is

`Q(T^(2j)(n)) in H for every 0 <= j <= R  =>  R <= 3`,

where `H` means every coefficient is in `9..18` and the exterior coefficient
is at least ten. The premise includes time zero and the endpoint `2R`.
This is a bound on consecutive two-step returns, not on total visits to H,
palindrome avoidance, or the first palindrome time. The proof makes no
assumption that an abstract graph path is an actual orbit.

## 2. First update and actual physical widths

Write the original width as `L>0`, `r_i=q_i-9`, and `a=r_0`. The exterior
condition starts carry one at the first column. Every remaining coefficient
is at least nine, so that carry persists. The actual first normalized digit
word has width `L+1`, with appended leading digit one. Pairing at that
width gives endpoints `a`, and internal coefficients `r_(i-1)+r_i`.
The width-one specialization is exactly `(a,a)`; it has two entries.

Thus the intermediate word P has width `M=L+1`, exterior `1<=a<=9`, is
symmetric, and has coefficients at most eighteen. If `a<=8`, the last
column plus its binary incoming carry is at most nine, so a second overflow
is impossible. The remaining case `a=9` is handled by the next section.

On a return to H there is no second overflow. Its physical width is then
exactly M, not M+1: the last output digit is `a+c_(M-1)`, positive and below
ten. Consequently every actual high return changes width from L to L+1.
This justifies both continued use of the three-column projection and its
reflection indices. It does not merely assert a symbolic padding width.

The existing `FoldedDecimal.nextWidth` selects L or L+1 from the actual
`carry q L`. Canonical interpretation comes from the existing normalization
and `iterPairs_representation` theorems; it must not be inferred for arbitrary
unbounded coefficient functions without the admissibility/representation
hypotheses.

## 3. Neutral-exterior obstruction, including overlap and tiny widths

Consider a bounded symmetric source P of width M, exterior nine, and final
carry one. If every coefficient were nine, initial carry zero would persist,
a contradiction. Let j be its first non-nine index. Exterior neutrality
gives `j>=1`; symmetry and minimality put a reflected copy at `M-1-j` and
make every subsequent coefficient neutral. If `p_j<=8`, that reflected
copy resets carry to zero, and the neutral suffix preserves zero, again a
contradiction. Hence `10<=p_j<=18`.

The initial neutral prefix gives `c_j=0`, so `d_j=p_j-10<=8`. The reflected
high copy resets carry to one; the next column, at `M-j`, is neutral and
has output digit zero. Since `j>=1` and `j<M`, this is an original source
column. The actual overflow output has width M+1, so j pairs with **M-j**,
not M-1-j. The resulting coefficient is `p_j-10<=8`.

At M=1 or M=2 there cannot be a non-nine interior consistent with neutral
exterior and symmetry, so the overflow premise is impossible. At M=3 the
first non-nine column may be the center; its partner after overflow is the
last neutral source column, and the same argument applies. No center-even
condition is required by this lemma. It is sound for a larger class than
realizable pair words.

`NeutralExterior.lean` follows this reasoning in a slightly stronger form:
it transports carry through the neutral suffix to establish
`carry q (L-j)=1`, obtains highness of the reflected predecessor, and pairs
the first non-nine position with `L-j`. Its `low_outer_high_next_no_overflow`
corollary first derives exterior exactly nine in the only possible
overflow case. It does not assume the desired absence of overflow.

## 4. Carry criterion and necessary three-column projection

Without second overflow, reflection has width M. Equal source coefficients
at reflected positions yield digit-pair values

| Source coefficient p | Actual pair value, with u the two incoming carries |
|---|---|
| `0..8` | `2p+u` |
| `9` | `18-9u` |
| `10..18` | `2p-20+u` |

When positions overlap, u is twice the same carry; the formula still holds.
The allowed coefficient set, requirements `u>=1` at 4/14 and `u<=1` at 9,
and the stronger exterior threshold `q_0>=14` follow directly. For exterior
`a<=8`, the exterior pair is `2a+c_(M-1)` and the carry is binary; for a=9,
no overflow forces that carry to zero. The nearest-nonneutral formulation
also has the correct directions: an incoming carry is determined by the
nearest preceding non-nine coefficient, and symmetry converts the reflected
incoming carry to the nearest non-nine coefficient on the other side.
Missing neighbors represent the initial carry zero.

For `L>=3`, the first three P coefficients are `a=A-9`, `x=A+B-18`,
`y=B+C-18`. Choose the **actual** control
`w=c_(M-3)=c_(L-2)`, rather than an independent carry. The low carries are
`c_1=0` and `c_2=floor(x/10)`. Reading the high reflected columns gives
`v=floor((y+w)/10)` and `z=floor((x+v)/10)`. Pairing the actual digits gives
exactly the successor triple in `HighReturnRank.next`.

The potentially overlapping cases deserve explicit checks:

- At L=3, symmetry forces C=A and therefore y=x. Intermediate width M=4
  gives `w=c_1=0`. The duplicated central target digits are consistent with
  the formulas; permitting w=1 in the finite relation adds only extra edges.
- At L=4, M=5 and `w=c_2=floor(x/10)`. The third target coefficient is a
  center pair and equals twice one digit. No two distinct carries are
  asserted at the same position.

`HighReturnPrefix.lean` derives these carry equalities from symmetry of the
first actual output. The use of `L-2` is valid under `L>=3`; the bounded
carry lemma separately proves the control is less than two. Its code
`100*(q0-10)+10*(q1-9)+(q2-9)` has range below 900 and is decoded exactly
using the source H bounds. The target-index subtraction in the existing
rank module is algebraically equivalent under the target lower bounds;
the source proof explicitly supplies those bounds.

The rank conclusion uses the existing exhaustive relation. Actual target
membership and the no-overflow constraint establish an admitted edge;
`edge_decreases` then establishes the strict rank decrease. No edge,
rank decrease, or final bound is supplied as an extra hypothesis.

**Integration order to preserve:** the final bridge must start with
highness at the actual second width
`nextWidth (nextColumns q L) (L+1)`. Apply the neutral-exterior corollary
first, derive second carry zero, then rewrite that width to L+1 and apply
`actual_prefix_edge`. Assuming the fixed-width target highness before
deriving no overflow would omit exactly the branch this work must exclude.

## 5. Widths one and two

For a realizable width-one word, A is even. Its first return is `(2a,2a)`,
so the only high returns have A=14,16,18, giving `(10,10)`, `(14,14)`,
`(18,18)`. Their next two-step images are respectively `(2,4,2)`,
`(11,0,11)`, `(10,8,8,10)`, all outside H. The last image includes an
overflow and must not be evaluated at a fixed width of three.

For width two, symmetry gives `(A,A)` and then P=`(a,2a,a)`. When a<=4
the target exterior is at most eight. For 5<=a<=8 its exact target is
`(2a+1,4a-20,2a+1)`; only a=8 is high, yielding `(17,12,17)`. Its next
two-step image is `(17,3,3,17)`. At a=9 the neutral-exterior obstruction
excludes a return. Thus both small widths allow at most one return.

`SmallWidth.lean` uses a different, valid stronger finite reduction:
symmetry makes every finite width-one/two source constant, and all
coefficients a=10..18 are checked, including unrealizable odd singletons.
`FiniteHigh` only requires every target coefficient to be at least nine;
failure of simultaneous membership in this weaker predicate excludes
simultaneous membership in H. Its `iterPairs` calculation includes all
actual overflow-dependent widths. The congruence lemmas compare only the
finite input positions and propagate actual next widths, so arbitrary
values in the infinite function tail cannot contaminate the reduction.

The closed finite statement uses ordinary kernel `decide`, not
`native_decide`. This observation is a source audit; actual successful
compilation and the full axiom report remain separately evidenced.

## 6. Finite independent controls and retained artifacts

Command from repository root:

```sh
python3 proofs/contributions/agent-105/actual-high-return/review/exact_controls.py
```

Result: PASS. The script imports no producer transition or certificate
code. It checks coefficient normalization against positional integer
evaluation. For canonical decimal high words it also constructs a concrete
ordinary realization and independently computes literal string
reverse-and-add twice.

- Neutral controls: all 22,773 symmetric words with exterior b-1, bases
  2..10 and widths 1..7, including odd centers. Of these, 11,355 overflow;
  the specified j and actual reflected partner are checked in every case.
- High controls: all 14,999 canonical high-region pair words of widths
  1..8. Counts per width: 5, 9, 45, 90, 450, 900, 4,500, 9,000.
- There are 843 returning cases of width at least three; every actual
  carry projection agrees, including all 12 returning width-three overlap
  cases. Every returning width-one/two source is checked to fail its next
  return.

The complete inputs, carries, outputs, and projection witnesses are retained
in `exact_controls.json.gz` (decoded size 5,467,074 bytes). Exact hashes,
compressed size, source hash, scope, counts, and the recovery command are
in `exact_controls_summary.json`. No bounded control result is used as the
proof of an all-width claim. No existing exhaustive graph search was rerun.

## 7. Trust boundary and remaining endpoint checks

The reviewed four sources contain no proof placeholder, custom axiom,
native computation tactic, external process assumption, or JSON-derived
logical premise. Their imported existing rank theorem uses ordinary
`decide`; the actual normalization module supplies the semantics. This does
not replace a complete transitive axiom audit of the final dependency
closure or a successful compiler exit status.

For the final ordinary-integer endpoint, check all of the following:

1. Actual `iterPairs` representations, or equivalent canonical numeric
   witnesses, provide H membership at times 0,2,...,2R.
2. The initial width is positive. Widths one/two invoke the small-width
   exclusion; widths at least three remain at least three because each
   successful return increases width by exactly one.
3. Four purported returns yield four actual checked edges, with every
   vertex in the 900-state domain, contradicting rank at most three.
4. The theorem concludes the non-strict bound R<=3 with the correct endpoint
   convention. It does not use a conditional graph-path premise as a
   replacement for the numeric orbit premise.

The old written report's statement that safe sharpness was UNKNOWN is a
historical scope note, superseded by Agent1's later finite witness. That
editorial history does not change the upper-bound argument reviewed here.

## 8. Ordinary-integer predicate and representation independence

`NumericHigh.lean` defines an ordinary-integer property by existence of a
canonical representation whose actual pair word is high. Its use of an
existential representation does not introduce an alternative orbit or an
arbitrary reflection width: `canonical_width_eq` identifies both widths
with the number's decimal length, and `canonical_columns_eq` uses canonical
digit-value injectivity to identify all used pair coefficients. Therefore
`numericHigh_iff` transfers membership to any canonical representation of
the same integer.

`numericHigh_orbit_iff` uses the already formalized exact
`iterPairs_representation`, at every natural time t. Both width and used
coefficients of the orbit representation are the actual iterated values.
The theorem does not postulate highness along an abstract graph path.
The canonical-column specialization removes an arbitrary source q
altogether. These definitions and transfer statements have the right
semantics for the intended final endpoint. The final numerical upper bound
itself was not yet present when this section was reviewed.
