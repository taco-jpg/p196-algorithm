# Agent 3 — T5: three-digit center projection, exact relaxation cycle

**Status: PAPER PROOF (projection soundness) + COMPUTED (complete graph and explicit walk). NOT LEAN-VERIFIED.** Extension of the center-only two-neutral-band projection [#372](https://github.com/taco-jpg/p196-algorithm/pull/372), not an existence theorem. The 7-edge walk below **is not lifted to a full reverse-add certificate**.

## Scope and exact mathematical definition

Use base-10 signed two-band phases as specified in [#320](https://github.com/taco-jpg/p196-algorithm/pull/320), with central fixed block M of **one, two, or three digits** in each phase. Incoming center carry c2 is 0 or 1. The exact central fixed-width addition and output are:

~~~text
N = value(M) + value(reverse(M)) + c2
c3 = floor(N / 10^len(M));  R = N mod 10^len(M) (with exactly len(M) digits)
U = 9 (1-c3); V = 9 (1-c2).
~~~

The inner neutral output runs can be complementary only if c3=1−c2, so omit states violating this necessary condition. Apply one signed move of size −1, 0 or +1 on each of the two boundaries touching R, considering both relative orders. Positive shift extracts a matching U/V from an edge of R; negative shift absorbs the run digit into R. Require target center M' to have length 1, 2 or 3.

**Deliberate overapproximation:** next incoming center carry c2' is allowed to be EITHER bit irrespective of exterior fixed blocks or their carry transport. For each admissible local operation (M,c2) to M', emit BOTH arcs (M',0) and (M',1). The graph therefore contains the center projection of every true signed full-phase edge with these center sizes and center-local moves, but not conversely. External A,B,D,E blocks and their widths, outer and inner-run parameters, exterior signed moves, and leading carry are not checked.

A projected directed cycle is only a *potential obstruction to an obstruction theorem*, never a Lychrel certificate by itself.

## Parity condition survives but center-only obstruction fails

The all-base PAPER lemma in [#365](https://github.com/taco-jpg/p196-algorithm/pull/365) states that each accepted signed full-phase edge satisfies

~~~text
|M_next|−|M| ≡ f (mod 2),  f = leading carry ∈ {0,1}.
~~~

On a positive-gain closed full-phase itinerary the fixed-block length budget gives 2 Σ(delta_g+delta_h)=Σ f > 0, so some edge switches center parity. The earlier projected graph with M length 1 or 2 had no mixed-parity cyclic SCC, proving the scoped negative in #372.

Allowing M length 3 adds **a mixed-parity cyclic SCC**. This precisely identifies a limit of the center-only parity obstruction, without proving a positive full cycle.

## Exhaustive COMPUTED graph and literal word checks

Reproduce using Python 3 standard library:

~~~sh
python3 calculation/agent-3/center123_projection.py
~~~

Completed uncapped local result:

~~~text
states 2220 allowed_sources 1100 raw_center_moves 1992 arcs 3984
SCCs 2057 cyclic_SCCs 3 cyclic_sizes [10, 38, 118]
mixed_parity_cyclic_SCCs 1 center_word_tests 3984
MIXED PARITY CYCLIC SCC PRESENT; THIS IS NOT A FULL CERTIFICATE
~~~

The 2,220 projected states are exactly 2*(10+100+1000), including leading zeros in fixed-width centers. The three cyclic SCCs have 10, 38, and 118 states. **Exactly one** contains both even and odd central lengths. The classification uses actual center length modulo two, not merely the number of distinct lengths.

The program constructs the following explicit **7-edge projected walk**. Every pair is (M,c2), with center digits most-significant-first:

~~~text
((1,0),1)
 -> ((9,1,2),0)
 -> ((1,3,1),1)
 -> ((2,6,3),1)
 -> ((6,2,6),0)
 -> ((2,5,2),1)
 -> ((5,0,5),0)
 -> ((1,0),1)
~~~

An accepted pair of local center-boundary signed shifts (left,right) for each edge is:

~~~text
(-1,0), (0,0), (0,0), (0,0), (0,0), (0,0), (+1,0).
~~~

It switches length parity twice (2→3 and 3→2). The script independently replays every projected arc from literal fixed-block addition and matching extraction/absorption and performs **3,984 exact center-run word equality checks** at run lengths h=3 and h=8 (two per locally admissible move). These computations supplement the mathematical semantics of the signed moves.

**No exterior lift established:** this 7-edge walk has not been matched to a common full exterior A/B/D/E phase, exact exterior-produced incoming carries, matched outer run gains, or positive total cycle gain. It is **COMPUTED CENTER PROJECTION ONLY**.

## Exact limitation and next step

The current center-only automaton cannot exclude positive-gain decimal signed two-band cycles once three-digit M is permitted. Next strengthen the product of the surviving mixed-parity SCC with selected exterior carry/boundary states, treating any survival as UNDECIDED until a complete witness is found. Alternatively expand center move magnitudes.

New paths only: calculation/agent-3/center123_projection.py and reports/agent-3-T5-center123-projection.md. Full repository verification with python3 tools/verify.py --changed **NOT RUN** (no complete checkout); no Lean theorem or registry entry; draft must remain unmerged pending independent review.