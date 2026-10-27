# Agent 3 — T5: orientation-refined decimal center ≤3 obstruction

**Status:** PAPER PROOF of sound necessary projection + COMPUTED exact finite SCC census. **NOT LEAN-VERIFIED** and **NOT a decimal Lychrel existence theorem**. This strengthens earlier signed-two-band center projections [#365](https://github.com/taco-jpg/p196-algorithm/pull/365), [#372](https://github.com/taco-jpg/p196-algorithm/pull/372), and corrects the deliberate relaxation of [#377](https://github.com/taco-jpg/p196-algorithm/pull/377).

## Scope

Base 10, the **signed two-neutral-band format** of [#320](https://github.com/taco-jpg/p196-algorithm/pull/320), with central fixed block M having **1, 2, or 3 digits at every phase**. The move touching each of the **two** central interfaces occurs **once** with signed magnitude in {-1,0,+1}; either order is allowed. Exterior fixed A,B,D,E widths and digits, lengths of both repeated bands, and the remaining six boundary move traces are unrestricted provided they obey the original signed-format semantics and full phase compatibility. Period is arbitrary.

**COMPUTED plus PAPER:** under precisely these center-move and center-width restrictions, there is no *positive-total-gain* closed signed certificate in base 10. This does not exclude signed certificates with longer M or stronger/multiple central moves, or other decimal Lychrel constructions.

## PAPER: exact carry-orientation identity

Let f in {0,1} be the leading carry emitted by the five fixed-block reverse-add computation. Denote net signed moves at the *left/right boundaries* of each of four neutral runs by L_i,R_i, i=0..3. A positive shift extracts an output-run digit from an adjacent fixed block into the band, and a negative shift absorbs one.

Output fixed-block widths before moves are (a+f,d,m,d,a); the next phase needs symmetric outer and side widths. The two corresponding members of each repeated neutral-band pair must also have equal final length shifts. These four necessary identities follow **without bounding the exterior blocks or moves**:

~~~text
L0 = R3 + f     [equal outer fixed-block lengths]
L3 = R0 + f     [equal outer neutral-run gains]
L1 = R2 + f     [equal side fixed-block lengths]
R1 = L2 − f     [equal inner neutral-run gains].
~~~

The two moves immediately touching the central fixed block are a=R1 (left side of M, from inner-left run) and d=L2 (right side of M, from inner-right run). Thus any genuinely liftable center operation must satisfy

~~~text
f = d−a ∈ {0,1}.
|M_next|−|M| = −a−d = f−2d.
~~~

This is stronger than the parity-only invariant in #365. It is a purely algebraic necessary condition in EVERY base b≥2 and ALL exterior widths, not a guessed correlation or a fixed-width numerical observation.

In particular, a center shrinking from three digits to two (Δm=−1) must have f=1, d=+1 and a=0: it must extract the *right* central digit. The earlier 7-edge center-only loop in #377 instead used (a,d)=(+1,0) on its final edge, requiring f=−1. Therefore that loop **provably cannot lift to any exact signed full-phase cycle**, irrespective of exterior width.

## PAPER: soundness of refined necessary automaton

Project any valid full phase to the decimal center block M and incoming central carry c2. The exact fixed-width central addition computes R and outgoing c3:

~~~text
N = value(M) + value(reverse(M)) + c2,
R = N mod 10^|M| (written in |M| digits),
c3 = floor(N / 10^|M|).
~~~

The inner output repeated digits are U=9(1−c3), V=9(1−c2), which can form a neutral complementary pair only if c3=1−c2. Perform one signed ±1/0 central boundary operation on each side of R, allowing both orders. Retain only operations with f=d−a in {0,1} and target center length 1..3. Finally allow **either** c2'=0 or c2'=1 for the next phase, regardless of the real exterior carry. This is a deliberately conservative overapproximation: every exact accepted edge of the scoped full model maps to a directed arc; not every projected arc lifts.

Any positive-gain closed full signed cycle has sum f=2 sum(delta_g+delta_h)>0 by the global fixed-block length budget from #365. Thus it must have at least one f=1, which switches M length parity. It would project to a closed walk in this refined center automaton occupying an SCC with **both** odd and even center lengths. If there is no such SCC, positive-gain closed cycles in the scoped full format are impossible.

## COMPUTED: exact complete graph and checks

Standalone standard-library command:

~~~sh
python3 calculation/agent-3/center123_orientation.py
~~~

Uncapped complete run:

~~~text
vertices 2220 active_sources 1100 local_move_records 1410 arcs 2820
SCCs 2172 cyclic_SCC_sizes [4, 10, 18, 20]
mixed_parity_cyclic_SCCs 0 literal_center_word_tests 2820
CENTER_1_TO_3_ALL_PERIOD_POSITIVE_GAIN_EXCLUDED_IN_SCOPED_FORMAT
NO_UNBOUNDED_DECIMAL_LYCHREL_CLAIM
~~~

The 2,220 vertices enumerate all 1–3-digit decimal blocks including zeros at the front of fixed-width M, with two carry choices. At each vertex, direct arithmetic enumerates all local signed moves in both orders. For each surviving center move record, **two literal centered run-word identities** are checked at h=3 and h=8: 2,820 independent finite arithmetic controls. Next carry remains unrestricted, so pruning cannot hide a full-phase edge merely because its exterior blocks are unknown. Kosaraju SCC analysis finds four cyclic SCCs of sizes 4,10,18,20, and **none** has both center length parities.

As a separate independent local check, NetworkX's own SCC algorithm (without reusing this script's Kosaraju function) reproduced exactly 2,220 nodes / 2,820 arcs / 2,172 SCCs / cyclic sizes [4,10,18,20] / zero mixed-parity cyclic SCCs. The included reproduction script needs Python standard library only and is the canonical check; independent NetworkX validation was local and is not a required dependency.

**Boundary of this exact argument:** if M is permitted to have length 4, the same orientation-refined center automaton (one move per center interface, ±1/0) has **22,220 vertices**, **28,400 arcs**, **21,949 SCCs**, and **one cyclic SCC mixing parity**. This is *projection-only*, and neither a positive full witness nor an exclusion at |M|=4.

## Limits and delivery

The obstruction covers **all periods and arbitrarily long outer fixed blocks**, but only M lengths ≤3 and bounded single central boundary shifts. No theorem is claimed for center length 4+, multiple operations on a central boundary, unknown certificate formats, or all decimal Lychrel numbers. No Lean source/registry entry has been created. Full repository `python3 tools/verify.py --changed` **NOT RUN** without a complete checkout; review PR should remain DRAFT. Only author-owned code/report are included under calculation/agent-3/ and reports/.