# Agent 3 — T5: paper-sound signed two-band pumping format

**Research status:** Conditional certificate **format** with PAPER PROOF of soundness and COMPUTED arithmetic audits. A nontrivial **base-2 four-phase positive-gain certificate** was found and independently replayed for 1,000 integer steps. This is a new-format positive control, **not** a novel claim of base-2 Lychrel existence (already Lean-proved by other repository certificates). No base-10 cycle, no new Lean result. Draft PR is UNVERIFIED / DO NOT MERGE; no `verify.py --changed` run.

## Exact digit template

Fix a base `b>=2`. A *phase* consists of five ordinary base-b digit blocks `A,B,M,D,E`, with `|A|=|E|>=1`, `|B|=|D|`, `A[0]!=0`, and four digits `x,y,u,v` satisfying `x+y=u+v=b-1`. Digits are most-significant first. Define the two-parameter word

`W(g,h) = A ++ [x]^g ++ B ++ [u]^h ++ M ++ [v]^h ++ D ++ [y]^g ++ E`

for any natural g,h. These are **two independently parameterized neutral mirrored pairs**, not just an extra empty band in the one-band format. A sufficient nonpalindrome witness is any unequal corresponding fixed mirrored blocks (`A!=reverse(E)`, `B!=reverse(D)`, or `M!=reverse(M)`), or a nonempty mirrored run with unequal left/right digits (`g>0 and x!=y` or `h>0 and u!=v`). In fact their disjunction is an exact nonpalindrome test for this aligned block structure.

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

A candidate closed phase itinerary `(P_j, moves_j)` is accepted by `signed_cycleOK` only when every signed edge is accepted, each phase has a nonzero initial digit and the exact block/run nonpalindrome disjunction holds at the selected seed bounds, the total increments over a full cycle satisfy `Δg>=0`, `Δh>=0`, and `Δg+Δh>0`. Signed offsets during an individual step may be negative; the checker computes a sufficiently large initial pair `(g0,h0)` covering every intermediate deficit in the first cycle. At subsequent cycles the entry parameters do not decrease because total increments are nonnegative, so every elementary move remains valid.

**Conditional soundness:** induction on all steps proves the actual reverse-and-add orbit has precisely the declared phase words with evolving `(g,h)`. Every phase word is nonpalindromic either by a mismatch in its fixed mirrored blocks or by a nonempty repeated-digit band with unequal reflected run digits. Choosing the returned seed ensures this at all phases; subsequent cycles have weakly greater g,h. Hence any accepted positive-gain cycle produces a base-b Lychrel integer as a **PAPER PROOF conditional theorem**, not a Lean kernel theorem.

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
base2_signed_cycle_4_phases_positive_inner_gain_1 seed (0, 0) 1000_steps_integer_replay_PASS
NO_DECIMAL_LYCHREL_CERTIFICATE_CLAIMED
~~~

The integer tests independently evaluate full template words and their digit reversals, including large g,h; rewrite tests compare 36,000 full **digit-word equalities** (not only their numerical values), with both positive and negative boundary shifts.

One concrete genuinely two-band decimal **single step** (NOT a closed cycle):

* source: `A=9, B=097, M=70272, D=279, E=0; x=5,y=4,u=2,v=7`;
* target: `A=1, B=06, M=9748, D=06, E=9; x=0,y=9,u=9,v=0`;
* exact for every g,h≥0: `reverse_add_10(W_source(g,h)) = W_target(g+1,h+1)`.

The four positive boundary moves are `(run0,L,+1), (run1,L,+1), (run2,L,+1), (run3,L,+1)`. Both initial and target band digits are different on adjacent neutral runs; the example has a nonempty separating pair of fixed blocks and unequal fixed outer digits. It demonstrates a nonzero-gain transition, but does **not** yield infinite nonpalindrome without a return certificate.

## COMPUTED positive control: explicit closed base-2 two-band cycle

**Important correction:** This positive known-base control supersedes the previous "no witness found" statement. It is **not** a decimal certificate and is not Lean-verified in this new format. The base-2 Lychrel-existence theorem was already established in the repository through Agent120's independent one-band certificate; the novelty here is the *two-band certificate format* with genuine nonzero pumping.

The four phase records below are `(A,B,M,D,E; x,y,u,v)` in **most-significant-first base-2 digits**:

| phase | A | B | M | D | E | x y u v |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | 10 | 11 | 1101 | 00 | 00 | 1 0 1 0 |
| P1 | 11 | 00 | 1000 | 11 | 01 | 0 1 0 1 |
| P2 | 10 | 11 | 101 | 00 | 00 | 1 0 1 0 |
| P3 | 11 | 00 | 010 | 11 | 01 | 0 1 0 1 |

Define move notation `(run, side, delta)` with run 0=outer-left,1=inner-left,2=inner-right,3=outer-right; `L`/`R` means fixed block bordering that run; a positive delta extracts digits from a block, a negative delta absorbs digits back into it. Four checked transitions:

1. P0→P1: no moves, gains `(0,0)`.
2. P1→P2: `(0,L,+1),(0,R,-1),(1,L,+1),(2,L,+1)`, gains `(0,+1)`.
3. P2→P3: no moves, gains `(0,0)`.
4. P3→P0: `(0,L,+1),(0,R,-1),(1,L,+1),(1,R,-1)`, gains `(0,0)`.

Every fixed phase satisfies complementary digit pairs, nonzero leading digit, and the output fixed-block identity. The signed checker **accepts all four edges** and returns minimal parameter seed `(g0,h0)=(0,0)`; for the independent integer demonstration select `(g0,h0)=(2,2)` so *both neutral-band pairs are nonempty*. Every phase is nonpalindromic. Consequently, as a PAPER PROOF (subject to reviewing the edge checker), for all `g,h≥2`, the four reverse-and-add steps satisfy

`T_2^4(val_2(W_P0(g,h))) = val_2(W_P0(g,h+1))`.

In particular, start `W_P0(2,2)=10111111110100000000₂ = 785664` (integer decimal representation), and the first four phase values are `785664, 788733, 1571328, 1574397`; the return is `3144192 = val_2(W_P0(2,3))`. The script checks **1,000** actual integer steps with each intermediate phase word matched and never palindromic. It also compares numerical reversal to independent binary string reversal. This is a substantive positive pumping **control in base 2**, not a new base-10 discovery.

## COMPUTED bounded discovery scope

`python3 calculation/agent-3/base2_bounded.py` (standard library; approximately 13 seconds in the test container) independently builds a base-2 phase graph with `1≤|A|=|E|≤2`, `0≤|B|=|D|≤2`, `0≤|M|≤4`, and one signed move per each of the eight run boundaries in `{-1,0,+1}`. It reports `26,040` phases, `6,720` active phase images, `12,088` admissible directed edges, and `26,028` vertices removed by Kahn leaving a **12-vertex cyclic core**. It then checks that the explicit four-phase positive-gain witness appears in those edges and independently passes `signed_cycleOK`. This is a bounded *discovery search*, not an exhaustive all-width/all-traces completeness theorem.

## Limits, next action

No Lean file or registry entry has been created; `verify.py --changed` has NOT been run. The signed checker admits the explicit b=2 positive-gain cycle but no b=10 cycle is known. The format is strictly the declared two-band word language with *trace-witnessed* boundary moves; it makes no claim of completeness for all two-band identities. Future work: optimize bounded b=10 graph constraints and seek a positive-return witness, independently re-check any candidate, and then register/build a Lean theorem as required before claiming decimal Lychrel existence.