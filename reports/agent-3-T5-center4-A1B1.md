# Agent 3 — T5: decimal signed two-band bounded exclusion, one-digit outer AND side blocks

**Status: PAPER sound necessary quotient + COMPUTED complete finite graph. NOT LEAN-VERIFIED.** This is disjoint from the empty-side case [#403](https://github.com/taco-jpg/p196-algorithm/pull/403). It uses the signed two-neutral-band format [#320](https://github.com/taco-jpg/p196-algorithm/pull/320) and exact parent helpers from [#396](https://github.com/taco-jpg/p196-algorithm/pull/396) and [#359](https://github.com/taco-jpg/p196-algorithm/pull/359).

## Exact negative scope

No positive-total-gain base-10 signed two-band closed phase itinerary exists, **for ANY number of phases**, when at every phase:

- middle fixed block has 1≤|M|≤4;
- both exterior fixed blocks A,E have **exactly 1 digit**, with A nonzero;
- both side fixed blocks B,D have **exactly 1 digit** each;
- all block digits arbitrary valid base10 digits, and the two neutral paired input run digits are 0/9 (necessary on every closed itinerary);
- each of the eight run boundaries has exactly one signed move in {-1,0,+1}, with both relative orders allowed per shared fixed block;
- repeated-run lengths may be arbitrary nonnegative integers, with the signed-global-gain condition of the original certificate.

Does NOT cover B/D empty at some phases and nonempty at others, outer width2 together with nonempty side blocks, center length≥5, multiple signed moves, or all decimal Lychrel numbers.

## PAPER sound overapproximation argument

From the universal full-phase signed-width identities in [#388](https://github.com/taco-jpg/p196-algorithm/pull/388), the central signed moves (a,d) must satisfy f=d−a∈{0,1} for leading carry f. The exact full-length accounting gives 2Σ(delta_g+delta_h)=Σ f on every closed cycle, so positive total gain requires some f=1 and a parity change in M. The exact 1–4 center-only graph has **one** cyclic SCC containing both odd and even center lengths, of exactly **244** states [#396](https://github.com/taco-jpg/p196-algorithm/pull/396). Every hypothetical positive-gain full cycle must project wholly into this SCC. Restricting to those 244 centers cannot discard a positive cycle.

With a=1=|A|=|E| and d=1=|B|=|D|, write the four exterior digits as A=a, E=e, B=b, D=d. The source incoming carry to M is **exactly**

~~~text
c1 = floor((a+e)/10)
c2 = floor((b+d+c1)/10).
~~~

For each c2 bit, exactly **4,500** exterior digit quadruples (a,b,d,e) satisfy these equations. Hence the necessary quotient has 244×4500 = **1,098,000** states. The source x/u 0/9 run digits are forgotten: the exact five-block reverse-add image is independent of which complementary input digits were used, since those inserted runs transmit their carry unchanged. Forgetting them can create spurious edges but cannot remove a real one.

For each quotient vertex, compute all five exact fixed-block additions, require BOTH output neutral-run pairs complementary (including the previously nontrivial *outer* carry relation), enumerate **all eight ±1/0 signed boundary moves** and both relative orders, enforce output B'=D'=one digit, A'=E'=one digit and canonical leading A' nonzero, and compute the target c2' from the **actual target digit quadruple**, not an independent guess. Retain only targets in the unique parity-mixed center SCC. Thus every full positive cycle in the precise scope induces a directed cycle in this explicit overapproximating quotient. If the quotient is acyclic, every such full positive cycle is impossible.

## COMPUTED complete exhaustion

Run (Python 3 standard library, using parent #396 and #359 source):

~~~sh
python3 calculation/agent-3/center4_scc_A1B1.py
~~~

Uncapped locally completed result:

~~~text
PREFLIGHT centers 244 quadruples_per_carry 4500 quotient_states 1098000
center_trace_options 2870
PASS1 vertices 1098000 active 131070 edges 207360
FINAL vertices 1098000 active 131070 arcs 207360 peeled 1098000 residual 0
COMPLETE BOUNDED NEGATIVE M<=4 A1 B1
~~~

Actual wall time **30.09 seconds**, maximum resident set size **134,988 KB**, exit **0**. Exact graph: **1,098,000 states**, **131,070 active source states**, **207,360 directed arcs**, **all 1,098,000 peeled** by Kahn, 0 cyclic residual. No caps, timeout, skipped states, or inferred completions. The implementation keeps compact 32-bit indegrees and a FIFO; exact successor arcs are computed once for indegrees and again during peeling, rather than storing a costly adjacency list. It fails on overflow, missing exact target quadruples, or disagreement with expected exact counts/terminal state.

The independent integer reverse-add controls and known base2 positive signed-format witness are documented in the parent scripts; this new computation specifically checks the new decimal digit carry coupling, complementary output streams and exact all-orders boundary transformations.

## Limitations and delivery

This excludes all periods for this **fixed 1-digit exterior and 1-digit side format only**, not periods that pass between empty and nonempty side blocks, not broader widths/center blocks, and not arbitrary decimal Lychrel numbers. No accepted base10 certificate, no Lean source or registry entry, no kernel theorem. Full repository python3 tools/verify.py --changed has **NOT RUN** without the complete checkout. This is a **DRAFT** dependent on review source from #396/#359 and requires independent arithmetic audit and the verification gate before merging.