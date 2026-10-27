# Agent 3 — T5: paper-sound signed two-band pumping format

**Research status:** Conditional certificate **format** specified with an independently checkable Python implementation and arithmetic audits. PAPER PROOF of soundness; COMPUTED cross-tests. Not Lean-verified. **No actual closed positive-gain certificate has been found**, in base 10 or any other base, so this does not prove existence of a Lychrel number. Review only; #289 Manager's AGENTS.md contribution-policy hold applies.

## Exact digit template

Fix a base `b>=2`. A *phase* consists of five ordinary base-b digit blocks `A,B,M,D,E`, with `|A|=|E|>=1`, `|B|=|D|`, `A[0]!=0`, and four digits `x,y,u,v` satisfying `x+y=u+v=b-1`. Digits are most-significant first. Define the two-parameter word

`W(g,h) = A ++ [x]^g ++ B ++ [u]^h ++ M ++ [v]^h ++ D ++ [y]^g ++ E`

for any natural g,h. These are **two independently parameterized neutral mirrored pairs**, not just an extra empty band in the one-band format. If `A[0]!=E[-1]`, all W(g,h) are nonpalindromic for arbitrary g,h.

## PAPER PROOF 1: two-band carry-transmission lemma

Split ordinary reverse-and-add into five finite-width block additions. Starting from the units end, compute:

* `R0,c1 = add_fixed(E, reverse(A), 0)`;
* `R1,c2 = add_fixed(D, reverse(B), c1)`;
* `R2,c3 = add_fixed(M, reverse(M), c2)`;
* `R3,c4 = add_fixed(B, reverse(D), c3)`;
* `R4,c5 = add_fixed(A, reverse(E), c4)`.

All carries ci are zero or one. Define the output run digits `X=(b-1)(1-c4)`, `U=(b-1)(1-c3)`, `V=(b-1)(1-c2)`, and `Y=(b-1)(1-c1)`. Because each reflected pair of inserted run digits sums to b−1, it transmits the incoming carry unchanged, and emits b−1 when the carry is zero and 0 when it is one. Thus, as an exact **integer** identity for all g,h≥0:

`reverse_add_b(val(W(g,h))) = val(O0 ++ X^g ++ O1 ++ U^h ++ O2 ++ V^h ++ O3 ++ Y^g ++ O4)`

where `(O0,O1,O2,O3,O4)=( [1]^c5++R4, R3, R2, R1, R0 )`. Leading zeros in the fixed-width result do not change the integer; valid target phases always begin with a nonzero digit. This is an elementary column proof, not a finite-sample inference. It is implemented by `image_blocks` in the attached source.

A successor phase can preserve **both** neutral pairs only when `X+Y=U+V=b−1`, equivalently `c4+c1=c3+c2=1`; these conditions are checked by matching to a valid target phase.

## PAPER PROOF 2: strict extraction-only format cannot pump cyclically

A tempting checker extracts a nonnegative number of copies of each run digit from the bordering finite blocks, without allowing reverse transfers back from the runs. This is implemented as the small `edgeOK` checker in the first source file. It is locally sound, and there exist genuine transitions of nonzero gain; however the phase fixed-block lengths `|A|,|B|,|M|,|D|,|E|` cannot increase, since the target E is a suffix of O4=R0 (same old |E|), target B,D and M are subwords of O1,O3,O2, and |A'|=|E'|. Along a closed finite phase itinerary every such block length must stay constant. Consequently no copies can have been extracted, so **every parameter gain on every edge is zero**. Any cycle required to have strictly positive total pumping gain is impossible, in every base. This refutes *that particular* extraction-only certificate format, NOT the entire two-band approach.

## PAPER PROOF 3: signed boundary moves give a sound nontrivial format

Allow the reverse elementary operation too. An output word is represented by five fixed blocks `O0..O4` separated by runs of single digits `X^g, U^h, V^h, Y^g`. For any one of the four runs, a finite *boundary move* can:

* extract r≥0 matching copies of its digit from the suffix of the fixed block immediately to the left, or prefix of the block to the right, and **increase** that run exponent by r; or
* absorb r≥0 copies of that run digit into the adjacent fixed block and **decrease** its exponent by r, provided the exponent is at least r at that point.

Every move is a literal word identity. A finite sequence of moves is checked exactly, using the run characters from PAPER PROOF 1; no opaque solver or arbitrary sample bound is used. For each run it also records the most negative intermediate exponent offset. A transition is accepted only if the final blocks match exactly a valid successor phase, the final run digits match, and the two mirrored exponents have matching shifts `δg` and `δh`. This is the attached `signed_edge` predicate.

A candidate closed phase itinerary `(P_j, moves_j)` is accepted by `signed_cycleOK` only when every signed edge is accepted, each phase has nonzero initial digit and a distinct first/last digit, the total increments over a full cycle satisfy `Δg>=0`, `Δh>=0`, and `Δg+Δh>0`. Signed offsets during an individual step may be negative; the checker computes a sufficiently large initial pair `(g0,h0)` covering every intermediate deficit in the first cycle. At subsequent cycles the entry parameters do not decrease because total increments are nonnegative, so every elementary move remains valid.

**Conditional soundness:** induction on all steps proves the actual reverse-and-add orbit has precisely the declared phase words with evolving `(g,h)`. Every phase word is nonpalindromic by its unequal outer digits, so any accepted *positive-gain cycle witness* would produce a genuine base-b Lychrel integer. This is a PAPER PROOF conditional theorem, not a Lean theorem; no witness is claimed here.

## COMPUTED controls

Exact commands (two Python 3 standard-library scripts, no dependencies):

~~~sh
python3 calculation/agent-3/two_band.py
python3 calculation/agent-3/signed_rewrite.py
~~~

Observed:

~~~text
two_band_bigint_crosschecks 12000 PASS by_base {2: 1334, 3: 1334, 4: 1334, 8: 1333, 10: 1333, 11: 1333, 17: 1333, 26: 1333, 32: 1333}
synthetic_valid_phase_transitions 5 PASS
NO BASE-10 CYCLE CLAIMED
signed_rewrite_word_equalities 36000 PASS 12000 random traces
base10_two_band_nontrivial_step_delta_1_1 PASS
NO_CYCLE_CERTIFICATE_OR_DECIMAL_LYCHREL_CLAIM
~~~

The integer tests independently evaluate full template words and their digit reversals, including large g,h; rewrite tests compare 36,000 full **digit-word equalities** (not only their numerical values), with both positive and negative boundary shifts.

One concrete genuinely two-band decimal **single step** (NOT a closed cycle):

* source: `A=9, B=097, M=70272, D=279, E=0; x=5,y=4,u=2,v=7`;
* target: `A=1, B=06, M=9748, D=06, E=9; x=0,y=9,u=9,v=0`;
* exact for every g,h≥0: `reverse_add_10(W_source(g,h)) = W_target(g+1,h+1)`.

The four positive boundary moves are `(run0,L,+1), (run1,L,+1), (run2,L,+1), (run3,L,+1)`. Both initial and target band digits are different on adjacent neutral runs; the example has a nonempty separating pair of fixed blocks and unequal fixed outer digits. It demonstrates a nonzero-gain transition, but does **not** yield infinite nonpalindrome without a return certificate.

## Limits, next action

No Lean file or registry entry has been created; `verify.py` has not run. The current signed checker has no accepted closed-cycle witness, and its precise scope is strictly the declared two-band word language with *trace-witnessed* boundary moves. It does not claim to be complete for all two-band identities. A next step is to search for small-base known positive pumping cycles as nonvacuity controls, followed by targeted base-10 search. A truly accepted base-10 witness must be translated to a registered Lean theorem and independently verified before any Lychrel-existence claim.