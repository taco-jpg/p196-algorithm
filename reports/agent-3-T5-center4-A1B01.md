# Agent 3 — T5: all-period decimal signed cycle exclusion with side-width switching 0↔1

**Research status: PAPER necessary overapproximation plus COMPUTED complete acyclicity. NOT LEAN-VERIFIED.** This *strictly strengthens the side-width scope* of [#406](https://github.com/taco-jpg/p196-algorithm/pull/406) for outer width1 and completes a disjoint bounded union with [#403](https://github.com/taco-jpg/p196-algorithm/pull/403). It is in the signed two-neutral-band pumping format of [#320](https://github.com/taco-jpg/p196-algorithm/pull/320), NOT the Agent120 one-band checker. Dependencies: exact helpers [#396](https://github.com/taco-jpg/p196-algorithm/pull/396), [#359](https://github.com/taco-jpg/p196-algorithm/pull/359).

## Exact scope of negative

There is **no positive-total-gain closed cycle of ANY period** under these simultaneous base10 constraints, at EVERY phase:

- 1≤|M|≤4 for the central fixed block.
- |A|=|E|=**1** with A nonzero.
- |B|=|D|∈**{0,1}**, crucially **the common side width may change between phases**. Thus empty→one-digit→empty side-block paths are fully represented, unlike in the two separate prior censuses.
- Every fixed-block digit is any legitimate 0–9 digit; all neutral run pairs remain complementary.
- Each of the eight neutral-run boundaries is processed by exactly one signed move whose size belongs to {-1,0,+1}, including zero moves, in either of the two relative orders whenever a fixed block touches two run boundaries.
- Repeated-run parameter lengths and phase period unrestricted; positive total signed pumping required by the original certificate definition.

This result does NOT exclude |A|≥2 with nonempty B,D, M≥5, side width≥2, multiple/larger boundary moves, a different certificate format, or all decimal Lychrel numbers.

## PAPER: why the 244-state central SCC restriction is exhaustive for positive gain

The signed full phase uses A x^g B u^h M v^h D y^g E with mirrored block lengths and complementary run digit pairs. For each exact signed reverse/add step, the central boundary shifts a,d obey the universal leading-carry orientation identity f=d−a∈{0,1} [#388](https://github.com/taco-jpg/p196-algorithm/pull/388). Summing fixed-block lengths over a closed signed cycle gives 2Σ(delta_g+delta_h)=Σf. Every positive-gain cycle therefore contains an edge with f=1 and a change in |M| parity.

For decimal centers 1..4, the exact center carry/move projection that **forgets only exterior constraints and freely allows next incoming center carry** has a unique strongly connected component containing both odd/even center lengths: exactly **244** states [#396](https://github.com/taco-jpg/p196-algorithm/pull/396). Thus any actual positive-gain cycle within M≤4 projects entirely to this SCC. Restricting to it cannot remove such a cycle.

## PAPER: correlated carry quotient with side-width changes

Now retain full digit content of A,E (one digit each), B,D (both empty or both one digit), and the projected (M,c2) center. Actual source central incoming carry must obey:

~~~text
c1=floor((A+E)/10)
c2=c1, if B=D=empty
c2=floor((B+D+c1)/10), if |B|=|D|=1.
~~~

For each specified c2 bit, there are **45** valid (A,E) pairs with B=D empty, plus **4,500** (A,B,D,E) one-digit-side quadruples, total **4,545** outer possibilities per center incoming-carry bit. Thus the sound fixed-state quotient has **244 × 4,545 = 1,108,980** vertices.

The original complementary x/u 0/9 source repeated-run symbols are intentionally forgotten. They do NOT influence five-fixed-block reverse/add output digits/carries: each neutral run transmits the incoming carry unchanged. This forgetful quotient can add, but cannot delete, full-phase transitions.

For each source state, compute the exact five-block reverse/add output, including c1,c2,c3,c4 and possible leading overflow. Require **both** output neutral run pairs complementary. Enumerate every necessary eight-boundary signed trace with each shift in {-1,0,+1}, checking **all shared-block relative orders**, not just a preferred chronological order. Allow target B'=D' widths either 0 or1, independent of their source width; require target A'=E' each one digit with nonzero leading A'. Compute target central incoming carry c2' from its **actual** A'/B'/D'/E' blocks, then require (M',c2') in the unique 244-state SCC. This includes every legitimate signed full edge in the declared scope, perhaps with extra quotient edges from forgotten old run symbols.

If the quotient is acyclic, **no actual positive-gain closed cycle** can exist within this bounded but side-width-switching class.

## COMPUTED: complete all-period exhaustion

Reproduce from the repo root with draft dependencies #396 and #359 available; Python 3 standard library only:

~~~sh
python3 calculation/agent-3/center4_scc_A1B01.py
~~~

Uncapped exact result:

~~~text
PREFLIGHT centers 244 quadruples_per_carry 4545 vertices 1108980
center_trace_options 8314
PASS1 vertices 1108980 active 133701 arcs 278139
FINAL vertices 1108980 active 133701 arcs 278139 peeled 1108980 residual 0
NO_POSITIVE_GAIN_SIGNED_CYCLE_WITH_A1_AND_B01
~~~

Local measured wall **68.80 seconds**, maximum resident memory **129,276 KB**, **exit 0**, no caps or timeout. Precisely **1,108,980** vertices, **133,701** active source vertices, **278,139** enumerated directed edges, **all vertices Kahn-peeled**, **ZERO** cyclic residual. Pre-filtering preserves all paired length/gain and center orientation constraints but DOES NOT impose fixed side width across successive phases.

The code uses dense indegree arrays and repeats exact edge enumeration during peeling, rather than materializing million-state adjacency objects. It rejects count mismatches, missing exact target carry tuples, overflow, or incomplete peeling. This is a bounded COMPUTED negative, not a symbolic all-width/format theorem.

## Verification and limitations

No base-10 full certificate, no decimal existence theorem, no unrestricted negative, no new Lean theorem or registry endpoint. The repository-wide python3 tools/verify.py --changed **has NOT RUN** because the full trusted checkout is unavailable. This is a **DRAFT**, stacked on #396/#359, and should not merge before dependency/source arithmetic and verification-gate review.