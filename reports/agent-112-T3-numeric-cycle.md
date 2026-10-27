# Agent 112 — An exact integer-only center-cycle criterion

Task: **T3.numeric-cycle-criterion**, coordination
[#289](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432980675).
Status: **PAPER PROOF + COMPUTED**. Depends on PR349's integer representation;
this follow-up supplies no new Lean theorem or decimal certificate.

## 1. Scope 和 credited foundations

The existing coefficient checker remains authoritative. This result gives
an equivalent verifier for its CENTER subsystem, using widths, signed
integers, prescribed carry/overflow bits, 和 arbitrary natural trim counts.
Acceptance performs no symmetric-word decoding or reconstruction.
A successful result has an explicit coefficient lift, independently replayed
against the old arithmetic. A matching actual exterior B cycle is still needed.

PR349 defines Z(C)=value_b(C)-(b^m-1), proves the general-base fixed-width
injectivity extension 和 exact transition, 和 credits the existing decimal
Lean injectivity results. The sign rule already appears in
`calculation/neutral_band/bases/decouple.py`. Pairing, carry flip 和 literal
trimming come from the unchanged A120 template/checker. Agent7's padding
covariance supports our transformed positive controls; the arbitrary-trim
criterion itself is proved below without assuming maximal normalization.

The new point is a predecessor argument: the integer recurrence is defined
on a larger interval than the realizable symmetric words, but EVERY successful
edge produces a realizable target. Periodic closure therefore supplies all
missing source-realizability conditions automatically.

## 2. PAPER PROOF — numerical criterion

Fix an integer base b>=2 and h=b-1. Use states (m,z) in

\[
\mathcal D_b=\{(m,z):m\ge1,\quad 0<|z|\le b^m-1\}.
\]

Let R_m(n) reverse exactly m ordinary base-b digits, including zero padding.
For x=|z|, s=sign(z), and g in {0,1}, put

\[
A_b(m,z,g)=s\bigl(x+b^gR_m(x-1)-b^{m+g}\bigr).
\]

A numerical edge from (m,z) to (m',z'), with labels (e,g,v), is accepted iff
both states lie in D_b, e,g are bits, v is a natural number, and

\[
e=\mathbf1_{z<0},\qquad m'=m+g-2v,\qquad
A_b(m,z,g)=b^v z'.
\]

**Theorem.** A nonempty closed list of accepted numerical edges is equivalent
to a center-only coefficient cycle with the same e/g/v labels. The lift is
unique at every phase. This covers arbitrary legal trims, including v=0
and deliberately nonmaximal trims. There is no finite width or period bound.

### Proof: every numerical target is realizable

For ANY source in D_b, construct the m ordinary digits D of

\[
Q=\begin{cases}z-1,&z>0,\\b^m+z,&z<0.\end{cases}
\]

These are valid digit values: 0<=Q<b^m. Let W=D when g=0 and
W=D++[he] when g=1. Define the raw coefficient word S=W+reverse(W),
where addition is componentwise. S is symmetric, has width m+g, and has
coefficients in [0,2h]. Its central coefficient is even whenever its width
is odd. Direct evaluation, using digit-complement reversal in the negative
case, gives Z(S)=A_b(m,z,g). This construction does not require a symmetric
word representing the SOURCE.

For any bounded symmetric word T,

\[
Z(T)\equiv T_0-h\pmod b,\qquad -h\le T_0-h\le h.
\]

Thus b divides Z(T) exactly when both endpoints equal h; stripping them
divides Z by b. The accepted edge equation implies b^v divides Z(S),
and m+g-2v=m'>=1 prevents overlapping endpoint removals. Apply this fact
v times. The resulting symmetric word has width m' and signed value z',
so it realizes the target. Nonzero z' excludes an all-neutral terminal word.

### Proof: close the orbit and recover the actual arithmetic

Every state on a nonempty closed list has a predecessor, so the construction
above supplies a bounded symmetric word C_i representing every state.
Fixed-width injectivity makes this representation unique. Given that word,
normalize its coefficients with incoming carry e_i=1[z_i<0]. Since
value(C_i)=b^(m_i)-1+z_i and all coefficients are at most 2b-2, normalization
exits with carry 1-e_i and gives exactly the ordinary digit word D_i above.
Consequently its actual nextC is the constructed S_i, and the prescribed
v_i literal neutral pairs trim it to C_(i+1). This proves the coefficient
cycle, including the final-to-first edge.

Conversely, every coefficient center cycle is symmetric because every phase
is a paired, trimmed output. Its all-neutral/empty states are excluded by
carry flip. Encoding its phases gives D_b, the sign rule, the width equation,
and the displayed numerical edge equation. This proves equivalence.

**Edge scope.** A single numerical edge may accept an unrealizable source.
For example, base10 (m,z)=(2,1) has no symmetric coefficient realization,
yet g=0 gives the valid target (2,-99), realized by [0,0]. The cycle theorem
uses closure; it does not identify all interval source states with centers.

**Graph consequence.** The numerical graph induces exactly the coefficient
graph on realizable states. Every additional interval state has indegree zero.
Therefore the graphs have identical cyclic strongly connected components
and identical labeled edges on closed walks, including after a common width
restriction. Their full transient vertex/SCC sets need not agree.

## 3. PAPER PROOF — signs cannot simply be discarded

For x>0 define F(m,x,g)=x+b^g R_m(x-1)-b^(m+g). On a nonterminal numerical
edge let epsilon=sign(F). Its magnitude and sign obey

\[
x'=|F|/b^v,\qquad s'=s\epsilon.
\]

On a closed magnitude itinerary with fixed m/g/v data, signed one-lap
closure holds exactly when the product of all epsilons is +1. A product -1
returns to the complement after one lap and returns to the starting signed
state after two laps. This describes a return time, not necessarily the least
period. The prescribed carry stream must satisfy the stronger LOCAL conditions

\[
\epsilon_i=(-1)^{e_i+e_{i+1}}
\]

at every cyclic edge. When the product is -1, the two-lap lift repeats m/g/v
and magnitudes, but its carry stream must complement on the second lap.
A one-lap repeating e stream cannot then be used unchanged.

Exact decimal width-one, g=v=0 control:

\[
[0]\to[2]\to[6]\to[14]\to[8]\to[18]\to[16]\to[12]\to[4]\to[10]\to[0].
\]

Its signed values are (-9,-7,-3,5,-1,9,7,3,-5,1): signed period10,
magnitude period5. The five-step signed return is rejected. This is only
a center cycle; its zero-overflow driver supplies no compatible B certificate.

## 4. Implementation 和 reproducibility

`calculation/agent-112/numeric_cycle.py` exposes:

- `raw_numeric(base, Center(m,z), g)`: whole-interval raw image; malformed
  input raises ValueError. A zero output is reported as terminal.
- `check_edge(base, source, target, e, g, v)`: explicit Boolean guards and
  the three numerical equalities. Zero states and Boolean-as-integer labels
  are rejected. No decoder is called.
- `check_cycle(base, states, carries, overflows, trims)`: nonempty equally
  sized list/tuple arrays with implicit final-to-first closure.
- `lift_cycle(...)`: after acceptance, constructs every state from its
  predecessor, checks literal neutral endpoints, then independently replays
  coefficient normalization, carry flip, pairing, and exact trim equality.

The production acceptance path has no assertions. The independent harness
refuses `python -O`, and separately executes positive/negative production
checks under optimization with explicit failure branches.

From repository root, standard-library Python only:

```bash
python3 calculation/agent-112/check_numeric_cycle.py
python3 calculation/agent-112/check_integer_state.py
python3 calculation/neutral_band_search.py selftest
python3 tools/verify.py --changed
```

## 5. COMPUTED controls

Whole-interval coverage: base2 widths<=7; base3<=5; base4<=4; base10<=3;
base26<=2. All 5,496 nonzero interval sources were checked, including 4,560
unrealizable sources. Direct digit pairing agreed on all 10,992 raw images;
278 images were terminal zero. Representable sources were also compared
with independently implemented coefficient normalization.

Complete bounded graphs include EVERY natural legal trim and both g bits:

| Base / maximum width | Numeric states / edges | Coefficient states / edges | Shared cyclic states / edges |
|---|---:|---:|---:|
| 2 / 6 | 240 / 608 | 72 / 188 | 40 / 88 |
| 3 / 4 | 232 / 382 | 56 / 102 | 16 / 16 |
| 4 / 4 | 672 / 1,100 | 108 / 202 | 52 / 72 |
| 10 / 3 | 2,214 / 2,806 | 396 / 486 | 52 / 52 |
| Total | 3,358 / 4,896 | 632 / 978 | 160 / 228 |

Cyclic SCCs and labeled cyclic-edge sets agree exactly. One circuit from
each of the 21 cyclic SCCs was independently extracted, accepted, lifted,
and matched to its coefficient words; this is not enumeration of all cycles.

Positive controls use the eight existing main-branch certificate sources
(bases2,4,8,11,16,17,26,32), plus Agent116's separately credited base20
certificate from PR356, commit b7a718b78d67cf54d362232ba1b8f90fbec23af8,
`lean/P196/Agent116Base20Certificate/Certificate.lean`.
The compact base20 fixture reconstructs all eight literal source edges
from B0/C0 and trim pairs, then checks their complete data SHA256 against
the independently parsed source. The test prints both attribution and hash.

Across nine bases: 64 original edges, 64 normalized edges, and 512 edges
from repeated cycles with all center trims moved to the last edge. These
exercise nonmaximal trims and trim counts3/5. All 640 edges pass independent
coefficient arithmetic and numerical lifting; all 36 full B/C cycles pass
the unchanged Python `cycleOK` mirror. The new base20 contribution is
8 original +8 normalized +64 transformed edges, reported separately.

Malformed controls reject 9 raw inputs, 29 edges, 17 cycles, and 13 lifts.
An explicit optimized-Python subprocess accepts a known positive and rejects
wrong carries, empty/mismatched arrays, negative trims, Boolean labels,
zero states, and invalid lifts. The harness ends with
`PASS: numerical cycle acceptance and lifting agree with independent coefficient arithmetic.`

The required `python3 tools/verify.py --changed` reports `ALL CHECKS PASSED`
for 5217 Lean files/301 projects, zero changed Lean modules, and zero audited
endpoints. This report/code gate confers no LEAN-VERIFIED status. Parent
arithmetic controls and the eight-base mirror selftest also pass.

## 6. Consequence 和 limits

An integer-only solver may safely omit explicit symmetric-source constraints
when checking a CLOSED nonterminal center orbit; the predecessor supplies
them. A partial path still needs its initial realization if that matters.
This criterion preserves all finite widths, periods, and natural trim choices,
but does not make the state space finite or certify any negative unbounded
search. A successful center orbit still needs the same e/g driver from an
actual exterior cycle and the unchanged full certificate checks.
